"""Separate pinned No-RAG/gold baseline plans and bounded sequential execution."""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict
from itertools import product
from pathlib import Path
from time import perf_counter
from types import SimpleNamespace

from ragbench_lab.answer_metrics import answer_scores
from ragbench_lab.baselines import baseline_candidates
from ragbench_lab.context import pack_context
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.generation import (
    GenerationError,
    GeneratorSettings,
    LocalGenerator,
    load_native_tokenizer,
)
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.run_store import read_records, request_key, verified_manifest
from ragbench_lab.serving import isolate_request, verify_uncached
from ragbench_lab.stage_a import implementation_identity
from ragbench_lab.stage_b import evaluation_question_ids, execution_plan, validate_study
from ragbench_lab.stage_b_runner import _verify_inputs, completion, request_checks, run_blocks
from ragbench_lab.tokenization import ReferenceTokenizer

BASELINE_RULES = {
    "kinds": ["no_rag", "gold"], "repetitions": 3, "quality_repetition": 1,
    "instruction": "unchanged grounded QA/abstention instruction, including No-RAG",
    "gold": "SQuAD diagnostic paragraphs; Hotpot annotated supporting sentences",
    "packing": "same reference tokenizer, evidence separators and 1024-token budget",
    "timing": "fresh baseline candidate construction, packing, generation; scoring afterward",
    "cache": "unload_then_empty_prompt_preload_per_request",
    "warmup": "synthetic generator-only warmup per block; no retrieval or reranker",
    "reuse": "separate execution identity; never append to or pool with main records",
}


def baseline_plan(config, study: dict, main_manifest: dict, records_sha256: str) -> dict:
    validate_study(config, study)
    identity = main_manifest["identity"]
    expected = execution_plan(config, study)
    if (study["question_count_per_dataset"] != 25 or "reduced_sample" not in study
            or identity["mode"] != "evaluation"
            or identity["study_sha256"] != study["manifest_sha256"]
            or identity["plan"]["main_requests"] != 3600
            or any(identity["plan"][k] != expected[k]
                   for k in ("conditions", "blocks", "question_orders"))
            or identity["config_sha256"] != config.sha256()
            or identity["generator_settings"] != study["generator_settings"]
            or identity["cache_policy"] != study["cache_policy"]
            or identity["reference_tokenizer"] != study["selection"]["tokenizer"]
            or identity["sources"] != study["selection"]["sources"]):
        raise DataError("baseline plan requires the completed reduced parent study")
    if not re.fullmatch(r"[0-9a-f]{64}", records_sha256):
        raise DataError("pin parent main records by SHA-256")
    plan = {"kind": "frozen_stage_b_baseline_plan", "schema_version": 1,
        "study_sha256": study["manifest_sha256"], "config_sha256": config.sha256(),
        "main_run_id": main_manifest["run_id"],
        "main_manifest_sha256": main_manifest["manifest_sha256"],
        "main_records_sha256": records_sha256,
        "question_ids": evaluation_question_ids(study), "question_count_per_dataset": 25,
        "conditions": 8, "blocks": 24, "requests": 600, "rules": BASELINE_RULES}
    plan["manifest_sha256"] = digest(plan)
    return plan


def verify_main(config, study: dict, output: Path) -> tuple[dict, str]:
    if (output / ".writer.lock").exists():
        raise DataError("main run must be stopped before baselines")
    manifest = verified_manifest(output / "manifest.json")
    rows = read_records(output, manifest)
    contexts, candidates = {}, {}
    for row in rows:
        request_checks(row, manifest["identity"], contexts, candidates)
    summary = completion(rows, manifest["identity"])
    if (summary["status"] != "complete" or summary["failed_attempts"]
            or summary["setup_failures"] or summary["successful_requests"] != 3600):
        raise DataError("complete failure-free reduced main matrix required")
    sha = file_sha256(output / "records.jsonl")
    baseline_plan(config, study, manifest, sha)
    return manifest, sha


def plan_baselines(config, study_path: Path, main_run: Path) -> dict:
    study = verified_manifest(study_path)
    manifest, sha = verify_main(config, study, main_run)
    return baseline_plan(config, study, manifest, sha)


def baseline_inputs(kind, question, reference, budget) -> dict:
    candidates = baseline_candidates(kind, question, reference)
    context = pack_context(candidates, reference, budget)
    return json.loads(canonical({"candidates": [asdict(hit) for hit in candidates],
        "context": asdict(context), "context_sha256": digest(context.text)}))


