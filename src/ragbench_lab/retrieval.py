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


def reciprocal_rank_fusion(rankings: list[list[RankedChunk]], constant: int = 60,
                           depth: int = 50) -> list[RankedChunk]:
    if type(constant) is not int or constant <= 0 or type(depth) is not int or depth <= 0:
        raise DataError("RRF constant and depth must be positive integers")
    scores: dict[str, float] = defaultdict(float)
    chunks: dict[str, Chunk] = {}
    for ranking in rankings:
        seen = set()
        for rank, hit in enumerate(ranking, 1):
            key = hit.chunk.chunk_id
            if key in chunks and chunks[key] != hit.chunk:
                raise DataError("conflicting chunk records in RRF inputs")
            chunks[key] = hit.chunk
            if key not in seen:
                scores[key] += 1 / (constant + rank)
                seen.add(key)
    keys = sorted(scores, key=lambda key: (-scores[key], key))[:depth]
    return [RankedChunk(chunks[key], scores[key]) for key in keys]


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

    @classmethod
    def from_payload(cls, chunks: list[Chunk], settings: BM25Config, payload: dict):
        instance = cls.__new__(cls)
        instance.chunks = sorted(chunks, key=lambda c: c.chunk_id)
        if chunks != instance.chunks or len({c.chunk_id for c in chunks}) != len(chunks):
            raise DataError("invalid BM25 chunk row order or duplicate IDs")
        lengths = payload["lengths"]
        if (len(lengths) != len(chunks) or any(type(n) is not int or n < 0 for n in lengths)
                or payload["average_length"] != (sum(lengths) / len(chunks) if chunks else 0)):
            raise DataError("invalid BM25 persisted lengths")
        totals = [0] * len(chunks)
        for term, postings in payload["postings"].items():
            if not term or not postings:
                raise DataError("invalid BM25 persisted term")
            previous = -1
            for row, frequency in postings:
                if (type(row) is not int or not previous < row < len(chunks)
                        or type(frequency) is not int or frequency <= 0):
                    raise DataError("invalid BM25 persisted postings")
                totals[row] += frequency
                previous = row
        if totals != lengths:
            raise DataError("BM25 persisted frequencies disagree with lengths")
        instance.settings, instance.lengths = settings, lengths
        instance.average_length, instance.postings = payload["average_length"], payload["postings"]
        return instance

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
