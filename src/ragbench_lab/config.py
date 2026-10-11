"""Configuration loading and Phase 0 validation."""

from __future__ import annotations

import hashlib
import json
import math
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when an experiment configuration is invalid."""


@dataclass(frozen=True)
class DatasetConfig:
    names: tuple[str, ...]
    revision: str
    development_questions: int
    evaluation_questions: int
    sampling_seed: int


@dataclass(frozen=True)
class RetrievalConfig:
    recipes: tuple[str, ...]
    candidate_depth: int
    rrf_constant: int
    context_budget_tokens: int


@dataclass(frozen=True)
class ChunkingConfig:
    methods: tuple[str, ...]
    sizes: tuple[int, ...]
    overlap_percent: int
    reference_tokenizer: str
    tokenizer_revision: str
    tokenizer_sha256: str = ""


@dataclass(frozen=True)
class BM25Config:
    k1: float = 1.5
    b: float = 0.75
    preprocessing: str = "unicode_words_casefold_v1"
    idf: str = "log1p_robertson_v1"

    def __post_init__(self) -> None:
        if (type(self.k1) not in (int, float) or not math.isfinite(self.k1) or self.k1 <= 0):
            raise ConfigError("bm25.k1 must be finite and positive")
        if (type(self.b) not in (int, float) or not math.isfinite(self.b) or not 0 <= self.b <= 1):
            raise ConfigError("bm25.b must be between 0 and 1")
        if (self.preprocessing != "unicode_words_casefold_v1"
                or self.idf != "log1p_robertson_v1"):
            raise ConfigError("unsupported BM25 preprocessing or IDF formula")


@dataclass(frozen=True)
class TimingConfig:
    repetitions: int
    sequential: bool
    quality_repetition: int


@dataclass(frozen=True)
class ExperimentConfig:
    schema_version: int
    name: str
    dataset: DatasetConfig
    retrieval: RetrievalConfig
    chunking: ChunkingConfig
    timing: TimingConfig
    bm25: BM25Config = BM25Config()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def sha256(self) -> str:
        canonical = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _table(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ConfigError(f"missing or invalid [{name}] table")
    return value


def _tuple(table: dict[str, Any], key: str) -> tuple[Any, ...]:
    value = table.get(key)
    if not isinstance(value, list) or not value:
        raise ConfigError(f"{key} must be a non-empty array")
    if len(value) != len(set(value)):
        raise ConfigError(f"{key} must not contain duplicates")
    return tuple(value)


def _positive_int(table: dict[str, Any], key: str) -> int:
    value = table.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ConfigError(f"{key} must be a positive integer")
    return value


def load_config(path: str | Path) -> ExperimentConfig:
    config_path = Path(path)
    try:
        with config_path.open("rb") as stream:
            raw = tomllib.load(stream)
    except FileNotFoundError as error:
        raise ConfigError(f"configuration does not exist: {config_path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"invalid TOML in {config_path}: {error}") from error

    datasets = _table(raw, "dataset")
    retrieval = _table(raw, "retrieval")
    chunking = _table(raw, "chunking")
    timing = _table(raw, "timing")
    bm25_raw = raw.get("bm25", {})
    if not isinstance(bm25_raw, dict) or set(bm25_raw) - {"k1", "b", "preprocessing", "idf"}:
        raise ConfigError("[bm25] must contain only supported settings")

    config = ExperimentConfig(
        schema_version=_positive_int(raw, "schema_version"),
        name=str(raw.get("name", "")).strip(),
        dataset=DatasetConfig(
            names=tuple(str(item) for item in _tuple(datasets, "names")),
            revision=str(datasets.get("revision", "")).strip(),
            development_questions=_positive_int(datasets, "development_questions"),
            evaluation_questions=_positive_int(datasets, "evaluation_questions"),
            sampling_seed=_positive_int(datasets, "sampling_seed"),
        ),
        retrieval=RetrievalConfig(
            recipes=tuple(str(item) for item in _tuple(retrieval, "recipes")),
            candidate_depth=_positive_int(retrieval, "candidate_depth"),
            rrf_constant=_positive_int(retrieval, "rrf_constant"),
            context_budget_tokens=_positive_int(retrieval, "context_budget_tokens"),
        ),
        chunking=ChunkingConfig(
            methods=tuple(str(item) for item in _tuple(chunking, "methods")),
            sizes=tuple(int(item) for item in _tuple(chunking, "sizes")),
            overlap_percent=chunking.get("overlap_percent"),
            reference_tokenizer=str(chunking.get("reference_tokenizer", "")).strip(),
            tokenizer_revision=str(chunking.get("tokenizer_revision", "")).strip(),
            tokenizer_sha256=str(chunking.get("tokenizer_sha256", "")).strip(),
        ),
        timing=TimingConfig(
            repetitions=_positive_int(timing, "repetitions"),
            sequential=timing.get("sequential"),
            quality_repetition=_positive_int(timing, "quality_repetition"),
        ),
        bm25=BM25Config(**bm25_raw),
    )
    _validate(config)
    return config


def _validate(config: ExperimentConfig) -> None:
    if config.schema_version != 1:
        raise ConfigError("schema_version must be 1")
    if not config.name:
        raise ConfigError("name must not be empty")
    if not config.dataset.revision:
        raise ConfigError("dataset.revision must be pinned")

    supported_datasets = {"squad", "hotpot_qa"}
    unknown_datasets = set(config.dataset.names) - supported_datasets
    if unknown_datasets:
        raise ConfigError(f"unsupported datasets: {', '.join(sorted(unknown_datasets))}")

    expected_recipes = {"bm25", "dense_bge", "dense_e5", "hybrid_bge", "hybrid_e5"}
    if set(config.retrieval.recipes) != expected_recipes:
        raise ConfigError("retrieval.recipes must contain the five Stage A recipes")
    if config.retrieval.candidate_depth != 50:
        raise ConfigError("retrieval.candidate_depth must be 50 for the core study")
    if config.retrieval.rrf_constant != 60:
        raise ConfigError("retrieval.rrf_constant must be 60 for the core study")
    if config.retrieval.context_budget_tokens != 1024:
        raise ConfigError("retrieval.context_budget_tokens must be 1024 for the core study")

    if set(config.chunking.methods) != {"fixed_token", "sentence_aware"}:
        raise ConfigError("chunking.methods must contain fixed_token and sentence_aware")
    if set(config.chunking.sizes) != {64, 128, 256}:
        raise ConfigError("chunking.sizes must contain 64, 128, and 256")
    if config.chunking.overlap_percent != 0:
        raise ConfigError("chunking.overlap_percent must be 0 for the core study")
    if not config.chunking.reference_tokenizer or not config.chunking.tokenizer_revision:
        raise ConfigError("reference tokenizer name and revision must be pinned")

    if config.timing.repetitions != 3 or config.timing.quality_repetition != 1:
        raise ConfigError("timing requires 3 repetitions and quality_repetition = 1")
    if config.timing.sequential is not True:
        raise ConfigError("timing.sequential must be true")

    stage_a_count = len(config.retrieval.recipes) * len(config.chunking.methods) * len(
        config.chunking.sizes
    )
    if stage_a_count != 30:
        raise ConfigError(f"Stage A must enumerate 30 conditions, got {stage_a_count}")
