from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ragbench_lab.config import ExperimentConfig
from ragbench_lab.data.adapters import hotpot, squad
from ragbench_lab.data.records import (
    DataError,
    DatasetBundle,
    Document,
    EvidenceSpan,
    Exclusion,
    Question,
    SourceSpan,
    Split,
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def validate_bundle(bundle: DatasetBundle) -> None:
    documents = {d.document_id: d for d in bundle.documents}
    if len(documents) != len(bundle.documents):
        raise DataError("duplicate document IDs")
    ids = [q.question_id for q in bundle.questions]
    exclusions = [e.question_id for e in bundle.exclusions]
    if len(ids + exclusions) != len(set(ids + exclusions)):
        raise DataError("duplicate or both included/excluded question IDs")
    for question in bundle.questions:
        for evidence in question.evidence + question.diagnostics:
            doc = documents.get(evidence.document_id)
            if doc is None or doc.dataset != question.dataset:
                raise DataError(f"missing or mismatched document for {question.question_id}")
            spans = {span.source_id: span for span in doc.source_spans}
            span = spans.get(evidence.source_id)
            if (span is None or not span.start <= evidence.start < evidence.end <= span.end
                    or doc.text[evidence.start:evidence.end] != evidence.text):
                raise DataError(f"invalid evidence mapping for {question.question_id}")


def make_split(bundle: DatasetBundle, development: int, evaluation: int, seed: int,
               allow_overlap: bool = False) -> Split:
    """Use seeded SHA-256 ordering, independent of source question iteration order.

    Development is selected first. Evaluation excludes its supporting document
    IDs and article titles by default. Never silently relax that policy.
    """
    validate_bundle(bundle)
    if any(type(n) is not int or n <= 0 for n in (development, evaluation)):
        raise DataError("split sample counts must be positive integers")
    if type(seed) is not int:
        raise DataError("split seed must be an integer")
    if len(bundle.questions) < development + evaluation:
        raise DataError("not enough eligible questions for requested disjoint question splits")
    ordered = sorted(bundle.questions, key=lambda q: (
        digest([seed, q.dataset, q.question_id]), q.question_id,
    ))
    docs = {d.document_id: d for d in bundle.documents}

    def sources(questions: list[Question]) -> tuple[set[str], set[str]]:
        ids = {e.document_id for q in questions for e in q.evidence}
        return ids, {docs[identifier].title for identifier in ids}

    dev = ordered[:development]
    dev_docs, dev_titles = sources(dev)
    candidates = []
    for question in ordered[development:]:
        query_docs, query_titles = sources([question])
        if allow_overlap or not (dev_docs & query_docs or dev_titles & query_titles):
            candidates.append(question)
    if len(candidates) < evaluation:
        raise DataError("not enough evaluation questions after source isolation; enlarge the pool "
                        "or explicitly allow and record source overlap")
    held_out = candidates[:evaluation]
    eval_docs, eval_titles = sources(held_out)
    return Split(tuple(q.question_id for q in dev), tuple(q.question_id for q in held_out), seed,
                 tuple(sorted(dev_docs & eval_docs)), tuple(sorted(dev_titles & eval_titles)))


def prepare(config: ExperimentConfig, dataset: str, source: Path, revision: str,
            expected_sha256: str, output: Path, pool_limit: int | None = None,
            allow_overlap: bool = False) -> dict[str, Any]:
    if dataset not in config.dataset.names:
        raise DataError("dataset must be enabled in the experiment configuration")
    if not revision.strip() or revision.startswith("pin-"):
        raise DataError("a concrete source revision/version is required")
    if pool_limit is not None and (type(pool_limit) is not int or pool_limit <= 0):
        raise DataError("pool limit must be positive")
    if dataset == "squad" and pool_limit is not None:
        raise DataError("pool limit applies only to HotpotQA validation rows")
    if output.exists():
        raise DataError(f"output already exists; choose a new artifact directory: {output}")
    content = source.read_bytes()
    actual_sha = hashlib.sha256(content).hexdigest()
    if actual_sha != expected_sha256:
        raise DataError("source SHA-256 mismatch")
    raw = json.loads(content)
    if dataset == "squad":
        bundle = squad(raw)
        pool_ids = sorted(q.question_id for q in bundle.questions)
        pool_ids += sorted(e.question_id for e in bundle.exclusions)
    else:
        if not isinstance(raw, list):
            raise DataError("HotpotQA source must be a native validation JSON array")
        # Select a pool before checking labels or sampling questions.
        pool = raw if pool_limit is None else raw[:pool_limit]
        pool_ids = [row["_id"] for row in pool]
        bundle = hotpot(pool)
    validate_bundle(bundle)
    split = make_split(bundle, config.dataset.development_questions,
                       config.dataset.evaluation_questions, config.dataset.sampling_seed,
                       allow_overlap)
    manifest = {
        "schema_version": 1, "dataset": dataset, "source_revision": revision,
        "source_sha256": actual_sha, "config_sha256": config.sha256(),
        "source_format": "squad-v1.1" if dataset == "squad" else "hotpot-distractor-validation",
        "corpus_scope": "reconstructed articles" if dataset == "squad" else "adapted shared corpus",
        "pool_policy": "entire source" if pool_limit is None else "first n source rows",
        "pool_limit": pool_limit, "pool_question_ids": pool_ids,
        "exclusion_policy": "exclude any question with missing, ambiguous, or invalid evidence",
        "exclusions": [asdict(e) for e in bundle.exclusions],
        "split_policy": "seeded sha256; development first; title and evidence-document isolation",
        "allow_source_overlap": allow_overlap, "split": asdict(split),
        "document_count": len(bundle.documents), "eligible_question_count": len(bundle.questions),
        "exclusion_count": len(bundle.exclusions),
        "same_title_variant_count": len(bundle.documents) - len(
            {d.title for d in bundle.documents}),
    }
    documents = [asdict(d) for d in sorted(bundle.documents, key=lambda d: d.document_id)]
    questions = [asdict(q) for q in sorted(bundle.questions, key=lambda q: q.question_id)]
    manifest["corpus_sha256"] = digest(documents)
    manifest["questions_sha256"] = digest(questions)
    manifest["manifest_sha256"] = digest(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".prepare-", dir=output.parent))
    try:
        for name, records in (("documents.jsonl", documents), ("questions.jsonl", questions)):
            with (staging / name).open("wb") as stream:
                for record in records:
                    stream.write(canonical(record) + b"\n")
        (staging / "manifest.json").write_bytes(canonical(manifest) + b"\n")
        # mkdir is exclusive even if another process created output after the initial check.
        output.mkdir()
        for artifact in staging.iterdir():
            artifact.rename(output / artifact.name)
    finally:
        shutil.rmtree(staging)
    return json.loads(canonical(manifest))


