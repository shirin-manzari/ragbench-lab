"""Bounded sequential Stage B execution with immutable provenance and explicit retries."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

from ragbench_lab.data.preparation import digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import MODELS, file_sha256, verify_file
from ragbench_lab.execution import measured_answer
from ragbench_lab.generation import GeneratorSettings, LocalGenerator, load_native_tokenizer
from ragbench_lab.pipeline import load_retriever, search_query
from ragbench_lab.reranking import LocalReranker, RerankerSettings
from ragbench_lab.resources import MemorySampler
from ragbench_lab.run_store import RunStore, read_records, request_key, verified_manifest
from ragbench_lab.serving import isolate_request, resident_model, verify_uncached
from ragbench_lab.stage_a import implementation_identity, timestamp
from ragbench_lab.stage_b import evaluation_question_ids, execution_plan
from ragbench_lab.tokenization import ReferenceTokenizer


def index_path(root: Path, plan: dict, study: dict, condition: dict) -> Path:
    return root / digest([plan["config_sha256"], study["selection"]["sources"][
        condition["dataset"]]["manifest_sha256"], None, condition["retrieval_condition_id"]])


def _verify_inputs(directory: Path, files: dict) -> None:
    actual = {p.name for p in directory.iterdir() if p.is_file()
              and p.suffix in {".json", ".txt", ".model", ".jinja", ".bin", ".safetensors"}}
    if actual != set(files) or any(file_sha256(directory / name) != value
                                   for name, value in files.items()):
        raise DataError("missing, changed or unpinned model loader inputs")


def runner_identity(config, study: dict, prepared: dict, assets: Path,
                    index_root: Path, tokenizer_path: Path, models_root: Path,
                    mode: str, question_limit: int | None) -> dict:
    plan = execution_plan(config, study)
    if mode not in {"diagnostic", "evaluation"}:
        raise DataError("unsupported Stage B execution mode")
    if mode == "diagnostic":
        if type(question_limit) is not int or not 1 <= question_limit <= 50:
            raise DataError("diagnostic question limit must be between 1 and 50")
    elif question_limit is not None:
        raise DataError("held-out evaluation cannot reduce the frozen matrix")
    if os.environ.get("TOKENIZERS_PARALLELISM") != "false":
        raise DataError("Stage B requires TOKENIZERS_PARALLELISM=false")
    if set(prepared) != {"squad", "hotpot_qa"}:
        raise DataError("Stage B requires both datasets")
    reference = ReferenceTokenizer(tokenizer_path, config.chunking)
    if reference.identity != study["selection"]["tokenizer"]:
        raise DataError("reference tokenizer differs from frozen study")
    sources, questions = {}, {}
    for dataset, (source, bundle) in prepared.items():
        frozen = study["selection"]["sources"][dataset]
        if source["dataset"] != dataset or any(source[k] != frozen[k] for k in frozen):
            raise DataError("prepared data differs from frozen study")
        sources[dataset] = frozen
        questions[dataset] = (sorted(source["split"]["development_ids"])[:question_limit]
                              if mode == "diagnostic"
                              else evaluation_question_ids(study)[dataset])
        if not set(questions[dataset]) <= {q.question_id for q in bundle.questions}:
            raise DataError("prepared question records are incomplete")
    settings = study["generator_settings"]
    for model, values in settings.items():
        _verify_inputs(assets / f"{model}-tokenizer", values["tokenizer_files"])
    reranker = RerankerSettings(**study["reranker"])
    _verify_inputs(assets / "reranker", reranker.files)
    family = study["selection"]["selected"]["embedder"]
    spec = MODELS[family]
    files = {name: verify_file(models_root / spec["directory"] / name, spec)
             for name in [*spec["files"], "model.safetensors"]}
    if files != study["selection"]["model_files"][family]:
        raise DataError("embedding assets differ from frozen study")
    indexes = {}
    for condition in plan["conditions"]:
        cid = condition["retrieval_condition_id"]
        if cid in indexes:
            continue
        manifest = verified_manifest(
            index_path(index_root, plan, study, condition) / "manifest.json")
        if (manifest["document_limit"] is not None
                or manifest["config_sha256"] != config.sha256()
                or manifest["source_manifest_sha256"] != sources[condition["dataset"]][
                    "manifest_sha256"] or manifest["recipe"] != condition["recipe"]
                or manifest["method"] != condition["method"]
                or manifest["size"] != condition["size"]):
            raise DataError("Stage B index differs from declared condition")
        indexes[cid] = manifest["manifest_sha256"]
    # Diagnostic questions get their own recorded order, never masquerading as held-out.
    for rep in (1, 2, 3):
        plan["question_orders"][str(rep)] = {dataset: sorted(ids,
            key=lambda qid: digest([config.dataset.sampling_seed, rep, dataset, qid]))
            for dataset, ids in sorted(questions.items())}
    plan.pop("manifest_sha256")
    plan.update(runner_status="implemented; model-backed validation required before evaluation",
                main_requests=sum(len(questions[c["dataset"]]) * 3 for c in plan["conditions"]),
                independent_questions_per_dataset=len(next(iter(questions.values()))))
    plan["manifest_sha256"] = digest(plan)
    return {"stage": "B", "mode": mode, "diagnostic": mode == "diagnostic",
            "split": "development" if mode == "diagnostic" else "evaluation",
            "study_sha256": study["manifest_sha256"], "config_sha256": config.sha256(),
            "plan": plan, "sources": sources, "indexes": indexes,
            "generator_settings": settings, "reranker_settings": asdict(reranker),
            "reference_tokenizer": reference.identity, "embedder_files": files,
            "question_limit": question_limit, "quality_repetition": 1,
            "warmup_policy": "generation and full retrieval/reranker warmup per condition block",
            "cache_policy": study["cache_policy"], "provenance": implementation_identity(),
            "execution_environment": {**study["execution_environment"],
                "tokenizers_parallelism": os.environ["TOKENIZERS_PARALLELISM"]}}


def request_checks(row: dict, identity: dict, contexts: dict, candidates: dict) -> None:
    conditions = {c["condition_id"]: c for c in identity["plan"]["conditions"]}
    c = conditions.get(row.get("condition_id"))
    rep = row.get("repetition")
    if c is None or type(rep) is not int or rep not in (1, 2, 3):
        raise DataError("request/event outside Stage B matrix")
    if row.get("kind") == "event":
        if (row.get("event"), row.get("status")) not in {
                ("block_warmup", "success"), ("block_setup_failure", "failed")}:
            raise DataError("unsupported Stage B event")
        return
    if (row["dataset"] != c["dataset"] or row["model_family"] != c["model_family"]
            or row["split"] != identity["split"]
            or row["question_id"] not in identity["plan"]["question_orders"][str(rep)][c["dataset"]]
            or row["request_key"] != request_key(c["condition_id"], row["question_id"], rep)):
        raise DataError("Stage B request differs from declared split/condition")
    if row["status"] != "success":
        return
    result = row["result"]
    if (result["status"] != "success" or result["question_id"] != row["question_id"]
            or result["dataset"] != row["dataset"]
            or result["config_sha256"] != identity["config_sha256"]
            or result["source_manifest_sha256"] != identity["sources"][c["dataset"]][
                "manifest_sha256"] or result["index_sha256"] != identity["indexes"][
                c["retrieval_condition_id"]]
            or result["context_sha256"] != digest(result["context"]["text"])
            or result["reranking"]["enabled"] is not c["reranking"]):
        raise DataError("persisted result identity differs from Stage B request")
    generated = result["generation"]
    verify_uncached(generated)
    final = generated["backend_final"]
    settings = identity["generator_settings"][c["model_family"]]
    if (generated["context_sha256"] != result["context_sha256"]
            or generated["context"] != result["context"]["text"]
            or type(generated["native_prompt_tokens"]) is not int
            or type(final["prompt_eval_count"]) is not int
            or generated["native_prompt_tokens"] != final["prompt_eval_count"]
            or generated["native_prompt_tokens"] + settings["maximum_output_tokens"]
                > settings["context_window"]
            or generated["generator"]["settings"] != settings):
        raise DataError("generator counts/context/settings differ from frozen request")
    if (row["isolation"]["policy"] != identity["cache_policy"]
            or row["resident_after"]["digest"] != c["model_digest"]
            or row["resident_after"]["context_length"] != settings["context_window"]
            or not row["resources"]["sample_count"] or row["resources"]["errors"]
            or not row["resources"]["peak_rss_bytes"]):
        raise DataError("invalid cache isolation/residency/resource measurement")
    context_key = digest([c["pipeline_id"], c["dataset"], row["question_id"]])
    candidate_key = digest([c["retrieval_condition_id"], row["question_id"]])
    candidate_hash = digest(result["retrieval"]["initial_candidates"])
    if candidate_hash != result["initial_candidates_sha256"]:
        raise DataError("initial candidate record/hash mismatch")
    for mapping, key, value in ((contexts, context_key, result["context_sha256"]),
                                (candidates, candidate_key, candidate_hash)):
        if key in mapping and mapping[key] != value:
            raise DataError("paired context/candidates changed across models or repetitions")
    contexts[context_key], candidates[candidate_key] = result["context_sha256"], candidate_hash


def completion(rows: list[dict], identity: dict) -> dict:
    requests = [r for r in rows if r.get("kind") != "event"]
    planned = identity["plan"]["main_requests"]
    succeeded = len({r["request_key"] for r in requests if r["status"] == "success"})
    return {"planned_requests": planned, "successful_requests": succeeded,
            "failed_attempts": sum(r["status"] == "failed" for r in requests),
            "setup_failures": sum(r.get("event") == "block_setup_failure" for r in rows),
            "remaining_requests": planned - succeeded, "diagnostic": identity["diagnostic"],
            "status": "complete" if planned == succeeded else "incomplete"}


def validate_gate(directory: Path, identity: dict) -> str:
    if (directory / ".writer.lock").exists():
        raise DataError("validation run must be stopped")
    manifest = verified_manifest(directory / "manifest.json")
    saved = manifest["identity"]
    if saved["mode"] != "diagnostic" or any(saved[k] != identity[k] for k in (
            "study_sha256", "config_sha256", "sources", "indexes", "generator_settings",
            "reranker_settings", "reference_tokenizer", "embedder_files", "provenance",
            "execution_environment", "cache_policy", "warmup_policy")):
        raise DataError("diagnostic validation identity differs from evaluation")
    limit = saved["question_limit"]
    if (type(limit) is not int or not 1 <= limit <= 50 or saved["split"] != "development"
            or len(saved["plan"]["conditions"]) != 48
            or saved["plan"]["conditions"] != identity["plan"]["conditions"]
            or saved["plan"]["blocks"] != identity["plan"]["blocks"]):
        raise DataError("validation requires the same full condition/block matrix")
    for orders in saved["plan"]["question_orders"].values():
        if set(orders) != set(saved["sources"]):
            raise DataError("validation lacks a required dataset question order")
        for dataset, source in saved["sources"].items():
            ids = sorted(source["split"]["development_ids"])[:limit]
            if len(orders[dataset]) != limit or set(orders[dataset]) != set(ids):
                raise DataError("validation questions differ from declared development sample")
    rows = read_records(directory, manifest)
    contexts, candidates = {}, {}
    for row in rows:
        request_checks(row, saved, contexts, candidates)
    summary = completion(rows, saved)
    if (summary["status"] != "complete" or summary["failed_attempts"]
            or summary["setup_failures"] or summary["planned_requests"] < 144
            or summary["planned_requests"] != 144 * limit
            or len(saved["plan"]["conditions"]) != 48
            or len(saved["plan"]["blocks"]) != 144):
        raise DataError("full 48-condition development diagnostic must pass before evaluation")
    return manifest["manifest_sha256"]


def run_blocks(identity: dict, output: Path, setup_block, execute, server_pid: int,
               max_requests: int, resume: bool = False, retry_failures: bool = False) -> dict:
    """Small orchestration seam permits synthetic resume/failure tests without models."""
    if type(max_requests) is not int or max_requests <= 0:
        raise DataError("an explicit positive max-requests bound is required")
    if retry_failures and not resume:
        raise DataError("retry-failures requires resume")
    if type(server_pid) is not int or server_pid <= 0 or server_pid == os.getpid():
        raise DataError("provide the dedicated model server PID, not the caller")
    contexts, candidates, history = {}, {}, {}
    attempted = 0
    with RunStore(output, identity, resume) as store:
        for row in store.rows:
            request_checks(row, identity, contexts, candidates)
            if row.get("kind") != "event":
                history.setdefault(row["request_key"], []).append(row)
        conditions = {c["condition_id"]: c for c in identity["plan"]["conditions"]}
        for block in identity["plan"]["blocks"]:
            c = conditions[block["condition_id"]]
            rep = block["repetition"]
            qids = identity["plan"]["question_orders"][str(rep)][c["dataset"]]
            pending = [qid for qid in qids if not any(r["status"] == "success" for r in
                history.get(request_key(c["condition_id"], qid, rep), [])) and
                (retry_failures or not history.get(request_key(c["condition_id"], qid, rep)))]
            if not pending:
                continue
            base = {"condition_id": c["condition_id"], "repetition": rep}
            try:
                session, generator, reranker, setup = setup_block(c)
                store.append({**base, "kind": "event", "event": "block_warmup",
                              "status": "success", "timestamp": timestamp(), "setup": setup})
            except (Exception, KeyboardInterrupt) as error:
                store.append({**base, "kind": "event", "event": "block_setup_failure",
                              "status": "failed", "timestamp": timestamp(),
                              "error_type": type(error).__name__, "error": str(error),
                              "cleanup_notes": getattr(error, "__notes__", []),
                              "partial_generation": getattr(error, "record", None)})
                if isinstance(error, KeyboardInterrupt):
                    raise
                return completion(store.rows, identity)
            summary = None
            try:
                for qid in pending:
                    key = request_key(c["condition_id"], qid, rep)
                    row = {**base, "kind": "request", "request_key": key,
                        "dataset": c["dataset"], "model_family": c["model_family"],
                        "question_id": qid, "split": identity["split"],
                        "attempt": len(history.get(key, [])) + 1,
                        "started_at": timestamp(), "status": "failed"}
                    memory = MemorySampler(server_pid)
                    interrupted = False
                    try:
                        with memory:
                            row["isolation"] = isolate_request(generator)
                            row["result"] = execute(session, qid, generator, reranker)
                            if row["result"]["status"] != "success":
                                raise DataError(row["result"].get("error", "request failed"))
                            row["resident_after"] = resident_model(generator)
                        row["resources"] = memory.summary()
                        if not any(server_pid in {p["pid"] for p in sample["processes"]}
                                   for sample in row["resources"]["samples"]):
                            raise DataError("dedicated server absent from memory samples")
                        row["status"] = "success"
                        request_checks(row, identity, contexts, candidates)
                    except (Exception, KeyboardInterrupt) as error:
                        interrupted = isinstance(error, KeyboardInterrupt)
                        row.update(status="failed", error_type=type(error).__name__,
                                   error=str(error), resources=memory.summary(),
                                   interrupted=interrupted)
                    row["finished_at"] = timestamp()
                    persisted = store.append(row)
                    history.setdefault(key, []).append(persisted)
                    attempted += 1
                    summary = completion(store.rows, identity)
                    print(json.dumps({**summary, "session_attempts": attempted,
                                      "last_status": row["status"]}), flush=True)
                    if interrupted:
                        raise KeyboardInterrupt()
                    if row["status"] == "failed" or attempted >= max_requests:
                        return summary
            finally:
                # No other model or server is stopped. Unload errors remain visible events.
                try:
                    generator._json("/api/generate", {"model": generator.settings.model,
                                    "stream": False, "keep_alive": 0})
                except Exception as error:
                    store.append({**base, "kind": "event", "event": "block_setup_failure",
                        "status": "failed", "timestamp": timestamp(),
                        "error_type": type(error).__name__, "error": f"unload failed: {error}"})
                if summary is not None:
                    summary.update(completion(store.rows, identity))
                del session, generator, reranker
        return completion(store.rows, identity)


def run_stage_b(config, study_path: Path, data_dirs: dict, assets: Path, index_root: Path,
                output: Path, tokenizer_path: Path, server_pid: int, max_requests: int,
                models_root: Path = Path("models"), mode: str = "diagnostic",
                question_limit: int | None = 1, resume: bool = False,
                retry_failures: bool = False, validation_run: Path | None = None) -> dict:
    # No backend side effects occur until local identities and evaluation gate pass.
    if type(max_requests) is not int or max_requests <= 0:
        raise DataError("an explicit positive max-requests bound is required")
    if mode == "evaluation" and validation_run is None:
        raise DataError("evaluation requires a completed compatible diagnostic validation run")
    study = verified_manifest(study_path)
    prepared = {name: load_prepared(path) for name, path in data_dirs.items()}
    identity = runner_identity(config, study, prepared, assets, index_root, tokenizer_path,
                               models_root, mode, question_limit)
    if mode == "evaluation":
        if validation_run is None:
            raise DataError("evaluation requires a completed compatible diagnostic validation run")
        identity["validation_manifest_sha256"] = validate_gate(validation_run, identity)
    elif validation_run is not None:
        raise DataError("diagnostics do not accept an evaluation validation gate")

    def setup_block(condition):
        started = perf_counter()
        model = condition["model_family"]
        settings = GeneratorSettings(**identity["generator_settings"][model])
        generator = LocalGenerator(settings, load_native_tokenizer(assets / f"{model}-tokenizer",
                                                                   settings))
        generator.identity["cache_policy"] = identity["cache_policy"]
        try:
            return warm_block(condition, generator, started)
        except (Exception, KeyboardInterrupt) as error:
            try:
                generator._json("/api/generate", {"model": settings.model,
                                                "stream": False, "keep_alive": 0})
            except Exception as unload_error:
                error.add_note(f"setup cleanup also failed: {unload_error}")
            raise

    def warm_block(condition, generator, started):
        dataset = condition["dataset"]
        # Warm weights/decoder once, then reset decoder for each measured request.
        isolate_request(generator)
        warm = generator.generate("Which city?", "The city is Paris.")
        verify_uncached(warm)
        session = load_retriever(config, data_dirs[dataset],
            index_path(index_root, identity["plan"], study, condition), tokenizer_path,
            condition["recipe"], models_root, prepared[dataset])
        if session.manifest["manifest_sha256"] != identity["indexes"][
                condition["retrieval_condition_id"]]:
            raise DataError("index changed after execution manifest preparation")
        reranker = LocalReranker(assets / "reranker", RerankerSettings(
            **identity["reranker_settings"])) if condition["reranking"] else None
        ranked, _, _ = search_query(session, "Warmup retrieval query.")
        if reranker:
            reranker.rerank("Warmup retrieval query.", ranked)
        return session, generator, reranker, {"offline_setup_seconds": perf_counter() - started,
            "warm_generation": warm, "index_statistics": session.manifest["statistics"],
            "generator_identity": generator.identity,
            "reranker_identity": reranker.identity if reranker else None}

    def execute(session, qid, generator, reranker):
        question = next(q for q in session.bundle.questions if q.question_id == qid)
        result = measured_answer(session, question, generator, reranker)
        purpose = "Stage B development diagnostic" if mode == "diagnostic" else "Stage B held-out"
        result.update(purpose=purpose, schema_version=1)
        if "generation" in result:
            result["generation"]["purpose"] = purpose
        return result

    return run_blocks(identity, output, setup_block, execute, server_pid, max_requests,
                      resume, retry_failures)
