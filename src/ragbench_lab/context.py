"""Rank-ordered context packing with exact source provenance after truncation."""

from __future__ import annotations

from dataclasses import dataclass

from ragbench_lab.chunking import TokenCounter
from ragbench_lab.data.records import DataError
from ragbench_lab.retrieval import RankedChunk


@dataclass(frozen=True)
class IncludedEvidence:
    chunk_id: str
    document_id: str
    source_start: int
    source_end: int
    context_start: int
    context_end: int
    text: str
    truncated: bool


@dataclass(frozen=True)
class PackedContext:
    text: str
    reference_tokens: int
    budget: int
    underfilled_tokens: int
    evidence: tuple[IncludedEvidence, ...]


def pack_context(ranked: list[RankedChunk], tokenizer: TokenCounter,
                 budget: int = 1024) -> PackedContext:
    if type(budget) is not int or budget <= 0:
        raise DataError("context budget must be positive")
    context = ""
    included = []
    seen = set()
    for item in ranked:
        chunk = item.chunk
        if chunk.chunk_id in seen:
            continue
        seen.add(chunk.chunk_id)
        header = ("\n\n" if context else "") + f"[{chunk.chunk_id}]\n"
        candidate = context + header + chunk.text
        end = len(chunk.text)
        if tokenizer.count(candidate) > budget:
            # Token counts can change at concatenation and WordPiece boundaries.
            # Check whole candidate strings; do not assume additive token counts.
            ends = sorted({b for _, b in tokenizer.offsets(chunk.text) if b > 0}, reverse=True)
            end = next((cut for cut in ends if tokenizer.count(
                context + header + chunk.text[:cut]) <= budget), 0)
        if not end:
            break  # cannot fit text from the next ranked chunk
        prefix = chunk.text[:end]
        context_start = len(context + header)
        context += header + prefix
        included.append(IncludedEvidence(chunk.chunk_id, chunk.document_id, chunk.start,
                                         chunk.start + end, context_start, len(context), prefix,
                                         end < len(chunk.text)))
        if end < len(chunk.text):
            break  # only the final included chunk can be partial
    count = tokenizer.count(context)
    if count > budget:
        raise DataError("packed context exceeds its reference-token budget")
    return PackedContext(context, count, budget, budget - count, tuple(included))
