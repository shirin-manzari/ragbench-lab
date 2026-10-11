"""Pinned reference-tokenizer adapter; no model weights or implicit truncation."""

from __future__ import annotations

import hashlib
import re
from importlib.metadata import version
from pathlib import Path

from ragbench_lab.config import ChunkingConfig
from ragbench_lab.data.records import DataError


class ReferenceTokenizer:
    def __init__(self, path: Path, config: ChunkingConfig):
        from tokenizers import Tokenizer

        if (config.reference_tokenizer != "BAAI/bge-small-en-v1.5"
                or not re.fullmatch(r"[0-9a-f]{40}", config.tokenizer_revision)
                or not re.fullmatch(r"[0-9a-f]{64}", config.tokenizer_sha256)):
            raise DataError("Phase 2 requires the pinned BGE tokenizer revision and file SHA-256")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != config.tokenizer_sha256:
            raise DataError("reference tokenizer SHA-256 mismatch")
        self.backend = Tokenizer.from_file(str(path))
        self.backend.no_truncation()
        self.backend.no_padding()
        self.identity = {"name": config.reference_tokenizer, "revision": config.tokenizer_revision,
                         "sha256": actual, "library_version": version("tokenizers"),
                         "special_tokens": False, "truncation": False}

    def offsets(self, text: str) -> list[tuple[int, int]]:
        return self.backend.encode(text, add_special_tokens=False).offsets

    def count(self, text: str) -> int:
        return len(self.offsets(text))