def baseline_identity(config, study: dict, plan: dict, prepared: dict,
                      assets: Path, tokenizer_path: Path, mode: str) -> dict:
    validate_study(config, study)
    if (study["question_count_per_dataset"] != 25 or "reduced_sample" not in study
            or plan.get("kind") != "frozen_stage_b_baseline_plan"
            or type(plan.get("schema_version")) is not int or plan["schema_version"] != 1
            or digest({k: v for k, v in plan.items() if k != "manifest_sha256"})
            != plan.get("manifest_sha256") or plan.get("rules") != BASELINE_RULES
            or plan.get("study_sha256") != study["manifest_sha256"]
            or plan.get("config_sha256") != config.sha256()
            or plan.get("question_ids") != evaluation_question_ids(study)
            or (plan.get("conditions"), plan.get("blocks"), plan.get("requests")) != (8, 24, 600)):
        raise DataError("baseline plan hash, scope or controls mismatch")
    if mode not in {"diagnostic", "evaluation"}:
        raise DataError("unsupported baseline mode")
    if set(prepared) != set(study["selection"]["sources"]):
        raise DataError("both frozen datasets required")
    reference = ReferenceTokenizer(tokenizer_path, config.chunking)
    if reference.identity != study["selection"]["tokenizer"]:
        raise DataError("baseline reference tokenizer differs from main study")
    if os.environ.get("TOKENIZERS_PARALLELISM") != "false":
        raise DataError("baselines require TOKENIZERS_PARALLELISM=false")
    questions = {}
    for dataset, (source, bundle) in prepared.items():
        frozen = study["selection"]["sources"][dataset]
        if source["dataset"] != dataset or any(source[k] != frozen[k] for k in frozen):
            raise DataError("baseline prepared source differs from frozen study")
        questions[dataset] = (sorted(source["split"]["development_ids"])[:1]
                              if mode == "diagnostic" else plan["question_ids"][dataset])
        if not set(questions[dataset]) <= {q.question_id for q in bundle.questions}:
            raise DataError("missing baseline question records")
    for model, settings in study["generator_settings"].items():
        _verify_inputs(assets / f"{model}-tokenizer", settings["tokenizer_files"])
    conditions = []
    for dataset, model, kind in product(sorted(questions), ("llama", "qwen"),
                                         BASELINE_RULES["kinds"]):
        condition = {"dataset": dataset, "model_family": model, "baseline": kind,
            "model_digest": study["generator_settings"][model]["model_digest"],
            "baseline_plan_sha256": plan["manifest_sha256"]}
        condition["condition_id"] = digest(condition)
        conditions.append(condition)
    seed = config.dataset.sampling_seed
    orders, blocks = {}, []
    for rep in (1, 2, 3):
        orders[str(rep)] = {dataset: sorted(ids, key=lambda qid:
            digest([seed, rep, dataset, qid])) for dataset, ids in questions.items()}
        for model in sorted(("llama", "qwen"), key=lambda m: digest([seed, rep, "model", m])):
            for c in sorted((c for c in conditions if c["model_family"] == model),
                            key=lambda c: digest([seed, rep, c["condition_id"]])):
                blocks.append({"condition_id": c["condition_id"], "model_family": model,
                               "repetition": rep, "question_order_dataset": c["dataset"]})
    expected = {}
    for dataset, (_, bundle) in prepared.items():
        by_id = {q.question_id: q for q in bundle.questions}
        for qid in questions[dataset]:
            for kind in BASELINE_RULES["kinds"]:
                expected[digest([dataset, qid, kind])] = baseline_inputs(kind, by_id[qid],
                    reference, config.retrieval.context_budget_tokens)
    return {"stage": "B_baselines", "mode": mode, "diagnostic": mode == "diagnostic",
        "split": "development" if mode == "diagnostic" else "evaluation",
        "baseline_plan_sha256": plan["manifest_sha256"],
        "study_sha256": study["manifest_sha256"], "config_sha256": config.sha256(),
        "sources": study["selection"]["sources"], "generator_settings": study["generator_settings"],
        "reference_tokenizer": reference.identity, "cache_policy": study["cache_policy"],
        "baseline_rules": BASELINE_RULES, "expected_inputs": expected,
        "provenance": implementation_identity(),
        "execution_environment": study["execution_environment"],
        "plan": {"conditions": conditions, "blocks": blocks, "question_orders": orders,
            "main_requests": 24 if mode == "diagnostic" else 600,
            "quality_repetition": 1, "independent_questions_per_dataset": 1
                if mode == "diagnostic" else 25}}


