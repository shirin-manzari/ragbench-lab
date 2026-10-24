from __future__ import annotations

from dataclasses import asdict
from time import perf_counter

from ragbench_lab.answer_metrics import answer_scores
from ragbench_lab.context import pack_context
from ragbench_lab.data.preparation import digest
from ragbench_lab.generation import GenerationError
from ragbench_lab.metrics import evidence_metrics
from ragbench_lab.pipeline import search_query
from ragbench_lab.serving import verify_uncached


def measured_answer(session, question, generator, reranker=None) -> dict:
    """No setup, disk writes, cache preparation, or evidence labels in generation."""
    result = {"status": "failed", "stage": "retrieval", "question_id": question.question_id,
              "dataset": question.dataset, "question": question.text,
              "config_sha256": session.config.sha256(),
              "source_manifest_sha256": session.source["manifest_sha256"],
              "index_sha256": session.manifest["manifest_sha256"]}
    started = perf_counter()
    try:
        ranked, constituents, timings = search_query(session, question.text)
        result["retrieval"] = {
            "initial_candidates": [asdict(hit) for hit in ranked],
            "constituents": {name: [asdict(hit) for hit in hits]
                             for name, hits in constituents.items()},
            "timings_seconds": timings,
            "embedding_query_tokens": session.encoder.last_lengths[0] if session.encoder else None,
        }
        result["initial_candidates_sha256"] = digest(result["retrieval"]["initial_candidates"])
        result["stage"] = "reranking"
        before = [hit.chunk.chunk_id for hit in ranked]
        rerank_started = perf_counter()
        if reranker is not None:
            ranked = reranker.rerank(question.text, ranked)
        after = [hit.chunk.chunk_id for hit in ranked]
        if len(after) != len(before) or set(after) != set(before):
            raise ValueError("reranker changed initial candidate membership")
        result["reranking"] = {"enabled": reranker is not None,
            "seconds": perf_counter() - rerank_started,
            "initial_candidate_ids": before, "candidate_ids": after,
            "input_lengths": reranker.last_lengths if reranker else []}
        result["stage"] = "packing"
        packing_started = perf_counter()
        context = pack_context(ranked, session.tokenizer,
                               session.config.retrieval.context_budget_tokens)
        result.update(context=asdict(context), context_sha256=digest(context.text),
                      packing_seconds=perf_counter() - packing_started)
        result["stage"] = "generation"
        generated = generator.generate(question.text, context.text)
        result.update(generation=generated, total_request_seconds=perf_counter() - started)
        result["stage"] = "validation"
        verify_uncached(generated)
        if generated["context_sha256"] != result["context_sha256"]:
            raise ValueError("generator context differs from packed evidence")
        result["answer_metrics"] = answer_scores(generated["answer"], question.answers,
                                                 question.dataset)
        result["metrics"] = {f"at_{k}": evidence_metrics(question, [
            (hit.chunk.document_id, hit.chunk.start, hit.chunk.end) for hit in ranked[:k]])
            for k in (5, 10, 50)}
        result["metrics"]["context"] = evidence_metrics(question, [
            (item.document_id, item.source_start, item.source_end) for item in context.evidence])
        result.update(status="success", stage="complete")
    except Exception as error:
        if isinstance(error, GenerationError):
            result["generation"] = error.record
        result.update(error=str(error), error_type=type(error).__name__,
                      failed_request_seconds=perf_counter() - started)
    return result
