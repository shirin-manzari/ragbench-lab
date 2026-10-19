# ragbench-lab

A local RAG benchmark that compares retrieval, chunking and reranking, then measures
their effect on evidence coverage, answer quality and latency. It includes a CLI,
offline analysis and a read-only results dashboard.

## Current results

The completed **Stage B v4 study** uses 50 questions per dataset: **7,200 main and 1,200
separate baseline requests**, with zero request/setup failures. Stage A remains
unchanged at 9,000 development and 18,000 held-out retrieval requests. Development
gates, pilots and older studies are counted separately.

- Datasets: SQuAD v1.1 and an adapted shared-corpus HotpotQA.
- Generators: Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, both Q4_K_M.
- Stage A: five retrieval recipes, two chunkers and three sizes.
- Stage B: BM25/Dense/Hybrid × sizes 128/256 × reranking off/on.
- Frozen selection: E5 with sentence-aware chunking.

Reranking added 0.13–1.23 seconds to mean online latency; F1 changed by −3.13 to +13.11
percentage points across matched configurations. Effects depend on pipeline, dataset and
generator. [report.md](report.md) has the measured ranges and limitations;
[ARCHITECTURE.md](ARCHITECTURE.md) maps the implementation.

## Setup and CLI

Check a fresh checkout with Python 3.11+, without downloads or ignored fixtures:

```sh
python3 scripts/verify_checkout.py
```

For the recorded Python 3.14/macOS ARM64 benchmark environment:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps -e .
PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/stage-a-study.toml
PYTHONPATH=src .venv/bin/python -m ragbench_lab --help
```

The lockfile is not a claim of a fresh model installation on every platform. Actual
benchmark execution also needs pinned prepared data, models, indexes, a compatible
development gate and an explicitly bounded compute allowance.

Inspect the current study without running model requests:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-b-plan \
  configs/stage-a-study.toml --study manifests/stage-b-study-v4-50.json
```

## Open the dashboard

With the saved snapshot and existing isolated viewer environment:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

Open http://127.0.0.1:8050 to compare saved configurations, answers and evidence. The v4
snapshot contains 176 cells and 2,920 examples across Stage A and Stage B. It reads
saved results only. Stop the viewer before timed experiments.
[PROJECT_DEEP_DIVE.md](PROJECT_DEEP_DIVE.md#install-and-open-the-dashboard) explains
viewer dependencies and installation limits.

## Saved outputs

| Path | Contents |
| --- | --- |
| `reports/stage-b-analysis-v4-50/` | Scores, paired intervals and CSV tables |
| `reports/stage-b-figures-v4-50/` | Six plots in SVG/PDF and stage-time tables |
| `reports/dashboard-snapshot-v4-50/` | Verified read-only viewer data |
| `reports/v4-handoff/START_HERE.md` | Archive verification and replay guidance |
| `artifacts/archives/ragbench-core-v4-50.zip` | Raw records, prepared data and measurement source |
| `artifacts/archives/ragbench-analysis-v4-50.zip` | Later analysis source, checks, reports and snapshot |

Generated assets are local; a normal checkout does not include them. Both v4 ZIPs passed
checksum/member verification, and numerical analysis replay passed using the installed
environment. They exclude weights and index arrays.

Earlier v1/v2/v3 records and archives remain separate. The existing [public aggregate
bundle](results/stage-b-v3/) and local ignored `REPORT_V3.md` still describe v3.
Check that bundle with `python3 scripts/verify_public_results.py`; its exporter remains
specific to v3.

## Interpretation

V4 is a post-results expansion of the existing evaluation pool, with fresh measurements
and no historical aggregate pooling. Its 100 question IDs span 14 SQuAD article clusters
and 50 Hotpot supporting-source components. Repeated timings do not create new
questions. EM/F1 measure text agreement, not factuality. No universal winning pipeline
is established.

[PROGRESS.md](PROGRESS.md) records current evidence; the ignored local history files
retain earlier decisions, failures and checkpoints. Only explicitly selected Markdown
is published; tests, raw runs and archives remain local. AI tools helped with
implementation and writing.
