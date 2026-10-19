"""Verify a checkout with Python 3.11+ only; no installed package or model assets.

Synthetic smoke scenarios exercise the real algorithms in temporary storage.
The character counter deliberately does not validate the frozen BGE tokenizer.
The ignored local unittest suite and full study replay remain separate checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import tempfile
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_IMPORTS = {"torch", "transformers", "tokenizers", "faiss", "numpy", "dash", "plotly"}


def require(condition: bool, message: str) -> None:
    # Explicit checks must also run under python -O.
    if not condition:
        raise ValueError(message)


def rejects(action, exception: type[Exception], message: str) -> None:
    try:
        action()
    except exception:
        return
    raise ValueError(message)


def runtime_guard(event: str, args: tuple) -> None:
    if event == "import" and args[0].split(".")[0] in FORBIDDEN_IMPORTS:
        raise RuntimeError(f"verification must not import {args[0]}")
    if ((event.startswith("socket.") and event != "socket.__new__")
            or event in {"subprocess.Popen", "os.system", "os.fork", "os.forkpty",
                         "os.posix_spawn", "os.exec"}):
        raise RuntimeError(f"verification must not use {event}")


class CharacterCounter:
    """Synthetic Unicode character units, including headers and whitespace."""

    def offsets(self, text: str) -> list[tuple[int, int]]:
        return [(i, i + 1) for i in range(len(text))]

    def count(self, text: str) -> int:
        return len(text)


def configuration(work: Path) -> dict:
    from ragbench_lab.config import ConfigError, load_config

    sources = sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "scripts").glob("*.py"))
    for path in sources:
        compile(path.read_bytes(), str(path), "exec")  # Syntax only; never execute/import models.
    paths = sorted((ROOT / "configs").glob("*.toml"))
    require(bool(paths), "no experiment configurations found")
    for path in paths:
        load_config(path)
    invalid = work / "invalid.toml"
    source = (ROOT / "configs/stage-a-study.toml").read_text(encoding="utf-8")
    require("candidate_depth = 50" in source, "cannot construct invalid configuration")
    invalid.write_text(source.replace("candidate_depth = 50", "candidate_depth = 20"),
                       encoding="utf-8")
    rejects(lambda: load_config(invalid), ConfigError, "unsupported candidate depth accepted")
    return {"python_files": len(sources), "configurations": len(paths),
            "unsupported_depth_rejected": True}


def factorials(_work: Path) -> dict:
    from ragbench_lab.conditions import stage_a_conditions
    from ragbench_lab.config import load_config
    from ragbench_lab.data.preparation import digest
    from ragbench_lab.data.records import DataError
    from ragbench_lab.run_store import verified_manifest
    from ragbench_lab.stage_b import plan_study, planned_requests, validate_study

    config = load_config(ROOT / "configs/stage-a-study.toml")
    conditions = stage_a_conditions(config)
    require(Counter(c.dataset for c in conditions) == {"squad": 30, "hotpot_qa": 30},
            "Stage A factorial differs from 30 per dataset")
    require(len({c.condition_id for c in conditions}) == 60, "duplicate Stage A conditions")
    totals = {}
    for name, expected in (("stage-b-study-v1.json", 14400), ("stage-b-study-v2.json", 14400),
                           ("stage-b-study-v3-reduced.json", 3600),
                           ("stage-b-study-v4-50.json", 7200)):
        path = ROOT / "manifests" / name
        plan = plan_study(config, path)
        require(plan == plan_study(config, path), "non-deterministic Stage B plan")
        require((plan["pipeline_count"], plan["condition_count"], plan["block_count"])
                == (12, 48, 144), "Stage B factorial changed")
        slots = list(planned_requests(plan))
        require(len(slots) == expected == plan["main_requests"], "incorrect request total")
        require(len({r["request_key"] for r in slots}) == expected, "duplicate request slots")
        pairs = defaultdict(list)
        for row in slots:
            pairs[row["pair_key"]].append(row["model_family"])
        require(all(sorted(models) == ["llama", "qwen"] for models in pairs.values()),
                "generator pairing differs")
        study = verified_manifest(path)
        for dataset, source in study["selection"]["sources"].items():
            dev = set(source["split"]["development_ids"])
            require(all(not (dev & set(order[dataset]))
                        for order in plan["question_orders"].values()),
                    "development questions entered evaluation plan")
        totals[name] = len(slots)
    invalid = deepcopy(study)
    invalid["reduced_sample"]["selected_ids"]["squad"][0] = (
        invalid["selection"]["sources"]["squad"]["split"]["development_ids"][0])
    invalid.pop("manifest_sha256")
    invalid["manifest_sha256"] = digest(invalid)
    rejects(lambda: validate_study(config, invalid), DataError,
            "a development ID was accepted into the reduced evaluation sample")
    return {"stage_a_conditions": 60, "stage_b_requests": totals}


def datasets(work: Path) -> dict:
    from ragbench_lab.config import load_config
    from ragbench_lab.data.adapters import hotpot, squad
    from ragbench_lab.data.preparation import inspect_prepared, make_split, prepare
    from ragbench_lab.data.records import DataError

    # Questions/answers are deliberately distinguishable from searchable source text.
    squad_raw = {"version": "1.1", "data": [
        {"title": f"synthetic article {i}", "paragraphs": [
            {"context": "Café 🐈.", "qas": []},
            {"context": "The color is blue.", "qas": [{"id": f"synthetic-s{i}",
                "question": "QUESTION_ONLY color?", "answers": [
                    {"text": "blue", "answer_start": 13}]}]}]} for i in range(4)]}
    hotpot_raw = [{"_id": f"synthetic-h{i}", "question": "QUESTION_ONLY supported?",
        "answer": "ANSWER_ONLY", "context": [
            [f"synthetic source {i}", ["Café 🐈. ", "The second fact."]],
            ["shared distractor", ["Unrelated passage."]]],
        "supporting_facts": [[f"synthetic source {i}", 1]]} for i in range(4)]
    config = load_config(ROOT / "configs/stage-a-study.toml")
    config = replace(config, dataset=replace(config.dataset, development_questions=1,
                                            evaluation_questions=1))
    counts = {}
    for dataset, raw, adapter in (("squad", squad_raw, squad),
                                   ("hotpot_qa", hotpot_raw, hotpot)):
        bundle = adapter(raw)
        require(len(bundle.questions) == 4 and not bundle.exclusions,
                "synthetic valid questions were lost")
        split = make_split(bundle, 1, 1, 17)
        reversed_bundle = replace(bundle, questions=tuple(reversed(bundle.questions)))
        require(split == make_split(reversed_bundle, 1, 1, 17), "split depends on input order")
        require(not (set(split.development_ids) & set(split.evaluation_ids))
                and not split.overlapping_document_ids and not split.overlapping_titles,
                "split isolation failed")
        docs = {d.document_id: d for d in bundle.documents}
        for question in bundle.questions:
            for evidence in question.evidence:
                doc = docs[evidence.document_id]
                require(doc.text[evidence.start:evidence.end] == evidence.text,
                        "Unicode evidence offsets differ from source")
                expected_start = (len("Café 🐈.\n\n") + 13 if dataset == "squad"
                                  else len("Café 🐈. "))
                require(evidence.start == expected_start, "paragraph/sentence offset shifted")
        require(all("QUESTION_ONLY" not in d.text and "ANSWER_ONLY" not in d.text
                    for d in bundle.documents), "evaluation labels entered corpus text")
        source = work / f"{dataset}.json"
        source.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        checksum = hashlib.sha256(source.read_bytes()).hexdigest()
        output = work / dataset
        saved = prepare(config, dataset, source, "synthetic-verification-v1", checksum, output)
        require(inspect_prepared(output)["manifest_sha256"] == saved["manifest_sha256"],
                "prepared artifact roundtrip differs")
        original = (output / "questions.jsonl").read_bytes()
        with (output / "questions.jsonl").open("ab") as stream:
            stream.write(b"{}\n")
        rejects(lambda: inspect_prepared(output), DataError,
                "corrupt prepared questions were accepted")
        require((output / "questions.jsonl").read_bytes() == original + b"{}\n",
                "inspection repaired a corrupt artifact")
        counts[dataset] = len(bundle.questions)
    bad = deepcopy(squad_raw)
    bad["data"][0]["paragraphs"][1]["qas"][0]["answers"][0]["answer_start"] = 0
    excluded = squad(bad)
    require(len(excluded.exclusions) == 1 and len(excluded.questions) == 3,
            "invalid annotation was silently repaired")
    return {"synthetic_questions": counts, "corrupt_inputs_rejected": True}


def chunk_boundaries(_work: Path) -> dict:
    from ragbench_lab.chunking import chunk_document
    from ragbench_lab.data.records import Document

    counter = CharacterCounter()
    doc = Document("synthetic-doc", "squad", "synthetic", "Café 🐈. A longer sentence! End.", ())
    fallback = 0
    for method in ("fixed_token", "sentence_aware"):
        for size in (8, 16):
            result = chunk_document(doc, counter, method, size)
            require("".join(c.text for c in result.chunks) == doc.text,
                    "chunking dropped or duplicated source characters")
            cursor = 0
            for chunk in result.chunks:
                require(chunk.start == cursor and chunk.text == doc.text[chunk.start:chunk.end]
                        and 0 < chunk.reference_tokens <= size, "invalid chunk boundary")
                cursor = chunk.end
            require(cursor == len(doc.text), "chunks did not reach source end")
            fallback += result.fallback_sentences
    require(fallback > 0, "overlong sentence fallback was not exercised")
    return {"profiles": 4, "units": "synthetic Unicode characters"}


def retrieval(_work: Path) -> dict:
    from ragbench_lab.chunking import Chunk
    from ragbench_lab.config import BM25Config
    from ragbench_lab.data.records import DataError
    from ragbench_lab.retrieval import BM25Index, RankedChunk, reciprocal_rank_fusion

    a = Chunk("a", "synthetic-a", 0, 11, "cobalt blue", 11, "fixed_token", 16)
    b = Chunk("b", "synthetic-b", 0, 7, "red red", 7, "fixed_token", 16)
    index = BM25Index([b, a], BM25Config())
    hits = index.search("cobalt", 2)
    require([h.chunk.chunk_id for h in hits] == ["a", "b"] and hits[0].score > 0
            and hits[1].score == 0, "BM25 relevance or zero-score ordering changed")
    a_hit, b_hit = RankedChunk(a, 9), RankedChunk(b, 8)
    fused = reciprocal_rank_fusion([[a_hit, a_hit, b_hit], [b_hit, a_hit]])
    scores = {h.chunk.chunk_id: h.score for h in fused}
    require(len(fused) == 2 and math.isclose(scores["a"], 1 / 61 + 1 / 62)
            and math.isclose(scores["b"], 1 / 63 + 1 / 61), "RRF deduplication/formula differs")
    conflict = RankedChunk(replace(a, text="different"), 1)
    rejects(lambda: reciprocal_rank_fusion([[a_hit], [conflict]]), DataError,
            "conflicting chunk IDs were accepted")
    return {"bm25_candidates": len(hits), "unique_fused_candidates": len(fused)}


def context_and_scoring(_work: Path) -> dict:
    from ragbench_lab.answer_metrics import answer_scores
    from ragbench_lab.chunking import Chunk
    from ragbench_lab.context import pack_context
    from ragbench_lab.data.records import EvidenceSpan, Question
    from ragbench_lab.metrics import evidence_metrics
    from ragbench_lab.retrieval import RankedChunk

    text = "alpha beta gamma"
    chunk = Chunk("a", "synthetic-doc", 20, 20 + len(text), text, len(text), "fixed_token", 32)
    hit = RankedChunk(chunk, 1)
    budget = len("[a]\nalpha beta")
    packed = pack_context([hit, hit], CharacterCounter(), budget)
    require(packed.text == "[a]\nalpha beta" and packed.reference_tokens == budget
            and len(packed.evidence) == 1, "headers, deduplication or context budget differ")
    item = packed.evidence[0]
    require(item.truncated and (item.source_start, item.source_end) == (20, 30)
            and packed.text[item.context_start:item.context_end] == text[:10] == item.text,
            "final truncated source/context offsets differ")
    second = RankedChunk(replace(chunk, chunk_id="b"), .5)
    full = pack_context([hit, hit, second], CharacterCounter(), 100)
    require(full.text == f"[a]\n{text}\n\n[b]\n{text}" and len(full.evidence) == 2
            and full.reference_tokens == len(full.text), "deduplication/separator budget differs")
    blocked = RankedChunk(replace(chunk, chunk_id="a" * 20), 2)
    require(pack_context([blocked, second], CharacterCounter(), 6).text == "",
            "packing skipped a higher-ranked chunk that could not fit")
    late = EvidenceSpan("synthetic-doc", "s", 31, 36, "gamma", "answer")
    question = Question("synthetic-q", "squad", "Which word?", ("gamma",), (late,))
    original_score = evidence_metrics(question, [(chunk.document_id, chunk.start, chunk.end)])
    packed_score = evidence_metrics(question, [
        (item.document_id, item.source_start, item.source_end)])
    require(original_score["evidence_coverage"] == 1 and packed_score["evidence_coverage"] == 0,
            "evidence lost to truncation was credited")
    early = EvidenceSpan("synthetic-doc", "s", 20, 25, "alpha", "sentence")
    hotpot = Question("synthetic-h", "hotpot_qa", "Which facts?", ("yes",),
                      (early, replace(late, kind="sentence")))
    scores = evidence_metrics(hotpot, [("synthetic-doc", 20, 23), ("synthetic-doc", 22, 25)] * 2)
    require(scores["evidence_coverage"] == .5 and not scores["all_required_evidence"],
            "overlapping evidence inflated coverage")
    require(answer_scores("The BLUE!", ("blue",), "squad")
            == {"exact_match": 1., "token_f1": 1.}, "answer normalization differs")
    require(math.isclose(answer_scores("blue sky", ("blue", "green"), "squad")["token_f1"],
                         2 / 3), "answer F1 differs")
    require(answer_scores("yes indeed", ("yes",), "hotpot_qa")["token_f1"] == 0,
            "HotpotQA special-answer scoring differs")
    return {"truncated_evidence_excluded": True, "overlap_deduplicated": True}


def resume_integrity(work: Path) -> dict:
    from ragbench_lab.data.records import DataError
    from ragbench_lab.run_store import RunStore, read_records, request_key, verified_manifest

    directory = work / "synthetic-run"
    identity = {"purpose": "synthetic checkout verification", "config": "a"}
    row = {"kind": "request", "condition_id": "c", "question_id": "q", "repetition": 1,
           "request_key": request_key("c", "q", 1), "attempt": 1, "status": "failed"}
    with RunStore(directory, identity) as store:
        store.append(row)
        rejects(lambda: RunStore(directory, identity, resume=True), DataError,
                "concurrent writer was accepted")
    rejects(lambda: RunStore(directory, {**identity, "config": "b"}, resume=True), DataError,
            "changed resume identity was accepted")
    with RunStore(directory, identity, resume=True) as store:
        require(len(store.rows) == 1 and store.rows[0]["status"] == "failed",
                "resume discarded the failed attempt")
        rejects(lambda: store.append({**row, "attempt": 3}), DataError,
                "nonconsecutive retry was accepted")
        store.append({**row, "attempt": 2, "status": "success"})
        rejects(lambda: store.append({**row, "attempt": 3, "status": "success"}), DataError,
                "duplicate successful request was accepted")
    manifest = verified_manifest(directory / "manifest.json")
    require(len(read_records(directory, manifest)) == 2
            and not (directory / ".writer.lock").exists(), "resume chain/lock differs")
    path = directory / "records.jsonl"
    original = path.read_bytes()
    for damaged in (original.replace(b'"status":"failed"', b'"status":"bogus!"', 1),
                    original + b'{"incomplete":'):
        require(damaged != original, "corruption scenario did not change saved records")
        path.write_bytes(damaged)
        rejects(lambda: RunStore(directory, identity, resume=True), DataError,
                "corrupt chain or incomplete tail was accepted")
        require(path.read_bytes() == damaged and not (directory / ".writer.lock").exists(),
                "corrupt records were repaired or a lock leaked")
    return {"preserved_attempts": 2, "chain_and_tail_corruption_rejected": True}


def public_results(_work: Path) -> dict:
    from verify_public_results import verify

    return verify(ROOT / "results/stage-b-v3")


CHECKS = (configuration, factorials, datasets, chunk_boundaries, retrieval,
          context_and_scoring, resume_integrity, public_results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print one machine-readable summary")
    args = parser.parse_args(argv)
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
    sys.addaudithook(runtime_guard)
    require(not (FORBIDDEN_IMPORTS & sys.modules.keys()), "model dependencies already imported")
    results = []
    with tempfile.TemporaryDirectory(prefix="ragbench-verify-") as temporary:
        for check in CHECKS:
            try:
                work = Path(temporary) / check.__name__
                work.mkdir()
                details = check(work)
                result = {"name": check.__name__, "status": "passed", "details": details}
            except Exception as error:
                result = {"name": check.__name__, "status": "failed",
                          "error": f"{type(error).__name__}: {error}"}
            results.append(result)
            if not args.json:
                print(f"{result['status'].upper()} {result['name']}"
                      + (f": {result['error']}" if "error" in result else ""), flush=True)
    passed = all(r["status"] == "passed" for r in results)
    if args.json:
        print(json.dumps({"schema_version": 1, "status": "passed" if passed else "failed",
                          "checks": results}, sort_keys=True))
    else:
        print(f"{sum(r['status'] == 'passed' for r in results)}/{len(results)} checks passed; "
              "model/tokenizer validation and raw-study replay are separate.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
