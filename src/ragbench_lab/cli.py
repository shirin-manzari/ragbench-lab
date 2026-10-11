"""Command-line entry point for ragbench-lab."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from ragbench_lab.config import ConfigError, load_config
from ragbench_lab.hardware import collect_inventory


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ragbench", description="Run controlled local RAG benchmarks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="load and validate an experiment config")
    validate.add_argument("config", help="path to a TOML configuration")

    hardware = subparsers.add_parser("hardware", help="print a local hardware/backend inventory")
    hardware.add_argument("--workspace", default=".", help="path whose disk capacity is reported")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "hardware":
        print(json.dumps(collect_inventory(args.workspace), indent=2, sort_keys=True))
        return 0
    try:
        config = load_config(args.config)
    except ConfigError as error:
        print(f"configuration error: {error}", file=sys.stderr)
        return 2
    print(f"valid configuration: {config.name}")
    print(f"config sha256: {config.sha256()}")
    print("stage a conditions per dataset: 30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
