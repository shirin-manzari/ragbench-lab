from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

from ragbench_lab.answer_metrics import answer_scores
from ragbench_lab.data.preparation import digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.figures import collect
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.pipeline import write_new_json
from ragbench_lab.run_store import iter_records, request_key, verified_manifest
from ragbench_lab.stage_a import implementation_identity

STRATA = ("candidate_evidence_incomplete", "packing_evidence_loss",
          "answer_error_with_full_evidence")


def failure_stratum(pair: list[dict]) -> str | None:
    if len(pair) != 2 or {r["model_family"] for r in pair} != {"llama", "qwen"}:
        raise DataError("failure review requires both generators")
    a, b = pair
    if any(a[k] != b[k] for k in ("dataset", "question_id", "pipeline_id", "top50", "packed",
                                 "context_sha256", "candidate_ids", "initial_ids")):
        raise DataError("failure review pair differs in evidence or pipeline")
    if all(r["exact_match"] == 1 for r in pair):
        return None
    if a["top50"] < 1:
        return STRATA[0]
    return STRATA[1] if a["packed"] < 1 else STRATA[2]


def select_cases(features: list[dict], protocol: dict) -> dict:
    if (protocol["version"] != "paired_failure_review_v1"
            or protocol["strata"] != list(STRATA)
            or protocol["datasets"] != ["squad", "hotpot_qa"]
            or protocol["per_stratum_dataset"] != 1
            or protocol["seed"] != 20261011 or protocol["salt"] != "failure-review-v1"):
        raise DataError("unsupported failure-review sampling protocol")
    groups = defaultdict(list)
    seen = set()
    for r in features:
        key = (r["dataset"], r["question_id"], r["pipeline_id"], r["model_family"])
        if key in seen:
            raise DataError("duplicate failure-review feature")
        seen.add(key)
        groups[key[:3]].append(r)
    eligible = defaultdict(list)
    for key, pair in sorted(groups.items()):
        stratum = failure_stratum(pair)
        if stratum:
            eligible[(key[0], stratum)].append({"dataset": key[0], "stratum": stratum,
                "question_id": key[1], "pipeline_id": key[2],
                "request_keys": sorted(r["request_key"] for r in pair),
                "selection_hash": digest([protocol["salt"], protocol["seed"], key[0], stratum,
                                          key[1], key[2]])})
    selected, inventory = [], []
    for dataset in protocol["datasets"]:
        used = set()
        for stratum in STRATA:
            pool = sorted(eligible[(dataset, stratum)], key=lambda r: r["selection_hash"])
            available = [r for r in pool if r["question_id"] not in used]
            chosen = available[:1]
            selected.extend(chosen)
            used.update(r["question_id"] for r in chosen)
            inventory.append({"dataset": dataset, "stratum": stratum,
                "eligible_pairs": len(pool), "eligible_unique_questions": len({
                    r["question_id"] for r in pool}),
                "available_after_question_dedup": len(available),
                "selected": len(chosen)})
    return {"cases": selected, "strata": inventory}


def inspect_record(row: dict, question, documents: dict, baseline: bool) -> dict:
    result = row["result"]
    context = result["inputs"]["context"] if baseline else result["context"]
    for e in context["evidence"]:
        source = documents[e["document_id"]].text[e["source_start"]:e["source_end"]]
        packed = context["text"][e["context_start"]:e["context_end"]]
        if e["text"] != source or source != packed:
            raise DataError("review evidence does not match source/context offsets")
    scores = answer_scores(result["generation"]["answer"], question.answers, question.dataset)
    if scores != result["answer_metrics"]:
        raise DataError("review answer scores differ from saved result")
    coverage = evidence_metrics(question, [(e["document_id"], e["source_start"], e["source_end"])
                                          for e in context["evidence"]])
    saved = result["context_evidence_metrics"] if baseline else result["metrics"]["context"]
    if coverage != saved:
        raise DataError("review packed coverage differs from source intervals")
    return {"request_key": row["request_key"], "record_sha256": row["record_sha256"],
        "condition_id": row["condition_id"], "model_family": row["model_family"],
        "answer": result["generation"]["answer"], "answer_metrics": scores,
        "abstained": result["generation"]["abstained"],
        "output_truncated": result["generation"]["output_truncated"],
        "context": context, "context_evidence_metrics": coverage,
        "baseline": result.get("baseline"),
        "rank_metrics": None if baseline else result["metrics"],
        "reranking": None if baseline else result["reranking"]}


