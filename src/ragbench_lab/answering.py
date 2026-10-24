from __future__ import annotations

import json
from dataclasses import asdict
from http.client import HTTPException
from pathlib import Path
from time import perf_counter
from urllib.error import HTTPError

from ragbench_lab.answer_metrics import answer_scores
from ragbench_lab.baselines import baseline_candidates
from ragbench_lab.config import ExperimentConfig
from ragbench_lab.context import pack_context
from ragbench_lab.data.preparation import canonical, digest, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.generation import (
    GenerationError,
    GeneratorSettings,
    LocalGenerator,
    load_native_tokenizer,
)
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.pipeline import load_retriever, search_query, write_new_json
from ragbench_lab.reranking import LocalReranker, RerankerSettings
from ragbench_lab.stage_a import implementation_identity
from ragbench_lab.tokenization import ReferenceTokenizer


def answer(config: ExperimentConfig, data: Path, index: Path | None, tokenizer_path: Path,
           generator_config: Path, native_tokenizer: Path, output: Path,
           question_id: str | None = None, recipe: str | None = None,
           models_root: Path = Path("models"), baseline: str = "rag",
           reranker_config: Path | None = None, reranker_dir: Path | None = None,
           warmup: bool = False) -> dict:
    if output.exists():
        raise DataError("answer output exists; choose a new diagnostic artifact")
    result = {"schema_version": 1, "purpose": "development answer diagnostic",
              "config_sha256": config.sha256(), "status": "failed", "stage": "setup"}
    setup = perf_counter()
    try:
        result["provenance"] = implementation_identity()
        if (baseline not in {"rag", "no_rag", "gold"}
                or (reranker_config is None) != (reranker_dir is None)
                or (baseline != "rag" and reranker_config is not None)
                or (baseline == "rag" and index is None)):
            raise DataError("unsupported baseline/index/reranker combination")
        source, bundle = load_prepared(data)
        permitted = source["split"]["development_ids"]
        qid = question_id or permitted[0]
        if qid not in permitted:
            raise DataError("answer diagnostics accept development questions only")
        question = next(q for q in bundle.questions if q.question_id == qid)
        reference = ReferenceTokenizer(tokenizer_path, config.chunking)
        settings = GeneratorSettings(**json.loads(generator_config.read_text(encoding="utf-8")))
        result["generator_settings"] = asdict(settings)
        tokenizer = load_native_tokenizer(native_tokenizer, settings)
        generator = LocalGenerator(settings, tokenizer)
        session = (load_retriever(config, data, index, tokenizer_path, recipe, models_root,
                                  prepared=(source, bundle)) if baseline == "rag" else None)
        reranker = (LocalReranker(reranker_dir, RerankerSettings(**json.loads(
            reranker_config.read_text(encoding="utf-8")))) if reranker_config else None)
        if warmup:
            warmed = perf_counter()
            if session is not None:
                warm_candidates, _, _ = search_query(session, "Warmup retrieval query.")
                if reranker is not None:
                    reranker.rerank("Warmup retrieval query.", warm_candidates[:1])
            result["retrieval_reranker_warmup_seconds"] = perf_counter() - warmed
        result.update(question_id=qid, dataset=source["dataset"], baseline=baseline,
                      source_manifest_sha256=source["manifest_sha256"],
                      settings_sha256=digest(asdict(settings)),
                      offline_setup_seconds=perf_counter() - setup, stage="retrieval")
        started = perf_counter()
        if session is not None:
            ranked, constituents, times = search_query(session, question.text)
            result["retrieval"] = {
                "index_sha256": session.manifest["manifest_sha256"],
                "recipe": session.manifest["recipe"],
                "embedding": session.encoder.identity if session.encoder else None,
                "embedding_query_tokens": session.encoder.last_lengths[0]
                if session.encoder else None,
                "initial_candidates": [asdict(hit) for hit in ranked],
                "constituents": {name: [asdict(hit) for hit in hits]
                                 for name, hits in constituents.items()},
                "timings_seconds": times,
            }
        else:
            ranked = baseline_candidates(baseline, question, reference)
        result["stage"] = "reranking"
        rerank_started = perf_counter()
        result["reranking"] = {
            "enabled": reranker is not None,
            "identity": reranker.identity if reranker else None,
            "initial_candidate_ids": [hit.chunk.chunk_id for hit in ranked],
        }
        try:
            if reranker is not None:
                ranked = reranker.rerank(question.text, ranked)
        finally:
            result["reranking"].update(
                seconds=perf_counter() - rerank_started,
                input_lengths=reranker.last_lengths if reranker else [])
        result["reranking"]["candidate_ids"] = [hit.chunk.chunk_id for hit in ranked]
        result["stage"] = "packing"
        packing_started = perf_counter()
        context = pack_context(ranked, reference, config.retrieval.context_budget_tokens)
        result.update(context=asdict(context), context_sha256=digest(context.text),
                      packing_seconds=perf_counter() - packing_started)
        result["stage"] = "generation"
        try:
            generated = generator.generate(question.text, context.text)
        except GenerationError as error:
            result["generation"] = error.record
            raise
        result.update(generation=generated, stage="evaluation",
                      total_request_seconds=perf_counter() - started)
        result["answer_metrics"] = answer_scores(generated["answer"], question.answers,
                                                 question.dataset)
        result["context_evidence_metrics"] = evidence_metrics(question, [
            (item.document_id, item.source_start, item.source_end) for item in context.evidence])
        result.update(status="success", stage="complete")
    except (OSError, HTTPException, ValueError, KeyError, TypeError) as error:
        result.update(status="failed", error=str(error), error_type=type(error).__name__)
        if isinstance(error, HTTPError):
            result["http_status"] = error.code
            error.close()
        if result["stage"] == "setup":
            result["offline_setup_seconds"] = perf_counter() - setup
        else:
            result["failed_request_seconds"] = perf_counter() - started
    write_new_json(output, result)
    return json.loads(canonical(result))
