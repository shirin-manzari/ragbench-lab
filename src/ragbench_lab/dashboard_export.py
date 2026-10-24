from __future__ import annotations

import json
import random
import shutil
import zipfile
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path
from statistics import mean

from ragbench_lab.dashboard_snapshot import csv_text, load_snapshot, table_rows
from ragbench_lab.data.preparation import digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.reporting import percentile, timing_summary
from ragbench_lab.run_store import iter_records, verified_manifest
from ragbench_lab.stage_a import implementation_identity, validate_requests
from ragbench_lab.synthesis import checked_artifact
from ragbench_lab.vector_export import save_vectors


def stage_a_vectors(run: dict, output: Path) -> list[Path]:
    """Publication files from the same precomputed cells, with no plotting dependency."""
    paths = []
    for metric in ("evidence_coverage", "latency_median"):
        items = [
            {
                "kind": "text",
                "x": 25,
                "y": 35,
                "size": 22,
                "text": f"Stage A {run['purpose']} / {metric}",
            },
            {
                "kind": "text",
                "x": 25,
                "y": 64,
                "size": 13,
                "text": "Repetition-one quality; within-question timing repeats. "
                "95% question-cluster intervals; source dependence not adjusted.",
            },
        ]
        estimates = [
            v
            for c in run["cells"]
            for v in [c["metrics"][metric]["estimate"], *(c["metrics"][metric]["ci95"] or [])]
            if v is not None
        ]
        maximum = 1 if metric == "evidence_coverage" else max(estimates or [1]) * 1.05
        maximum = maximum or 1
        for panel, dataset in enumerate(("squad", "hotpot_qa")):
            left, top, width = 215 + panel * 600, 150, 345
            items.append(dict(kind="text", x=left - 180, y=110, text=dataset, size=18))
            cells = sorted(
                [c for c in run["cells"] if c["dataset"] == dataset],
                key=lambda c: (c["recipe"], c["method"], c["size"]),
            )
            counts = sorted(
                {
                    (c.get("questions", "unavailable"), c.get("timing_measurements", "unavailable"))
                    for c in cells
                }
            )
            items.append(
                dict(
                    kind="text",
                    x=left - 180,
                    y=132,
                    size=10,
                    text="Per cell: "
                    + "; ".join(f"n={q} questions, {t} timing measurements" for q, t in counts),
                )
            )
            for i, cell in enumerate(cells):
                y = top + i * 22
                m = cell["metrics"][metric]
                label = f"{cell['recipe']}/{cell['method'][:4]}/{cell['size']}"
                items.append(dict(kind="text", x=left - 185, y=y + 10, text=label, size=10))
                if m["estimate"] is not None:
                    items.append(
                        dict(
                            kind="rect",
                            x=left,
                            y=y,
                            w=width * m["estimate"] / maximum,
                            h=13,
                            color="#0072B2",
                        )
                    )
                    if m["ci95"]:
                        lo, hi = m["ci95"]
                        items.append(
                            dict(
                                kind="line",
                                x=left + width * lo / maximum,
                                y=y + 6,
                                a=left + width * hi / maximum,
                                b=y + 6,
                                color="#222222",
                            )
                        )
            for i in range(6):
                x = left + width * i / 5
                label = f"{maximum * i / 5 * (100 if metric == 'evidence_coverage' else 1):.2f}"
                items.append(dict(kind="text", x=x - 8, y=845, text=label, size=11))
            items.append(
                dict(
                    kind="text",
                    x=left,
                    y=877,
                    size=13,
                    text="Evidence coverage (%)"
                    if metric == "evidence_coverage"
                    else "Median online retrieval seconds",
                )
            )
        name = f"stage_a_{run['purpose']}_{metric}"
        save_vectors(output / name, items, f"Run {run['key']}; exact dashboard cell estimates")
        paths.extend((output / f"{name}.svg", output / f"{name}.pdf"))
    return paths


