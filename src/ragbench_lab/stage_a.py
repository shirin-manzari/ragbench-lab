from __future__ import annotations

import os
import platform
import subprocess
from datetime import UTC, datetime
from importlib.metadata import distributions
from pathlib import Path
from time import perf_counter

from ragbench_lab.conditions import Condition, block_order, stage_a_conditions
from ragbench_lab.config import ExperimentConfig
from ragbench_lab.data.preparation import digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import MODELS, file_sha256, verify_file
from ragbench_lab.pipeline import build_index, load_retriever, retrieve_query
from ragbench_lab.run_store import RunStore, request_key, verified_manifest
from ragbench_lab.tokenization import ReferenceTokenizer

SELECTION_RULE = {
    "version": "equal_dataset_dense_hybrid_size_context_coverage_v1",
    "quality_repetition": 1, "quality_attempt": 1, "close_absolute": 0.01,
    "tie_breakers": ["mean_per_question_retrieval_latency", "mean_indexing_seconds",
                     "lexical_embedder_chunker"],
    "warmups_per_block": 1, "reusable_query_cache": False,
}


def timestamp() -> str:
    return datetime.now(UTC).isoformat()


def implementation_identity() -> dict:
    def git(*args):
        result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
        if result.returncode:
            raise DataError("Stage A provenance requires a Git workspace")
        return result.stdout.strip()

    files = sorted([*Path("src/ragbench_lab").rglob("*.py"),
                    *Path("configs").glob("*.toml"), Path("pyproject.toml"),
                    Path("requirements.lock")])
    return {"git_revision": git("rev-parse", "HEAD"),
            "git_dirty": bool(git("status", "--porcelain")),
            "source_tree_sha256": digest({str(p): file_sha256(p) for p in files}),
            "packages": dict(sorted((d.metadata["Name"].lower(), d.version)
                                    for d in distributions())),
            "hardware": {"system": platform.system(), "release": platform.release(),
                         "machine": platform.machine(), "cpu": platform.processor(),
                         "logical_cores": os.cpu_count(), "python": platform.python_version()},
            "thread_environment": {key: os.environ.get(key) for key in
                                   ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                    "VECLIB_MAXIMUM_THREADS", "KMP_DUPLICATE_LIB_OK")}}


def manifest_identity(config: ExperimentConfig, prepared: dict, tokenizer_path: Path,
                      models_root: Path, split: str, document_limit: int | None,
                      question_limit: int | None, condition_limit: int | None,
                      freeze: dict | None) -> dict:
    if split not in {"development", "evaluation"}:
        raise DataError("unsupported Stage A split")
    if config.embedding is None:
        raise DataError("Stage A requires pinned embedding configuration")
    for name, limit in (("document", document_limit), ("question", question_limit),
                        ("condition", condition_limit)):
        if limit is not None and (type(limit) is not int or limit <= 0):
            raise DataError(f"{name} limit must be positive")
    if set(prepared) != set(config.dataset.names):
        raise DataError("provide each configured dataset exactly once")
    tokenizer = ReferenceTokenizer(tokenizer_path, config.chunking)
    model_files = {}
    for family, spec in MODELS.items():
        model_files[family] = {name: verify_file(models_root / spec["directory"] / name, spec)
                               for name in [*spec["files"], "model.safetensors"]}
    conditions = stage_a_conditions(config)
    if condition_limit is not None:
        conditions = conditions[:condition_limit]
    questions = {}
    sources = {}
    for dataset, (source, _) in prepared.items():
        if source["dataset"] != dataset:
            raise DataError("dataset directory does not match its declared dataset")
        saved = source["split"]
        if (len(saved["development_ids"]) != config.dataset.development_questions
                or len(saved["evaluation_ids"]) != config.dataset.evaluation_questions):
            raise DataError("prepared split counts do not match config; prepare a new run set")
        questions[dataset] = saved[split + "_ids"][:question_limit]
        sources[dataset] = {key: source[key] for key in
                            ("manifest_sha256", "source_sha256", "corpus_sha256", "split")}
    diagnostic = any(limit is not None for limit in
                     (document_limit, question_limit, condition_limit))
    if split == "evaluation":
        if freeze is None or diagnostic:
            raise DataError("held-out Stage A requires a verified freeze and unbounded matrix")
        if (freeze["config_sha256"] != config.sha256() or freeze["sources"] != sources
                or freeze["model_files"] != model_files
                or freeze["tokenizer"] != tokenizer.identity):
            raise DataError("selection freeze does not match evaluation config/data/models")
    provenance = implementation_identity()
    if split == "evaluation" and any(provenance[key] != freeze["provenance"][key] for key in
                                     ("source_tree_sha256", "packages", "hardware",
                                      "thread_environment")):
        raise DataError("frozen implementation/environment changed; start a separate study")
    return {
        "stage": "A", "split": split, "diagnostic": diagnostic,
        "config": config.as_dict(), "config_sha256": config.sha256(),
        "sources": sources, "model_files": model_files, "tokenizer": tokenizer.identity,
        "conditions": [c.record() for c in conditions], "question_ids": questions,
        "document_limit": document_limit, "question_limit": question_limit,
        "condition_limit": condition_limit, "selection_rule": SELECTION_RULE,
        "selection_freeze_sha256": freeze["manifest_sha256"] if freeze else None,
        "provenance": provenance,
        "block_orders": {str(rep): [c.condition_id for c in block_order(
            conditions, config.dataset.sampling_seed, rep)] for rep in (1, 2, 3)},
    }


