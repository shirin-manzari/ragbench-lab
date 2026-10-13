"""Explicit oracle and empty-context diagnostic baselines, separate from the factorial."""

from __future__ import annotations

from ragbench_lab.chunking import Chunk, TokenCounter
from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError, Question
from ragbench_lab.retrieval import RankedChunk


def baseline_candidates(kind: str, question: Question, tokenizer: TokenCounter):
    if kind == "no_rag":
        return []
    if kind != "gold":
        raise DataError("unsupported diagnostic baseline")
    spans = question.diagnostics if question.dataset == "squad" else question.evidence
    if not spans:
        raise DataError("gold baseline lacks declared evidence context")
    unique = {(e.document_id, e.start, e.end): e for e in spans}
    candidates = []
    for key in sorted(unique):
        evidence = unique[key]
        tokens = tokenizer.count(evidence.text)
        identifier = digest(["explicit_gold_baseline", *key])
        chunk = Chunk(identifier, evidence.document_id, evidence.start, evidence.end,
                      evidence.text, tokens, "gold_evidence", tokens)
        candidates.append(RankedChunk(chunk, 0.0))
    return candidates
