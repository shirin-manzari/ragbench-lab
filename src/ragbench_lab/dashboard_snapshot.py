"""Small validated read-only snapshot contract, independent of Dash/model libraries."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError


def safe_file(root: Path, name: str) -> Path:
    p = Path(name)
    if not name or p.is_absolute() or ".." in p.parts or p == Path(".") or "\\" in name:
        raise DataError("unsafe snapshot asset path")
    path = root / p
    if root.is_symlink() or any(
        (root / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts) + 1)
    ):
        raise DataError("snapshot assets must not follow symlinks")
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise DataError("snapshot asset is missing/outside its directory")
    return path


def csv_text(rows: list[dict]) -> str:
    """Spreadsheet-safe text; numeric negatives remain numbers, not formulas."""
    output = io.StringIO(newline="")
    fields = list(rows[0]) if rows else ["status"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                k: "'" + v
                if isinstance(v, str)
                and (
                    v.startswith(("\t", "\r", "\n")) or v.lstrip().startswith(("=", "+", "-", "@"))
                )
                else v
                for k, v in row.items()
            }
        )
    return output.getvalue()


def table_rows(run: dict, cells: list[dict]) -> list[dict]:
    """Lossless numeric long table; uncertainty units and scope travel with downloads."""
    return [
        {
            "run_key": run["key"],
            "purpose": run["purpose"],
            "stage": run["stage"],
            "condition_id": cell["condition_id"],
            "dataset": cell["dataset"],
            **{
                key: cell.get(key)
                for key in (
                    "model_family",
                    "recipe",
                    "method",
                    "size",
                    "reranking",
                    "context_budget",
                )
            },
            "metric": name,
            "estimate": metric["estimate"],
            "unit": metric["unit"],
            "ci95_low": (metric.get("ci95") or [None, None])[0],
            "ci95_high": (metric.get("ci95") or [None, None])[1],
            "source_clusters": json.dumps(metric.get("source_clusters"), sort_keys=True),
            "uncertainty": run["uncertainty"],
            "questions": cell["questions"],
            "timing_measurements": cell["timing_measurements"],
            "failures": cell.get("failures", 0),
            "retries": cell.get("retries", 0),
        }
        for cell in cells
        for name, metric in cell["metrics"].items()
    ]


def _count(value, label: str) -> None:
    if type(value) is not int or value < 0:
        raise DataError(f"{label} must be a nonnegative integer")


def _metric(metric: dict, *, signed=False) -> None:
    if not isinstance(metric, dict) or metric.get("unit") not in {"fraction", "seconds"}:
        raise DataError("unknown or missing dashboard metric unit")
    if "estimate" not in metric:
        raise DataError("dashboard metric estimate is missing; use explicit null if unavailable")
    ci = metric.get("ci95")
    if ci is not None and (not isinstance(ci, list) or len(ci) != 2):
        raise DataError("invalid dashboard interval")
    values = [metric["estimate"], *(ci or [])]
    if any(v is not None and (type(v) not in {int, float} or not math.isfinite(v)) for v in values):
        raise DataError("nonfinite dashboard metric")
    if ci is not None and (None in ci or ci[0] > ci[1] or metric["estimate"] is None):
        raise DataError("invalid dashboard interval or unavailable estimate")
    if any(
        v is not None
        and (
            (not signed and v < 0)
            or (metric["unit"] == "fraction" and (v < (-1 if signed else 0) or v > 1))
        )
        for v in values
    ):
        raise DataError("dashboard metric outside declared units")


def validate_snapshot(snapshot: dict) -> None:
    """Reject structural errors; explicit nulls in incomplete studies stay unavailable."""
    try:
        _validate_snapshot(snapshot)
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise DataError(f"invalid dashboard snapshot structure: {error}") from error


def _validate_snapshot(snapshot: dict) -> None:
    if snapshot.get("schema_version") != 1 or snapshot.get("kind") != "readonly_results":
        raise DataError("unsupported dashboard snapshot schema")
    if not isinstance(snapshot["runs"], list) or not isinstance(snapshot["files"], dict):
        raise DataError("snapshot runs/files must be a list/object")
    seen = set()
    for run in snapshot["runs"]:
        key = run["key"]
        if (
            key in seen
            or not key
            or run["purpose"]
            not in {"development", "evaluation", "diagnostic", "pilot", "extension"}
        ):
            raise DataError("duplicate run key or unsupported purpose")
        seen.add(key)
        if run["stage"] not in {"A", "B", "baseline"} or not run["compatibility_key"]:
            raise DataError("run stage/compatibility identity missing")
        for field in ("label", "run_id", "uncertainty", "example_scope"):
            if not isinstance(run[field], str) or not run[field]:
                raise DataError(f"dashboard run {field} is missing")
        if not isinstance(run["provenance"], dict):
            raise DataError("dashboard run provenance must be an object")
        completion = run["completion"]
        if completion.get("status") not in {
            "complete",
            "incomplete",
            "in_progress",
            "failed",
            "pending",
        }:
            raise DataError("unknown dashboard completeness state")
        for name, value in completion.items():
            if name not in {"status", "diagnostic"}:
                _count(value, name)
        ids = set()
        cells = {}
        for cell in run["cells"]:
            if cell["condition_id"] in ids:
                raise DataError("duplicate dashboard cell")
            ids.add(cell["condition_id"])
            cells[cell["condition_id"]] = cell
            if cell["dataset"] not in {"squad", "hotpot_qa"}:
                raise DataError("unsupported dashboard dataset")
            for name in ("questions", "timing_measurements"):
                _count(cell[name], name)
            if cell["questions"] > cell["timing_measurements"]:
                raise DataError("quality question count exceeds successful measurements")
            for name in ("first_attempts", "failures", "retries"):
                if name in cell:
                    _count(cell[name], name)
            required = (
                {"evidence_coverage", "latency_median"}
                if run["stage"] == "A"
                else {"token_f1", "latency_mean"}
            )
            if not required <= cell["metrics"].keys():
                raise DataError("dashboard cell is missing required stage metrics")
            for name, metric in cell["metrics"].items():
                _metric(metric)
                if name.startswith("latency_") != (metric["unit"] == "seconds"):
                    raise DataError("dashboard metric name/unit mismatch")
            if run["stage"] != "A":
                if not isinstance(cell["stage_seconds"], dict):
                    raise DataError("stage seconds must be an object; use empty if unavailable")
                for value in cell["stage_seconds"].values():
                    _metric(dict(estimate=value, unit="seconds"))
        if completion.get("successful_requests") is not None and completion[
            "successful_requests"
        ] != sum(c["timing_measurements"] for c in cells.values()):
            raise DataError("dashboard completion/cell totals differ")
        if any(e["condition_id"] not in ids for e in run["examples"]):
            raise DataError("example refers to a foreign condition")
        if any(r["condition_id"] not in ids for r in run.get("requests", [])):
            raise DataError("request refers to a foreign condition")
        attempts, success, failed, retries, request_links = set(), Counter(), 0, 0, {}
        for request in run.get("requests", []):
            pair = (request["request_key"], request["attempt"])
            if pair in attempts or request["status"] not in {"success", "failed"}:
                raise DataError("duplicate attempt or invalid request status")
            attempts.add(pair)
            for name in ("attempt", "repetition"):
                if type(request[name]) is not int or request[name] < 1:
                    raise DataError("invalid request attempt/repetition")
            failed += request["status"] == "failed"
            retries += request["attempt"] > 1
            if request["status"] == "success":
                success[request["condition_id"]] += 1
            request_links[request["request_key"]] = request
        if attempts:
            for field, value in (
                ("successful_requests", sum(success.values())),
                ("failed_attempts", failed),
                ("retry_attempts", retries),
            ):
                if field in completion and completion[field] != value:
                    raise DataError("dashboard completion/request totals differ")
            if any(c["timing_measurements"] != success[cid] for cid, c in cells.items()):
                raise DataError("dashboard cell timing/request totals differ")
        seen_examples = set()
        for example in run["examples"]:
            if example["request_key"] in seen_examples:
                raise DataError("duplicate dashboard example")
            seen_examples.add(example["request_key"])
            question, context = example["question"], example["context"]
            if not isinstance(question["text"], str) or not isinstance(context["text"], str):
                raise DataError("question/context text must be plain strings")
            if not isinstance(question.get("answers", []), list) or any(
                not isinstance(a, str) for a in question.get("answers", [])
            ):
                raise DataError("reference answers must be a list of strings")
            if example["status"] not in {"success", "failed"}:
                raise DataError("unknown example status")
            if example["answer"] is not None and not isinstance(example["answer"], str):
                raise DataError("generated answer must be a string or null")
            for metric in (example.get("answer_metrics") or {}).values():
                _metric(dict(estimate=metric, unit="fraction"))
            for included in context["evidence"]:
                for name in ("source_start", "source_end", "context_start", "context_end"):
                    _count(included[name], name)
                if (
                    included["source_start"] > included["source_end"]
                    or included["context_start"] > included["context_end"]
                    or included["context_end"] > len(context["text"])
                    or context["text"][included["context_start"] : included["context_end"]]
                    != included["text"]
                ):
                    raise DataError("packed evidence text/offset mismatch")
            for item in example["retrieved_top5"]:
                chunk = item["chunk"]
                if (
                    not isinstance(chunk["text"], str)
                    or type(chunk["start"]) is not int
                    or type(chunk["end"]) is not int
                    or not 0 <= chunk["start"] <= chunk["end"]
                ):
                    raise DataError("invalid retrieved chunk text/offsets")
            for evidence in question.get("evidence", []):
                if (
                    type(evidence["start"]) is not int
                    or type(evidence["end"]) is not int
                    or not 0 <= evidence["start"] <= evidence["end"]
                ):
                    raise DataError("invalid annotation offsets")
            if example.get("question", {}).get("dataset") not in {
                None,
                cells[example["condition_id"]]["dataset"],
            }:
                raise DataError("example dataset differs from condition")
            if attempts:
                request = request_links.get(example["request_key"], {})
                if any(
                    request.get(k) != example.get(k)
                    for k in ("condition_id", "question_id", "record_sha256")
                ):
                    raise DataError("example/request lineage differs")
        for contrast in run["paired_contrasts"]:
            left, right = (
                cells.get(contrast[k]) for k in ("left_condition_id", "right_condition_id")
            )
            if not left or not right or left["dataset"] != right["dataset"]:
                raise DataError("paired contrast crosses incompatible conditions")
            for name, metric in contrast["metrics"].items():
                if name not in left["metrics"] or name not in right["metrics"]:
                    raise DataError("paired contrast metric is missing from conditions")
                _metric(
                    dict(
                        estimate=metric["estimate"],
                        ci95=metric.get("source_ci95"),
                        unit=left["metrics"][name]["unit"],
                    ),
                    signed=True,
                )


def load_snapshot(directory: Path) -> dict:
    path = safe_file(directory, "snapshot.json")
    try:
        snapshot = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        raise DataError("dashboard snapshot is not valid UTF-8 JSON") from error
    try:
        identity = snapshot.get("manifest_sha256")
        if digest({k: v for k, v in snapshot.items() if k != "manifest_sha256"}) != identity:
            raise DataError("dashboard snapshot identity mismatch")
    except (AttributeError, ValueError, TypeError) as error:
        raise DataError("dashboard snapshot must be a finite JSON object") from error
    validate_snapshot(snapshot)
    for name, sha in snapshot["files"].items():
        if name == "snapshot.json":
            raise DataError("snapshot cannot inventory itself")
        with safe_file(directory, name).open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != sha:
                raise DataError("dashboard asset checksum mismatch")
    return snapshot
