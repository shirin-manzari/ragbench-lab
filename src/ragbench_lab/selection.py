from __future__ import annotations

from pathlib import Path
from statistics import mean

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import read_records, verified_manifest
from ragbench_lab.stage_a import SELECTION_RULE, completion, validate_requests


def choose(candidates: list[dict]) -> dict:
    best = max(c["coverage"] for c in candidates)
    close = [c for c in candidates if best - c["coverage"] <= 0.01 + 1e-12]
    return min(close, key=lambda c: (c["retrieval_seconds"], c["indexing_seconds"],
                                    c["embedder"], c["chunker"]))


def selection_table(identity: dict, rows: list[dict]) -> list[dict]:
    if identity["split"] != "development" or identity["selection_rule"] != SELECTION_RULE:
        raise DataError("selection requires the declared development-only rule")
    validate_requests(rows, identity)
    if completion(rows, identity)["remaining_requests"]:
        raise DataError("selection requires a complete run, including timing repetitions")
    if len(identity["conditions"]) != 60:
        raise DataError("selection requires all 30 conditions on each of two datasets")
    requests = [r for r in rows if r.get("kind") != "event"]
    if any(r["attempt"] != 1 or r["status"] != "success" for r in requests):
        raise DataError("failed first attempts require review; cannot silently select retries")
    stats = {r["condition_id"]: r["index_statistics"] for r in rows
             if r.get("event") == "block_warmup" and r["status"] == "success"}
    candidates = []
    for embedder in ("bge", "e5"):
        for chunker in ("fixed_token", "sentence_aware"):
            dataset_scores = []
            for dataset in identity["question_ids"]:
                conditions = [c for c in identity["conditions"] if c["dataset"] == dataset
                              and c["method"] == chunker
                              and c["recipe"] in (f"dense_{embedder}", f"hybrid_{embedder}")]
                if len(conditions) != 6:
                    raise DataError("selection candidate lacks six family/size conditions")
                scores, latencies, costs = [], [], []
                for condition in conditions:
                    selected = [r for r in requests
                                if r["condition_id"] == condition["condition_id"]]
                    scores.append(mean(r["result"]["metrics"]["context"]["evidence_coverage"]
                                       for r in selected if r["repetition"] == 1))
                    # Equal per-question weighting: repeated measurements are not new questions.
                    latencies.append(mean(mean(r["result"]["timings_seconds"][
                        "online_retrieval_path"] for r in selected if r["question_id"] == qid)
                        for qid in identity["question_ids"][dataset]))
                    stat = stats[condition["condition_id"]]
                    costs.append(sum(stat.get(key, 0.0) for key in (
                        "chunking_seconds", "bm25_build_seconds", "corpus_embedding_seconds",
                        "faiss_build_seconds", "persistence_seconds")))
                dataset_scores.append({"dataset": dataset, "coverage": mean(scores),
                                       "retrieval_seconds": mean(latencies),
                                       "indexing_seconds": mean(costs)})
            candidates.append({"embedder": embedder, "chunker": chunker,
                               **{key: mean(d[key] for d in dataset_scores) for key in
                                  ("coverage", "retrieval_seconds", "indexing_seconds")},
                               "datasets": dataset_scores})
    return candidates


def validate_freeze(freeze: dict) -> None:
    if (freeze.get("kind") != "stage_a_selection" or freeze.get("diagnostic") is not False
            or freeze.get("selection_rule") != SELECTION_RULE
            or freeze["selected"] != choose(freeze["candidates"])):
        raise DataError("invalid Stage A selection freeze")
    pairs = {(c["embedder"], c["chunker"]) for c in freeze["candidates"]}
    if pairs != {(e, m) for e in ("bge", "e5") for m in ("fixed_token", "sentence_aware")}:
        raise DataError("selection freeze lacks declared candidates")
    for source in freeze["sources"].values():
        if (len(source["split"]["development_ids"]) != 50
                or len(source["split"]["evaluation_ids"]) != 100):
            raise DataError("final selection requires the PRD 50/100 split, not pilot counts")


def select_run(directory: Path, output: Path, freeze_path: Path | None = None) -> dict:
    if (directory / ".writer.lock").exists():
        raise DataError("selection requires a stopped run")
    manifest = verified_manifest(directory / "manifest.json")
    identity = manifest["identity"]
    rows = read_records(directory, manifest)
    candidates = selection_table(identity, rows)
    report = {"kind": "stage_a_selection", "diagnostic": identity["diagnostic"],
              "selection_rule": identity["selection_rule"], "candidates": candidates,
              "selected": choose(candidates), "development_run_sha256": manifest["manifest_sha256"],
              "records_sha256": file_sha256(directory / "records.jsonl"),
              **{key: identity[key] for key in
                 ("config_sha256", "sources", "model_files", "tokenizer", "provenance")}}
    if freeze_path is not None:
        validate_freeze(report)
        if freeze_path.exists():
            raise DataError("freeze already exists; never overwrite a frozen study")
    report["manifest_sha256"] = digest(report)
    write_new_json(output, report)
    if freeze_path is not None:
        write_new_json(freeze_path, report)
    return {"diagnostic": report["diagnostic"], "selected": report["selected"],
            "output": str(output), "freeze": str(freeze_path) if freeze_path else None}