def baseline_checks(row: dict, identity: dict, contexts: dict, candidates: dict) -> None:
    c = next((c for c in identity["plan"]["conditions"]
              if c["condition_id"] == row.get("condition_id")), None)
    rep = row.get("repetition")
    if c is None or type(rep) is not int or rep not in (1, 2, 3):
        raise DataError("baseline row outside matrix")
    if row.get("kind") == "event":
        if (row.get("event"), row.get("status")) not in {
                ("block_warmup", "success"), ("block_setup_failure", "failed")}:
            raise DataError("unsupported baseline event")
        return
    qid = row["question_id"]
    if (row["dataset"] != c["dataset"] or row["model_family"] != c["model_family"]
            or row["split"] != identity["split"]
            or qid not in identity["plan"]["question_orders"][str(rep)][c["dataset"]]
            or row["request_key"] != request_key(c["condition_id"], qid, rep)):
        raise DataError("baseline row identity mismatch")
    if row["status"] == "failed":
        return
    result = row["result"]
    expected = identity["expected_inputs"][digest([c["dataset"], qid, c["baseline"]])]
    if (row["status"] != "success" or result["status"] != "success"
            or result["baseline"] != c["baseline"] or result["question_id"] != qid
            or result["dataset"] != c["dataset"]
            or result["config_sha256"] != identity["config_sha256"]
            or result["source_manifest_sha256"] != identity["sources"][c["dataset"]][
                "manifest_sha256"] or result["inputs"] != expected
            or result["inputs"]["context_sha256"] != digest(result["inputs"]["context"]["text"])
            or result["retrieval_enabled"] is not False
            or result["reranking_enabled"] is not False):
        raise DataError("baseline context/candidate/source controls changed")
    generated = result["generation"]
    verify_uncached(generated)
    settings = identity["generator_settings"][c["model_family"]]
    count = generated["native_prompt_tokens"]
    backend_count = generated["backend_final"]["prompt_eval_count"]
    if (generated["context"] != expected["context"]["text"]
            or generated["context_sha256"] != expected["context_sha256"]
            or type(count) is not int or type(backend_count) is not int or count != backend_count
            or count + settings["maximum_output_tokens"] > settings["context_window"]
            or generated["generator"]["settings"] != settings
            or row["isolation"]["policy"] != identity["cache_policy"]
            or row["resident_after"]["digest"] != c["model_digest"]
            or row["resident_after"]["context_length"] != settings["context_window"]
            or not row["resources"]["sample_count"] or row["resources"]["errors"]
            or not row["resources"]["peak_rss_bytes"]):
        raise DataError("baseline generation/cache/residency/resources differ from pinned controls")
    key = digest([c["dataset"], qid, c["baseline"]])
    for mapping, value in ((contexts, expected["context_sha256"]),
                           (candidates, digest(expected["candidates"]))):
        if key in mapping and mapping[key] != value:
            raise DataError("paired baseline inputs changed")
        mapping[key] = value


def baseline_gate(directory: Path, identity: dict) -> str:
    if (directory / ".writer.lock").exists():
        raise DataError("baseline validation must be stopped")
    manifest = verified_manifest(directory / "manifest.json")
    saved = manifest["identity"]
    if (saved["stage"] != "B_baselines" or saved["mode"] != "diagnostic"
            or saved["split"] != "development" or saved["plan"]["main_requests"] != 24
            or len(saved["plan"]["conditions"]) != 8 or len(saved["plan"]["blocks"]) != 24
            or saved["plan"]["conditions"] != identity["plan"]["conditions"]
            or saved["plan"]["blocks"] != identity["plan"]["blocks"]
            or any(saved[k] != identity[k] for k in (
                "baseline_plan_sha256", "study_sha256", "config_sha256", "sources",
                "generator_settings", "reference_tokenizer", "cache_policy", "baseline_rules",
                "provenance", "execution_environment"))):
        raise DataError("baseline validation differs from execution identity")
    for orders in saved["plan"]["question_orders"].values():
        if orders != {d: sorted(s["split"]["development_ids"])[:1]
                      for d, s in saved["sources"].items()}:
            raise DataError("baseline validation must use the declared development questions")
    rows = read_records(directory, manifest)
    contexts, candidates = {}, {}
    for row in rows:
        baseline_checks(row, saved, contexts, candidates)
    summary = completion(rows, saved)
    if (summary["successful_requests"] != 24 or summary["failed_attempts"]
            or summary["setup_failures"]):
        raise DataError("full 24-request baseline development validation required")
    return manifest["manifest_sha256"]


