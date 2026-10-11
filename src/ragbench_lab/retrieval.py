"""Small inverted BM25 index with an explicit positive Robertson IDF variant."""

from __future__ import annotations

import heapq
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass

from ragbench_lab.chunking import Chunk
from ragbench_lab.config import BM25Config
from ragbench_lab.data.records import DataError


def terms(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.casefold(), flags=re.UNICODE)


@dataclass(frozen=True)
class RankedChunk:
    chunk: Chunk
    score: float


class BM25Index:
    def __init__(self, chunks: list[Chunk], settings: BM25Config):
        if len({c.chunk_id for c in chunks}) != len(chunks):
            raise DataError("duplicate chunk IDs")
        self.chunks = sorted(chunks, key=lambda c: c.chunk_id)
        self.settings = settings
        self.lengths = []
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for index, chunk in enumerate(self.chunks):
            counts = Counter(terms(chunk.text))
            self.lengths.append(sum(counts.values()))
            for term, count in counts.items():
                self.postings[term].append((index, count))
        self.average_length = sum(self.lengths) / len(chunks) if chunks else 0.0

    def search(self, query: str, depth: int = 50) -> list[RankedChunk]:
        if type(depth) is not int or depth <= 0:
            raise DataError("retrieval depth must be positive")
        scores: dict[int, float] = defaultdict(float)
        n = len(self.chunks)
        if self.average_length:
            for term, query_frequency in Counter(terms(query)).items():
                postings = self.postings.get(term, [])
                idf = math.log1p((n - len(postings) + 0.5) / (len(postings) + 0.5))
                for index, frequency in postings:
                    norm = self.settings.k1 * (1 - self.settings.b + self.settings.b
                                              * self.lengths[index] / self.average_length)
                    scores[index] += query_frequency * idf * frequency * (self.settings.k1 + 1) / (
                        frequency + norm)
        # Include deterministic zero-score results when fewer than depth chunks match.
        ranked = heapq.nsmallest(min(depth, n), range(n), key=lambda i: (
            -scores.get(i, 0.0), self.chunks[i].chunk_id,
        ))
        return [RankedChunk(self.chunks[i], scores.get(i, 0.0)) for i in ranked]
