import json
import math
import os
from dataclasses import asdict, replace
from itertools import product
from pathlib import Path
from statistics import mean

from ragbench_lab.answering import answer
from ragbench_lab.conditions import stage_a_conditions
from ragbench_lab.data.preparation import digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.generation import (
    INSTRUCTION,
    GeneratorSettings,
    LocalGenerator,
    load_native_tokenizer,
)
from ragbench_lab.hardware import collect_inventory
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.resources import MemorySampler
from ragbench_lab.run_store import RunStore, request_key, verified_manifest
from ragbench_lab.selection import validate_freeze
from ragbench_lab.serving import isolate_request, resident_model, verify_uncached
from ragbench_lab.stage_a import implementation_identity


def validate_plan(plan: dict) -> None:
    if (plan.get("schema_version") != 1 or plan.get("questions_per_dataset") != 10
            or plan.get("models") != ["qwen", "llama"]
            or type(plan.get("seed")) is not int
            or plan.get("cache_policy") != "unload_then_empty_prompt_preload_per_request"):
        raise DataError("pilot requires 20 development questions and both planned models")
    profiles = plan.get("profiles", [])
    if (len(profiles) != 6 or len({digest(p) for p in profiles}) != 6
            or any(set(p) != {"family", "size", "reranking"}
                   or p["family"] not in {"bm25", "dense", "hybrid"}
                   or p["size"] not in {128, 256} or type(p["reranking"]) is not bool
                   for p in profiles)
            or {p["family"] for p in profiles} != {"bm25", "dense", "hybrid"}
            or {p["size"] for p in profiles} != {128, 256}
            or {p["reranking"] for p in profiles} != {False, True}):
        raise DataError("pilot profiles must cover all declared factor levels without duplicates")
    for name in ("planning_headroom", "wall_budget_hours", "memory_limit_bytes"):
        if (type(plan.get(name)) not in {int, float}
                or not math.isfinite(plan[name]) or plan[name] <= 0):
            raise DataError(f"invalid pilot planning allowance: {name}")
    if plan["planning_headroom"] < 1:
        raise DataError("planning headroom cannot reduce the measured estimate")


def sample_questions(ids: list[str], dataset: str, seed: int) -> list[str]:
    if len(set(ids)) != len(ids) or len(ids) < 10:
        raise DataError("pilot requires ten unique development questions per dataset")
    return sorted(ids, key=lambda qid: digest([seed, "phase6", dataset, qid]))[:10]


def full_profiles() -> list[dict]:
    return [{"family": family, "size": size, "reranking": on}
            for family, size, on in product(("bm25", "dense", "hybrid"),
                                            (128, 256), (False, True))]


def feasibility_summary(results: list[dict], plan: dict) -> dict:
    successful = [r for r in results if r["status"] == "success"]
    model_costs = {}
    for family in plan["models"]:
        cells = []
        for dataset in ("squad", "hotpot_qa"):
            for profile in plan["profiles"]:
                group = [r for r in successful if r["model_family"] == family
                         and r["dataset"] == dataset and r["profile"] == profile]
                if group:
                    cells.append(mean(r["result"]["total_request_seconds"]
                                      + r["isolation"]["seconds"] for r in group))
        model_costs[family] = {"represented_cells": len(cells),
                              "mean_online_plus_isolation_seconds": mean(cells) if cells else None}
    peak = max((r.get("resources", {}).get("peak_rss_bytes") or 0 for r in results), default=0)
    complete = (len(successful) == 40 and len(results) == 40
                and all(m["represented_cells"] == 12 for m in model_costs.values()))
    raw_hours = (sum(m["mean_online_plus_isolation_seconds"] * 7200
                     for m in model_costs.values()) / 3600) if complete else None
    # Future sequential blocks: 48 conditions x three repetitions. Setup is not online latency.
    setup_hours = (max(r["result"]["offline_setup_seconds"] for r in successful) * 144 / 3600
                   if successful else None)
    allowance = ((raw_hours + setup_hours) * plan["planning_headroom"] if complete else None)
    memory_valid = bool(peak) and all(r.get("resources", {}).get("sample_count", 0) > 0
                                     and not r["resources"]["errors"] for r in results)
    ready = (complete and memory_valid and peak <= plan["memory_limit_bytes"]
             and allowance <= plan["wall_budget_hours"])
    return {"planned_requests": 40, "successful_requests": len(successful),
            "failed_requests": len(results) - len(successful), "complete": complete,
            "models": model_costs, "main_study_requests": 14400,
            "projected_online_plus_isolation_hours": raw_hours,
            "projected_block_setup_hours": setup_hours,
            "planning_allowance_hours": allowance, "peak_sampled_rss_bytes": peak,
            "memory_sampling_valid": memory_valid, "freeze_ready": ready,
            "limitations": plan["limitations"]}