def example(row: dict, question, baseline=False) -> dict:
    r = row["result"]
    context = r["inputs"]["context"] if baseline else r["context"]
    if "retrieval" in r:
        chunks = {e["chunk"]["chunk_id"]: e for e in r["retrieval"]["initial_candidates"]}
        retrieved = [chunks[cid] for cid in r["reranking"]["candidate_ids"][:5]]
    else:
        retrieved = r.get("retrieved", [])[:5]
    return {
        "condition_id": row["condition_id"],
        "question_id": row["question_id"],
        "request_key": row["request_key"],
        "record_sha256": row["record_sha256"],
        "repetition": row["repetition"],
        "question": asdict(question),
        "context": context,
        "retrieved_top5": retrieved,
        "answer": r.get("generation", {}).get("answer"),
        "answer_metrics": r.get("answer_metrics"),
        "metrics": r.get("metrics"),
        "output_truncated": r.get("generation", {}).get("output_truncated"),
        "baseline": r.get("baseline"),
        "status": row["status"],
        "error": r.get("error"),
    }


def stage_a_snapshot(directory: Path, summary_path: Path, prepared: dict) -> dict:
    if (directory / ".writer.lock").exists():
        raise DataError("dashboard export requires stopped measurement runs")
    manifest = verified_manifest(directory / "manifest.json")
    saved = json.loads(summary_path.read_text())
    identity = manifest["identity"]
    if saved["run_manifest_sha256"] != manifest["manifest_sha256"] or saved[
        "records_sha256"
    ] != file_sha256(directory / "records.jsonl"):
        raise DataError("Stage A saved summary/run identity mismatch")
    first, retries = Counter(), Counter()
    failures, quality = defaultdict(list), defaultdict(list)
    times = defaultdict(lambda: defaultdict(list))
    requests, examples = [], []
    selected = {
        d: min(ids, key=lambda q: digest(["dashboard-example-v1", d, q]))
        for d, ids in identity["question_ids"].items()
    }
    for row in iter_records(directory, manifest):
        validate_requests([row], identity)
        if row.get("kind") == "event":
            continue
        requests.append(
            {
                k: row[k]
                for k in (
                    "condition_id",
                    "question_id",
                    "request_key",
                    "record_sha256",
                    "attempt",
                    "repetition",
                    "status",
                )
            }
        )
        cid = row["condition_id"]
        if row["attempt"] != 1:
            retries[cid] += 1
            continue
        first[cid] += 1
        if row["status"] != "success":
            failures[cid].append(row.get("result", {}).get("error", "failed"))
            continue
        times[cid][row["question_id"]].append(
            row["result"]["timings_seconds"]["online_retrieval_path"]
        )
        if row["repetition"] == 1:
            quality[cid].append(row["result"]["metrics"]["context"]["evidence_coverage"])
            if row["question_id"] == selected[row["dataset"]]:
                examples.append(example(row, prepared[row["dataset"]][row["question_id"]]))
    cells = []
    seed = identity["config"]["dataset"]["sampling_seed"]
    for item in saved["conditions"]:
        c = item["condition"]
        cid = c["condition_id"]
        groups = [
            times[cid][qid] for qid in identity["question_ids"][c["dataset"]] if times[cid][qid]
        ]
        timing = timing_summary(groups, seed)
        coverage = mean(quality[cid]) if quality[cid] else None
        if (
            timing != item["retrieval_seconds"]
            or coverage != item["context_coverage"]
            or first[cid] != item["first_attempts"]
            or len(failures[cid]) != item["failed_first_attempts"]
            or retries[cid] != item["retry_attempts"]
        ):
            raise DataError("offline Stage A aggregate differs from saved report")
        ci = None
        if len(quality[cid]) >= 2:
            rng = random.Random(seed)
            resamples = [mean(rng.choices(quality[cid], k=len(quality[cid]))) for _ in range(500)]
            ci = [percentile(resamples, 0.025), percentile(resamples, 0.975)]
        cells.append(
            {
                **c,
                "family": c["recipe"].split("_")[0],
                "model_family": None,
                "context_budget": identity["config"]["retrieval"]["context_budget_tokens"],
                "questions": len(quality[cid]),
                "timing_measurements": timing["measurements"],
                "first_attempts": first[cid],
                "failures": len(failures[cid]),
                "retries": retries[cid],
                "failure_messages": failures[cid],
                "metrics": {
                    "evidence_coverage": {"estimate": coverage, "ci95": ci, "unit": "fraction"},
                    "latency_median": {
                        "estimate": timing["median"],
                        "ci95": timing["median_ci95"],
                        "unit": "seconds",
                    },
                    "latency_p95": {
                        "estimate": timing["p95"],
                        "ci95": timing["p95_ci95"],
                        "unit": "seconds",
                    },
                },
            }
        )
    return {
        "key": manifest["manifest_sha256"],
        "run_id": manifest["run_id"],
        "stage": "A",
        "label": f"Stage A / {identity['split']} / {manifest['run_id'][:8]}",
        "purpose": identity["split"],
        "compatibility_key": digest(identity),
        "completion": saved["completion"],
        "provenance": identity["provenance"],
        "sources": identity["sources"],
        "cells": cells,
        "examples": examples,
        "requests": requests,
        "uncertainty": "500 question-cluster bootstrap draws; source dependence not adjusted",
        "example_scope": "one ID-hash-selected repetition-one question per dataset/condition",
        "paired_contrasts": [],
        "missing_fields": ["generator answers not measured in Stage A"],
    }