def review_failures(report_dir: Path, proof: Path, main: Path, baselines: Path,
                    data_dirs: dict, protocol_path: Path, output: Path) -> dict:
    if output.exists():
        raise DataError("failure review requires a fresh directory")
    protocol = json.loads(protocol_path.read_text())
    # Reuse the complete raw/report proof audit; nothing is remeasured.
    report, _ = collect(report_dir, proof, {"main": main, "baselines": baselines})
    manifests = {role: verified_manifest(path/"manifest.json")
                 for role, path in (("main", main), ("baselines", baselines))}
    conditions = {c["condition"]["condition_id"]: c["condition"] for c in report["cells"]}
    features = []
    for row in iter_records(main, manifests["main"]):
        if row["kind"] == "event" or row["repetition"] != 1:
            continue
        r, c = row["result"], conditions[row["condition_id"]]
        features.append({k: row[k] for k in ("dataset", "question_id", "model_family",
                                           "request_key")} | {
            "pipeline_id": c["pipeline_id"], "top50": r["metrics"]["at_50"]["evidence_coverage"],
            "packed": r["metrics"]["context"]["evidence_coverage"],
            "exact_match": r["answer_metrics"]["exact_match"],
            "context_sha256": r["context_sha256"],
            "candidate_ids": r["reranking"]["candidate_ids"],
            "initial_ids": r["reranking"]["initial_candidate_ids"]})
    sample = select_cases(features, protocol)
    output.mkdir(parents=True)
    selection = {"protocol": protocol, "protocol_sha256": digest(protocol),
                 "report_sha256": report["manifest_sha256"], **sample}
    selection["manifest_sha256"] = digest(selection)
    # Persist the selected IDs before reading the selected answers/evidence for review.
    write_new_json(output/"selection.json", selection)
    prepared, sources = {}, {}
    for dataset, path in data_dirs.items():
        source, bundle = load_prepared(path)
        expected = manifests["main"]["identity"]["sources"][dataset]
        if any(source[k] != v for k, v in expected.items()):
            raise DataError("review prepared sources differ from measured run")
        prepared[dataset] = ({q.question_id: q for q in bundle.questions},
                             {d.document_id: d for d in bundle.documents})
        sources[dataset] = source["manifest_sha256"]
    wanted = {k for c in sample["cases"] for k in c["request_keys"]}
    question_ids = {(c["dataset"], c["question_id"]) for c in sample["cases"]}
    records = {}
    for role, path in (("main", main), ("baselines", baselines)):
        for row in iter_records(path, manifests[role]):
            if row["kind"] == "event" or row["repetition"] != 1:
                continue
            selected = (row["request_key"] in wanted if role == "main" else
                        (row["dataset"], row["question_id"]) in question_ids)
            if not selected:
                continue
            questions, documents = prepared[row["dataset"]]
            records[row["request_key"]] = inspect_record(
                row, questions[row["question_id"]], documents, role == "baselines")
    cases = []
    for unit in sample["cases"]:
        questions, _ = prepared[unit["dataset"]]
        q = questions[unit["question_id"]]
        main_records = [records[k] for k in unit["request_keys"]]
        # Link baseline request keys to this question, not merely its dataset.
        baseline_keys = {request_key(cid, q.question_id, 1) for cid, c in conditions.items()
                         if c.get("baseline") and c["dataset"] == q.dataset}
        baseline_records = [records[k] for k in sorted(baseline_keys) if k in records]
        if len(main_records) != 2 or len(baseline_records) != 4:
            raise DataError("review case lacks paired main/baseline records")
        cases.append({**unit, "question": asdict(q), "main": main_records,
                      "baselines": baseline_records})
    write_new_json(output/"cases.json", {"selection_sha256": selection["manifest_sha256"],
                                         "cases": cases})
    manifest = {"kind": "exploratory_failure_review", "inputs": report["inputs"],
                "report_sha256": report["manifest_sha256"], "prepared_sources": sources,
                "protocol_sha256": digest(protocol), "provenance": implementation_identity(),
                "files": {p.name: file_sha256(p) for p in sorted(output.iterdir())}}
    manifest["manifest_sha256"] = digest(manifest)
    write_new_json(output/"manifest.json", manifest)
    return {"output": str(output), "cases": len(cases), "paired_main_answers": 2*len(cases),
            "manifest_sha256": manifest["manifest_sha256"]}
