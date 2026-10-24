from __future__ import annotations

from collections import defaultdict

from ragbench_lab.data.records import EvidenceSpan, Question


def evidence_metrics(question: Question, intervals: list[tuple[str, int, int]]) -> dict:
    merged: dict[str, list[tuple[int, int]]] = defaultdict(list)
    by_document: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for document, start, end in intervals:
        if start < end:
            by_document[document].append((start, end))
    for document, spans in by_document.items():
        for start, end in sorted(spans):
            if merged[document] and start <= merged[document][-1][1]:
                old_start, old_end = merged[document][-1]
                merged[document][-1] = (old_start, max(old_end, end))
            else:
                merged[document].append((start, end))

    def covered(span: EvidenceSpan) -> bool:
        return any(start <= span.start and end >= span.end
                   for start, end in merged.get(span.document_id, []))

    def fraction(span: EvidenceSpan) -> float:
        included = sum(max(0, min(end, span.end) - max(start, span.start))
                       for start, end in merged.get(span.document_id, []))
        return included / (span.end - span.start)

    hits = [covered(span) for span in question.evidence]
    if question.dataset == "squad":
        # Annotators supply alternative answer locations, not multiple required facts.
        return {"answer_span_covered": any(hits), "evidence_coverage": float(any(hits)),
                "supporting_paragraph_coverage": max(
                    (fraction(span) for span in question.diagnostics), default=0.0)}
    return {"evidence_coverage": sum(hits) / len(hits), "all_required_evidence": all(hits),
            "supporting_sentence_count": len(hits)}
