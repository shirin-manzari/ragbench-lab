"""Two-part offline delivery: immutable raw archive plus verified analysis overlay."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from ragbench_lab.archiving import scoped_path, verify_archive
from ragbench_lab.data.preparation import canonical, digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.stage_a import implementation_identity, timestamp
from ragbench_lab.synthesis import checked_artifact


def inventory(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        return json.loads(archive.read("archive.json"))


def verify_delivery(path: Path, raw_archive: Path) -> dict:
    result = verify_archive(path)
    record = inventory(path)
    if record["kind"] != "analysis_delivery" or record["schema_version"] != 1:
        raise DataError("not a supported analysis delivery")
    raw = verify_archive(raw_archive)
    if raw != record["required_raw_archive"]["verification"]:
        raise DataError("delivery raw companion identity differs")
    return {**result, "raw_archive_sha256": raw["archive_sha256"],
            "raw_files": raw["files"], "scope": record["scope"]}


def bundle_delivery(specification: Path, output: Path) -> dict:
    if output.exists() or output.suffix != ".zip":
        raise DataError("delivery requires a fresh .zip output")
    root = Path.cwd()
    spec = json.loads(specification.read_text())
    if spec["version"] != "analysis_delivery_v1" or not spec["exclusions"]:
        raise DataError("unsupported delivery protocol or missing exclusions")
    raw_path = scoped_path(root, spec["raw_archive"])
    raw_before = raw_path.stat()
    print("verifying unchanged raw archive and every member", flush=True)
    raw = verify_archive(raw_path)
    raw_proof = scoped_path(root, spec["raw_proof"])
    if raw != json.loads(raw_proof.read_text()):
        raise DataError("raw archive differs from original verification proof")
    raw_inventory = inventory(raw_path)
    files = {str(specification.resolve().relative_to(root)), spec["raw_proof"]}
    artifacts, pins = {}, {}
    for entry in spec["artifacts"]:
        directory = scoped_path(root, entry["directory"])
        proof = scoped_path(root, entry["proof"])
        role = entry["role"]
        if role in artifacts:
            raise DataError("duplicate delivery artifact role")
        artifacts[role] = checked_artifact(directory, proof, entry["kind"],
                                            entry["identity_key"], entry["manifest"])
        files.add(entry["proof"])
        pins[entry["proof"]] = file_sha256(proof)
        for child in directory.rglob("*"):
            name = str(child.relative_to(root))
            scoped_path(root, name)
            if child.is_file():
                files.add(name)
                pins[name] = file_sha256(child)
    if set(artifacts) != {"analysis", "figures", "review", "synthesis"}:
        raise DataError("delivery needs all four verified analysis artifact families")
    analysis = artifacts["analysis"]
    if any(a["report_sha256"] != analysis["manifest_sha256"]
           for role, a in artifacts.items() if role != "analysis"):
        raise DataError("delivery artifacts refer to different analyses")
    if analysis["archive_sha256"] != raw["archive_sha256"]:
        raise DataError("analysis belongs to another raw archive")
    for role, binding in analysis["inputs"].items():
        if any(binding[k] != raw_inventory["runs"][role][k]
               for k in ("run_id", "manifest_sha256", "records_sha256")):
            raise DataError("analysis run binding differs from companion archive")
    for name in spec["files"]:
        path = scoped_path(root, name)
        if not path.is_file():
            raise DataError("delivery file scope must select files")
        files.add(name)
    for tree in spec["trees"]:
        directory = scoped_path(root, tree["path"])
        for child in directory.rglob("*"):
            name = str(child.relative_to(root))
            scoped_path(root, name)
            if child.is_file() and child.suffix in tree["suffixes"]:
                files.add(name)
    if spec["raw_archive"] in files or "archive.json" in files:
        raise DataError("raw companion must not be duplicated or inventory replaced")
    # Hash everything before copying; a changed input leaves the failed ZIP for review.
    for name in sorted(files):
        sha = file_sha256(scoped_path(root, name))
        if name in pins and pins[name] != sha:
            raise DataError("verified delivery input changed before copy")
        pins[name] = sha
    provenance = implementation_identity()
    members = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as target, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED,
                                                     compresslevel=6) as archive:
        for name in sorted(files):
            path = scoped_path(root, name)
            sha, size = hashlib.sha256(), 0
            with path.open("rb") as source, archive.open(name, "w", force_zip64=True) as dest:
                while data := source.read(1024*1024):
                    dest.write(data)
                    sha.update(data)
                    size += len(data)
            if sha.hexdigest() != pins[name]:
                raise DataError("delivery input changed while copying")
            members.append({"path": name, "bytes": size, "sha256": sha.hexdigest()})
        record = {"kind": "analysis_delivery", "schema_version": 1, "created_at": timestamp(),
            "scope": "two-part offline analysis replay; not a self-contained model rerun",
            "privacy": "local only pending raw-text/license/path review before sharing",
            "required_raw_archive": {"suggested_path": spec["raw_archive"], "verification": raw},
            "artifacts": {role: a["manifest_sha256"] for role, a in artifacts.items()},
            "protocol_sha256": digest(spec), "provenance": provenance,
            "files": members, "exclusions": spec["exclusions"]}
        record["manifest_sha256"] = digest(record)
        archive.writestr("archive.json", canonical(record))
    raw_after = raw_path.stat()
    if (raw_before.st_size, raw_before.st_mtime_ns) != (raw_after.st_size, raw_after.st_mtime_ns):
        raise DataError("raw companion changed during delivery export")
    print("verifying every analysis delivery member", flush=True)
    return {"output": str(output), **verify_archive(output),
            "raw_archive_sha256": raw["archive_sha256"], "raw_files": raw["files"]}
