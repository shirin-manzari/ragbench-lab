"""Exclusive-writer, hash-chained JSONL records with strict append-only recovery."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from ragbench_lab.data.preparation import canonical, digest
from ragbench_lab.data.records import DataError
from ragbench_lab.pipeline import write_new_json


def request_key(condition_id: str, question_id: str, repetition: int) -> str:
    return digest([condition_id, question_id, repetition])


def verified_manifest(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"))
    identity = result.pop("manifest_sha256")
    if digest(result) != identity:
        raise DataError("run manifest identity mismatch")
    result["manifest_sha256"] = identity
    return result


def read_records(directory: Path, manifest: dict) -> list[dict]:
    path = directory / "records.jsonl"
    if not path.exists():
        raise DataError("run records are missing")
    rows = []
    previous = manifest["manifest_sha256"]
    attempts: dict[str, int] = {}
    successes = set()
    with path.open("rb") as stream:
        for line in stream:
            if not line.endswith(b"\n"):
                raise DataError("incomplete JSONL tail; preserve run and repair explicitly")
            try:
                row = json.loads(line)
                identity = row.pop("record_sha256")
                if digest(row) != identity or row["previous_sha256"] != previous:
                    raise DataError("run record chain mismatch")
                row["record_sha256"] = identity
                if row["run_manifest_sha256"] != manifest["manifest_sha256"]:
                    raise DataError("mixed run identities")
                if row["sequence"] != len(rows) + 1:
                    raise DataError("invalid request sequence/status")
                if row.get("kind") == "event":
                    previous = identity
                    rows.append(row)
                    continue
                if row["status"] not in {"success", "failed"}:
                    raise DataError("invalid request status")
                key = row["request_key"]
                if key != request_key(row["condition_id"], row["question_id"], row["repetition"]):
                    raise DataError("invalid request identity")
                if key in successes or row["attempt"] != attempts.get(key, 0) + 1:
                    raise DataError("duplicate success or invalid attempt sequence")
                attempts[key] = row["attempt"]
                if row["status"] == "success":
                    successes.add(key)
                previous = identity
                rows.append(row)
            except (ValueError, KeyError, TypeError) as error:
                raise DataError(f"invalid persisted request record: {error}") from error
    return rows


class RunStore:
    def __init__(self, directory: Path, identity: dict, resume: bool = False):
        self.directory = directory
        if directory.exists() != resume:
            raise DataError("new run requires a new directory; existing runs require --resume")
        if not resume:
            directory.mkdir(parents=True)
        self.lock = directory / ".writer.lock"
        try:
            self.lock_fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as error:
            raise DataError(
                "run writer lock exists; verify no writer before explicit recovery") from error
        try:
            os.write(self.lock_fd, str(os.getpid()).encode())
            os.fsync(self.lock_fd)
            if resume:
                self.manifest = verified_manifest(directory / "manifest.json")
                if self.manifest["identity"] != json.loads(canonical(identity)):
                    raise DataError("resume identity mismatch; start a separate run")
            else:
                self.manifest = {"schema_version": 1, "identity": identity,
                                 "run_id": str(uuid4()),
                                 "created_at": datetime.now(UTC).isoformat()}
                self.manifest["manifest_sha256"] = digest(self.manifest)
                write_new_json(directory / "manifest.json", self.manifest)
                (directory / "records.jsonl").touch(exist_ok=False)
            self.rows = read_records(directory, self.manifest)
        except BaseException:
            self.close()
            raise

    def append(self, row: dict) -> dict:
        if row.get("kind") != "event":
            key = row["request_key"]
            if (row["status"] not in {"success", "failed"}
                    or key != request_key(row["condition_id"], row["question_id"],
                                          row["repetition"])):
                raise DataError("invalid request status or identity")
            existing = [r for r in self.rows if r.get("request_key") == key]
            if any(r["status"] == "success" for r in existing):
                raise DataError("cannot append after a successful request")
            if row["attempt"] != len(existing) + 1:
                raise DataError("attempt numbers must be consecutive")
        record = {**row, "sequence": len(self.rows) + 1,
                  "run_manifest_sha256": self.manifest["manifest_sha256"],
                  "previous_sha256": self.rows[-1]["record_sha256"] if self.rows
                  else self.manifest["manifest_sha256"]}
        record["record_sha256"] = digest(record)
        with (self.directory / "records.jsonl").open("ab") as stream:
            stream.write(canonical(record) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.rows.append(record)
        return record

    def close(self) -> None:
        os.close(self.lock_fd)
        self.lock.unlink()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