def validate_requests(rows: list[dict], identity: dict) -> None:
    conditions = {c["condition_id"]: c for c in identity["conditions"]}
    for row in rows:
        condition = conditions.get(row.get("condition_id"))
        if row.get("kind") == "event":
            if (condition is None or row.get("repetition") not in (1, 2, 3)
                    or (row.get("event"), row.get("status")) not in {
                        ("block_warmup", "success"), ("block_setup_failure", "failed")}):
                raise DataError("event has invalid condition, repetition, or status")
            continue
        if (condition is None or row["dataset"] != condition["dataset"]
                or row["split"] != identity["split"]
                or row["question_id"] not in identity["question_ids"][condition["dataset"]]
                or type(row["repetition"]) is not int or row["repetition"] not in (1, 2, 3)):
            raise DataError("persisted request outside declared Stage A matrix/split")
        if row["status"] == "success":
            result = row["result"]
            if (result["config_sha256"] != identity["config_sha256"]
                    or result["dataset"] != condition["dataset"]
                    or result["question_id"] != row["question_id"]
                    or result["recipe"] != condition["recipe"]
                    or result["method"] != condition["method"]
                    or result["size"] != condition["size"]
                    or result["index_sha256"] != row["index_sha256"]
                    or result["source_manifest_sha256"] != identity["sources"][
                        condition["dataset"]]["manifest_sha256"]):
                raise DataError("persisted result differs from declared request")


