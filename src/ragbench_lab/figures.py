from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import iter_records, verified_manifest
from ragbench_lab.stage_a import implementation_identity
from ragbench_lab.vector_export import save_vectors

STAGES = ("query_embedding", "bm25_search", "dense_search", "fusion", "reranking",
          "packing", "baseline_preparation", "generation", "unattributed_online")
COLORS = ("#0072B2", "#56B4E9", "#009E73", "#E69F00", "#D55E00", "#CC79A7",
          "#999999", "#332288", "#BBBBBB")
FAMILIES = {"bm25": "#0072B2", "dense": "#D55E00", "hybrid": "#009E73"}


def stage_seconds(result: dict, baseline: bool) -> dict:
    values = dict.fromkeys(STAGES, 0.0)
    if baseline:
        values["baseline_preparation"] = result["context_preparation_seconds"]
    else:
        timers = result["retrieval"]["timings_seconds"]
        if set(timers) != set(STAGES[:4]):
            raise DataError("unexpected or overlapping retrieval timers")
        values.update(timers)
        values["reranking"] = result["reranking"]["seconds"]
        values["packing"] = result["packing_seconds"]
    values["generation"] = result["generation"]["generation_seconds"]
    total = result["total_request_seconds"]
    if any(type(v) not in {float, int} or not math.isfinite(v) or v < 0
           for v in [total, *values.values()]):
        raise DataError("invalid stage timing")
    residual = total - sum(values.values())
    if residual < 0:
        raise DataError("named stages exceed online time; timers may overlap")
    values["unattributed_online"] = residual
    return values


def collect(report_dir: Path, proof_path: Path, runs: dict) -> tuple[dict, list[dict]]:
    report = verified_manifest(report_dir / "report.json")
    proof = verified_manifest(proof_path)
    required = {"analysis-plan.json", "cells.csv", "contrasts.csv", "observations.jsonl",
                "report.json", "source-clusters.json"}
    if (proof["kind"] != "independent_analysis_checks" or set(proof["files"]) != required
            or proof["report_sha256"] != report["manifest_sha256"]):
        raise DataError("independent proof belongs to another report")
    for name, sha in proof["files"].items():
        if Path(name).name != name or file_sha256(report_dir / name) != sha:
            raise DataError("verified numerical report bytes changed")
    observations = {}
    for line in (report_dir / "observations.jsonl").read_text().splitlines():
        row = json.loads(line)
        if row["request_key"] in observations:
            raise DataError("duplicate report observation")
        observations[row["request_key"]] = row
    timings, evidence = defaultdict(list), defaultdict(list)
    seen = set()
    for role, directory in runs.items():
        if (directory / ".writer.lock").exists():
            raise DataError("figures require stopped runs")
        manifest = verified_manifest(directory / "manifest.json")
        binding = report["inputs"][role]
        if (manifest["manifest_sha256"] != binding["manifest_sha256"]
                or file_sha256(directory / "records.jsonl") != binding["records_sha256"]):
            raise DataError("raw inputs differ from independently verified analysis")
        for row in iter_records(directory, manifest):
            if row["kind"] == "event":
                continue
            key = row["request_key"]
            if (key in seen or key not in observations or row["attempt"] != 1
                    or row["status"] != "success"
                    or row["record_sha256"] != observations[key]["record_sha256"]):
                raise DataError("raw request does not match report observation")
            seen.add(key)
            cid, result = row["condition_id"], row["result"]
            timings[cid].append(stage_seconds(result, role == "baselines"))
            if role == "main" and row["repetition"] == 1:
                values = {k: result["metrics"][k]["evidence_coverage"]
                          for k in ("at_5", "at_10", "at_50", "context")}
                if any(type(v) not in {int, float} or not math.isfinite(v) or not 0 <= v <= 1
                       for v in values.values()):
                    raise DataError("invalid ranked evidence coverage")
                evidence[cid].append(values)
    if seen != observations.keys():
        raise DataError("figure inputs omit report observations")
    summaries = []
    for cell in report["cells"]:
        cid = cell["condition"]["condition_id"]
        stages = {s: fmean(r[s] for r in timings[cid]) for s in STAGES}
        if (len(timings[cid]) != cell["timing_measurements"]
                or not math.isclose(sum(stages.values()),
                                    cell["metrics"]["latency_mean"]["estimate"], abs_tol=1e-10)):
            raise DataError("stage means do not reconstruct verified online mean")
        ranked = {k: fmean(r[k] for r in evidence[cid])
                  for k in ("at_5", "at_10", "at_50", "context")} if evidence[cid] else {}
        if ranked and (len(evidence[cid]) != cell["questions"] or not math.isclose(
                ranked["context"], cell["metrics"]["evidence_coverage"]["estimate"],
                abs_tol=1e-12)):
            raise DataError("packed evidence mean differs from verified report")
        summaries.append({"condition_id": cid, "condition": cell["condition"],
                          "timing_measurements": len(timings[cid]), "questions": cell["questions"],
                          "stages": stages, "evidence": ranked})
    return report, summaries


