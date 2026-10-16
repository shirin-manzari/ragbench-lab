"""Export aggregate-only copies of the checked Stage B v3 results; never run models."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

from verify_public_results import (
    CONDITION_FIELDS,
    DEFAULT_BUNDLE,
    FIGURES,
    NOTES,
    ROOT,
    STUDY,
    canonical,
    require,
    sha256,
    verified_json,
    verify,
    verify_payload,
)


def build(analysis: Path, figures: Path, proof_path: Path) -> dict[str, bytes]:
    report = verified_json(analysis / "report.json")
    proof = verified_json(proof_path)
    figure_manifest = verified_json(figures / "manifest.json")
    require(proof["kind"] == "independent_analysis_checks"
            and proof["report_sha256"] == report["manifest_sha256"],
            "analysis proof belongs to another report")
    require(figure_manifest["report_sha256"] == report["manifest_sha256"]
            and figure_manifest["proof_sha256"] == sha256(proof_path.read_bytes()),
            "figures belong to another verified analysis")
    require(proof["files"]["report.json"] == sha256((analysis / "report.json").read_bytes()),
            "analysis report bytes changed")
    require(report["question_units"] == 50 and report["measurements"] == 4200
            and report["protocol"]["version"] == "paired_source_clusters_v1"
            and report["protocol"]["bootstrap_samples"] == STUDY["bootstrap_samples"]
            and report["protocol"]["seed"] == STUDY["bootstrap_seed"]
            and report["protocol"]["quality_repetition"] == STUDY["quality_repetition"]
            and report["protocol"]["confidence"] == STUDY["confidence"],
            "unsupported study scope or analysis settings")
    require({d: len(set(labels.values())) for d, labels in report["clusters"].items()}
            == STUDY["source_clusters"], "source-cluster counts changed")
    frozen = verified_json(ROOT / "manifests/stage-b-study-v3-reduced.json")
    require(report["scientific_study_sha256"] == frozen["manifest_sha256"],
            "report belongs to another study")
    require(frozen["selection"]["selected"]["embedder"] == STUDY["embedder"]
            and frozen["selection"]["selected"]["chunker"] == STUDY["chunker"]
            and frozen["config"]["retrieval"]["context_budget_tokens"]
            == STUDY["context_budget_reference_tokens"], "frozen retrieval settings changed")
    require(frozen["repetitions"] == STUDY["repetitions"]
            and frozen["main_requests"] == STUDY["main_measurements"]
            and frozen["baseline_plan"]["requests"] == STUDY["baseline_measurements"]
            and set(frozen["generator_settings"]) == set(STUDY["models"])
            and all(g["quantization"] == STUDY["quantization"]
                    for g in frozen["generator_settings"].values()), "frozen model/matrix changed")

    files = {}
    for name in ("cells.csv", "contrasts.csv", "stage-times.csv", *FIGURES):
        directory, inventory = ((analysis, proof["files"]) if name in (
            "cells.csv", "contrasts.csv") else (figures, figure_manifest["files"]))
        files[name] = (directory / name).read_bytes()
        require(sha256(files[name]) == inventory[name], f"source file changed: {name}")

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=CONDITION_FIELDS, lineterminator="\n")
    writer.writeheader()
    for cell in sorted(report["cells"], key=lambda c: c["condition"]["condition_id"]):
        c = cell["condition"]
        writer.writerow({
            "condition_id": c["condition_id"], "dataset": c["dataset"],
            "model": c["model_family"], "role": c.get("baseline", "rag"),
            "family": c.get("family", ""), "chunk_tokens": c.get("size", ""),
            "reranking": ("on" if c["reranking"] else "off") if "reranking" in c else "",
            "questions": cell["questions"], "timing_measurements": cell["timing_measurements"],
            "source_clusters": STUDY["source_clusters"][c["dataset"]],
        })
    files["conditions.csv"] = stream.getvalue().encode("utf-8")
    manifest = {
        "schema_version": 1, "kind": "public_stage_b_aggregates", "study": STUDY, "notes": NOTES,
        "sources": {
            "analysis_manifest_sha256": report["manifest_sha256"],
            "figure_manifest_sha256": figure_manifest["manifest_sha256"],
            "analysis_proof_sha256": sha256(proof_path.read_bytes()),
            "study_manifest_sha256": report["scientific_study_sha256"],
            "source_files": {name: sha256(data) for name, data in sorted(files.items())
                             if name != "conditions.csv"},
        },
        "files": {name: {"sha256": sha256(data), "bytes": len(data)}
                  for name, data in sorted(files.items())},
    }
    manifest["manifest_sha256"] = sha256(canonical(manifest))
    files["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True,
                                         ensure_ascii=False, allow_nan=False) + "\n").encode()
    verify_payload(files)  # Reject unsafe or inconsistent inputs before writing public files.
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-dir", type=Path, default=ROOT / "reports/stage-b-analysis-v1")
    parser.add_argument("--figures-dir", type=Path, default=ROOT / "reports/stage-b-figures-v1")
    parser.add_argument("--proof", type=Path,
                        default=ROOT / "artifacts/stage-b-analysis-verification-v1.json")
    parser.add_argument("--output", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--check", action="store_true",
                        help="compare the bundle with checked local inputs without writing")
    args = parser.parse_args()
    try:
        files = build(args.analysis_dir, args.figures_dir, args.proof)
        if args.check:
            require(all((args.output / name).read_bytes() == data for name, data in files.items()),
                    "public export differs from checked local inputs")
        else:
            args.output.mkdir(parents=True, exist_ok=False)
            for name, data in files.items():
                with (args.output / name).open("xb") as stream:
                    stream.write(data)
        print(json.dumps(verify(args.output), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"export failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