def run_stage_a(config: ExperimentConfig, data_dirs: dict[str, Path], index_root: Path,
                output: Path, tokenizer_path: Path, models_root: Path = Path("models"),
                split: str = "development", document_limit: int | None = None,
                question_limit: int | None = None, condition_limit: int | None = None,
                resume: bool = False, retry_failures: bool = False,
                max_requests: int | None = None, freeze_path: Path | None = None) -> dict:
    if max_requests is not None and (type(max_requests) is not int or max_requests <= 0):
        raise DataError("max requests must be positive")
    if retry_failures and not resume:
        raise DataError("retry failures requires --resume")
    prepared = {name: load_prepared(path) for name, path in data_dirs.items()}
    freeze = verified_manifest(freeze_path) if freeze_path else None
    if freeze is not None:
        from ragbench_lab.selection import validate_freeze

        validate_freeze(freeze)
    identity = manifest_identity(config, prepared, tokenizer_path, models_root, split,
                                 document_limit, question_limit, condition_limit, freeze)
    conditions = {c["condition_id"]: Condition(**{k: v for k, v in c.items()
                                               if k != "condition_id"})
                  for c in identity["conditions"]}
    executed = 0
    with RunStore(output, identity, resume) as store:
        validate_requests(store.rows, identity)
        history: dict[str, list[dict]] = {}
        for row in store.rows:
            if row.get("kind") != "event":
                history.setdefault(row["request_key"], []).append(row)
        for repetition in (1, 2, 3):
            for condition_id in identity["block_orders"][str(repetition)]:
                condition = conditions[condition_id]
                qids = identity["question_ids"][condition.dataset]
                pending = [qid for qid in qids if not any(r["status"] == "success" for r in
                           history.get(request_key(condition_id, qid, repetition), []))
                           and (retry_failures or not history.get(
                               request_key(condition_id, qid, repetition)))]
                if not pending:
                    continue
                index_dir = index_root / digest([identity["config_sha256"],
                    identity["sources"][condition.dataset]["manifest_sha256"],
                    document_limit, condition_id])
                session = None
                started = perf_counter()
                try:
                    if not index_dir.exists():
                        build_index(config, data_dirs[condition.dataset], tokenizer_path,
                                    condition.method, condition.size, index_dir,
                                    document_limit, condition.recipe, models_root)
                    session = load_retriever(config, data_dirs[condition.dataset], index_dir,
                                             tokenizer_path, condition.recipe, models_root,
                                             prepared[condition.dataset])
                    if session.manifest["document_limit"] != document_limit:
                        raise DataError("saved index corpus limit mismatch")
                    warmup_started = perf_counter()
                    retrieve_query(session, pending[0], qids)
                    warmup = {"kind": "event", "event": "block_warmup", "status": "success",
                                  "condition_id": condition_id, "repetition": repetition,
                                  "timestamp": timestamp(), "index_sha256": session.manifest[
                                      "manifest_sha256"], "question_id": pending[0],
                                  "warmup_seconds": perf_counter() - warmup_started,
                                  "offline_setup_seconds": perf_counter() - started,
                                  "index_statistics": session.manifest["statistics"]}
                except Exception as error:
                    store.append({"kind": "event", "event": "block_setup_failure",
                                  "status": "failed", "condition_id": condition_id,
                                  "repetition": repetition, "timestamp": timestamp(),
                                  "error_type": type(error).__name__, "error": str(error),
                                  "elapsed_seconds": perf_counter() - started})
                    # Never turn an offline setup/warmup failure into an online timing sample.
                    continue
                store.append(warmup)
                for question_id in pending:
                    key = request_key(condition_id, question_id, repetition)
                    base = {"kind": "request", "run_id": store.manifest["manifest_sha256"],
                            "request_key": key, "condition_id": condition_id,
                            "dataset": condition.dataset, "question_id": question_id,
                            "repetition": repetition, "attempt": len(history.get(key, [])) + 1,
                            "split": split, "started_at": timestamp(),
                            "index_sha256": session.manifest["manifest_sha256"]}
                    started = perf_counter()
                    try:
                        result = retrieve_query(session, question_id, qids)
                        result["purpose"] = (
                            "Stage A diagnostic" if identity["diagnostic"] else "Stage A")
                        row = {**base, "status": "success", "finished_at": timestamp(),
                               "result": result}
                    except Exception as error:
                        row = {**base, "status": "failed", "finished_at": timestamp(),
                               "error_type": type(error).__name__, "error": str(error),
                               "failed_request_seconds": perf_counter() - started}
                    row = store.append(row)
                    history.setdefault(key, []).append(row)
                    executed += 1
                    if max_requests is not None and executed >= max_requests:
                        return completion(store.rows, identity)
                del session
        return completion(store.rows, identity)


def completion(rows: list[dict], identity: dict) -> dict:
    requests = [row for row in rows if row.get("kind") != "event"]
    successes = {row["request_key"] for row in requests if row["status"] == "success"}
    expected = sum(len(identity["question_ids"][c["dataset"]]) * 3
                   for c in identity["conditions"])
    return {"planned_requests": expected, "successful_requests": len(successes),
            "failed_attempts": sum(r["status"] == "failed" for r in requests),
            "setup_failures": sum(r.get("event") == "block_setup_failure" for r in rows),
            "remaining_requests": expected - len(successes),
            "status": "complete" if expected == len(successes) else "incomplete",
            "diagnostic": identity["diagnostic"]}
