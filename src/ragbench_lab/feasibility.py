from __future__ import annotations

import argparse
import gc
import json
import resource
import sys
from dataclasses import asdict
from pathlib import Path
from statistics import median
from time import perf_counter

from ragbench_lab.config import load_config
from ragbench_lab.data.preparation import canonical, load_prepared
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import LocalEncoder, prefixed_texts
from ragbench_lab.hardware import collect_inventory
from ragbench_lab.pipeline import profile, write_new_json
from ragbench_lab.retrieval import BM25Index
from ragbench_lab.stage_a import implementation_identity, timestamp
from ragbench_lab.tokenization import ReferenceTokenizer


def sample_positions(count: int, limit: int) -> list[int]:
    """Evenly spaced source-independent positions after sorting by chunk identity."""
    if type(count) is not int or count <= 0 or type(limit) is not int or limit <= 0:
        raise DataError("sample count and limit must be positive integers")
    size = min(count, limit)
    return [i * count // size for i in range(size)]


def project_profile(count: int, chunks_bytes: int, postings_bytes: int,
                    chunking_seconds: float, bm25_seconds: float,
                    encodings: dict) -> dict:
    # Five independently persisted recipes; four vector assets, three postings assets.
    return {
        "index_payload_bytes": 5 * chunks_bytes + 3 * postings_bytes + 4 * (45 + count * 384 * 4),
        "chunking_and_bm25_seconds": 5 * chunking_seconds + 3 * bm25_seconds,
        "corpus_embedding_seconds": sum(
            2 * count * e["seconds_per_chunk"] for e in encodings.values()),
        "excludes": ["manifest bytes", "filesystem overhead", "model/index loading",
                     "serialization/persistence time", "online queries", "raw request records"],
    }


def measure(config_path: Path, data_dirs: dict[str, Path], output: Path,
            models: Path, sample_chunks: int = 64) -> dict:
    if output.exists():
        raise DataError("preflight output exists; choose a new directory")
    if type(sample_chunks) is not int or sample_chunks <= 0:
        raise DataError("encoding sample must be positive")
    config = load_config(config_path)
    if config.embedding is None or set(data_dirs) != set(config.dataset.names):
        raise DataError("preflight requires pinned embedders and all configured datasets")
    output.mkdir(parents=True)
    tokenizer = ReferenceTokenizer(models / "bge-small-en-v1.5/tokenizer.json", config.chunking)
    report = {"schema_version": 1, "purpose": "capacity preflight; not selection or evaluation",
              "created_at": timestamp(), "config_sha256": config.sha256(),
              "provenance": implementation_identity(), "hardware": collect_inventory(),
              "tokenizer": tokenizer.identity, "sample_policy": "evenly spaced sorted chunk IDs",
              "sample_chunks": sample_chunks, "sources": {}, "profiles": [],
              "planned_development_requests": 60 * config.dataset.development_questions * 3,
              "planned_evaluation_requests": 60 * config.dataset.evaluation_questions * 3,
              "limitations": ["sampled encoding throughput can vary with length and thermal load",
                              "index payload projection excludes manifests and filesystem overhead",
                              "peak RSS covers preflight, not accumulated runner history",
                              "no held-out question text or labels used for profiling"]}
    encoders = {family: LocalEncoder(family, models, config.embedding) for family in ("bge", "e5")}
    report["encoders"] = {family: encoder.identity for family, encoder in encoders.items()}
    for dataset, data in data_dirs.items():
        source, bundle = load_prepared(data)
        if (source["dataset"] != dataset
                or len(source["split"]["development_ids"]) != config.dataset.development_questions
                or len(source["split"]["evaluation_ids"]) != config.dataset.evaluation_questions):
            raise DataError("prepared dataset/split differs from preflight config")
        report["sources"][dataset] = {key: source[key] for key in
                                     ("manifest_sha256", "corpus_sha256", "source_revision")}
        for method in config.chunking.methods:
            for size in config.chunking.sizes:
                chunks, stats = profile(bundle.documents, tokenizer, method, size)
                chunks.sort(key=lambda c: c.chunk_id)
                chunks_bytes = sum(len(canonical(asdict(c))) + 1 for c in chunks)
                started = perf_counter()
                bm25 = BM25Index(chunks, config.bm25)
                bm25_seconds = perf_counter() - started
                postings_bytes = len(canonical({"lengths": bm25.lengths,
                    "average_length": bm25.average_length, "postings": bm25.postings})) + 1
                del bm25
                selected = [chunks[i].text for i in sample_positions(len(chunks), sample_chunks)]
                encoding = {}
                for family, encoder in encoders.items():
                    maximum, overlength = 0, []
                    # Inspect every source passage under its native tokenizer before encoding.
                    for start in range(0, len(chunks), 512):
                        group = chunks[start:start + 512]
                        inputs = prefixed_texts(family, [c.text for c in group], "passage")
                        tokens = encoder.tokenizer(inputs, truncation=False, padding=False,
                                                   add_special_tokens=True)
                        for chunk, ids in zip(group, tokens["input_ids"], strict=True):
                            maximum = max(maximum, len(ids))
                            if len(ids) > encoder.maximum:
                                overlength.append({"chunk_id": chunk.chunk_id, "tokens": len(ids)})
                    if overlength:
                        encoding[family] = {"native_tokens_max": maximum,
                                            "overlength": overlength, "seconds_per_chunk": None}
                        continue
                    encoder.encode(selected[:config.embedding.batch_size], "passage")
                    timings = []
                    for _ in range(3):
                        started = perf_counter()
                        encoder.encode(selected, "passage")
                        timings.append(perf_counter() - started)
                    encoding[family] = {"native_tokens_max": maximum, "overlength": [],
                                        "sample_count": len(selected), "sample_seconds": timings,
                                        "seconds_per_chunk": median(timings) / len(selected)}
                row = {"dataset": dataset, "method": method, "size": size,
                       "statistics": stats, "chunks_bytes": chunks_bytes,
                       "postings_bytes": postings_bytes, "bm25_build_seconds": bm25_seconds,
                       "encoding": encoding}
                if all(e["seconds_per_chunk"] is not None for e in encoding.values()):
                    row["projection"] = project_profile(len(chunks), chunks_bytes, postings_bytes,
                                                        stats["chunking_seconds"], bm25_seconds,
                                                        encoding)
                with (output / "profiles.jsonl").open("ab") as stream:
                    stream.write(canonical(row) + b"\n")
                report["profiles"].append(row)
                print(f"{dataset} {method} {size}: {len(chunks)} chunks", flush=True)
                del chunks
                gc.collect()
        del bundle
        gc.collect()
    report["passage_lengths_valid"] = all(not e["overlength"] for row in report["profiles"]
                                         for e in row["encoding"].values())
    if report["passage_lengths_valid"]:
        report["projection"] = {key: sum(row["projection"][key] for row in report["profiles"])
                                for key in ("index_payload_bytes", "chunking_and_bm25_seconds",
                                            "corpus_embedding_seconds")}
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report["measured_peak_rss_bytes"] = peak if sys.platform == "darwin" else peak * 1024
    report["finished_at"] = timestamp()
    write_new_json(output / "summary.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=(
        'Source-only Stage A capacity checks; sampled encoding is a cost '
        'estimate.'
    ))
    parser.add_argument("config", type=Path)
    parser.add_argument("--squad-dir", type=Path, required=True)
    parser.add_argument("--hotpot-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models-dir", type=Path, default=Path("models"))
    parser.add_argument("--sample-chunks", type=int, default=64)
    args = parser.parse_args()
    result = measure(args.config, {"squad": args.squad_dir, "hotpot_qa": args.hotpot_dir},
                     args.output, args.models_dir, args.sample_chunks)
    print(json.dumps({key: result[key] for key in
                      ("passage_lengths_valid", "measured_peak_rss_bytes")}, indent=2))


if __name__ == "__main__":
    main()
