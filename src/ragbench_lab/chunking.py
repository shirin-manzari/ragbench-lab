from __future__ import annotations

import re
from bisect import bisect_left
from dataclasses import dataclass
from typing import Protocol

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError, Document


class TokenCounter(Protocol):
    def offsets(self, text: str) -> list[tuple[int, int]]: ...
    def count(self, text: str) -> int: ...


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    start: int
    end: int
    text: str
    reference_tokens: int
    method: str
    target_size: int


@dataclass(frozen=True)
class ChunkedDocument:
    chunks: tuple[Chunk, ...]
    fallback_sentences: int = 0


def fixed_ranges(text: str, tokenizer: TokenCounter, size: int,
                 start: int = 0, end: int | None = None) -> list[tuple[int, int]]:
    """Preserve whitespace/source characters; re-tokenize standalone slices.

    WordPiece fragments can tokenize differently at a new slice boundary. Check
    actual slice lengths and shrink the candidate rather than assuming token IDs
    from the full document remain valid.
    """
    if type(size) is not int or size <= 0:
        raise DataError("chunk size must be positive")
    end = len(text) if end is None else end
    ranges = []
    cursor = start
    starts = [start + a for a, _ in tokenizer.offsets(text[start:end])]
    while cursor < end:
        first = bisect_left(starts, cursor)
        cut = starts[first + size] if first + size < len(starts) else end
        if cut <= cursor:
            raise DataError("token offsets do not permit a progressing source split")
        while tokenizer.count(text[cursor:cut]) > size:
            earlier = [a for a in starts[first:first + size] if cursor < a < cut]
            if not earlier:
                raise DataError("cannot split this source span within the token limit")
            cut = earlier[-1]
        ranges.append((cursor, cut))
        cursor = cut
    return ranges


def sentence_ranges(document: Document) -> list[tuple[int, int]]:
    if document.source_spans and all(s.kind == "sentence" for s in document.source_spans):
        # HotpotQA provides source sentence boundaries; no labels are involved.
        return [(s.start, s.end) for s in document.source_spans if s.end > s.start]
    # A deterministic punctuation/paragraph heuristic, not a learned sentence model.
    boundary = re.compile(r'''[.!?]["'”’)]*(?:\s+|$)|\n\s*\n''')
    cuts = [0] + [m.end() for m in boundary.finditer(document.text)] + [len(document.text)]
    cuts = sorted(set(cuts))
    return list(zip(cuts[:-1], cuts[1:]))


def chunk_document(document: Document, tokenizer: TokenCounter, method: str,
                   size: int) -> ChunkedDocument:
    if type(size) is not int or size <= 0:
        raise DataError("chunk size must be positive")
    fallback = 0
    if method == "fixed_token":
        ranges = fixed_ranges(document.text, tokenizer, size)
    elif method == "sentence_aware":
        ranges = []
        pending: tuple[int, int] | None = None
        for start, end in sentence_ranges(document):
            if tokenizer.count(document.text[start:end]) > size:
                if pending is not None:
                    ranges.append(pending)
                    pending = None
                ranges.extend(fixed_ranges(document.text, tokenizer, size, start, end))
                fallback += 1
            elif pending is None:
                pending = (start, end)
            elif tokenizer.count(document.text[pending[0]:end]) <= size:
                pending = (pending[0], end)
            else:
                ranges.append(pending)
                pending = (start, end)
        if pending is not None:
            ranges.append(pending)
    else:
        raise DataError(f"unsupported chunking method: {method}")
    chunks = []
    for start, end in ranges:
        text = document.text[start:end]
        tokens = tokenizer.count(text)
        if tokens > size:
            raise DataError("chunk exceeds verified reference-token target")
        if not tokens:
            continue  # blank/control-only source regions cannot be searched
        identifier = digest([document.document_id, method, size, start, end])
        chunks.append(Chunk(identifier, document.document_id, start, end, text, tokens,
                            method, size))
    return ChunkedDocument(tuple(chunks), fallback)