def label(c: dict) -> str:
    if "baseline" in c:
        return "gold" if c["baseline"] == "gold" else "no-rag"
    return f"{c['family'][0].upper()}{c['size']}{'+' if c['reranking'] else '-'}"


def plot(report: dict, summaries: list[dict], kind: str, output: Path) -> None:
    items = []

    def text(x, y, value, size=14):
        items.append(dict(kind="text", x=x, y=y, text=value, size=size))

    def line(x, y, a, b, color="#BBBBBB"):
        items.append(dict(kind="line", x=x, y=y, a=a, b=b, color=color))

    def rect(x, y, w, h, color, filled=True):
        items.append(dict(kind="rect", x=x, y=y, w=w, h=h, color=color, filled=filled))

    baseline = "baselines" in kind
    cells = [c for c in report["cells"] if ("baseline" in c["condition"]) == baseline]
    by_id = {s["condition_id"]: s for s in summaries}
    scatter = kind in {"quality_latency", "evidence_quality", "quality_latency_baselines"}
    stages = kind.startswith("stage_times")
    xmetric = "evidence_coverage" if kind == "evidence_quality" else "latency_mean"
    xmax = 100 if xmetric == "evidence_coverage" else max(
        max(c["metrics"]["latency_mean"]["source_ci95"] +
            [c["metrics"]["latency_mean"]["estimate"]]) for c in cells) * 1.08
    if not scatter and not stages:
        xmax = 100
    text(25, 32, kind.replace("_", " "), 24)
    text(25, 58, "25 questions/cell; quality/evidence: repetition 1; latency: all 75 measurements.")
    text(25, 80, "Intervals: descriptive, unadjusted 95% source-cluster bootstrap; "
         "no winner selection." if scatter or stages else
         "Evidence bars are descriptive means without confidence intervals.")
    for panel, (dataset, model) in enumerate((d, m) for d in ("squad", "hotpot_qa")
                                           for m in ("llama", "qwen")):
        ox, oy = 100 + (panel % 2) * 595, 150 + (panel // 2) * 350
        width, height = (350 if scatter else 445), 240
        selected = sorted([c for c in cells if c["condition"]["dataset"] == dataset
                           and c["condition"]["model_family"] == model],
                          key=lambda c: label(c["condition"]))
        text(ox, oy-24, f"{dataset} / {model}", 18)
        for i in range(6):
            x = ox + width*i/5
            line(x, oy, x, oy+height)
            text(x-8, oy+height+20, f"{xmax*i/5:.1f}", 12)
        line(ox, oy, ox, oy+height, "#222222")
        line(ox, oy+height, ox+width, oy+height, "#222222")
        text(ox, oy+height+43, "Packed evidence coverage (%)" if xmetric == "evidence_coverage"
             else "Mean online seconds" if scatter or stages else "Evidence coverage (%)")
        if scatter:
            text(ox, oy-5, "Answer token F1 (%)", 12)
            for i in range(6):
                y = oy+height-height*i/5
                line(ox, y, ox+width, y)
                text(ox-30, y+4, str(i*20), 12)
        annotations = []
        for index, cell in enumerate(selected):
            c = cell["condition"]
            cid = c["condition_id"]
            color = FAMILIES.get(c.get("family"), "#CC79A7" if c.get("baseline") == "gold"
                                 else "#777777")
            if scatter:
                scale = 100 if xmetric == "evidence_coverage" else 1
                mx, my = cell["metrics"][xmetric], cell["metrics"]["token_f1"]
                x = ox+width*mx["estimate"]*scale/xmax
                y = oy+height*(1-my["estimate"])
                line(ox+width*mx["source_ci95"][0]*scale/xmax, y,
                     ox+width*mx["source_ci95"][1]*scale/xmax, y, color)
                line(x, oy+height*(1-my["source_ci95"][0]),
                     x, oy+height*(1-my["source_ci95"][1]), color)
                rect(x-3, y-3, 6, 6, color, c.get("reranking", True))
                annotations.append((y, x, label(c)))
            else:
                spacing = height/len(selected)
                y = oy+index*spacing+4
                text(ox-65, y+11, label(c), 12)
                summary = by_id[cid]
                if stages:
                    left = ox
                    for stage, color in zip(STAGES, COLORS, strict=True):
                        w = width*summary["stages"][stage]/xmax
                        rect(left, y, w, spacing*.65, color)
                        left += w
                    lo, hi = cell["metrics"]["latency_mean"]["source_ci95"]
                    line(ox+width*lo/xmax, y+spacing*.33,
                         ox+width*hi/xmax, y+spacing*.33, "#000000")
                else:
                    for j, (key, color) in enumerate(zip(
                            ("at_5", "at_10", "at_50", "context"), COLORS[:4], strict=True)):
                        rect(ox, y+j*spacing*.18, width*summary["evidence"][key],
                             spacing*.16, color)
        # Put labels in a separate rail, retaining the actual data coordinates.
        ordered = sorted(annotations)
        label_y = []
        for y, _, _ in ordered:
            label_y.append(max(oy+12, y, label_y[-1]+17 if label_y else oy+12))
        if label_y and label_y[-1] > oy+height-4:
            label_y[-1] = oy+height-4
            for i in range(len(label_y)-2, -1, -1):
                label_y[i] = min(label_y[i], label_y[i+1]-17)
        for (y, x, name), target in zip(ordered, label_y, strict=True):
            line(x+4, y, ox+width+8, target-4, "#999999")
            text(ox+width+12, target, name, 11)
    if stages:
        for i, (s, color) in enumerate(zip(STAGES, COLORS, strict=True)):
            x, y = 25+(i % 4)*295, 822+(i//4)*26
            rect(x, y-10, 12, 12, color)
            text(x+18, y, s.replace("_", " "), 12)
        text(25, 910, "Disjoint online timers; remainder is unattributed. "
             "Setup/isolation/scoring excluded.", 12)
    elif scatter:
        text(25, 830, "B=BM25, D=Dense, H=Hybrid; 128/256=chunk size; "
             "-=reranking off, +=on (filled).")
        text(25, 855, "Baseline plots separate: no-RAG keeps grounding instructions; "
             "gold is diagnostic evidence.")
        text(25, 880, "Baseline/main online implementations differ; do not pool their timings.")
    else:
        for i, (name, color) in enumerate(zip(("top 5", "top 10", "top 50", "packed"),
                                              COLORS[:4], strict=True)):
            rect(25+i*280, 820, 12, 12, color)
            text(45+i*280, 832, name)
        text(25, 862, "Rank evidence is after reranking where enabled. "
             "Bars are descriptive means, without intervals.")
    save_vectors(output/kind, items, f"Report {report['manifest_sha256']}; {kind}")


def export_figures(report_dir: Path, proof: Path, main: Path, baselines: Path,
                   protocol_path: Path, output: Path) -> dict:
    protocol = json.loads(protocol_path.read_text())
    expected = ["quality_latency", "evidence_quality", "quality_latency_baselines",
                "stage_times_main", "stage_times_baselines", "retrieval_evidence"]
    if protocol["version"] != "offline_vectors_v1" or protocol["figures"] != expected:
        raise DataError("unsupported figure protocol")
    if output.exists():
        raise DataError("figures require a fresh output directory")
    report, summaries = collect(report_dir, proof, {"main": main, "baselines": baselines})
    output.mkdir(parents=True)
    write_new_json(output/"stage-evidence.json", {"cells": summaries,
                   "report_sha256": report["manifest_sha256"], "protocol": protocol})
    with (output/"stage-times.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["condition_id", "dataset", "model",
                                "profile", "questions", "timing_measurements", *STAGES])
        writer.writeheader()
        for s in summaries:
            c = s["condition"]
            writer.writerow({"condition_id": s["condition_id"], "dataset": c["dataset"],
                             "model": c["model_family"], "profile": label(c),
                             "questions": s["questions"],
                             "timing_measurements": s["timing_measurements"],
                             **s["stages"]})
    for kind in expected:
        plot(report, summaries, kind, output)
    manifest = {"kind": "offline_figures", "report_sha256": report["manifest_sha256"],
                "proof_sha256": file_sha256(proof), "inputs": report["inputs"],
                "protocol_sha256": digest(protocol), "provenance": implementation_identity(),
                "files": {p.name: file_sha256(p) for p in sorted(output.iterdir())}}
    manifest["manifest_sha256"] = digest(manifest)
    write_new_json(output/"manifest.json", manifest)
    return {"output": str(output), "figures": len(expected), "vector_files": 2*len(expected),
            "cells": len(summaries), "manifest_sha256": manifest["manifest_sha256"]}