def export_dashboard(protocol_path: Path, output: Path) -> dict:
    if output.exists():
        raise DataError("dashboard export requires a fresh directory")
    protocol = json.loads(protocol_path.read_text())
    if protocol["version"] != "readonly_results_v1" or protocol["schema_version"] != 1:
        raise DataError("unsupported dashboard export protocol")
    proof = json.loads(Path(protocol["archive_proof"]).read_text())
    if file_sha256(Path(protocol["archive"])) != proof["archive_sha256"]:
        raise DataError("dashboard raw archive checksum differs")
    with zipfile.ZipFile(protocol["archive"]) as archive:
        inventory = json.loads(archive.read("archive.json"))
    if (
        digest({k: v for k, v in inventory.items() if k != "manifest_sha256"})
        != proof["manifest_sha256"]
    ):
        raise DataError("dashboard raw inventory differs")
    pins = {e["path"]: e["sha256"] for e in inventory["files"]}

    def pin(path):
        name = str(path)
        if pins.get(name) != file_sha256(path):
            raise DataError(f"dashboard input differs from archived bytes: {name}")

    prepared = {}
    for dataset, path in protocol["prepared"].items():
        for name in ("manifest.json", "documents.jsonl", "questions.jsonl"):
            pin(Path(path) / name)
        _, bundle = load_prepared(Path(path))
        prepared[dataset] = {q.question_id: q for q in bundle.questions}
    runs = []
    for entry in protocol["stage_a"]:
        directory, summary = Path(entry["run"]), Path(entry["summary"])
        for path in (directory / "manifest.json", directory / "records.jsonl", summary):
            pin(path)
        print(f"exporting verified {directory}", flush=True)
        runs.append(stage_a_snapshot(directory, summary, prepared))
    analysis_dir = Path(protocol["analysis"])
    report = checked_artifact(
        analysis_dir,
        Path(protocol["analysis_proof"]),
        "independent_analysis_checks",
        "report_sha256",
        "report.json",
    )
    stages = {}
    figure_dir = Path(protocol["figures"])
    figure_manifest = checked_artifact(
        figure_dir,
        Path(protocol["figure_proof"]),
        "independent_figure_checks",
        "figure_manifest_sha256",
        "manifest.json",
    )
    if figure_manifest["report_sha256"] != report["manifest_sha256"]:
        raise DataError("dashboard figures belong to another analysis")
    for s in json.loads((figure_dir / "stage-evidence.json").read_text())["cells"]:
        stages[s["condition_id"]] = s["stages"]
    for role, stage in (("main", "B"), ("baselines", "baseline")):
        directory = Path(protocol[role])
        if (directory / ".writer.lock").exists():
            raise DataError("dashboard cannot export active runs")
        manifest = verified_manifest(directory / "manifest.json")
        binding = report["inputs"][role]
        if (
            manifest["manifest_sha256"] != binding["manifest_sha256"]
            or file_sha256(directory / "records.jsonl") != binding["records_sha256"]
        ):
            raise DataError("dashboard Stage B raw identity mismatch")
        cells, examples, requests = [], [], []
        for row in iter_records(directory, manifest):
            if row["kind"] == "event":
                continue
            if row["status"] != "success" or row["attempt"] != 1:
                raise DataError("verified core analysis cannot substitute retries/failures")
            requests.append(
                {
                    k: row[k]
                    for k in (
                        "condition_id",
                        "question_id",
                        "request_key",
                        "record_sha256",
                        "attempt",
                        "repetition",
                        "status",
                    )
                }
            )
            if row["repetition"] == 1:
                examples.append(
                    example(row, prepared[row["dataset"]][row["question_id"]], stage == "baseline")
                )
        for item in report["cells"]:
            c = item["condition"]
            if ("baseline" in c) != (stage == "baseline"):
                continue
            cells.append(
                {
                    **c,
                    "family": c.get("family"),
                    "method": c.get("method"),
                    "recipe": c.get("recipe", c.get("baseline")),
                    "size": c.get("size"),
                    "reranking": c.get("reranking"),
                    "context_budget": 1024,
                    "questions": item["questions"],
                    "timing_measurements": item["timing_measurements"],
                    "first_attempts": item["timing_measurements"],
                    "failures": 0,
                    "retries": 0,
                    "stage_seconds": stages[c["condition_id"]],
                    "metrics": {
                        m: {
                            "estimate": v["estimate"],
                            "ci95": v["source_ci95"],
                            "question_sensitivity_ci95": v["question_sensitivity_ci95"],
                            "source_clusters": v["source_clusters"],
                            "unit": report["units"][m],
                        }
                        for m, v in item["metrics"].items()
                    },
                }
            )
        cids = {c["condition_id"] for c in cells}
        runs.append(
            {
                "key": manifest["manifest_sha256"],
                "run_id": manifest["run_id"],
                "label": f"{'Stage B main' if stage == 'B' else 'Separate baselines'} / evaluation",
                "stage": stage,
                "purpose": "evaluation",
                "compatibility_key": digest(binding),
                "completion": {
                    "status": "complete",
                    "successful_requests": len(requests),
                    "failed_attempts": 0,
                    "retry_attempts": 0,
                },
                "provenance": binding["provenance"],
                "cells": cells,
                "examples": examples,
                "requests": requests,
                "uncertainty": (
                    "2000 whole-source-cluster paired bootstrap draws; unadjusted descriptive"
                ),
                "example_scope": (
                    "all repetition-one questions; other repetitions are timing measurements"
                ),
                "paired_contrasts": [
                    p
                    for p in report["contrasts"]
                    if p["left_condition_id"] in cids and p["right_condition_id"] in cids
                ],
                "missing_fields": [],
            }
        )
    output.mkdir(parents=True)
    rows = []
    for run in runs:
        rows.extend(table_rows(run, run["cells"]))
    with (output / "tables.csv").open("x", encoding="utf-8") as stream:
        stream.write(csv_text(rows))
    files = {"tables.csv": file_sha256(output / "tables.csv")}
    (output / "figures").mkdir()
    for name, sha in figure_manifest["files"].items():
        if Path(name).suffix in {".svg", ".pdf"}:
            shutil.copyfile(figure_dir / name, output / "figures" / name)
            files[f"figures/{name}"] = sha
    for run in runs:
        if run["stage"] == "A":
            for path in stage_a_vectors(run, output / "figures"):
                files[f"figures/{path.name}"] = file_sha256(path)
    snapshot = {
        "kind": "readonly_results",
        "schema_version": 1,
        "protocol": protocol,
        "protocol_sha256": digest(protocol),
        "runs": runs,
        "files": files,
        "missing_studies": protocol["missing_studies"],
        "provenance": implementation_identity(),
        "raw_archive_sha256": proof["archive_sha256"],
    }
    snapshot["manifest_sha256"] = digest(snapshot)
    write_new_json(output / "snapshot.json", snapshot)
    load_snapshot(output)
    return {
        "output": str(output),
        "runs": len(runs),
        "cells": sum(len(r["cells"]) for r in runs),
        "examples": sum(len(r["examples"]) for r in runs),
        "manifest_sha256": snapshot["manifest_sha256"],
    }
