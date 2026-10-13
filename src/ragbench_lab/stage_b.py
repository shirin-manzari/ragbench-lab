"""Validate the frozen scientific study and enumerate its prospective execution plan.

Planning never loads model weights, reads answers, starts a server, or runs queries.
Execution provenance and safe resumption belong to the subsequent runner task.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path

from ragbench_lab.conditions import Condition
from ragbench_lab.config import ExperimentConfig, _validate
from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.generation import INSTRUCTION, GeneratorSettings
from ragbench_lab.reranking import RerankerSettings
from ragbench_lab.run_store import request_key, verified_manifest
from ragbench_lab.selection import validate_freeze


def _verify_hash(record: dict, label: str) -> None:
    if not isinstance(record, dict):
        raise DataError(f"{label} must be a manifest object")
    body = {key: value for key, value in record.items() if key != "manifest_sha256"}
    if digest(body) != record.get("manifest_sha256"):
        raise DataError(f"{label} manifest identity mismatch")


def _ids(source: dict) -> dict[str, list[str]]:
    splits = source["split"]
    for name, count in (("development_ids", 50), ("evaluation_ids", 100)):
        ids = splits[name]
        if (not isinstance(ids, list) or len(ids) != count
                or any(not isinstance(qid, str) or not qid for qid in ids)
                or len(set(ids)) != count):
            raise DataError("Stage B requires unique, nonempty frozen 50/100 split IDs")
    if set(splits["development_ids"]) & set(splits["evaluation_ids"]):
        raise DataError("development and held-out question IDs overlap")
    return splits


def reduced_question_ids(selection: dict, seed: int) -> dict[str, list[str]]:
    """Rank only frozen IDs, never answers, saved outcomes, or execution order."""
    return {dataset: sorted(sorted(source["split"]["evaluation_ids"],
        key=lambda qid: digest(["stage-b-reduced-25-v1", seed, dataset, qid]))[:25])
        for dataset, source in sorted(selection["sources"].items())}


def evaluation_question_ids(study: dict) -> dict[str, list[str]]:
    if "reduced_sample" in study:
        return study["reduced_sample"]["selected_ids"]
    return {dataset: sorted(source["split"]["evaluation_ids"])
            for dataset, source in study["selection"]["sources"].items()}


def validate_study(config: ExperimentConfig, study: dict) -> None:
    """Check scientific consistency, not the presence of local model/data assets."""
    _validate(config)
    _verify_hash(study, "Stage B study")
    try:
        if (study["kind"] != "frozen_generation_study_plan" or study["schema_version"] != 1
                or digest(study["config"]) != config.sha256()
                or config.embedding is None):
            raise DataError("Stage B study/config mismatch")
        reduced = "reduced_sample" in study
        count = 25 if reduced else 100
        for key, expected in (("pipeline_count", 12), ("dataset_model_conditions", 48),
                              ("main_requests", 144 * count), ("question_count_per_dataset", count),
                              ("repetitions", 3)):
            if type(study[key]) is not int or study[key] != expected:
                raise DataError(f"unsupported Stage B count: {key}")
        if (set(config.dataset.names) != {"squad", "hotpot_qa"}
                or config.dataset.development_questions != 50
                or config.dataset.evaluation_questions != 100):
            raise DataError("Stage B requires the complete two-dataset 50/100 study")
        selection = study["selection"]
        _verify_hash(selection, "Stage A selection")
        validate_freeze(selection)
        if (selection["config_sha256"] != config.sha256()
                or set(selection["sources"]) != set(config.dataset.names)):
            raise DataError("frozen selection differs from Stage B config/datasets")
        for dataset, source in selection["sources"].items():
            splits = _ids(source)
            if splits["seed"] != config.dataset.sampling_seed:
                raise DataError(f"frozen sampling seed mismatch: {dataset}")
        if reduced:
            sample = study["reduced_sample"]
            if (set(sample) != {"version", "seed", "selected_ids"}
                    or sample["version"] != "sha256_dataset_question_rank_v1"
                    or type(sample["seed"]) is not int
                    or sample["seed"] != config.dataset.sampling_seed
                    or sample["selected_ids"] != reduced_question_ids(selection, sample["seed"])):
                raise DataError("reduced sample must match the frozen outcome-blind 25-ID rule")
        expected_profiles = [
            {"family": family, "size": size, "reranking": on}
            for family, size, on in product(("bm25", "dense", "hybrid"),
                                            (128, 256), (False, True))
        ]
        profiles = study["pipeline_profiles"]
        if (not isinstance(profiles, list) or len(profiles) != 12
                or any(not isinstance(p, dict)
                       or set(p) != {"family", "size", "reranking"}
                       or type(p["size"]) is not int or type(p["reranking"]) is not bool
                       for p in profiles)
                or {digest(p) for p in profiles} != {digest(p) for p in expected_profiles}):
            raise DataError("Stage B requires the exact twelve unique factorial profiles")
        if set(study["generator_settings"]) != {"qwen", "llama"}:
            raise DataError("Stage B requires both frozen generators")
        generators = [GeneratorSettings(**settings)
                      for settings in study["generator_settings"].values()]
        if (len({g.model_digest for g in generators}) != 2
                or any(g.seed != config.dataset.sampling_seed or g.threads != 4
                       or g.context_window != 4096 or g.maximum_output_tokens != 64
                       or g.quantization != "Q4_K_M" for g in generators)):
            raise DataError("unsupported frozen generator settings")
        if len({(g.backend_version, g.template_date) for g in generators}) != 1:
            raise DataError("paired generators require a shared backend and template date")
        RerankerSettings(**study["reranker"])
        if (study["instruction"] != INSTRUCTION
                or study["instruction_sha256"] != digest(INSTRUCTION)
                or study["cache_policy"] != "unload_then_empty_prompt_preload_per_request"
                or study["execution_environment"] != {
                    "loaded_model_limit": 1, "model_parallelism": 1,
                    "tokenizers_parallelism": "false"}):
            raise DataError("frozen prompt/cache/execution controls are unsupported")
        feasibility = study["feasibility"]
        if (feasibility["freeze_ready"] is not True or feasibility["complete"] is not True
                or type(feasibility["successful_requests"]) is not int
                or feasibility["successful_requests"] != 40
                or feasibility["failed_requests"] != 0
                or feasibility["memory_sampling_valid"] is not True
                or feasibility["run_manifest_sha256"] != study["pilot_manifest_sha256"]):
            raise DataError("study lacks a passing linked feasibility pilot")
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        if isinstance(error, DataError):
            raise
        raise DataError(f"invalid frozen Stage B study: {error}") from error


@dataclass(frozen=True)
class StageBCondition:
    dataset: str
    model_family: str
    model_digest: str
    family: str
    recipe: str
    method: str
    size: int
    reranking: bool
    study_sha256: str

    @property
    def condition_id(self) -> str:
        return digest(asdict(self))

    @property
    def pipeline_id(self) -> str:
        return digest({key: getattr(self, key) for key in
                       ("family", "recipe", "method", "size", "reranking", "study_sha256")})

    @property
    def retrieval_condition_id(self) -> str:
        # Reranking/generator settings never change the initial retrieval index.
        return Condition(self.dataset, self.recipe, self.method, self.size).condition_id

    def record(self) -> dict:
        return {**asdict(self), "condition_id": self.condition_id,
                "pipeline_id": self.pipeline_id,
                "retrieval_condition_id": self.retrieval_condition_id}


def stage_b_conditions(config: ExperimentConfig, study: dict) -> list[StageBCondition]:
    validate_study(config, study)
    selected = study["selection"]["selected"]
    conditions = []
    for dataset, model, profile in product(sorted(config.dataset.names),
            sorted(study["generator_settings"]), sorted(study["pipeline_profiles"], key=digest)):
        family = profile["family"]
        recipe = "bm25" if family == "bm25" else f"{family}_{selected['embedder']}"
        conditions.append(StageBCondition(dataset, model,
            study["generator_settings"][model]["model_digest"], family, recipe,
            selected["chunker"], profile["size"], profile["reranking"], study["manifest_sha256"]))
    return conditions


def execution_plan(config: ExperimentConfig, study: dict) -> dict:
    conditions = stage_b_conditions(config, study)
    seed = config.dataset.sampling_seed
    questions = evaluation_question_ids(study)
    blocks = []
    orders = {}
    for repetition in (1, 2, 3):
        orders[str(repetition)] = {
            dataset: sorted(ids, key=lambda qid: digest([seed, repetition, dataset, qid]))
            for dataset, ids in sorted(questions.items())
        }
        # Randomized model groups load one generator at a time. Conditions within
        # each group are randomized; request work is still sequential, not cached.
        models = sorted(study["generator_settings"],
                        key=lambda model: digest([seed, repetition, "model", model]))
        for model in models:
            group = [c for c in conditions if c.model_family == model]
            for condition in sorted(group,
                    key=lambda c: digest([seed, repetition, c.condition_id])):
                blocks.append({"condition_id": condition.condition_id,
                               "model_family": model, "repetition": repetition,
                               "question_order_dataset": condition.dataset})
    plan = {"kind": "stage_b_execution_plan", "schema_version": 1,
            "study_sha256": study["manifest_sha256"], "config_sha256": config.sha256(),
            "runner_status": "pending; enumeration is not an execution manifest",
            "scientific_selection": study["selection"]["selected"],
            "pipeline_count": 12, "condition_count": len(conditions),
            "block_count": len(blocks), "main_requests": study["main_requests"],
            "quality_repetition": 1, "repetitions": 3,
            "independent_questions_per_dataset": study["question_count_per_dataset"],
            "conditions": [c.record() for c in conditions], "blocks": blocks,
            "question_orders": orders,
            "pairing": "same pipeline/dataset/question/repetition across both generators",
            "baseline_policy": "no_rag and gold are separate from the main matrix"}
    plan["manifest_sha256"] = digest(plan)
    return plan


def planned_requests(plan: dict):
    """Yield identities only: no generated answers or precomputed query results."""
    conditions = {c["condition_id"]: c for c in plan["conditions"]}
    for block in plan["blocks"]:
        condition = conditions[block["condition_id"]]
        repetition = block["repetition"]
        for qid in plan["question_orders"][str(repetition)][condition["dataset"]]:
            yield {"condition_id": condition["condition_id"], "question_id": qid,
                   "dataset": condition["dataset"], "model_family": condition["model_family"],
                   "repetition": repetition,
                   "request_key": request_key(condition["condition_id"], qid, repetition),
                   "pair_key": digest([condition["pipeline_id"], condition["dataset"],
                                       qid, repetition]),
                   "candidate_pair_key": digest([condition["retrieval_condition_id"],
                                                  qid, repetition])}


def plan_study(config: ExperimentConfig, study_path: Path) -> dict:
    return execution_plan(config, verified_manifest(study_path))
