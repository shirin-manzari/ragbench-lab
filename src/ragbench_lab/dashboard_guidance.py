"""Presentation-only explanations and descriptive facts from a single saved run."""

METRIC_HELP = {
    "token_f1": "Token F1 measures normalized word overlap with reference answers. "
    "Higher overlap is not proof of factual correctness or grounding.",
    "exact_match": "Exact match is the fraction matching a normalized reference answer. "
    "Correct but more verbose answers can receive zero.",
    "evidence_coverage": "Packed annotated coverage measures dataset-labeled evidence "
    "inside the exact context sent to the generator. It is not semantic sufficiency.",
    "abstention": "Abstention rate counts the declared exact abstention sentinel. "
    "Other wording expressing uncertainty may not be counted; higher is not always better.",
    "output_truncation": "Output truncation rate counts saved outputs stopped at the "
    "generation limit. It does not measure answer correctness.",
    "latency_mean": "Mean online latency averages successful request times. Setup, "
    "cache isolation and scoring are excluded; this is not total session duration.",
    "latency_median": "Median latency is the middle successful online request time. "
    "Stage A measures retrieval only; Stage B includes generation.",
    "latency_p95": "95th percentile latency describes the slow tail, not a worst-case "
    "guarantee. Small samples make tail estimates fragile.",
}

UNCERTAINTY_HELP = (
    "95% bootstrap intervals describe sampling uncertainty under the recorded resampling "
    "scheme, not a 95% chance that a pipeline wins. Stage B uses source-cluster intervals; "
    "Stage A uses question clusters without adjusting source dependence. Intervals are "
    "descriptive and unadjusted for multiple comparisons. Use original paired-difference "
    "intervals, not overlap of separate cell intervals, to examine a saved contrast. "
    "Unavailable intervals are not zero uncertainty."
)


def observations(run: dict) -> list[str]:
    """No cross-run pooling, ranking, bootstrap or new quality measurements."""
    cells = run["cells"]
    if run["stage"] != "B":
        return [
            "Stage A measures retrieval, not generated-answer quality."
            if run["stage"] == "A"
            else "Baselines are separate diagnostics, not additional factorial pipelines.",
            "The charts retain all saved configurations; unavailable values stay unavailable.",
            "These observations apply only to the selected run, not to an unrun extension.",
        ]
    pairs = [p for p in run["paired_contrasts"] if p["contrast"] == "reranking_on_minus_off"]
    timing = [p["metrics"].get("latency_mean", {}).get("estimate") for p in pairs]
    timing = [v for v in timing if v is not None]
    f1 = [p["metrics"].get("token_f1", {}).get("estimate") for p in pairs]
    f1 = [v for v in f1 if v is not None]
    groups = sorted({(c["dataset"], c.get("model_family")) for c in cells})
    ranges = []
    for dataset, model in groups:
        values = [
            c["metrics"].get("token_f1", {}).get("estimate")
            for c in cells
            if (c["dataset"], c.get("model_family")) == (dataset, model)
        ]
        values = [v for v in values if v is not None]
        if values:
            ranges.append(f"{dataset}/{model}: {min(values)*100:.2f}–{max(values)*100:.2f}%")
    return [
        f"Higher mean latency with reranking: "
        f"{sum(v > 0 for v in timing)}/{len(timing)} saved pairs."
        if timing else "No saved reranking latency contrast is available.",
        f"Reranking F1 differences: {sum(v > 0 for v in f1)} positive, "
        f"{sum(v < 0 for v in f1)} negative, {sum(v == 0 for v in f1)} zero. "
        if f1 else "No saved reranking F1 contrast is available.",
        "F1 ranges (not confidence intervals): " + "; ".join(ranges)
        if ranges else "F1 is unavailable in this run.",
    ]


def comparable_cells(run: dict, left_id: str | None) -> list[dict]:
    left = next((c for c in run["cells"] if c["condition_id"] == left_id), None)
    return [
        c for c in run["cells"]
        if left and c["dataset"] == left["dataset"] and c["condition_id"] != left_id
    ]


def shared_examples(run: dict, left_id: str, right_id: str) -> list[dict]:
    if right_id not in {c["condition_id"] for c in comparable_cells(run, left_id)}:
        return []
    right = {e["question_id"] for e in run["examples"] if e["condition_id"] == right_id}
    return [e for e in run["examples"]
            if e["condition_id"] == left_id and e["question_id"] in right]
