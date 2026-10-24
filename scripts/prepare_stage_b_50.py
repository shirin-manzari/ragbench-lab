from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ragbench_lab.config import load_config  # noqa: E402
from ragbench_lab.data.preparation import digest  # noqa: E402
from ragbench_lab.pipeline import write_new_json  # noqa: E402
from ragbench_lab.run_store import verified_manifest  # noqa: E402
from ragbench_lab.stage_b import reduced_question_ids, validate_study  # noqa: E402


def prepare() -> dict:
    config = load_config(ROOT / "configs/stage-a-study.toml")
    parent = verified_manifest(ROOT / "manifests/stage-b-study-v3-reduced.json")
    validate_study(config, parent)
    if parent["manifest_sha256"] != (
            "60c8fcb5bae6c6a6ea71ca040e491bdbfe44a0863a5a5d61019dc9866022f71c"):
        raise ValueError("expansion requires the unchanged completed v3 study plan")
    study = copy.deepcopy(parent)
    study.update(question_count_per_dataset=50, main_requests=7200,
        reduced_sample={"version": "sha256_dataset_question_rank_50_v1",
            "seed": config.dataset.sampling_seed,
            "selected_ids": reduced_question_ids(parent["selection"],
                                                  config.dataset.sampling_seed, 50)},
        execution_runner="50-question support implemented; fresh development gate pending",
        expansion_lineage={
            "decision_date": "2026-10-17",
            "parent_study_sha256": parent["manifest_sha256"],
            "reason": "user selected 50 evaluation questions per dataset",
            "sampling": "same v3 ID-only hash order, take 50; original 25 included",
            "reuse_policy": "fresh measurements only; no imported or pooled historical rows",
            "scope_status": "post-results expansion, not an untouched confirmatory holdout",
            "historical_metadata": "inherited provenance and feasibility describe parent history",
            "revalidation_required": "fresh compatible 144-request development diagnostic",
            "compute_status": "pending bounded allowance and development gate; no launch",
        },
        baseline_plan={"conditions": ["no_rag", "gold"], "datasets": 2, "models": 2,
            "question_count_per_dataset": 50, "question_policy": "same 50 IDs as main",
            "repetitions": 3, "requests": 1200,
            "status": "pending completed v4 main parent and own 24-request development gate"})
    study["manifest_sha256"] = digest({k: v for k, v in study.items() if k != "manifest_sha256"})
    validate_study(config, study)
    return study


def main() -> None:
    parser = argparse.ArgumentParser(description=(
        'Prepare the ID-only 50-question expansion; never execute model '
        'requests.'
    ))
    parser.add_argument("--output", type=Path,
                        default=ROOT / "manifests/stage-b-study-v4-50.json")
    args = parser.parse_args()
    study = prepare()
    write_new_json(args.output, study)
    print(f"Prepared {args.output}: 7,200 main + 1,200 separate baseline slots; no compute")


if __name__ == "__main__":
    main()
