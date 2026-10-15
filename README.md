# ragbench-lab

An academic study of retrieval-augmented generation (RAG) on one local machine.
It compares retrieval, chunking and reranking choices, then measures their effect
on answer quality and latency.

## Scope

- Datasets: SQuAD v1.1 and an adapted shared-corpus HotpotQA.
- Generators: Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, both Q4_K_M.
- Stage A: five retrieval recipes, two chunkers and three chunk sizes.
- Stage B: BM25, Dense and Hybrid; sizes 128/256; reranking off/on.

The completed matrix contains 9,000 development retrieval requests, 18,000
held-out retrieval requests, 3,600 main generation requests and 600 separate
No-RAG/gold-evidence baseline requests. Pilots and historical attempts are separate.

## Setup

The recorded environment is Python 3.14 on macOS ARM64. The package requires
Python 3.11+, but the supplied locks are not tested across all platforms.

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps -e .
PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/stage-a-study.toml
```

Use `PYTHONPATH=src .venv/bin/python -m ragbench_lab --help` for commands.
New experiments need pinned data, models, indexes and a separate compute allowance.

## Dashboard

With the saved snapshot and isolated dashboard environment available locally:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v3 --port 8050
```

Open http://127.0.0.1:8050. Start with the study overview and metric explanations,
then compare saved configurations, answers and evidence side by side. Original
intervals, question counts and CSV/SVG/PDF downloads remain available.
Longer explanations are under expandable notes.
Stop it before timed experiments. Setup from the offline viewer package is in
[PROJECT_DEEP_DIVE.md](PROJECT_DEEP_DIVE.md#install-and-open-the-dashboard).

## Results

- [report.md](report.md): methods, completed work, results and limitations.
- `reports/stage-b-analysis-v1/`: per-condition scores and paired intervals.
- `reports/stage-b-figures-v1/`: publication figures and stage-time tables.
- `reports/study-synthesis-v1/DISCUSSION.md`: detailed findings and validity.
- `reports/final-delivery-v1/START_HERE.md`: core archive verification and replay.

Reranking increased mean online latency in every matched comparison, but answer
scores did not consistently improve. Model and chunk-size effects varied by dataset;
these results do not identify a universal winning pipeline.

## Limitations

Stage B uses 25 questions per dataset, with source dependence. Three timings per
question are repeated measurements, not independent samples. EM/F1 are text-match
scores, not factuality judgments.