def measured_baseline(session, question, generator) -> dict:
    result = {"baseline": session.baseline, "question_id": question.question_id,
        "dataset": question.dataset, "question": question.text, "status": "failed",
        "config_sha256": session.config.sha256(), "source_manifest_sha256": session.source[
            "manifest_sha256"], "retrieval_enabled": False, "reranking_enabled": False,
        "purpose": "separate baseline comparison", "stage": "baseline_candidates"}
    started = perf_counter()
    try:
        result["inputs"] = baseline_inputs(session.baseline, question, session.reference,
                                          session.config.retrieval.context_budget_tokens)
        result["context_preparation_seconds"] = perf_counter() - started
        result["stage"] = "generation"
        generated = generator.generate(question.text, result["inputs"]["context"]["text"])
        generated["purpose"] = result["purpose"]
        result.update(generation=generated, total_request_seconds=perf_counter() - started)
        verify_uncached(generated)
        result["stage"] = "evaluation"
        result["answer_metrics"] = answer_scores(generated["answer"], question.answers,
                                                 question.dataset)
        result["context_evidence_metrics"] = evidence_metrics(question, [
            (e["document_id"], e["source_start"], e["source_end"])
            for e in result["inputs"]["context"]["evidence"]])
        result.update(status="success", stage="complete")
    except Exception as error:
        if isinstance(error, GenerationError):
            result["generation"] = error.record
        result.update(error=str(error), error_type=type(error).__name__,
                      failed_request_seconds=perf_counter() - started)
    return result


def run_baselines(config, study_path: Path, plan_path: Path, main_run: Path, data_dirs: dict,
                  assets: Path, tokenizer_path: Path, output: Path, server_pid: int,
                  max_requests: int, mode: str = "diagnostic", resume: bool = False,
                  retry_failures: bool = False, validation_run: Path | None = None) -> dict:
    if type(max_requests) is not int or max_requests <= 0:
        raise DataError("explicit positive baseline request bound required")
    study = verified_manifest(study_path)
    plan = verified_manifest(plan_path)
    if plan != plan_baselines(config, study_path, main_run):
        raise DataError("baseline plan differs from completed parent or declared controls")
    prepared = {dataset: load_prepared(path) for dataset, path in data_dirs.items()}
    identity = baseline_identity(config, study, plan, prepared, assets, tokenizer_path, mode)
    if mode == "evaluation":
        if validation_run is None:
            raise DataError("baseline evaluation requires its own completed development gate")
        identity["validation_manifest_sha256"] = baseline_gate(validation_run, identity)
    elif validation_run is not None:
        raise DataError("baseline diagnostics do not accept an evaluation gate")
    reference = ReferenceTokenizer(tokenizer_path, config.chunking)

    def setup(c):
        started = perf_counter()
        model = c["model_family"]
        settings = GeneratorSettings(**identity["generator_settings"][model])
        generator = LocalGenerator(settings, load_native_tokenizer(assets / f"{model}-tokenizer",
                                                                   settings))
        generator.identity["cache_policy"] = identity["cache_policy"]
        try:
            isolate_request(generator)
            warm = generator.generate("Which city?", "The city is Paris.")
            verify_uncached(warm)
            source, bundle = prepared[c["dataset"]]
            session = SimpleNamespace(config=config, source=source, reference=reference,
                                      baseline=c["baseline"], bundle=bundle, mode=mode)
            return session, generator, None, {"offline_setup_seconds": perf_counter() - started,
                "warm_generation": warm, "generator_identity": generator.identity,
                "baseline": c["baseline"], "retrieval_enabled": False, "reranking_enabled": False}
        except (Exception, KeyboardInterrupt) as error:
            try:
                generator._json("/api/generate", {"model": settings.model,
                                                "stream": False, "keep_alive": 0})
            except Exception as unload_error:
                error.add_note(f"baseline setup cleanup failed: {unload_error}")
            raise

    def execute(session, qid, generator, reranker):
        question = next(q for q in session.bundle.questions if q.question_id == qid)
        result = measured_baseline(session, question, generator)
        result["purpose"] = f"Stage B baseline {mode}"
        if "generation" in result:
            result["generation"]["purpose"] = result["purpose"]
        return result

    return run_blocks(identity, output, setup, execute, server_pid, max_requests,
                      resume, retry_failures, check_request=baseline_checks)
