"""Traceable offline paired comparisons of frozen main and baseline measurements."""

from __future__ import annotations

import csv
import json
import math
import zipfile
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from ragbench_lab.answer_metrics import answer_scores, normalize_answer
from ragbench_lab.baseline_runner import baseline_checks, baseline_plan
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.generation import ABSTENTION
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.paired_statistics import paired_summary, source_clusters
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import iter_records, verified_manifest
from ragbench_lab.stage_a import implementation_identity
from ragbench_lab.stage_b import evaluation_question_ids
from ragbench_lab.stage_b_runner import request_checks

METRICS = ("exact_match", "token_f1", "evidence_coverage", "abstention", "output_truncation",
           "latency_mean", "latency_median", "latency_p95")
CONTRASTS = ("qwen_minus_llama", "reranking_on_minus_off", "size_256_minus_128",
             "dense_minus_bm25", "hybrid_minus_bm25", "hybrid_minus_dense",
             "gold_minus_no_rag", "rag_minus_no_rag", "gold_minus_rag")


def validate_protocol(protocol: dict) -> None:
    if (protocol["schema_version"] != 1 or protocol["version"] != "paired_source_clusters_v1"
            or protocol["metrics"] != list(METRICS) or protocol["contrasts"] != list(CONTRASTS)
            or type(protocol["bootstrap_samples"]) is not int
            or protocol["bootstrap_samples"] != 2000
            or type(protocol["seed"]) is not int or protocol["seed"] != 20261011
            or protocol["confidence"] != .95 or protocol["quality_repetition"] != 1
            or protocol["source_clusters"] != {
                "squad": "reconstructed article document ID",
                "hotpot_qa": ("connected components of selected questions sharing supporting "
                              "document IDs or casefolded titles, including passage variants")}):
        raise DataError("unsupported analysis protocol; changed methods require a separate plan")


def condition_key(c: dict) -> tuple:
    return (c["dataset"], c["model_family"], c.get("baseline", "rag"),
            c.get("family"), c.get("size"), c.get("reranking"))


def observations(directory: Path, family: str, prepared: dict) -> tuple[dict, list[dict]]:
    if (directory / ".writer.lock").exists():
        raise DataError("analysis requires stopped runs")
    manifest = verified_manifest(directory / "manifest.json")
    identity = manifest["identity"]
    if identity["split"] != "evaluation" or identity["diagnostic"]:
        raise DataError("diagnostics and historical runs cannot enter held-out analysis")
    if identity["stage"] != ("B" if family == "main" else "B_baselines"):
        raise DataError("analysis run family differs from input role")
    conditions = {c["condition_id"]: c for c in identity["plan"]["conditions"]}
    by_id = {d: {q.question_id: q for q in bundle.questions}
             for d, (_, bundle) in prepared.items()}
    data, contexts, candidates = [], {}, {}
    for row in iter_records(directory, manifest):
        checker = request_checks if family == "main" else baseline_checks
        checker(row, identity, contexts, candidates)
        if row["kind"] == "event":
            if row["status"] != "success":
                raise DataError("setup failures require a separate missingness analysis")
            continue
        if row["attempt"] != 1 or row["status"] != "success":
            raise DataError("complete-study report cannot substitute retries or drop failures")
        c, result = conditions[row["condition_id"]], row["result"]
        question = by_id[row["dataset"]][row["question_id"]]
        generation = result["generation"]
        scores = answer_scores(generation["answer"], question.answers, question.dataset)
        if scores != result["answer_metrics"]:
            raise DataError("stored answer scores differ from recomputed normalized scores")
        if (generation["abstained"] != (generation["answer"].strip() == ABSTENTION)
                or generation["output_truncated"]
                != (generation["backend_final"]["done_reason"] == "length")):
            raise DataError("stored abstention/truncation flags differ from raw generation")
        context = result["context"] if family == "main" else result["inputs"]["context"]
        evidence = evidence_metrics(question, [(e["document_id"], e["source_start"], e[
            "source_end"]) for e in context["evidence"]])
        saved = result["metrics"]["context"] if family == "main" else result[
            "context_evidence_metrics"]
        if evidence != saved:
            raise DataError("stored evidence scores differ from actually packed source intervals")
        latency = result["total_request_seconds"]
        if type(latency) not in {int, float} or not math.isfinite(latency) or latency <= 0:
            raise DataError("invalid online latency")
        data.append({"run_id": manifest["run_id"], "request_key": row["request_key"],
            "record_sha256": row["record_sha256"], "condition_id": c["condition_id"],
            "dataset": row["dataset"], "model_family": row["model_family"],
            "question_id": row["question_id"], "repetition": row["repetition"],
            **scores, "evidence_coverage": evidence["evidence_coverage"],
            "abstention": float(generation["abstained"]),
            "output_truncation": float(generation["output_truncated"]), "latency": latency,
            "answer_sha256": digest(generation["answer"]),
            "normalized_answer_sha256": digest(normalize_answer(generation["answer"]))})
    expected = {(c["condition_id"], qid, rep) for c in conditions.values() for rep in (1, 2, 3)
                for qid in identity["plan"]["question_orders"][str(rep)][c["dataset"]]}
    if {(r["condition_id"], r["question_id"], r["repetition"]) for r in data} != expected:
        raise DataError("analysis requires the exact complete question/repetition matrix")
    return manifest, data


