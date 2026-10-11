"""Exact normalized inner-product search with stable boundary ties and frozen persistence."""

from __future__ import annotations

from pathlib import Path

import faiss
import numpy as np

from ragbench_lab.chunking import Chunk
from ragbench_lab.data.records import DataError
from ragbench_lab.native import require_native_environment
from ragbench_lab.retrieval import RankedChunk


def normalized_matrix(vectors, rows: int, dimension: int | None = None):
    matrix = np.ascontiguousarray(vectors, dtype="float32")
    if (matrix.ndim != 2 or matrix.shape[0] != rows or not matrix.shape[1]
            or (dimension is not None and matrix.shape[1] != dimension)
            or not np.isfinite(matrix).all()
            or not np.allclose(np.linalg.norm(matrix, axis=1), 1, atol=1e-5, rtol=0)):
        raise DataError("dense vectors must be finite normalized float32 rows of expected shape")
    return matrix


class DenseIndex:
    def __init__(self, chunks: list[Chunk], vectors, threads: int = 4):
        require_native_environment()
        if not chunks or len({c.chunk_id for c in chunks}) != len(chunks):
            raise DataError("dense corpus must be nonempty with unique chunk IDs")
        if chunks != sorted(chunks, key=lambda c: c.chunk_id):
            raise DataError("dense chunk rows must be sorted by chunk ID")
        faiss.omp_set_num_threads(threads)
        self.chunks = chunks
        matrix = normalized_matrix(vectors, len(chunks))
        self.index = faiss.IndexFlatIP(matrix.shape[1])
        self.index.add(matrix)

    def save(self, path: Path) -> None:
        if path.exists():
            raise DataError("dense index output already exists")
        faiss.write_index(self.index, str(path))

    @classmethod
    def load(cls, path: Path, chunks: list[Chunk], dimension: int, threads: int = 4):
        require_native_environment()
        faiss.omp_set_num_threads(threads)
        index = faiss.read_index(str(path))
        if (type(index) is not faiss.IndexFlatIP or index.ntotal != len(chunks)
                or index.d != dimension or index.metric_type != faiss.METRIC_INNER_PRODUCT):
            raise DataError("dense index type, rows, or dimension mismatch")
        if not chunks or len({c.chunk_id for c in chunks}) != len(chunks):
            raise DataError("invalid dense chunk IDs")
        if chunks != sorted(chunks, key=lambda c: c.chunk_id):
            raise DataError("dense chunk row order mismatch")
        normalized_matrix(index.reconstruct_n(0, index.ntotal), len(chunks), dimension)
        instance = cls.__new__(cls)
        instance.chunks, instance.index = chunks, index
        return instance

    def search(self, query_vector, depth: int = 50) -> list[RankedChunk]:
        if type(depth) is not int or depth <= 0:
            raise DataError("retrieval depth must be positive")
        query = normalized_matrix(query_vector, 1, self.index.d)
        count = min(depth, len(self.chunks))
        scores, rows = self.index.search(query, min(count + 1, len(self.chunks)))
        if len(rows[0]) > count and scores[0][count] == scores[0][count - 1]:
            # Include every cutoff tie before selecting by ID, not FAISS's arbitrary row tie.
            cutoff = float(np.nextafter(scores[0][count - 1], np.float32(-np.inf)))
            _, distances, labels = self.index.range_search(query, cutoff)
            hits = zip(labels.tolist(), distances.tolist())
        else:
            hits = zip(rows[0].tolist(), scores[0].tolist())
        ordered = sorted(hits, key=lambda hit: (-hit[1], self.chunks[hit[0]].chunk_id))[:count]
        return [RankedChunk(self.chunks[row], float(score)) for row, score in ordered]
