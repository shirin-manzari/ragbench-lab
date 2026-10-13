"""Pinned six-layer cross-encoder with explicit pair limits and stable candidate identity."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path

from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256, validate_lengths
from ragbench_lab.native import require_native_environment
from ragbench_lab.retrieval import RankedChunk

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L6-v2"


def loading_report_json(loading: dict) -> dict:
    """Transformers 5 returns sets; persist their exact members in stable order."""
    return {key: sorted(value) if isinstance(value, set) else value
            for key, value in loading.items()}


@dataclass(frozen=True)
class RerankerSettings:
    revision: str
    files: dict[str, str]
    batch_size: int = 16
    threads: int = 4
    seed: int = 20261011

    def __post_init__(self):
        if (not re.fullmatch(r"[0-9a-f]{40}", self.revision)
                or not {"model.safetensors", "config.json", "tokenizer_config.json",
                        "tokenizer.json"} <= self.files.keys()
                or any(Path(name).name != name or not re.fullmatch(r"[0-9a-f]{64}", checksum)
                       for name, checksum in self.files.items())):
            raise DataError("pin the reranker revision and every loader input")
        for name in ("batch_size", "threads"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise DataError(f"reranker {name} must be positive")
        if type(self.seed) is not int or not 0 <= self.seed < 2**32:
            raise DataError("reranker seed must be an unsigned 32-bit integer")


def order_candidates(ranked: list[RankedChunk], scores: list[float]) -> list[RankedChunk]:
    if len({hit.chunk.chunk_id for hit in ranked}) != len(ranked):
        raise DataError("reranker initial candidates must be unique")
    if len(scores) != len(ranked) or any(not math.isfinite(score) for score in scores):
        raise DataError("reranker needs one finite score per initial candidate")
    results = [RankedChunk(hit.chunk, score) for hit, score in zip(ranked, scores, strict=True)]
    return sorted(results, key=lambda hit: (-hit.score, hit.chunk.chunk_id))


class LocalReranker:
    def __init__(self, directory: Path, settings: RerankerSettings):
        require_native_environment()
        import torch
        from safetensors import safe_open
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        actual = {p.name for p in directory.iterdir() if p.is_file()
                  and p.suffix in {".json", ".txt", ".bin", ".safetensors", ".model"}}
        if actual != settings.files.keys():
            raise DataError("reranker directory has missing or unpinned loader inputs")
        if any(file_sha256(directory / name) != checksum
               for name, checksum in settings.files.items()):
            raise DataError("reranker file identity mismatch")
        torch.manual_seed(settings.seed)
        torch.set_num_threads(settings.threads)
        torch.use_deterministic_algorithms(True)
        self.settings = settings
        self.tokenizer = AutoTokenizer.from_pretrained(directory, local_files_only=True,
                                                       trust_remote_code=False)
        self.tokenizer.backend_tokenizer.no_truncation()
        self.tokenizer.backend_tokenizer.no_padding()
        self.model, loading = AutoModelForSequenceClassification.from_pretrained(
            directory, local_files_only=True, trust_remote_code=False, use_safetensors=True,
            attn_implementation="eager", output_loading_info=True)
        if (loading["missing_keys"] or loading["mismatched_keys"] or loading["error_msgs"]
                or set(loading["unexpected_keys"]) - {"bert.embeddings.position_ids"}):
            raise DataError(f"reranker weight loading mismatch: {loading}")
        if loading["unexpected_keys"]:
            path = directory / "model.safetensors"
            with safe_open(path, framework="pt", device="cpu") as weights:
                if not torch.equal(weights.get_tensor("bert.embeddings.position_ids"),
                                   self.model.bert.embeddings.position_ids):
                    raise DataError("reranker position buffer differs from pinned weights")
        self.maximum = min(512, self.model.config.max_position_embeddings,
                           self.tokenizer.model_max_length)
        if (self.maximum != 512 or self.model.config.num_labels != 1
                or self.model.config.model_type != "bert"
                or self.model.config.num_hidden_layers != 6
                or self.model.config.hidden_size != 384):
            raise DataError("unsupported reranker input limit or classification head")
        self.model.to(device="cpu", dtype=torch.float32).eval()
        self.last_lengths = []
        self.identity = {"name": MODEL_NAME, "settings": asdict(settings), "maximum_tokens": 512,
                         "dtype": "float32", "device": "cpu",
                         "loading_report": loading_report_json(loading),
                         "versions": {name: version(name) for name in ("torch", "transformers")}}

    def rerank(self, query: str, ranked: list[RankedChunk]) -> list[RankedChunk]:
        if not ranked or not isinstance(query, str) or not query.strip():
            raise DataError("reranking requires a query and nonempty initial candidates")
        if len({hit.chunk.chunk_id for hit in ranked}) != len(ranked):
            raise DataError("reranker initial candidates must be unique")
        tokens = self.tokenizer([query] * len(ranked), [hit.chunk.text for hit in ranked],
                                truncation=False, padding=False, add_special_tokens=True)
        self.last_lengths = [len(ids) for ids in tokens["input_ids"]]
        validate_lengths(self.last_lengths, self.maximum, "reranking pair")
        import torch

        scores = []
        for start in range(0, len(ranked), self.settings.batch_size):
            batch = {key: values[start:start + self.settings.batch_size]
                     for key, values in tokens.items()}
            batch = self.tokenizer.pad(batch, padding=True, return_tensors="pt")
            with torch.inference_mode():
                logits = self.model(**batch).logits
            scores.extend(logits[:, 0].cpu().tolist())
        return order_candidates(ranked, scores)