def contrast_pairs(conditions: list[dict]) -> list[tuple[str, dict, dict]]:
    """All declared contrasts, never select configurations based on observed scores."""
    pairs = []
    for a, b in combinations(sorted(conditions, key=condition_key), 2):
        if a["dataset"] != b["dataset"]:
            continue
        ka, kb = condition_key(a), condition_key(b)
        if ka[2] == kb[2] == "rag":
            changed = [i for i in (1, 3, 4, 5) if ka[i] != kb[i]]
            if len(changed) != 1:
                continue
            factor = changed[0]
            if factor == 1:
                left, right = (a, b) if a["model_family"] == "qwen" else (b, a)
                label = "qwen_minus_llama"
            elif factor == 4:
                left, right = (a, b) if a["size"] == 256 else (b, a)
                label = "size_256_minus_128"
            elif factor == 5:
                left, right = (a, b) if a["reranking"] else (b, a)
                label = "reranking_on_minus_off"
            else:
                order = {"bm25": 0, "dense": 1, "hybrid": 2}
                left, right = (a, b) if order[a["family"]] > order[b["family"]] else (b, a)
                label = f"{left['family']}_minus_{right['family']}"
            pairs.append((label, left, right))
        elif ka[1] == kb[1]:
            if {ka[2], kb[2]} == {"gold", "no_rag"}:
                left, right = (a, b) if ka[2] == "gold" else (b, a)
                pairs.append(("gold_minus_no_rag", left, right))
            elif "rag" in {ka[2], kb[2]}:
                rag, baseline = (a, b) if ka[2] == "rag" else (b, a)
                pairs.append(("rag_minus_no_rag", rag, baseline) if baseline["baseline"] == "no_rag"
                             else ("gold_minus_rag", baseline, rag))
    return pairs


def metric_samples(rows: list[dict], metric: str) -> dict:
    groups = defaultdict(dict)
    for row in rows:
        if row["repetition"] in groups[row["question_id"]]:
            raise DataError("duplicate analysis question/repetition")
        groups[row["question_id"]][row["repetition"]] = row
    if any(set(reps) != {1, 2, 3} for reps in groups.values()):
        raise DataError("all timing repetitions required without creating new question units")
    timing = metric.startswith("latency_")
    ids = sorted(groups)
    return {"question_ids": ids, "statistic": metric.removeprefix("latency_") if timing else "mean",
        "values": [[groups[qid][r]["latency"] for r in (1, 2, 3)] if timing
                   else [groups[qid][1][metric]] for qid in ids]}


