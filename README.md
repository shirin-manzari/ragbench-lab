# ragbench-lab

A local benchmark for understanding how retrieval, chunking and reranking affect
retrieval-augmented generation. It measures the evidence a pipeline finds, the answer
it produces and the time each request takes. The project includes a Python CLI,
reproducible experiment definitions, public results and a read-only dashboard.

## The benchmark

The study compares **twelve RAG pipelines** on SQuAD and an adapted HotpotQA shared
corpus, using Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct. Both generators use
Q4_K_M quantization and receive identical evidence for each matched pipeline/question.

| Choice | Settings |
| --- | --- |
| Retrieval | BM25, Dense, Hybrid |
| Chunk size | 128 or 256 reference tokens |
| Reranking | Off or on |
| Embeddings and chunking | E5 and sentence-aware chunking, selected on development data |
| Evidence budget | 1,024 reference tokens |
| Answer limit | 64 native output tokens |

The completed answering evaluation contains **7,200 main requests and 1,200 separate
No-RAG/gold-evidence baseline requests**, with zero request/setup failures. These
measurements cover **100 distinct question IDs**, with three timing repetitions.
Answer quality uses the first repetition; repeats do not create independent questions.

Reranking added **0.13–1.23 seconds** to mean online latency. Token F1 changed by
**−3.13 to +13.11 percentage points**, depending on the pipeline, dataset and generator.
The results show trade-offs rather than one universally best configuration.

[The study report](report.md) explains the findings and limitations.
[The architecture guide](ARCHITECTURE.md) maps the implementation, and
[the project deep dive](PROJECT_DEEP_DIVE.md) explains the methods and controls.

## Explore the results

The [public results bundle](results/stage-b-v4/) contains aggregate CSVs, three SVG
figures and a checksum manifest. It includes no question/answer text or source passages.
Verify it from a checkout using Python 3.11+, without installing packages or models:

```sh
python3 scripts/verify_public_results.py results/stage-b-v4
```

Join `cells.csv` and `contrasts.csv` to `conditions.csv` by condition ID. Scores use
fractions, latency uses seconds, and paired differences are left minus right.

For an offline presentation, build a standalone HTML document from the public results:

```sh
python3 scripts/build_results_demo.py
```

Open `presentations/stage-b-v4.html` in a browser. It embeds the plots, includes speaker
notes and prints to PDF. The builder refuses to overwrite an existing file; use
`--check` to verify it or `--output NEW_PATH` to create another copy.
Presentation outputs stay local.

## Open the dashboard

With the saved local snapshot and existing viewer environment:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

Open http://127.0.0.1:8050 to compare recorded configurations, answers and packed
evidence. The dashboard reads saved results; it does not run inference. The snapshot
and optional viewer environment are local assets, separate from the public bundle.
[Viewer setup](PROJECT_DEEP_DIVE.md#install-and-open-the-dashboard) explains the requirements.

## Setup and CLI

Check the source checkout without downloading models:

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

The CLI provides data preparation, indexing, bounded experiment execution and offline
analysis. The lockfile records the measured environment; a complete rerun also needs
pinned data, model assets, indexes and a compatible development validation run.
[The deep dive](PROJECT_DEEP_DIVE.md#running-and-reproducing-the-study) covers those controls.

## Interpretation

EM and token F1 measure reference-text agreement, not factual correctness. Evidence
coverage uses source annotations and does not guarantee semantic sufficiency. The
sample was expanded after earlier results were inspected, using fresh measurements
without pooling earlier records; it is not an untouched confirmatory holdout.

The 100 questions span 14 SQuAD article clusters and 50 Hotpot supporting-source
components. Source dependence, adapted corpora and sequential timing on one machine
limit generalization. Concurrency and alternative model/context settings were not
measured. AI tools assisted implementation and writing.
