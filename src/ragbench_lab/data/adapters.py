from __future__ import annotations

import hashlib
import json
from typing import Any

from ragbench_lab.data.records import (
    DataError,
    DatasetBundle,
    Document,
    EvidenceSpan,
    Exclusion,
    Question,
    SourceSpan,
)


def _identity(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise DataError(f"{field} must be a string")
    return value


def _unique_question(identifier: str, seen: set[str]) -> None:
    if not identifier or identifier in seen:
        raise DataError(f"empty or duplicate question ID: {identifier!r}")
    seen.add(identifier)


def squad(raw: dict[str, Any]) -> DatasetBundle:
    """Join paragraphs in article order; do not normalize or repair source text."""
    if raw.get("version") != "1.1":
        raise DataError("expected native SQuAD version 1.1")
    documents, questions, exclusions = [], [], []
    seen: set[str] = set()
    for article_index, article in enumerate(raw["data"]):
        title = _text(article["title"], "title")
        paragraphs = article["paragraphs"]
        contexts = [_text(p["context"], "context") for p in paragraphs]
        document_id = f"squad:{article_index}:{_identity([title, contexts])}"
        spans = []
        offset = 0
        for paragraph_index, context in enumerate(contexts):
            spans.append(SourceSpan(f"{article_index}:{paragraph_index}", offset,
                                    offset + len(context), "paragraph"))
            offset += len(context) + 2  # explicit separator: two newlines
        document = Document(document_id, "squad", title, "\n\n".join(contexts), tuple(spans))
        documents.append(document)
        for paragraph, span in zip(paragraphs, spans, strict=True):
            for qa in paragraph["qas"]:
                identifier = _text(qa["id"], "id")
                _unique_question(identifier, seen)
                evidence, answers = [], []
                reason = ""
                for answer in qa["answers"]:
                    text = _text(answer["text"], "answer text")
                    start = answer["answer_start"]
                    if (type(start) is not int or start < 0 or not text
                            or start + len(text) > span.end - span.start
                            or paragraph["context"][start:start + len(text)] != text):
                        reason = "invalid_answer_offset_or_text"
                        break
                    mapped = EvidenceSpan(document_id, span.source_id, span.start + start,
                                          span.start + start + len(text), text, "answer")
                    if mapped not in evidence:
                        evidence.append(mapped)
                    if text not in answers:
                        answers.append(text)
                if reason or not evidence:
                    exclusions.append(Exclusion(identifier, reason or "missing_answer_evidence"))
                    continue
                diagnostic = EvidenceSpan(document_id, span.source_id, span.start, span.end,
                                          paragraph["context"], "paragraph")
                questions.append(Question(identifier, "squad", _text(qa["question"], "question"),
                                          tuple(answers), tuple(evidence), (diagnostic,)))
    return DatasetBundle(tuple(documents), tuple(questions), tuple(exclusions))


def hotpot(raw: list[dict[str, Any]]) -> DatasetBundle:
    """Deduplicate exact title/sentence passages across one declared validation pool.

    Distinct passages sharing a title remain distinct. Evidence resolves against
    the question's own context; ambiguous same-title mappings are excluded.
    """
    documents: dict[str, Document] = {}
    questions, exclusions = [], []
    seen: set[str] = set()
    for row in raw:
        identifier = _text(row["_id"], "_id")
        _unique_question(identifier, seen)
        local: dict[str, dict[str, Document]] = {}
        for title, sentences in row["context"]:
            title = _text(title, "title")
            if not isinstance(sentences, list):
                raise DataError("context sentences must be a list")
            sentences = [_text(s, "sentence") for s in sentences]
            document_id = f"hotpot_qa:{_identity([title, sentences])}"
            spans, offset = [], 0
            for sentence_index, sentence in enumerate(sentences):
                spans.append(SourceSpan(str(sentence_index), offset,
                                        offset + len(sentence), "sentence"))
                offset += len(sentence)
            doc = Document(document_id, "hotpot_qa", title, "".join(sentences), tuple(spans))
            documents.setdefault(document_id, doc)
            local.setdefault(title, {})[document_id] = doc
        evidence = []
        reason = ""
        for title, sentence_index in row["supporting_facts"]:
            candidates = list(local.get(title, {}).values())
            if len(candidates) != 1:
                reason = "missing_or_ambiguous_supporting_title"
                break
            doc = candidates[0]
            if (type(sentence_index) is not int or sentence_index < 0
                    or sentence_index >= len(doc.source_spans)):
                reason = "missing_supporting_sentence"
                break
            span = doc.source_spans[sentence_index]
            if span.start == span.end:
                reason = "empty_supporting_sentence"
                break
            mapped = EvidenceSpan(doc.document_id, span.source_id, span.start, span.end,
                                  doc.text[span.start:span.end], "sentence")
            if mapped not in evidence:
                evidence.append(mapped)
        if reason or not evidence:
            exclusions.append(Exclusion(identifier, reason or "missing_supporting_facts"))
            continue
        questions.append(Question(identifier, "hotpot_qa", _text(row["question"], "question"),
                                  (_text(row["answer"], "answer"),), tuple(evidence)))
    return DatasetBundle(tuple(sorted(documents.values(), key=lambda d: d.document_id)),
                         tuple(questions), tuple(exclusions))