def compute_report(conditions: list[dict], rows: list[dict], clusters: dict,
                   protocol: dict) -> dict:
    by_condition = defaultdict(list)
    for row in rows:
        by_condition[row["condition_id"]].append(row)
    samples = {c["condition_id"]: {m: metric_samples(by_condition[c["condition_id"]], m)
                                  for m in METRICS} for c in conditions}

    def metrics(left, right=None):
        return {metric: paired_summary(
            {c["dataset"]: samples[c["condition_id"]][metric] for c in left},
            {c["dataset"]: samples[c["condition_id"]][metric] for c in right}
                if right is not None else None, clusters, protocol) for metric in METRICS}

    cells = []
    macro_cells = defaultdict(list)
    for c in sorted(conditions, key=condition_key):
        selected = by_condition[c["condition_id"]]
        answers = defaultdict(list)
        normalized = defaultdict(list)
        for row in selected:
            answers[row["question_id"]].append(row["answer_sha256"])
            normalized[row["question_id"]].append(row["normalized_answer_sha256"])
        cells.append({"condition": c, "questions": len(answers),
            "timing_measurements": len(selected),
            "metrics": metrics([c]), "output_instability": {
                "raw": sum(len(set(v)) > 1 for v in answers.values()) / len(answers),
                "normalized": sum(len(set(v)) > 1 for v in normalized.values()) / len(normalized)}})
        macro_cells[condition_key(c)[1:]].append(c)
    contrasts, macro_pairs = [], defaultdict(list)
    for label, left, right in contrast_pairs(conditions):
        contrasts.append({"contrast": label, "dataset": left["dataset"],
            "left_condition_id": left["condition_id"], "right_condition_id": right["condition_id"],
            "metrics": metrics([left], [right])})
        key = (label, condition_key(left)[1:], condition_key(right)[1:])
        macro_pairs[key].append((left, right))
    if any(len(group) != 2 for group in macro_cells.values()) or any(
            len(group) != 2 for group in macro_pairs.values()):
        raise DataError("macro summaries require both matched datasets")
    return {"cells": cells, "contrasts": contrasts,
        "macro_cells": [{"condition_ids": [c["condition_id"] for c in group],
                         "metrics": metrics(group)} for _, group in sorted(macro_cells.items())],
        "macro_contrasts": [{"contrast": key[0],
            "pairs": [{"dataset": a["dataset"], "left_condition_id": a["condition_id"],
                       "right_condition_id": b["condition_id"]} for a, b in group],
            "metrics": metrics([a for a, _ in group], [b for _, b in group])}
            for key, group in sorted(macro_pairs.items())]}


def write_tables(output: Path, report: dict) -> None:
    for name in ("cells", "contrasts"):
        with (output / f"{name}.csv").open("x", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["dataset", "condition_or_contrast", "left_id", "right_id",
                             "metric", "unit", "estimate", "source_low95", "source_high95",
                             "questions", "clusters"])
            for item in report[name]:
                c = item.get("condition", {})
                dataset = c.get("dataset", item.get("dataset"))
                for metric, summary in item["metrics"].items():
                    ci = summary["source_ci95"] or [None, None]
                    writer.writerow([dataset, item.get("contrast", c.get("condition_id")),
                        item.get("left_condition_id", c.get("condition_id")),
                        item.get("right_condition_id", ""), metric,
                        "seconds" if metric.startswith("latency_") else "fraction",
                        summary["estimate"], *ci,
                        summary["questions"][dataset], summary["source_clusters"][dataset]])


