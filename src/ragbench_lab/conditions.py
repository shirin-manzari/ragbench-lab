from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product

from ragbench_lab.config import ExperimentConfig, _validate
from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError


@dataclass(frozen=True)
class Condition:
    dataset: str
    recipe: str
    method: str
    size: int
    overlap_percent: int = 0
    reranking: bool = False

    @property
    def condition_id(self) -> str:
        return digest(asdict(self))

    def record(self) -> dict:
        return {**asdict(self), "condition_id": self.condition_id}


def stage_a_conditions(config: ExperimentConfig) -> list[Condition]:
    _validate(config)
    conditions = [Condition(*values) for values in product(
        sorted(config.dataset.names), sorted(config.retrieval.recipes),
        sorted(config.chunking.methods), sorted(config.chunking.sizes))]
    if len(conditions) != 30 * len(config.dataset.names):
        raise DataError("Stage A must contain 30 conditions per dataset")
    if len({c.condition_id for c in conditions}) != len(conditions):
        raise DataError("duplicate Stage A conditions")
    return conditions


def block_order(conditions: list[Condition], seed: int, repetition: int) -> list[Condition]:
    return sorted(conditions, key=lambda c: digest([seed, repetition, c.condition_id]))
