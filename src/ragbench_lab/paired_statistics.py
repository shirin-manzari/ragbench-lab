from __future__ import annotations

from collections import defaultdict

import numpy as np

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError


def source_clusters(dataset, questions, documents) -> dict[str, str]:
    titles = {d.document_id: d.title.casefold().strip() for d in documents}
    parent = {q.question_id: q.question_id for q in questions}

    def find(qid):
        while parent[qid] != qid:
            parent[qid] = parent[parent[qid]]
            qid = parent[qid]
        return qid

    owners = {}
    for q in sorted(questions, key=lambda q: q.question_id):
        if q.dataset != dataset:
            raise DataError("source clusters cannot mix datasets")
        documents_seen = {e.document_id for e in q.evidence}
        if not documents_seen or not documents_seen <= titles.keys():
            raise DataError("source clustering requires every supporting document")
        keys = {("document", doc) for doc in documents_seen}
        if dataset == "hotpot_qa":
            keys |= {("title", titles[doc]) for doc in documents_seen if titles[doc]}
        elif dataset != "squad" or len(documents_seen) != 1:
            raise DataError("SQuAD source cluster must identify one reconstructed article")
        for key in sorted(keys):
            if key in owners:
                a, b = find(q.question_id), find(owners[key])
                parent[max(a, b)] = min(a, b)
            owners[key] = q.question_id
    return {qid: find(qid) for qid in sorted(parent)}


def bootstrap_weights(labels: list[str], samples: int, seed: int):
    if not labels or type(samples) is not int or samples <= 0:
        raise DataError("bootstrap needs question clusters and positive resample count")
    groups = sorted(set(labels))
    indices = {label: i for i, label in enumerate(groups)}
    chosen = np.random.default_rng(seed).integers(len(groups), size=(samples, len(groups)))
    counts = np.zeros((samples, len(groups)), dtype=np.int64)
    np.add.at(counts, (np.arange(samples)[:, None], chosen), 1)
    return counts[:, [indices[label] for label in labels]], len(groups)


def estimates(values, weights, statistic: str):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights)
    if (values.ndim != 2 or weights.ndim != 2 or weights.shape[1] != values.shape[0]
            or not np.isfinite(values).all() or not values.size
            or not np.issubdtype(weights.dtype, np.integer) or (weights < 0).any()
            or (weights.sum(axis=1) == 0).any()):
        raise DataError("invalid clustered estimator values/weights")
    flat = values.ravel()
    expanded = np.repeat(weights, values.shape[1], axis=1)
    if statistic == "mean":
        return (expanded * flat).sum(axis=1) / expanded.sum(axis=1)
    if statistic not in {"median", "p95"}:
        raise DataError("unsupported clustered estimator")
    order = np.argsort(flat, kind="stable")
    flat = flat[order]
    cumulative = np.cumsum(expanded[:, order], axis=1)
    positions = (cumulative[:, -1] - 1) * (.5 if statistic == "median" else .95)
    left, right = np.floor(positions), np.ceil(positions)
    a = flat[(cumulative <= left[:, None]).sum(axis=1)]
    b = flat[(cumulative <= right[:, None]).sum(axis=1)]
    return a + (positions - left) * (b - a)


def paired_summary(left: dict, right: dict | None, groups: dict, protocol: dict) -> dict:
    """Dataset-stratified estimates; the exact same bootstrap weights pair both sides."""
    if not left or (right is not None and set(left) != set(right)):
        raise DataError("paired summaries require the same datasets")
    results = defaultdict(list)
    point, clusters, questions = [], {}, {}
    for dataset, sample in sorted(left.items()):
        ids = sample["question_ids"]
        if len(set(ids)) != len(ids) or not ids:
            raise DataError("paired sample requires unique question IDs")
        other = right[dataset] if right is not None else None
        if other is not None and other["question_ids"] != ids:
            raise DataError("paired samples must use identical ordered question IDs")
        values = sample["values"]
        ones = np.ones((1, len(ids)), dtype=np.int64)
        estimate = estimates(values, ones, sample["statistic"])
        if other is not None:
            estimate -= estimates(other["values"], ones, sample["statistic"])
        point.append(float(estimate[0]))
        questions[dataset] = len(ids)
        for method in ("source", "question"):
            labels = [groups[dataset][qid] for qid in ids] if method == "source" else ids
            seed = int(digest([protocol["seed"], dataset, method])[:16], 16)
            weights, count = bootstrap_weights(labels, protocol["bootstrap_samples"], seed)
            if method == "source":
                clusters[dataset] = count
            if count < 2:
                results[method].append(None)
                continue
            resampled = estimates(values, weights, sample["statistic"])
            if other is not None:
                resampled -= estimates(other["values"], weights, sample["statistic"])
            results[method].append(resampled)
    result = {"estimate": float(np.mean(point)), "questions": questions,
              "source_clusters": clusters, "source_ci95": None, "question_sensitivity_ci95": None}
    for method, output in (("source", "source_ci95"),
                           ("question", "question_sensitivity_ci95")):
        if all(x is not None for x in results[method]):
            result[output] = np.quantile(np.mean(results[method], axis=0), [.025, .975]).tolist()
    return result
