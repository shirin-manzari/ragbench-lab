from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

from ragbench_lab.baseline_runner import baseline_checks, baseline_gate, baseline_plan
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.run_store import iter_records, request_key, verified_manifest
from ragbench_lab.stage_a import timestamp, validate_requests
from ragbench_lab.stage_b import evaluation_question_ids, execution_plan
from ragbench_lab.stage_b_runner import request_checks, validate_gate


def scoped_path(root: Path, name: str) -> Path:
    path = Path(name)
    if not name or path.is_absolute() or ".." in path.parts or path == Path("."):
        raise DataError("archive paths must be explicit project-relative paths")
    candidate = root / path
    if root.is_symlink() or any((root / Path(*path.parts[:i])).is_symlink()
                               for i in range(1, len(path.parts) + 1)):
        raise DataError("archive inputs must not follow symlinks")
    if not candidate.exists() or not candidate.resolve().is_relative_to(root.resolve()):
        raise DataError(f"archive input missing/outside project: {name}")
    return candidate


def audit_run(directory: Path, family: str, expected_slots: int,
              require_complete: bool) -> tuple[dict, dict]:
    if (directory / ".writer.lock").exists():
        raise DataError("archive requires stopped runs, including historical runs")
    manifest = verified_manifest(directory / "manifest.json")
    identity = manifest["identity"]
    if family == "A":
        conditions = identity["conditions"]
        questions = {str(r): identity["question_ids"] for r in (1, 2, 3)}
    elif family in {"B", "baseline"}:
        if identity["stage"] != ("B" if family == "B" else "B_baselines"):
            raise DataError("archive run family mismatch")
        conditions = identity["plan"]["conditions"]
        questions = identity["plan"]["question_orders"]
    else:
        raise DataError("unsupported archive run family")
    expected = {request_key(c["condition_id"], qid, rep)
        for c in conditions for rep in (1, 2, 3)
        for qid in questions[str(rep)][c["dataset"]]}
    if len(expected) != expected_slots:
        raise DataError("archive run matrix differs from declared slot count")
    successes, attempted = set(), set()
    failures, retries, setup_failures, rows_count = 0, 0, 0, 0
    contexts, candidates, counts = {}, {}, Counter()
    for row in iter_records(directory, manifest):
        rows_count += 1
        if family == "A":
            validate_requests([row], identity)
        else:
            checker = request_checks if family == "B" else baseline_checks
            checker(row, identity, contexts, candidates)
        if row.get("kind") == "event":
            setup_failures += row.get("event") == "block_setup_failure"
            continue
        if row["request_key"] not in expected:
            raise DataError("archive request outside declared matrix")
        attempted.add(row["request_key"])
        retries += row["attempt"] > 1
        failures += row["status"] == "failed"
        if row["status"] == "success":
            successes.add(row["request_key"])
            counts[(row["condition_id"], row["repetition"])] += 1
    if require_complete and (successes != expected or failures or retries or setup_failures):
        raise DataError("primary archive requires complete first-attempt failure-free measurements")
    report = {"run_id": manifest["run_id"], "manifest_sha256": manifest["manifest_sha256"],
        "manifest_file_sha256": file_sha256(directory / "manifest.json"),
        "records_sha256": file_sha256(directory / "records.jsonl"), "family": family,
        "split": identity["split"], "diagnostic": identity["diagnostic"],
        "planned_slots": len(expected), "successful_slots": len(successes),
        "missing_successes": len(expected - successes),
        "unattempted_slots": len(expected - attempted),
        "failed_attempts": failures, "retry_attempts": retries, "setup_failures": setup_failures,
        "records": rows_count, "primary": require_complete,
        "condition_repetition_counts": [{"condition_id": cid, "repetition": rep, "successes": n}
            for (cid, rep), n in sorted(counts.items())],
        "provenance": identity["provenance"]}
    return report, manifest


def source_snapshot(root: Path, revision: str) -> tuple[list[tuple[str, bytes]], str]:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise DataError("pin source snapshot by full Git revision")
    result = subprocess.run(["git", "archive", "--format=zip", revision], cwd=root,
                            capture_output=True, check=True)
    files, fingerprint = [], {}
    with zipfile.ZipFile(io.BytesIO(result.stdout)) as snapshot:
        for member in snapshot.infolist():
            if member.is_dir():
                continue
            name = member.filename
            if Path(name).is_absolute() or ".." in Path(name).parts:
                raise DataError("unsafe source snapshot member")
            data = snapshot.read(member)
            files.append((f"source/{revision}/{name}", data))
            if ((name.startswith("src/ragbench_lab/") and name.endswith(".py"))
                    or (name.startswith("configs/") and name.endswith(".toml"))
                    or name in {"pyproject.toml", "requirements.lock"}):
                fingerprint[name] = hashlib.sha256(data).hexdigest()
    return files, digest(fingerprint)


