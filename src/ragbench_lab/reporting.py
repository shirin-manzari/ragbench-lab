from __future__ import annotations

import random
from pathlib import Path
from statistics import mean

from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import read_records, verified_manifest
from ragbench_lab.stage_a import completion, validate_requests


def percentile(values: list[float], fraction: float) -> float:
    values = sorted(values)
    position = (len(values) - 1) * fraction
    left = int(position)
    right = min(left + 1, len(values) - 1)
    return values[left] + (values[right] - values[left]) * (position - left)


def timing_summary(groups: list[list[float]], seed: int, bootstrap_samples: int = 500) -> dict:
    samples = [value for group in groups for value in group]
    if not samples:
        return {"questions": 0, "measurements": 0, "median": None, "p95": None,
                "median_ci95": None, "p95_ci95": None}
    result = {"questions": len(groups), "measurements": len(samples),
              "median": percentile(samples, .5), "p95": percentile(samples, .95),
              "median_ci95": None, "p95_ci95": None}
    if len(groups) >= 2:
        rng = random.Random(seed)
        estimates = {"median": [], "p95": []}
        for _ in range(bootstrap_samples):
            sampled = [value for group in rng.choices(groups, k=len(groups)) for value in group]
            estimates["median"].append(percentile(sampled, .5))
            estimates["p95"].append(percentile(sampled, .95))
        for key, values in estimates.items():
            result[key + "_ci95"] = [percentile(values, .025), percentile(values, .975)]
    return result


def summarize_run(directory: Path, output: Path) -> dict:
    if (directory / ".writer.lock").exists():
        raise DataError("report requires a stopped run")
    manifest = verified_manifest(directory / "manifest.json")
    identity = manifest["identity"]
    rows = read_records(directory, manifest)
    validate_requests(rows, identity)
    summaries = []
    for condition in identity["conditions"]:
        requests = [r for r in rows if r.get("kind") != "event"
                    and r["condition_id"] == condition["condition_id"]]
        first = [r for r in requests if r["attempt"] == 1]
        success = [r for r in first if r["status"] == "success"]
        quality = [r for r in success if r["repetition"] == 1]
        groups = [[r["result"]["timings_seconds"]["online_retrieval_path"] for r in success
                   if r["question_id"] == qid] for qid in
                  identity["question_ids"][condition["dataset"]]]
        summaries.append({"condition": condition, "first_attempts": len(first),
                          "failed_first_attempts": sum(r["status"] == "failed" for r in first),
                          "retry_attempts": len(requests) - len(first),
                          "quality_questions": len(quality),
                          "context_coverage": mean(r["result"]["metrics"]["context"][
                              "evidence_coverage"] for r in quality) if quality else None,
                          "retrieval_seconds": timing_summary([g for g in groups if g],
                              identity["config"]["dataset"]["sampling_seed"])})
    report = {"run_manifest_sha256": manifest["manifest_sha256"],
              "records_sha256": file_sha256(directory / "records.jsonl"),
              "split": identity["split"], "completion": completion(rows, identity),
              "uncertainty": {"method": "question-cluster percentile bootstrap",
                              "resamples": 500, "confidence": .95,
                              "single_question_intervals": "unavailable",
                              "retry_policy": "first attempts only"},
              "conditions": summaries}
    write_new_json(output, report)
    return {"output": str(output), **report["completion"]}