def load_prepared(directory: Path) -> tuple[dict[str, Any], DatasetBundle]:
    """Check saved hashes, evidence offsets, and declared split isolation on disk."""
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    stored_hash = manifest.pop("manifest_sha256")
    if manifest.get("schema_version") != 1 or digest(manifest) != stored_hash:
        raise DataError("prepared manifest identity mismatch")
    manifest["manifest_sha256"] = stored_hash
    records = {}
    for name in ("documents", "questions"):
        records[name] = [json.loads(line) for line in
                         (directory / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
    if (digest(records["documents"]) != manifest["corpus_sha256"]
            or digest(records["questions"]) != manifest["questions_sha256"]):
        raise DataError("prepared corpus or question identity mismatch")
    documents = tuple(Document(**{**d, "source_spans": tuple(
        SourceSpan(**s) for s in d["source_spans"])}) for d in records["documents"])
    questions = tuple(Question(**{**q, "answers": tuple(q["answers"]),
                                  "evidence": tuple(EvidenceSpan(**e) for e in q["evidence"]),
                                  "diagnostics": tuple(
                                      EvidenceSpan(**e) for e in q["diagnostics"])})
                      for q in records["questions"])
    bundle = DatasetBundle(documents, questions,
                           tuple(Exclusion(**e) for e in manifest["exclusions"]))
    validate_bundle(bundle)
    saved = manifest["split"]
    expected = make_split(bundle, len(saved["development_ids"]), len(saved["evaluation_ids"]),
                          saved["seed"], manifest["allow_source_overlap"])
    if canonical(asdict(expected)) != canonical(saved):
        raise DataError("saved split differs from deterministic selection")
    if (manifest["document_count"] != len(documents)
            or manifest["eligible_question_count"] != len(questions)
            or manifest["exclusion_count"] != len(bundle.exclusions)):
        raise DataError("prepared manifest counts mismatch")
    return manifest, bundle


def inspect_prepared(directory: Path) -> dict[str, Any]:
    return load_prepared(directory)[0]
