from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

from ragbench_lab.dashboard_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]


def prepare(directory: Path = ROOT / "deployment/dashboard") -> dict:
    metadata = json.loads((ROOT / "configs/hosted-dashboard.json").read_text())
    with gzip.open(directory / "snapshot.json.gz", "rb") as stream:
        content = stream.read(metadata["snapshot_bytes"] + 1)
    if len(content) != metadata["snapshot_bytes"]:
        raise ValueError("hosted snapshot size mismatch")
    if hashlib.sha256(content).hexdigest() != metadata["snapshot_sha256"]:
        raise ValueError("hosted snapshot checksum mismatch")
    (directory / "snapshot.json").write_bytes(content)
    del content
    snapshot = load_snapshot(directory)
    if snapshot["manifest_sha256"] != metadata["snapshot_manifest_sha256"]:
        raise ValueError("hosted snapshot identity mismatch")
    print(json.dumps({"snapshot": snapshot["manifest_sha256"], "runs": len(snapshot["runs"])}))
    return snapshot


if __name__ == "__main__":
    prepare(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "deployment/dashboard")
