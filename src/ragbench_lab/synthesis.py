"""Descriptive dataset/model synthesis from verified saved analysis artifacts."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import verified_manifest
from ragbench_lab.stage_a import implementation_identity

CONTRASTS = ("qwen_minus_llama", "reranking_on_minus_off", "size_256_minus_128",
             "dense_minus_bm25", "hybrid_minus_bm25", "hybrid_minus_dense")


def checked_artifact(directory: Path, proof_path: Path, kind: str,
                     identity_key: str, filename: str) -> dict:
    proof = verified_manifest(proof_path)
    manifest = verified_manifest(directory/filename)
    if (proof["kind"] != kind
            or proof[identity_key] != manifest["manifest_sha256"]):
        raise DataError("synthesis artifact/proof identity mismatch")
    for inventory in (proof.get("files", {}), manifest.get("files", {})):
        for name, sha in inventory.items():
            if Path(name).name != name or file_sha256(directory/name) != sha:
                raise DataError("synthesis input bytes differ from verified artifact")
    if not proof.get("files") and not manifest.get("files"):
        raise DataError("synthesis needs a verified file inventory")
    return manifest


def estimate_range(values: list[float]) -> dict:
    if not values or any(type(v) not in {int, float} or not math.isfinite(v) for v in values):
        raise DataError("summary range needs finite point estimates")
    return {"min": min(values), "max": max(values), "positive": sum(v > 0 for v in values),
            "negative": sum(v < 0 for v in values), "zero": sum(v == 0 for v in values),
            "count": len(values)}


def summarize(report: dict, stage_cells: list[dict], protocol: dict) -> dict:
    if (protocol["version"] != "descriptive_synthesis_v1"
            or protocol["contrasts"] != list(CONTRASTS)):
        raise DataError("unsupported synthesis protocol")
    cells = {c["condition"]["condition_id"]: c for c in report["cells"]}
    if len(cells) != len(report["cells"]):
        raise DataError("duplicate synthesis condition")
    main = {cid: c for cid, c in cells.items() if "baseline" not in c["condition"]}
    groups, comparisons = defaultdict(list), defaultdict(list)
    for cid, c in main.items():
        groups[(c["condition"]["dataset"], c["condition"]["model_family"])].append(cid)
    ranges = []
    for (dataset, model), ids in sorted(groups.items()):
        ranges.append({"dataset": dataset, "model_family": model, "condition_ids": sorted(ids),
            "metrics": {m: estimate_range([cells[cid]["metrics"][m]["estimate"] for cid in ids])
                        for m in cells[ids[0]]["metrics"]}})
    paired = [c for c in report["contrasts"] if c["contrast"] in CONTRASTS]
    for c in paired:
        left, right = cells[c["left_condition_id"]], cells[c["right_condition_id"]]
        if c["left_condition_id"] not in main or c["right_condition_id"] not in main:
            raise DataError("main contrast summary cannot pool baseline conditions")
        model = ("paired_generators" if c["contrast"] == "qwen_minus_llama"
                 else left["condition"]["model_family"])
        if c["dataset"] != left["condition"]["dataset"] or c["dataset"] != right[
                "condition"]["dataset"]:
            raise DataError("paired comparison dataset mismatch")
        comparisons[(c["dataset"], model, c["contrast"])].append(c)
    contrast_ranges = [{"dataset": dataset, "model_family": model, "contrast": contrast,
        "metrics": {m: estimate_range([c["metrics"][m]["estimate"] for c in rows])
                    for m in rows[0]["metrics"]}}
        for (dataset, model, contrast), rows in sorted(comparisons.items())]
    shares = []
    if {s["condition_id"] for s in stage_cells} != cells.keys():
        raise DataError("stage conditions differ from paired analysis")
    for s in stage_cells:
        cid = s["condition_id"]
        total = sum(s["stages"].values())
        if not math.isclose(total, cells[cid]["metrics"]["latency_mean"]["estimate"],
                            abs_tol=1e-10):
            raise DataError("stage total differs from verified latency mean")
        if cid in main:
            shares.append({"condition_id": cid,
                           "generation_share": s["stages"]["generation"]/total})
    return {"cell_ranges": ranges, "contrast_ranges": contrast_ranges,
            "main_cells_with_original_intervals": list(main.values()),
            "paired_details_with_original_intervals": paired,
            "baselines_with_original_intervals": [c for cid, c in cells.items() if cid not in main],
            "main_stage_shares": shares,
            "generation_share_range": estimate_range([s["generation_share"] for s in shares]),
            "range_interpretation": "min/max across configurations, NOT a confidence interval",
            "sign_counts_interpretation": (
                "descriptive point-estimate signs, NOT significance counts")}


def write_tables(path: Path, facts: dict) -> None:
    def span(value, scale=1, signed=False):
        fmt = "+.2f" if signed else ".2f"
        return f"{value['min']*scale:{fmt}} to {value['max']*scale:{fmt}}"

    lines = ["# Dataset and model synthesis: numerical tables", "",
        "All ranges below are min/max across frozen profiles, NOT confidence intervals.",
        "Token F1 is a normalized token-overlap score, not factual accuracy. "
        "Signs are descriptive.",
        "Each condition has 25 questions and 75 timing measurements; "
        "source units remain clustered.",
        "Original per-cell/per-pair intervals are retained in facts.json, "
        "without new inference.", "",
        "## Main profiles", "",
        "| Dataset | Model | Profiles | Token F1 (%) | EM (%) | "
        "Packed evidence (%) | Mean online s |",
        "| --- | --- | --- | --- | --- | --- | --- |"]
    for row in facts["cell_ranges"]:
        m = row["metrics"]
        lines.append(f"| {row['dataset']} | {row['model_family']} | {len(row['condition_ids'])} | "
                     f"{span(m['token_f1'], 100)} | {span(m['exact_match'], 100)} | "
                     f"{span(m['evidence_coverage'], 100)} | {span(m['latency_mean'])} |")
    lines += ["", "## All main paired contrast groups", "",
        "Positive deltas mean left is higher; positive latency means slower.",
        "Rows span different fixed profiles; they are not independent "
        "replications or pooled effects.",
        "The source analysis includes all individual intervals and "
        "question-sensitivity checks.", "",
        "| Dataset | Model | Left minus right | Pairs | "
        "Token F1 delta (pp) | Mean online delta s |",
        "| --- | --- | --- | --- | --- | --- |"]
    for row in facts["contrast_ranges"]:
        m = row["metrics"]
        lines.append(f"| {row['dataset']} | {row['model_family']} | {row['contrast']} | "
            f"{m['token_f1']['count']} | {span(m['token_f1'], 100, True)} | "
            f"{span(m['latency_mean'], signed=True)} |")
    lines += ["", "## Separate baselines", "",
        "Baseline/main online implementations differ; timings must not be pooled.",
        "No-RAG retains grounding instructions. Gold is not a guaranteed semantic upper bound.", "",
        "| Dataset | Model | Baseline | Token F1 (%) | Source 95% interval (%) | Mean online s |",
        "| --- | --- | --- | --- | --- | --- |"]
    for row in facts["baselines_with_original_intervals"]:
        c, m = row["condition"], row["metrics"]
        lo, hi = m["token_f1"]["source_ci95"]
        lines.append(f"| {c['dataset']} | {c['model_family']} | {c['baseline']} | "
            f"{100*m['token_f1']['estimate']:.2f} | {100*lo:.2f} to {100*hi:.2f} | "
            f"{m['latency_mean']['estimate']:.2f} |")
    with path.open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines)+"\n")


def synthesize(analysis_dir: Path, analysis_proof: Path, figure_dir: Path, figure_proof: Path,
               review_dir: Path, review_proof: Path, protocol_path: Path, output: Path) -> dict:
    if output.exists():
        raise DataError("synthesis requires a fresh output directory")
    report = checked_artifact(analysis_dir, analysis_proof, "independent_analysis_checks",
                              "report_sha256", "report.json")
    figures = checked_artifact(figure_dir, figure_proof, "independent_figure_checks",
                               "figure_manifest_sha256", "manifest.json")
    review = checked_artifact(review_dir, review_proof, "independent_failure_review_checks",
                              "case_manifest_sha256", "manifest.json")
    if any(m["report_sha256"] != report["manifest_sha256"] for m in (figures, review)):
        raise DataError("synthesis inputs refer to different paired analyses")
    protocol = json.loads(protocol_path.read_text())
    stages = json.loads((figure_dir/"stage-evidence.json").read_text())
    facts = summarize(report, stages["cells"], protocol)
    facts.update(report_sha256=report["manifest_sha256"], protocol=protocol,
                 question_units=report["question_units"], measurements=report["measurements"])
    output.mkdir(parents=True)
    write_new_json(output/"facts.json", facts)
    write_tables(output/"TABLES.md", facts)
    manifest = {"kind": "descriptive_study_synthesis", "report_sha256": report["manifest_sha256"],
        "figure_manifest_sha256": figures["manifest_sha256"],
        "review_manifest_sha256": review["manifest_sha256"],
        "proofs": {str(p): file_sha256(p) for p in (analysis_proof, figure_proof, review_proof)},
        "protocol_sha256": digest(protocol), "provenance": implementation_identity(),
        "files": {p.name: file_sha256(p) for p in sorted(output.iterdir())}}
    manifest["manifest_sha256"] = digest(manifest)
    write_new_json(output/"manifest.json", manifest)
    return {"output": str(output), "dataset_model_groups": len(facts["cell_ranges"]),
            "contrast_groups": len(facts["contrast_ranges"]),
            "manifest_sha256": manifest["manifest_sha256"]}
