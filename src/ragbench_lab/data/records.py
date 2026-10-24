from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


class DataError(ValueError):
    """Invalid source data, evidence mapping, or preparation settings."""


@dataclass(frozen=True)
class SourceSpan:
    source_id: str
    start: int
    end: int
    kind: Literal["paragraph", "sentence"]

    def __post_init__(self) -> None:
        if not self.source_id or self.kind not in {"paragraph", "sentence"}:
            raise DataError("source span needs an ID and supported kind")
        if type(self.start) is not int or type(self.end) is not int:
            raise DataError("offsets must be integers")
        if not 0 <= self.start <= self.end:
            raise DataError("source offsets must satisfy 0 <= start <= end")


@dataclass(frozen=True)
class Document:
    document_id: str
    dataset: str
    title: str
    text: str
    source_spans: tuple[SourceSpan, ...]

    def __post_init__(self) -> None:
        if not self.document_id or self.dataset not in {"squad", "hotpot_qa"}:
            raise DataError("document needs an ID and supported dataset")
        previous_end = 0
        identifiers = set()
        for span in self.source_spans:
            if span.end > len(self.text) or span.start < previous_end:
                raise DataError("source spans must be ordered, non-overlapping, and in bounds")
            if span.source_id in identifiers:
                raise DataError("duplicate source span ID")
            identifiers.add(span.source_id)
            previous_end = span.end


@dataclass(frozen=True)
class EvidenceSpan:
    document_id: str
    source_id: str
    start: int
    end: int
    text: str
    kind: Literal["answer", "paragraph", "sentence"]

    def __post_init__(self) -> None:
        if not self.document_id or not self.source_id:
            raise DataError("evidence needs document and source IDs")
        if self.kind not in {"answer", "paragraph", "sentence"}:
            raise DataError("unsupported evidence kind")
        if type(self.start) is not int or type(self.end) is not int:
            raise DataError("evidence offsets must be integers")
        if not 0 <= self.start < self.end or self.end - self.start != len(self.text):
            raise DataError("evidence offsets must match non-empty text length")


@dataclass(frozen=True)
class Question:
    question_id: str
    dataset: str
    text: str
    answers: tuple[str, ...]
    evidence: tuple[EvidenceSpan, ...]
    diagnostics: tuple[EvidenceSpan, ...] = ()

    def __post_init__(self) -> None:
        if not self.question_id or not self.text or not self.answers or not self.evidence:
            raise DataError("question needs ID, text, answers, and evidence")
        if self.dataset not in {"squad", "hotpot_qa"}:
            raise DataError("unsupported question dataset")


@dataclass(frozen=True)
class Exclusion:
    question_id: str
    reason: str


@dataclass(frozen=True)
class DatasetBundle:
    documents: tuple[Document, ...]
    questions: tuple[Question, ...]
    exclusions: tuple[Exclusion, ...] = ()


@dataclass(frozen=True)
class Split:
    development_ids: tuple[str, ...]
    evaluation_ids: tuple[str, ...]
    seed: int
    overlapping_document_ids: tuple[str, ...]
    overlapping_titles: tuple[str, ...]

    def __post_init__(self) -> None:
        combined = self.development_ids + self.evaluation_ids
        if len(combined) != len(set(combined)):
            raise DataError("split question IDs must be unique and disjoint")
