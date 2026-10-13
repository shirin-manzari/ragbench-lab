"""SQuAD/HotpotQA answer normalization and scoring, independent of evidence labels."""

from __future__ import annotations

import re
import string
from collections import Counter

from ragbench_lab.data.records import DataError


def normalize_answer(text: str) -> str:
    lowered = text.lower()
    unpunctuated = "".join(char for char in lowered if char not in string.punctuation)
    unarticled = re.sub(r"\b(a|an|the)\b", " ", unpunctuated)
    return " ".join(unarticled.split())


def answer_scores(prediction: str, answers: tuple[str, ...], dataset: str) -> dict:
    if dataset not in {"squad", "hotpot_qa"} or not answers:
        raise DataError("answer scoring requires a supported dataset and reference answers")
    normalized = normalize_answer(prediction)
    candidates = []
    for answer in answers:
        target = normalize_answer(answer)
        exact = float(normalized == target)
        predicted_tokens, target_tokens = normalized.split(), target.split()
        special = {"yes", "no", "noanswer"}
        if (dataset == "hotpot_qa" and normalized != target
                and (normalized in special or target in special)):
            f1 = 0.0
        elif not predicted_tokens or not target_tokens:
            f1 = 0.0
        else:
            shared = sum((Counter(predicted_tokens) & Counter(target_tokens)).values())
            precision, recall = shared / len(predicted_tokens), shared / len(target_tokens)
            f1 = 2 * precision * recall / (precision + recall) if shared else 0.0
        candidates.append((exact, f1))
    return {"exact_match": max(exact for exact, _ in candidates),
            "token_f1": max(f1 for _, f1 in candidates)}
