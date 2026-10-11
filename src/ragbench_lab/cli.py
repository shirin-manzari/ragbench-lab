"""Command-line entry point for ragbench-lab."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from ragbench_lab.config import ConfigError, load_config
from ragbench_lab.data.preparation import inspect_prepared, prepare
from ragbench_lab.data.records import DataError
from ragbench_lab.hardware import collect_inventory


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ragbench", description="Run controlled local RAG benchmarks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="load and validate an experiment config")
    validate.add_argument("config", help="path to a TOML configuration")

    hardware = subparsers.add_parser("hardware", help="print a local hardware/backend inventory")
    hardware.add_argument("--workspace", default=".", help="path whose disk capacity is reported")

    data = subparsers.add_parser("prepare", help="prepare a pinned native dataset JSON file")
    data.add_argument("config", help="experiment TOML configuration")
    data.add_argument("--dataset", required=True, choices=("squad", "hotpot_qa"))
    data.add_argument("--source", required=True, type=Path)
    data.add_argument("--revision", required=True, help="concrete source version/revision")
    data.add_argument("--sha256", required=True, help="expected source file SHA-256")
    data.add_argument("--output", required=True, type=Path, help="new local artifact directory")
    data.add_argument("--pool-limit", type=int, help="first N HotpotQA validation rows")
    data.add_argument("--allow-source-overlap", action="store_true",
                      help="explicitly allow and record shared evidence documents/article titles")
    inspect = subparsers.add_parser("inspect-data", help="verify prepared hashes, evidence, and splits")
    inspect.add_argument("directory", type=Path)
    for name, help_text in (
        ("chunks", "inspect all six chunk profiles"),
        ("index", "build source chunks and a BM25 index artifact"),
        ("retrieve", "retrieve and score a development question with BM25"),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("config")
        command.add_argument("--data-dir", required=True, type=Path)
        command.add_argument("--tokenizer-json", type=Path,
                             default=Path("models/bge-small-en-v1.5/tokenizer.json"))
        command.add_argument("--output", required=True, type=Path)
        if name in {"chunks", "index"}:
            command.add_argument("--document-limit", type=int,
                                 help="source-order prefix; diagnostic-only smaller corpus")
        if name == "index":
            command.add_argument("--method", choices=("fixed_token", "sentence_aware"), required=True)
            command.add_argument("--size", type=int, choices=(64, 128, 256), required=True)
        if name == "retrieve":
            command.add_argument("--index", required=True, type=Path)
            command.add_argument("--question-id", help="development ID; defaults to first saved ID")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "hardware":
        print(json.dumps(collect_inventory(args.workspace), indent=2, sort_keys=True))
        return 0
    try:
        if args.command == "inspect-data":
            manifest = inspect_prepared(args.directory)
            print(f"valid prepared dataset: {manifest['dataset']}")
            print(f"manifest sha256: {manifest['manifest_sha256']}")
            return 0
        config = load_config(args.config)
        if args.command in {"chunks", "index", "retrieve"}:
            from ragbench_lab.pipeline import build_index, chunk_profiles, retrieve

            if args.command == "chunks":
                result = chunk_profiles(config, args.data_dir, args.tokenizer_json,
                                        args.output, args.document_limit)
                print(f"saved {len(result['profiles'])} chunk profiles to {args.output}")
            elif args.command == "index":
                result = build_index(config, args.data_dir, args.tokenizer_json, args.method,
                                     args.size, args.output, args.document_limit)
                print(f"indexed {result['statistics']['chunk_count']} chunks into {args.output}")
            else:
                result = retrieve(config, args.data_dir, args.index, args.tokenizer_json,
                                  args.question_id, args.output)
                print(json.dumps({"question_id": result["question_id"],
                                  "context_tokens": result["context"]["reference_tokens"],
                                  "metrics": result["metrics"], "output": str(args.output)}, indent=2))
            return 0
        if args.command == "prepare":
            manifest = prepare(config, args.dataset, args.source, args.revision, args.sha256,
                               args.output, args.pool_limit, args.allow_source_overlap)
            summary = {key: manifest[key] for key in (
                "dataset", "document_count", "eligible_question_count", "exclusion_count",
                "source_sha256", "corpus_sha256", "manifest_sha256", "split",
            )}
            summary["output"] = str(args.output)
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
    except ConfigError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2
    except (DataError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"data preparation error: {error}", file=sys.stderr)
        return 2
    print(f"valid configuration: {config.name}")
    print(f"config sha256: {config.sha256()}")
    print("stage a conditions per dataset: 30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