def local_source_snapshot(root: Path, directory: str, revision: str,
                          expected: str) -> tuple[list[tuple[str, bytes]], str]:
    """Archive only fingerprinted measurement inputs from an explicit saved tree."""
    if (not re.fullmatch(r"[0-9a-f]{40}", revision)
            or not re.fullmatch(r"[0-9a-f]{64}", expected)):
        raise DataError("local source snapshot requires full revision and fingerprint")
    saved = scoped_path(root, directory)
    paths = sorted([*saved.joinpath("src/ragbench_lab").rglob("*.py"),
                    *saved.joinpath("configs").glob("*.toml"),
                    saved / "pyproject.toml", saved / "requirements.lock"])
    files, fingerprint = [], {}
    for path in paths:
        scoped_path(root, str(path.relative_to(root)))
        name = str(path.relative_to(saved))
        data = path.read_bytes()
        fingerprint[name] = hashlib.sha256(data).hexdigest()
        files.append((f"source/{revision}/local-{expected}/{name}", data))
    if digest(fingerprint) != expected:
        raise DataError("saved local source does not match recorded measurement fingerprint")
    return files, expected


def verify_archive(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or "archive.json" not in names:
            raise DataError("duplicate archive names or missing inventory")
        record = json.loads(archive.read("archive.json"))
        if digest({k: v for k, v in record.items() if k != "manifest_sha256"}) != record.get(
                "manifest_sha256"):
            raise DataError("archive inventory hash mismatch")
        expected = {entry["path"] for entry in record["files"]}
        if len(expected) != len(record["files"]) or set(names) != expected | {"archive.json"}:
            raise DataError("archive member inventory differs")
        for entry in record["files"]:
            name = entry["path"]
            if Path(name).is_absolute() or ".." in Path(name).parts:
                raise DataError("unsafe archive member")
            sha, size = hashlib.sha256(), 0
            with archive.open(name) as stream:
                while data := stream.read(1024 * 1024):
                    sha.update(data)
                    size += len(data)
            if size != entry["bytes"] or sha.hexdigest() != entry["sha256"]:
                raise DataError(f"archive checksum mismatch: {name}")
    return {"files": len(record["files"]), "manifest_sha256": record["manifest_sha256"],
            "archive_sha256": file_sha256(path), "archive_bytes": path.stat().st_size,
            "uncompressed_bytes": sum(f["bytes"] for f in record["files"])}


def archive_study(config, specification: Path, output: Path, root: Path = Path(".")) -> dict:
    if output.exists() or output.suffix != ".zip":
        raise DataError("archive output must be a fresh .zip file")
    spec = json.loads(specification.read_text(encoding="utf-8"))
    if spec["schema_version"] != 1 or not spec["exclusions"]:
        raise DataError("archive specification must declare scope and exclusions")
    study = verified_manifest(scoped_path(root, spec["study"]))
    plan = verified_manifest(scoped_path(root, spec["baseline_plan"]))
    expected_files = {name: file_sha256(scoped_path(root, name))
                      for name in (spec["study"], spec["baseline_plan"])}
    audits, manifests, files = {}, {}, set()
    for run in spec["runs"]:
        if run["role"] in audits:
            raise DataError("duplicate archive run role")
        directory = scoped_path(root, run["path"])
        print(f"checking {run['role']}", flush=True)
        report, manifest = audit_run(directory, run["family"], run["slots"], run["complete"])
        audits[run["role"]], manifests[run["role"]] = report, manifest
        expected_files[f"{run['path']}/records.jsonl"] = report["records_sha256"]
        expected_files[f"{run['path']}/manifest.json"] = report["manifest_file_sha256"]
        for path in directory.iterdir():
            if path.is_file() and path.name in {"manifest.json", "records.jsonl", "summary.json"}:
                files.add(str(path.relative_to(root)))
    main, baseline = manifests["main"], manifests["baselines"]
    expected_main = execution_plan(config, study)
    for key in ("conditions", "blocks", "question_orders", "main_requests"):
        if main["identity"]["plan"][key] != expected_main[key]:
            raise DataError("primary main matrix differs from frozen study")
    if plan != baseline_plan(config, study, main, audits["main"]["records_sha256"]):
        raise DataError("baseline parent/controls differ from archived main")
    if (baseline["identity"]["baseline_plan_sha256"] != plan["manifest_sha256"]
            or baseline["identity"]["study_sha256"] != study["manifest_sha256"]):
        raise DataError("baseline identity differs from scientific plan")
    if validate_gate(scoped_path(root, spec["main_validation"]), main["identity"]) != main[
            "identity"]["validation_manifest_sha256"]:
        raise DataError("main validation linkage changed")
    gate = baseline_gate(scoped_path(root, spec["baseline_validation"]), baseline["identity"])
    if gate != baseline["identity"]["validation_manifest_sha256"]:
        raise DataError("baseline validation linkage changed")
    if (baseline["identity"]["plan"]["main_requests"] != plan["requests"]
            or audits["baselines"]["planned_slots"] != plan["requests"]):
        raise DataError("baseline workload differs from its frozen plan")
    for orders in baseline["identity"]["plan"]["question_orders"].values():
        if {d: sorted(ids) for d, ids in orders.items()} != evaluation_question_ids(study):
            raise DataError("baseline/main question pairing differs")
    selection = study["selection"]
    if (audits["stage_a_development"]["manifest_sha256"] != selection["development_run_sha256"]
            or audits["stage_a_development"]["records_sha256"] != selection["records_sha256"]
            or manifests["stage_a_evaluation"]["identity"]["selection_freeze_sha256"]
                != selection["manifest_sha256"]):
        raise DataError("archived Stage A selection/evaluation lineage changed")
    for dataset, directory in spec["prepared"].items():
        source, _ = load_prepared(scoped_path(root, directory))
        if any(source[k] != v for k, v in study["selection"]["sources"][dataset].items()):
            raise DataError("archive prepared source differs from frozen study")
        for filename in ("manifest.json", "documents.jsonl", "questions.jsonl"):
            name = f"{directory}/{filename}"
            expected_files[name] = file_sha256(scoped_path(root, name))
    for name in spec["include"]:
        path = scoped_path(root, name)
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    scoped_path(root, str(child.relative_to(root)))
                    files.add(str(child.relative_to(root)))
        else:
            files.add(name)
    snapshots = {}
    source_files = []
    for report in audits.values():
        revision = report["provenance"]["git_revision"]
        expected = report["provenance"]["source_tree_sha256"]
        overlays = [s for s in spec.get("local_source_snapshots", [])
                    if s["git_revision"] == revision and s["source_tree_sha256"] == expected]
        if len(overlays) > 1:
            raise DataError("duplicate local source snapshot declaration")
        key = f"{revision}/local-{expected}" if overlays else revision
        if key not in snapshots:
            if overlays:
                snapshot, fingerprint = local_source_snapshot(
                    root, overlays[0]["directory"], revision, expected)
            else:
                snapshot, fingerprint = source_snapshot(root, revision)
            snapshots[key] = fingerprint
            source_files.extend(snapshot)
        if snapshots[key] != expected:
            raise DataError("source snapshot does not reproduce recorded source fingerprint")
    inventory = []
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive output creation. Any interrupted/failed export is kept for explicit review.
    with output.open("xb") as target, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED,
                                                     compresslevel=3) as archive:
        for name in sorted(files):
            path = scoped_path(root, name)
            before = path.stat()
            sha, size = hashlib.sha256(), 0
            print(f"archiving {name}", flush=True)
            with path.open("rb") as source, archive.open(name, "w", force_zip64=True) as dest:
                while data := source.read(1024 * 1024):
                    dest.write(data)
                    sha.update(data)
                    size += len(data)
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise DataError("archive input changed while copying")
            if name in expected_files and sha.hexdigest() != expected_files[name]:
                raise DataError("audited input changed before archive copy")
            inventory.append({"path": name, "sha256": sha.hexdigest(), "bytes": size})
        for name, data in source_files:
            archive.writestr(name, data)
            inventory.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(),
                              "bytes": len(data)})
        record = {"kind": "local_research_archive", "schema_version": 1,
            "created_at": timestamp(), "scientific_study_sha256": study["manifest_sha256"],
            "baseline_plan_sha256": plan["manifest_sha256"], "runs": audits,
            "source_snapshots": snapshots, "files": inventory, "exclusions": spec["exclusions"],
            "scope": ("raw measurements and prepared corpora for offline analysis; "
                      "not a self-contained model rerun"),
            "privacy": ("local archive; raw prompts/provenance/docs require review "
                        "before external sharing")}
        record["manifest_sha256"] = digest(record)
        archive.writestr("archive.json", canonical(record))
    print("verifying every archived member", flush=True)
    return {"output": str(output), "runs": audits, **verify_archive(output)}