def analyze_study(config, study_path: Path, baseline_path: Path, main_run: Path,
                  baseline_run: Path, data_dirs: dict, protocol_path: Path,
                  archive_path: Path, output: Path) -> dict:
    if output.exists():
        raise DataError("analysis output exists; preserve it and choose a new directory")
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    validate_protocol(protocol)
    proof = json.loads(Path(protocol["archive_proof"]).read_text(encoding="utf-8"))
    if file_sha256(archive_path) != proof["archive_sha256"]:
        raise DataError("archive differs from independently verified checksum proof")
    with zipfile.ZipFile(archive_path) as archive:
        inventory = json.loads(archive.read("archive.json"))
    if (digest({k: v for k, v in inventory.items() if k != "manifest_sha256"})
            != proof["manifest_sha256"]
            or inventory["manifest_sha256"] != proof["manifest_sha256"]):
        raise DataError("analysis archive inventory identity mismatch")
    pins = {entry["path"]: entry["sha256"] for entry in inventory["files"]}

    def pin(path):
        relative = str(path.resolve().relative_to(Path.cwd()))
        sha = file_sha256(path)
        if pins.get(relative) != sha:
            raise DataError(f"analysis input differs from archived bytes: {relative}")
        return sha

    for path in (study_path, baseline_path):
        pin(path)
    study, plan = verified_manifest(study_path), verified_manifest(baseline_path)
    prepared = {}
    for dataset, path in data_dirs.items():
        for name in ("manifest.json", "documents.jsonl", "questions.jsonl"):
            pin(path / name)
        prepared[dataset] = load_prepared(path)
        source, _ = prepared[dataset]
        if any(source[k] != v for k, v in study["selection"]["sources"][dataset].items()):
            raise DataError("analysis source differs from scientific study")
    manifests, compact, bindings = {}, [], {}
    for family, path in (("main", main_run), ("baselines", baseline_run)):
        pin(path / "manifest.json")
        sha = pin(path / "records.jsonl")
        manifest, data = observations(path, "main" if family == "main" else "baseline", prepared)
        archived = inventory["runs"][family]
        if (manifest["manifest_sha256"] != archived["manifest_sha256"]
                or sha != archived["records_sha256"] or len(data) != archived["planned_slots"]
                or archived["missing_successes"] or archived["failed_attempts"]):
            raise DataError("analysis input differs from audited complete run")
        manifests[family] = manifest
        bindings[family] = {"run_id": manifest["run_id"], "manifest_sha256": manifest[
            "manifest_sha256"], "records_sha256": sha,
            "provenance": manifest["identity"]["provenance"]}
        compact.extend(data)
    if plan != baseline_plan(config, study, manifests["main"], bindings["main"]["records_sha256"]):
        raise DataError("analysis baseline/main scientific linkage differs")
    if manifests["baselines"]["identity"]["baseline_plan_sha256"] != plan["manifest_sha256"]:
        raise DataError("analysis baseline plan differs")
    selected = evaluation_question_ids(study)
    clusters = {d: source_clusters(d, [q for q in bundle.questions if q.question_id in selected[d]],
                                   bundle.documents) for d, (_, bundle) in prepared.items()}
    conditions = [c for m in manifests.values() for c in m["identity"]["plan"]["conditions"]]
    print("computing paired source-cluster and question-sensitivity intervals", flush=True)
    report = compute_report(conditions, compact, clusters, protocol)
    report.update(kind="stage_b_paired_analysis", schema_version=1, protocol=protocol,
        protocol_sha256=digest(protocol), scientific_study_sha256=study["manifest_sha256"],
        inputs=bindings, archive_sha256=proof["archive_sha256"], clusters=clusters,
        analysis_provenance=implementation_identity(), measurements=len(compact),
        question_units=sum(len(ids) for ids in selected.values()),
        units={m: "seconds" if m.startswith("latency_") else "fraction" for m in METRICS},
        contrast_sign=("left minus right; positive latency means slower; "
                       "fraction deltas x100 are percentage points"),
        notes=protocol["limits"], inferential_status="descriptive; unadjusted multiple comparisons")
    report["manifest_sha256"] = digest(report)
    output.mkdir(parents=True)
    write_new_json(output / "report.json", report)
    write_new_json(output / "analysis-plan.json", {"protocol": protocol,
        "protocol_sha256": digest(protocol), "inputs": bindings, "clusters": clusters})
    write_new_json(output / "source-clusters.json", {"rules": protocol["source_clusters"],
        "question_to_cluster": clusters, "counts": {d: len(set(v.values()))
                                                    for d, v in clusters.items()}})
    with (output / "observations.jsonl").open("xb") as stream:
        for row in sorted(compact, key=lambda r: r["request_key"]):
            stream.write(canonical(row) + b"\n")
    write_tables(output, report)
    return {"output": str(output), "report_sha256": report["manifest_sha256"],
            "cells": len(report["cells"]), "contrasts": len(report["contrasts"]),
            "measurements": len(compact), "question_units": report["question_units"]}