def run_pilot(config, plan_path: Path, selection: Path, data_dirs: dict[str, Path],
              assets: Path, index_root: Path, output: Path, server_pid: int,
              base_url: str, cache_proof: Path, freeze_path: Path | None = None) -> dict:
    plan = json.loads(plan_path.read_text())
    validate_plan(plan)
    selected = verified_manifest(selection)
    validate_freeze(selected)
    if config.sha256() != selected["config_sha256"]:
        raise DataError("pilot config differs from frozen retrieval study")
    proof = json.loads(cache_proof.read_text())["observations"]
    if (len(proof) != 6 or {r["family"] for r in proof} != {"qwen", "llama"}
            or any(r["cached"] != 0 for r in proof)):
        raise DataError("successful isolated repeated-prompt proof is required")
    tasks = []
    for dataset in sorted(data_dirs):
        source, bundle = load_prepared(data_dirs[dataset])
        if source["manifest_sha256"] != selected["sources"][dataset]["manifest_sha256"]:
            raise DataError("pilot prepared data differs from frozen source")
        ids = sample_questions(source["split"]["development_ids"], dataset, plan["seed"])
        del bundle
        for i, qid in enumerate(ids):
            profile = plan["profiles"][i % 6]
            recipe = ("bm25" if profile["family"] == "bm25" else
                      f'{profile["family"]}_{selected["selected"]["embedder"]}')
            condition = next(c for c in stage_a_conditions(config) if c.dataset == dataset
                             and c.recipe == recipe and c.size == profile["size"]
                             and c.method == selected["selected"]["chunker"])
            tasks.append({"dataset": dataset, "question_id": qid, "profile": profile,
                          "condition": condition.record()})
    if len(tasks) != 20 or set(data_dirs) != {"squad", "hotpot_qa"}:
        raise DataError("pilot requires exactly twenty questions across both datasets")
    generators = {}
    for family in plan["models"]:
        settings = replace(GeneratorSettings(**json.loads(
            (assets / f"{family}-settings.json").read_text())), base_url=base_url)
        generators[family] = settings
    identity = {"stage": "phase6_pilot", "diagnostic": True, "plan": plan, "tasks": tasks,
                "selection_sha256": selected["manifest_sha256"], "config_sha256": config.sha256(),
                "cache_proof_sha256": file_sha256(cache_proof),
                "provenance": implementation_identity(), "inventory": collect_inventory(),
                "execution_environment": {"tokenizers_parallelism": os.getenv(
                    "TOKENIZERS_PARALLELISM"), "model_parallelism": 1, "loaded_model_limit": 1},
                "models": {f: asdict(s) for f, s in generators.items()}}
    results, contexts = [], {}
    with RunStore(output, identity) as store:
        for family, settings in generators.items():
            settings_file = output / f"{family}-settings.json"
            write_new_json(settings_file, asdict(settings))
            tokenizer = load_native_tokenizer(assets / f"{family}-tokenizer", settings)
            generator = LocalGenerator(settings, tokenizer)
            # Warm generation once, then reset decoder state for each measured request.
            isolate_request(generator)
            warm = generator.generate("Which city?", "The city is Paris.")
            write_new_json(output / f"{family}-warmup.json", warm)
            order = sorted(tasks, key=lambda t: digest([plan["seed"], family, t["question_id"]]))
            for task in order:
                condition = task["condition"]
                cid = digest([family, condition, task["profile"]])
                key = request_key(cid, task["question_id"], 1)
                row = {"kind": "request", "request_key": key, "condition_id": cid,
                       "question_id": task["question_id"], "repetition": 1, "attempt": 1,
                       "model_family": family, "dataset": task["dataset"],
                       "profile": task["profile"], "status": "failed"}
                memory = MemorySampler(server_pid)
                try:
                    with memory:
                        row["isolation"] = isolate_request(generator)
                        index = index_root / digest([config.sha256(),
                            selected["sources"][task["dataset"]]["manifest_sha256"],
                            None, condition["condition_id"]])
                        rerank = task["profile"]["reranking"]
                        result = answer(config, data_dirs[task["dataset"]], index,
                            Path("models/bge-small-en-v1.5/tokenizer.json"), settings_file,
                            assets / f"{family}-tokenizer", output / "answers" / f"{key}.json",
                            question_id=task["question_id"],
                            reranker_config=assets / "reranker-settings.json" if rerank else None,
                            reranker_dir=assets / "reranker" if rerank else None, warmup=True)
                        row["result"] = result
                        if result["status"] != "success":
                            raise DataError(result.get("error", "answer diagnostic failed"))
                        verify_uncached(result.get("generation", {}))
                        row["resident_after"] = resident_model(generator)
                        pair = digest(task)
                        if pair in contexts and contexts[pair] != result["context_sha256"]:
                            raise DataError("paired pilot models received different evidence")
                        contexts[pair] = result["context_sha256"]
                        row["status"] = "success"
                except Exception as error:
                    row.update(error_type=type(error).__name__, error=str(error))
                row["resources"] = memory.summary()
                results.append(row)
                store.append(row)
                print(json.dumps({"completed": len(results), "planned": 40,
                                  "status": row["status"], "model": family}), flush=True)
            generator._json("/api/generate", {"model": settings.model,
                            "stream": False, "keep_alive": 0})
        summary = feasibility_summary(results, plan)
        summary["run_manifest_sha256"] = store.manifest["manifest_sha256"]
        write_new_json(output / "summary.json", summary)
    if freeze_path is not None and summary["freeze_ready"]:
        frozen = {"kind": "frozen_generation_study_plan", "schema_version": 1,
                  "pilot_manifest_sha256": summary["run_manifest_sha256"],
                  "pilot_records_sha256": file_sha256(output / "records.jsonl"),
                  "selection": selected, "generator_settings": identity["models"],
                  "provenance": identity["provenance"], "config": config.as_dict(),
                  "inventory": identity["inventory"],
                  "execution_environment": identity["execution_environment"],
                  "instruction": INSTRUCTION, "instruction_sha256": digest(INSTRUCTION),
                  "reranker": json.loads((assets / "reranker-settings.json").read_text()),
                  "pipeline_profiles": full_profiles(),
                  "question_count_per_dataset": 100, "repetitions": 3,
                  "pipeline_count": 12, "dataset_model_conditions": 48,
                  "main_requests": 14400, "cache_policy": plan["cache_policy"],
                  "feasibility": summary, "execution_runner": "Phase 7 pending implementation",
                  "native_templates": "file hashes pinned in generator settings"}
        frozen["manifest_sha256"] = digest(frozen)
        write_new_json(freeze_path, frozen)
    return summary
