"""Check the public aggregate bundle without models, raw data or third-party packages."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "results/stage-b-v3"
FIGURES = ("quality_latency.svg", "quality_latency_baselines.svg", "stage_times_main.svg")
TABLES = ("conditions.csv", "cells.csv", "contrasts.csv", "stage-times.csv")
PAYLOAD = (*TABLES, *FIGURES)
METRICS = ("exact_match", "token_f1", "evidence_coverage", "abstention", "output_truncation",
           "latency_mean", "latency_median", "latency_p95")
CONDITION_FIELDS = ("condition_id", "dataset", "model", "role", "family", "chunk_tokens",
                    "reranking", "questions", "timing_measurements", "source_clusters")
METRIC_FIELDS = ("dataset", "condition_or_contrast", "left_id", "right_id", "metric", "unit",
                 "estimate", "source_low95", "source_high95", "questions", "clusters")
STAGES = ("query_embedding", "bm25_search", "dense_search", "fusion", "reranking", "packing",
          "baseline_preparation", "generation", "unattributed_online")
STAGE_FIELDS = ("condition_id", "dataset", "model", "profile", "questions",
                "timing_measurements", *STAGES)
STUDY = {
    "name": "stage-b-v3-reduced", "datasets": ["hotpot_qa", "squad"],
    "models": ["llama", "qwen"], "quantization": "Q4_K_M", "embedder": "e5",
    "chunker": "sentence_aware", "context_budget_reference_tokens": 1024,
    "questions_per_dataset": 25, "question_units": 50, "repetitions": 3,
    "quality_repetition": 1, "main_conditions": 48, "baseline_conditions": 8,
    "main_measurements": 3600, "baseline_measurements": 600,
    "source_clusters": {"hotpot_qa": 25, "squad": 12}, "bootstrap_samples": 2000,
    "bootstrap_seed": 20261011, "confidence": 0.95,
}
NOTES = [
    "Stage B only; Stage A, pilots, development gates and historical v1/v2 runs are excluded.",
    "The 25-ID sample is a budget amendment after partial execution, not preregistration.",
    "Quality uses repetition one; three timings per question are not independent questions.",
    "Intervals are original source-cluster percentile intervals, unadjusted for multiplicity.",
    "Scores and intervals use fractions; latency uses seconds. "
    "Contrast direction is left minus right.",
    "EM/F1 are text-match scores; annotated evidence coverage is not semantic sufficiency.",
    "Baseline/main execution paths differ; No-RAG keeps grounding instructions; gold can truncate.",
    "Online time excludes setup, warmup, cache isolation, scoring and record writes.",
    "Small source-dependent samples and resumed single-host timings "
    "limit generalization and tails.",
    "Aggregate checks do not recompute bootstraps, audit raw runs "
    "or establish independent replication.",
    "Hashes detect changes against this unsigned inventory; "
    "they are not signatures or data-access clearance.",
]
PRIVATE = re.compile(
    r"/Users/|/home/|/private/|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|"
    r"-----BEGIN .*PRIVATE KEY|\b(?:password|api_key|access_token)\s*[:=]|\b[0-9a-f]{24}\b",
    re.IGNORECASE,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def verified_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    return verified_manifest(value)


def verified_manifest(value: dict) -> dict:
    body = {k: v for k, v in value.items() if k != "manifest_sha256"}
    require(sha256(canonical(body)) == value.get("manifest_sha256"),
            "manifest identity mismatch")
    return value


def table(data: bytes, fields: tuple[str, ...]) -> list[dict]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""))
    require(reader.fieldnames == list(fields), "unexpected CSV columns")
    rows = list(reader)
    require(all(set(row) == set(fields) and None not in row.values() for row in rows),
            "invalid CSV row width")
    return rows


def number(value: str) -> float:
    result = float(value)
    require(math.isfinite(result), "nonfinite metric or timer")
    return result


def expected_pairs(conditions: dict[str, dict]) -> set[tuple[str, str, str]]:
    pairs = set()
    for left, right in product(conditions.values(), repeat=2):
        if left["condition_id"] == right["condition_id"] or left["dataset"] != right["dataset"]:
            continue
        label = None
        if left["role"] == right["role"] == "rag":
            fields = ("model", "family", "chunk_tokens", "reranking")
            changed = [key for key in fields if left[key] != right[key]]
            if changed == ["model"] and left["model"] == "qwen":
                label = "qwen_minus_llama"
            elif changed == ["chunk_tokens"] and left["chunk_tokens"] == "256":
                label = "size_256_minus_128"
            elif changed == ["reranking"] and left["reranking"] == "on":
                label = "reranking_on_minus_off"
            elif changed == ["family"]:
                order = {"bm25": 0, "dense": 1, "hybrid": 2}
                if order[left["family"]] > order[right["family"]]:
                    label = f"{left['family']}_minus_{right['family']}"
        elif left["model"] == right["model"]:
            label = {("gold", "no_rag"): "gold_minus_no_rag",
                     ("rag", "no_rag"): "rag_minus_no_rag",
                     ("gold", "rag"): "gold_minus_rag"}.get((left["role"], right["role"]))
        if label:
            pairs.add((label, left["condition_id"], right["condition_id"]))
    return pairs


def verify(bundle: Path) -> dict:
    require(not bundle.is_symlink(), "symlink bundle is not supported")
    require({p.name for p in bundle.iterdir()} == {*PAYLOAD, "manifest.json"},
            "unexpected or missing public files")
    require(all(p.is_file() and not p.is_symlink() for p in bundle.iterdir()),
            "public files must be regular, non-symlink files")
    return verify_payload({p.name: p.read_bytes() for p in bundle.iterdir()})


def verify_payload(contents: dict[str, bytes]) -> dict:
    require(set(contents) == {*PAYLOAD, "manifest.json"}, "unexpected public payload")
    manifest = verified_manifest(json.loads(contents["manifest.json"]))
    require(set(manifest) == {"schema_version", "kind", "study", "notes", "sources", "files",
                              "manifest_sha256"}, "unexpected manifest fields")
    require(manifest["schema_version"] == 1 and manifest["kind"] == "public_stage_b_aggregates"
            and manifest["study"] == STUDY and manifest["notes"] == NOTES,
            "public scope or methods changed")
    sources = manifest["sources"]
    require(set(sources) == {"analysis_manifest_sha256", "figure_manifest_sha256",
                             "analysis_proof_sha256", "study_manifest_sha256", "source_files"},
            "unexpected provenance fields")
    require(all(re.fullmatch(r"[0-9a-f]{64}", value) for key, value in sources.items()
                if key != "source_files"), "invalid source identity")
    require(set(manifest["files"]) == set(PAYLOAD), "invalid payload inventory")
    data = {name: contents[name] for name in PAYLOAD}
    for name, content in contents.items():
        require(not PRIVATE.search(content.decode("utf-8")), f"private-looking text: {name}")
        if name in data:
            require(manifest["files"][name] == {"sha256": sha256(content), "bytes": len(content)},
                    f"file integrity mismatch: {name}")
    require(sources["source_files"] == {name: sha256(data[name]) for name in PAYLOAD
                                       if name != "conditions.csv"}, "source copies changed")

    rows = table(data["conditions.csv"], CONDITION_FIELDS)
    conditions = {row["condition_id"]: row for row in rows}
    require(len(rows) == len(conditions) == 56, "expected 56 distinct conditions")
    profiles = set()
    for cid, row in conditions.items():
        require(re.fullmatch(r"[0-9a-f]{64}", cid) is not None, "invalid condition ID")
        dataset, model, role = row["dataset"], row["model"], row["role"]
        require(dataset in STUDY["datasets"] and model in STUDY["models"], "unknown dataset/model")
        require(row["questions"] == "25" and row["timing_measurements"] == "75"
                and row["source_clusters"] == str(STUDY["source_clusters"][dataset]),
                "question/timing/cluster counts changed")
        profile = (dataset, model, role, row["family"], row["chunk_tokens"], row["reranking"])
        require(profile not in profiles, "duplicate condition profile")
        profiles.add(profile)
    expected = {(d, m, "rag", f, size, rr) for d, m, f, size, rr in product(
        STUDY["datasets"], STUDY["models"], ("bm25", "dense", "hybrid"), ("128", "256"),
        ("off", "on"))}
    expected |= {(d, m, role, "", "", "") for d, m, role in product(
        STUDY["datasets"], STUDY["models"], ("gold", "no_rag"))}
    require(profiles == expected, "incomplete or changed factorial matrix")

    points, pairs = {}, expected_pairs(conditions)
    require(len(pairs) == 220, "invalid contrast matrix")
    for name in ("cells.csv", "contrasts.csv"):
        seen = set()
        for row in table(data[name], METRIC_FIELDS):
            left, right, metric = row["left_id"], row["right_id"], row["metric"]
            require(left in conditions and metric in METRICS, "unknown cell or metric")
            condition = conditions[left]
            require(row["dataset"] == condition["dataset"] and row["questions"] == "25"
                    and row["clusters"] == condition["source_clusters"], "metric scope mismatch")
            require(row["unit"] == ("seconds" if metric.startswith("latency_") else "fraction"),
                    "metric units changed")
            estimate, low, high = (number(row[k]) for k in (
                "estimate", "source_low95", "source_high95"))
            require(low <= high, "reversed interval")
            if name == "cells.csv":
                key = (left, metric)
                require(not right and row["condition_or_contrast"] == left, "invalid cell key")
                require(estimate >= 0 and low >= 0, "negative cell metric")
                require(metric.startswith("latency_") or max(estimate, high) <= 1,
                        "fraction outside [0,1]")
                points[key] = estimate
            else:
                key = (row["condition_or_contrast"], left, right, metric)
                require(key[:3] in pairs, "missing, reversed or incompatible contrast")
                require(math.isclose(estimate, points[left, metric] - points[right, metric],
                                     rel_tol=1e-12, abs_tol=1e-12), "contrast arithmetic mismatch")
            require(key not in seen, "duplicate metric row")
            seen.add(key)
        expected_keys = (set(product(conditions, METRICS)) if name == "cells.csv" else
                         {(*pair, metric) for pair in pairs for metric in METRICS})
        require(seen == expected_keys, f"incomplete metrics: {name}")

    stages = table(data["stage-times.csv"], STAGE_FIELDS)
    require(len(stages) == 56 and {r["condition_id"] for r in stages} == conditions.keys(),
            "incomplete stage timings")
    for row in stages:
        c = conditions[row["condition_id"]]
        profile = (f"{c['family'][0].upper()}{c['chunk_tokens']}"
                   f"{'+' if c['reranking'] == 'on' else '-'}" if c["role"] == "rag" else
                   c["role"].replace("_", "-"))
        fields = ("dataset", "model", "questions", "timing_measurements")
        require(all(row[k] == c[k] for k in fields)
                and row["profile"] == profile, "stage profile mismatch")
        seconds = [number(row[k]) for k in STAGES]
        require(min(seconds) >= 0 and math.isclose(sum(seconds),
                points[c["condition_id"], "latency_mean"], abs_tol=1e-10),
                "stages do not reconstruct online mean")
    for name in FIGURES:
        require(b"<!DOCTYPE" not in data[name].upper() and b"<!ENTITY" not in data[name].upper(),
                "SVG declarations are not supported")
        scene = ET.fromstring(data[name])
        allowed = {f"{{http://www.w3.org/2000/svg}}{tag}" for tag in (
            "svg", "desc", "rect", "line", "text")}
        require(scene.tag.endswith("}svg") and all(node.tag in allowed for node in scene.iter()),
                "unsupported SVG content")
        attributes = {"viewBox", "width", "height", "fill", "stroke", "x", "y", "x1", "y1",
                      "x2", "y2", "font-family", "font-size"}
        require(all(key in attributes and "url(" not in value.lower()
                    for node in scene.iter() for key, value in node.attrib.items()),
                "active or external SVG content")
    return {"conditions": 56, "metric_rows": 448, "contrast_rows": 1760, "figures": len(FIGURES)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", nargs="?", type=Path, default=DEFAULT_BUNDLE)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.bundle), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
