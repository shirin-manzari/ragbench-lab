# RAGBench Lab: how it works

The project runs controlled local RAG experiments and keeps the records needed to
check the results. [README.md](README.md) covers setup; [report.md](report.md)
covers the completed study and findings.

## Code map

Paths below are under `src/ragbench_lab/`. Settings live in `configs/`; frozen
study definitions and hashes live in `manifests/`.

| Area                   | Main files                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| Data and evidence      | `data/adapters.py`, `data/preparation.py`, `data/records.py`                             |
| Chunking and retrieval | `chunking.py`, `retrieval.py`, `dense.py`, `embeddings.py`, `pipeline.py`                |
| Generation             | `generation.py`, `reranking.py`, `execution.py`                                          |
| Sessions and records   | `stage_a.py`, `stage_b_runner.py`, `baseline_runner.py`, `run_store.py`                  |
| Analysis               | `analysis.py`, `paired_statistics.py`, `figures.py`, `failure_review.py`, `synthesis.py` |
| Saved-results viewer   | `dashboard_export.py`, `dashboard_snapshot.py`, `dashboard.py`, `dashboard_assets/`      |
| Archives               | `archiving.py`, `delivery.py`                                                            |

## Design choices

Stage A screens retrieval before paying for generation and freezes the embedder
and chunker using development data. Stage B compares twelve pipelines across two
datasets and two generators. Reduced v3 uses 25 questions per dataset; earlier
stopped runs remain separate. [The report](report.md) records the budget amendment
and interpretation limits.

Documents contain source text only. Character offsets survive chunking and
packing, so coverage scores the evidence actually included. Hybrid fuses two
depth-50 searches with RRF constant 60; reranking preserves candidate membership.
The pinned BGE tokenizer controls the 1,024-token context budget, including IDs
and separators. Both generators receive identical evidence, with native prompt
counts and output limits checked separately.

Requests run sequentially in randomized blocks, one generator at a time. Online
latency covers fresh retrieval, reranking, packing and generation; setup, warmup,
cache isolation and scoring are separate. Unload/empty-prompt preload checks zero
prompt reuse, though decoder kernels may still be cold.

Append-only hash chains preserve attempts and failures. Resume checks identities
and skips successes; retries are explicit. Source/model changes need a new
compatible development gate. Quality uses repetition one, while timing repeats
stay within each question; source-cluster intervals account for shared evidence.

## Install and open the dashboard

With the saved snapshot and isolated environment already available:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v3 --port 8050
```

Open http://127.0.0.1:8050. The viewer reads saved results, answers and evidence
without loading models or running experiments. Stop it before timed work.
For offline installation, use the local handoff at `reports/dashboard-handoff-v2/README.md`.
Its wheels were checked on Python 3.14/macOS ARM64; current workspace UI changes
are newer than that package.

## Verify and replay

Keep the raw and analysis ZIPs together under `artifacts/archives/`:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab delivery-verify \
  artifacts/archives/ragbench-analysis-v1.zip \
  --raw-archive artifacts/archives/ragbench-core-v1.zip
```

Follow the local replay guide at `reports/final-delivery-v1/START_HERE.md` in a fresh
checkout. These archives support offline analysis, not a self-contained model
rerun. Git omits data, weights, indexes, tests and generated results.
The local `PROGRESS.md` holds the validation history and unresolved limits.

## AI use

I used AI tools throughout this project to help with planning, coding, debugging, and writing documentation.
