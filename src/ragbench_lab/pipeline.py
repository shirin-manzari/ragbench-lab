"""Phase 2 offline indexing and uncached online BM25 retrieval diagnostics."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

from ragbench_lab.chunking import Chunk, chunk_document
from ragbench_lab.config import ExperimentConfig
from ragbench_lab.context import pack_context
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError, Document
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.retrieval import BM25Index
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
                size: int, output: Path, limit: int | None = None) -> dict:
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
    index = BM25Index(chunks, config.bm25)
    stats["bm25_build_seconds"] = perf_counter() - started
    if not index.chunks:
        raise DataError("cannot index an empty searchable corpus")
    rows = [asdict(c) for c in index.chunks]
    manifest = {
        "schema_version": 1, "recipe": "bm25", "dataset": source["dataset"],
        "purpose": "diagnostic-only bounded corpus" if limit else "full prepared corpus",
        "source_manifest_sha256": source["manifest_sha256"],
        "source_corpus_sha256": source["corpus_sha256"], "config_sha256": config.sha256(),
        "tokenizer": tokenizer.identity, "bm25": asdict(config.bm25),
        "sentence_rule": "source_sentences_or_punctuation_paragraph_v1",
        "context_template": "bracketed_full_chunk_id_v1",
        "method": method, "size": size, "document_limit": limit,
        "document_ids_sha256": digest([d.document_id for d in documents]),
        "chunks_sha256": digest(rows), "statistics": stats,
        "persistence": "source chunks; BM25 postings rebuilt during offline load",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    with (output / "chunks.jsonl").open("xb") as stream:
        for row in rows:
            stream.write(canonical(row) + b"\n")
    manifest["chunks_bytes"] = (output / "chunks.jsonl").stat().st_size
    manifest["manifest_sha256"] = digest(manifest)
    write_new_json(output / "manifest.json", manifest)
    return manifest


def retrieve(config: ExperimentConfig, data: Path, directory: Path, tokenizer_path: Path,
             question_id: str | None, output: Path) -> dict:
    if output.exists():
        raise DataError("retrieval output already exists; choose a new file")
    initialization = perf_counter()
    source, bundle = load_prepared(data)
    tokenizer = ReferenceTokenizer(tokenizer_path, config.chunking)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    identity = manifest.pop("manifest_sha256")
    if digest(manifest) != identity or manifest["schema_version"] != 1:
        raise DataError("index manifest identity mismatch")
    manifest["manifest_sha256"] = identity
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
    question_id = question_id or source["split"]["development_ids"][0]
    if question_id not in source["split"]["development_ids"]:
        raise DataError("Phase 2 diagnostic retrieval accepts development questions only")
    question = next(q for q in bundle.questions if q.question_id == question_id)
    index = BM25Index(chunks, config.bm25)
    offline_load_seconds = perf_counter() - initialization
    online = perf_counter()
    ranked = index.search(question.text, config.retrieval.candidate_depth)
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
        "context": asdict(context), "context_sha256": digest(context.text), "metrics": metrics,
        "timings_seconds": {"offline_load_and_postings_rebuild": offline_load_seconds,
                            "search": searched - online, "packing": packed - searched,
                            "online_retrieval_path": packed - online},
    }
    write_new_json(output, result)
    return result
