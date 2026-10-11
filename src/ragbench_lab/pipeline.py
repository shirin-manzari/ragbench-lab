"""Offline indexing and uncached development retrieval diagnostics."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from ragbench_lab.chunking import Chunk, chunk_document
from ragbench_lab.config import ExperimentConfig
from ragbench_lab.context import pack_context
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError, DatasetBundle, Document
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.retrieval import BM25Index, reciprocal_rank_fusion
from ragbench_lab.tokenization import ReferenceTokenizer


def profile(documents: tuple[Document, ...], tokenizer: ReferenceTokenizer,
            method: str, size: int) -> tuple[list[Chunk], dict]:
    started = perf_counter()
    chunks = []
    fallback = affected = 0
    counts = []
    for doc in documents:
        result = chunk_document(doc, tokenizer, method, size)
        chunks.extend(result.chunks)
        fallback += result.fallback_sentences
        affected += bool(result.fallback_sentences)
        counts.append(len(result.chunks))
    lengths = [c.reference_tokens for c in chunks]
    return chunks, {
        "chunking_seconds": perf_counter() - started, "document_count": len(documents),
        "chunk_count": len(chunks), "fallback_sentences": fallback,
        "fallback_document_count": affected,
        "fallback_document_percent": 100 * affected / len(documents) if documents else 0.0,
        "tokens_min": min(lengths, default=0), "tokens_max": max(lengths, default=0),
        "tokens_mean": statistics.mean(lengths) if lengths else 0.0,
        "tokens_median": statistics.median(lengths) if lengths else 0.0,
        "token_length_histogram": {str(n): count for n, count in sorted(Counter(lengths).items())},
        "split_document_count": sum(count > 1 for count in counts),
        "split_document_percent": 100 * sum(count > 1 for count in counts) / len(documents)
        if documents else 0.0,
        "chunks_per_document": counts,
    }


def _documents(bundle, limit: int | None) -> tuple[Document, ...]:
    if limit is not None and (type(limit) is not int or limit <= 0):
        raise DataError("document limit must be positive")
    # The prefix is independent of queries/evidence labels; marked diagnostic-only.
    return bundle.documents if limit is None else bundle.documents[:limit]


def write_new_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(value) + b"\n")


def chunk_profiles(config: ExperimentConfig, data: Path, tokenizer_path: Path,
                   output: Path, limit: int | None = None) -> dict:
    if output.exists():
        raise DataError("profile output already exists")
    source, bundle = load_prepared(data)
    tokenizer = ReferenceTokenizer(tokenizer_path, config.chunking)
    documents = _documents(bundle, limit)
    results = []
    for method in config.chunking.methods:
        for size in config.chunking.sizes:
            chunks, stats = profile(documents, tokenizer, method, size)
            results.append({"method": method, "size": size, "statistics": stats,
                            "chunks_sha256": digest([asdict(c) for c in chunks])})
    result = {"schema_version": 1, "purpose": "chunk profile diagnostic",
              "source_manifest_sha256": source["manifest_sha256"],
              "config_sha256": config.sha256(), "tokenizer": tokenizer.identity,
              "document_limit": limit, "profiles": results}
    write_new_json(output, result)
    return result


def build_index(config: ExperimentConfig, data: Path, tokenizer_path: Path, method: str,
                size: int, output: Path, limit: int | None = None, recipe: str = "bm25",
                models_root: Path = Path("models")) -> dict:
    offline_started = perf_counter()
    if recipe not in config.retrieval.recipes:
        raise DataError("unsupported retrieval recipe")
    if recipe != "bm25" and config.embedding is None:
        raise DataError("Dense/Hybrid requires pinned [embedding] configuration")
    if method not in config.chunking.methods or size not in config.chunking.sizes:
        raise DataError("index profile must be enabled in configuration")
    if output.exists():
        raise DataError("index output already exists; choose a new directory")
    source, bundle = load_prepared(data)
    if source["dataset"] not in config.dataset.names:
        raise DataError("prepared dataset is not enabled in configuration")
    tokenizer = ReferenceTokenizer(tokenizer_path, config.chunking)
    documents = _documents(bundle, limit)
    chunks, stats = profile(documents, tokenizer, method, size)
    started = perf_counter()
    chunks = sorted(chunks, key=lambda c: c.chunk_id)
    bm25 = None
    if recipe == "bm25" or recipe.startswith("hybrid_"):
        bm25 = BM25Index(chunks, config.bm25)
        stats["bm25_build_seconds"] = perf_counter() - started
    if not chunks:
        raise DataError("cannot index an empty searchable corpus")
    dense = encoder = None
    if recipe != "bm25":
        from ragbench_lab.dense import DenseIndex
        from ragbench_lab.embeddings import LocalEncoder

        started = perf_counter()
        encoder = LocalEncoder(recipe.rsplit("_", 1)[1], models_root, config.embedding)
        stats["model_load_seconds"] = perf_counter() - started
        started = perf_counter()
        vectors = encoder.encode([c.text for c in chunks], "passage")
        stats["corpus_embedding_seconds"] = perf_counter() - started
        stats["embedding_tokens_max"] = max(encoder.last_lengths)
        stats["embedding_overlength_inputs"] = 0
        started = perf_counter()
        dense = DenseIndex(chunks, vectors, config.embedding.threads)
        stats["faiss_build_seconds"] = perf_counter() - started
    rows = [asdict(c) for c in chunks]
    manifest = {
        "schema_version": 1, "recipe": recipe, "dataset": source["dataset"],
        "purpose": "diagnostic-only bounded corpus" if limit else "full prepared corpus",
        "source_manifest_sha256": source["manifest_sha256"],
        "source_corpus_sha256": source["corpus_sha256"], "config_sha256": config.sha256(),
        "tokenizer": tokenizer.identity, "bm25": asdict(config.bm25),
        "sentence_rule": "source_sentences_or_punctuation_paragraph_v1",
        "context_template": "bracketed_full_chunk_id_v1",
        "method": method, "size": size, "document_limit": limit,
        "document_ids_sha256": digest([d.document_id for d in documents]),
        "chunks_sha256": digest(rows), "statistics": stats,
        "persistence": "source chunks; saved BM25 postings and/or exact FAISS vectors",
    }
    started = perf_counter()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    with (output / "chunks.jsonl").open("xb") as stream:
        for row in rows:
            stream.write(canonical(row) + b"\n")
    if bm25 is not None:
        payload = {"lengths": bm25.lengths, "average_length": bm25.average_length,
                   "postings": bm25.postings}
        write_new_json(output / "bm25.json", payload)
        manifest["bm25_postings_sha256"] = digest(payload)
    if dense is not None:
        from importlib.metadata import version

        from ragbench_lab.embeddings import file_sha256

        dense.save(output / "dense.faiss")
        manifest["embedding"] = encoder.identity
        manifest["faiss"] = {"type": "IndexFlatIP", "version": version("faiss-cpu"),
                             "threads": config.embedding.threads,
                             "tie_rule": "descending_score_ascending_chunk_id_boundary_range_v1",
                             "sha256": file_sha256(output / "dense.faiss")}
    stats["persistence_seconds"] = perf_counter() - started
    stats["index_asset_bytes"] = sum(p.stat().st_size for p in output.iterdir())
    stats["offline_build_before_manifest_seconds"] = perf_counter() - offline_started
    manifest["chunks_bytes"] = (output / "chunks.jsonl").stat().st_size
    manifest["manifest_sha256"] = digest(manifest)
    write_new_json(output / "manifest.json", manifest)
    return manifest


@dataclass
class RetrievalSession:
    config: ExperimentConfig
    source: dict
    bundle: DatasetBundle
    tokenizer: ReferenceTokenizer
    manifest: dict
    bm25: BM25Index | None
    dense: Any
    encoder: Any
    offline_load_seconds: float


def load_retriever(config: ExperimentConfig, data: Path, directory: Path, tokenizer_path: Path,
                   recipe: str | None = None, models_root: Path = Path("models"),
                   prepared: tuple[dict, DatasetBundle] | None = None,
                   encoder_override=None) -> RetrievalSession:
    initialization = perf_counter()
    source, bundle = prepared if prepared is not None else load_prepared(data)
    tokenizer = ReferenceTokenizer(tokenizer_path, config.chunking)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    identity = manifest.pop("manifest_sha256")
    if digest(manifest) != identity or manifest["schema_version"] != 1:
        raise DataError("index manifest identity mismatch")
    manifest["manifest_sha256"] = identity
    recipe = recipe or manifest["recipe"]
    if recipe not in config.retrieval.recipes or recipe != manifest["recipe"]:
        raise DataError("requested recipe does not match saved index")
    if (manifest["config_sha256"] != config.sha256()
            or manifest["source_manifest_sha256"] != source["manifest_sha256"]
            or manifest["tokenizer"] != tokenizer.identity
            or manifest["bm25"] != asdict(config.bm25)):
        raise DataError("index is stale or incompatible with config/corpus/tokenizer")
    rows = [json.loads(line) for line in (directory / "chunks.jsonl").read_text(
        encoding="utf-8").splitlines()]
    if digest(rows) != manifest["chunks_sha256"]:
        raise DataError("index chunks identity mismatch")
    chunks = [Chunk(**row) for row in rows]
    documents = _documents(bundle, manifest["document_limit"])
    document_ids = {d.document_id for d in documents}
    if (manifest["source_corpus_sha256"] != source["corpus_sha256"]
            or manifest["document_ids_sha256"] != digest([d.document_id for d in documents])
            or len(chunks) != manifest["statistics"]["chunk_count"]
            or any(c.document_id not in document_ids for c in chunks)):
        raise DataError("index corpus membership mismatch")
    docs = {d.document_id: d for d in bundle.documents}
    for chunk in chunks:
        doc = docs.get(chunk.document_id)
        if (doc is None or not 0 <= chunk.start < chunk.end <= len(doc.text)
                or chunk.text != doc.text[chunk.start:chunk.end]
                or chunk.reference_tokens != tokenizer.count(chunk.text)
                or not 0 < chunk.reference_tokens <= manifest["size"]
                or chunk.method != manifest["method"] or chunk.target_size != manifest["size"]
                or chunk.chunk_id != digest([chunk.document_id, chunk.method,
                                            chunk.target_size, chunk.start, chunk.end])):
            raise DataError("invalid indexed chunk source mapping or token length")
    bm25 = dense = encoder = None
    if recipe == "bm25" or recipe.startswith("hybrid_"):
        if "bm25_postings_sha256" in manifest:
            payload = json.loads((directory / "bm25.json").read_text(encoding="utf-8"))
            if digest(payload) != manifest["bm25_postings_sha256"]:
                raise DataError("BM25 postings identity mismatch")
            bm25 = BM25Index.from_payload(chunks, config.bm25, payload)
        else:
            bm25 = BM25Index(chunks, config.bm25)  # Phase 2 artifact compatibility.
    if recipe != "bm25":
        from importlib.metadata import version

        from ragbench_lab.dense import DenseIndex
        from ragbench_lab.embeddings import LocalEncoder, file_sha256

        if config.embedding is None:
            raise DataError("Dense/Hybrid requires [embedding] configuration")
        encoder = encoder_override or LocalEncoder(recipe.rsplit("_", 1)[1], models_root,
                                                   config.embedding)
        if (manifest["embedding"] != encoder.identity
                or manifest["faiss"]["version"] != version("faiss-cpu")
                or manifest["faiss"]["threads"] != config.embedding.threads
                or manifest["faiss"]["type"] != "IndexFlatIP"
                or manifest["faiss"]["sha256"] != file_sha256(directory / "dense.faiss")):
            raise DataError("dense index/model identity mismatch")
        dense = DenseIndex.load(directory / "dense.faiss", chunks, 384, config.embedding.threads)
    return RetrievalSession(config, source, bundle, tokenizer, manifest, bm25, dense, encoder,
                            perf_counter() - initialization)


def retrieve_query(session: RetrievalSession, question_id: str,
                   allowed_ids: list[str] | None = None) -> dict:
    config, source, manifest = session.config, session.source, session.manifest
    permitted = source["split"]["development_ids"] if allowed_ids is None else allowed_ids
    if question_id not in permitted:
        raise DataError("question is not authorized for this retrieval split")
    question = next(q for q in session.bundle.questions if q.question_id == question_id)
    tokenizer, bm25 = session.tokenizer, session.bm25
    dense, encoder = session.dense, session.encoder
    recipe, identity = manifest["recipe"], manifest["manifest_sha256"]
    offline_load_seconds = session.offline_load_seconds
    online = perf_counter()
    timings = {"query_embedding": 0.0, "bm25_search": 0.0, "dense_search": 0.0, "fusion": 0.0}
    constituents = {}
    if encoder is not None:
        started = perf_counter()
        query_vector = encoder.encode([question.text], "query")
        timings["query_embedding"] = perf_counter() - started
    if bm25 is not None:
        started = perf_counter()
        constituents["bm25"] = bm25.search(question.text, config.retrieval.candidate_depth)
        timings["bm25_search"] = perf_counter() - started
    if dense is not None:
        started = perf_counter()
        constituents["dense"] = dense.search(query_vector, config.retrieval.candidate_depth)
        timings["dense_search"] = perf_counter() - started
    if recipe.startswith("hybrid_"):
        started = perf_counter()
        ranked = reciprocal_rank_fusion(list(constituents.values()), config.retrieval.rrf_constant,
                                       config.retrieval.candidate_depth)
        timings["fusion"] = perf_counter() - started
    else:
        ranked = next(iter(constituents.values()))
    searched = perf_counter()
    context = pack_context(ranked, tokenizer, config.retrieval.context_budget_tokens)
    packed = perf_counter()
    metrics = {f"at_{k}": evidence_metrics(question, [
        (r.chunk.document_id, r.chunk.start, r.chunk.end) for r in ranked[:k]
    ]) for k in (5, 10, 50)}
    metrics["context"] = evidence_metrics(question, [
        (e.document_id, e.source_start, e.source_end) for e in context.evidence
    ])
    result = {
        "schema_version": 1, "purpose": "development retrieval smoke; not a benchmark run",
        "status": "success", "dataset": question.dataset, "question_id": question_id,
        "question": question.text, "config_sha256": config.sha256(),
        "source_manifest_sha256": source["manifest_sha256"], "index_sha256": identity,
        "tokenizer": tokenizer.identity, "method": manifest["method"], "size": manifest["size"],
        "document_limit": manifest["document_limit"], "retrieved": [asdict(r) for r in ranked],
        "recipe": recipe, "embedding": encoder.identity if encoder is not None else None,
        "embedding_query_tokens": encoder.last_lengths[0] if encoder is not None else None,
        "embedding_truncation": False,
        "constituents": {name: [asdict(r) for r in hits] for name, hits in constituents.items()},
        "context": asdict(context), "context_sha256": digest(context.text), "metrics": metrics,
        "timings_seconds": {**timings, "offline_load_and_postings_rebuild": offline_load_seconds,
                            "offline_load": offline_load_seconds,
                            "search": sum(timings[k] for k in
                                          ("bm25_search", "dense_search", "fusion")),
                            "packing": packed - searched,
                            "online_retrieval_path": packed - online},
    }
    return result


def retrieve(config: ExperimentConfig, data: Path, directory: Path, tokenizer_path: Path,
             question_id: str | None, output: Path, recipe: str | None = None,
             models_root: Path = Path("models")) -> dict:
    if output.exists():
        raise DataError("retrieval output already exists; choose a new file")
    session = load_retriever(config, data, directory, tokenizer_path, recipe, models_root)
    result = retrieve_query(session, question_id or session.source["split"]["development_ids"][0])
    write_new_json(output, result)
    return result
