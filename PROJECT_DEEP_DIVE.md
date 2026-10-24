# RAGBench Lab: how it works

RAGBench Lab studies the cost and quality of retrieval-augmented generation on one
local machine. It connects source-preserving chunking, lexical and neural retrieval,
optional reranking, local generation and offline analysis. The same saved records
support numerical comparisons, evidence inspection and a read-only dashboard.

## The study

The research question is how retrieval, chunk size and reranking affect evidence
coverage, answer quality and online latency. The datasets are SQuAD v1.1 and an
adapted shared-corpus HotpotQA; the generators are Qwen2.5-3B-Instruct and
Llama-3.2-3B-Instruct, both Q4_K_M.

The answering experiment compares BM25, Dense and Hybrid retrieval, chunk sizes
128/256 and reranking off/on. That gives twelve pipelines, or 48 conditions across
the two datasets and two generators. Each condition uses 50 questions and three
timing repetitions; the first repetition supplies the answer-quality observation.

The completed evaluation contains 7,200 main and 1,200 separate diagnostic baseline
requests over 100 distinct question IDs, with zero request/setup failures. Models run
sequentially through a dedicated local Ollama backend. Concurrent serving capacity is
outside the measurements.

### Selecting retrieval components

Before evaluating full answering pipelines, retrieval screening compares five recipes:
BM25, Dense–BGE, Dense–E5, Hybrid–BGE and Hybrid–E5. Each uses fixed-token or
sentence-aware chunking at 64, 128 or 256 reference tokens, with zero overlap and
reranking disabled. The matrix has 30 conditions per dataset.

Development-only selection averages packed evidence coverage equally across datasets
and the declared Dense/Hybrid size conditions. Candidates within one absolute
percentage point are compared by retrieval latency, then indexing cost and the
deterministic final tie-break. E5 and sentence-aware chunking were selected and frozen
before held-out retrieval evaluation.

Screening completed 9,000 development and 18,000 held-out retrieval requests.
Development/evaluation pools contain 50/100 questions per dataset. These retrieval
measurements are separate from the answering experiment; they do not establish an
end-to-end answer-quality ranking of every embedder and chunker.

### Sample and interpretation

The final answering sample contains 50 IDs per dataset from a deterministic ID-only
ranking. It was expanded after earlier results were inspected. All reported answering
measurements were freshly collected without importing earlier aggregates, but the
sample is not an untouched confirmatory holdout.

The 100 IDs span 14 SQuAD article clusters and 50 Hotpot supporting-source components.
Repeated timings do not create new question samples. Source dependence and the
single-host setting limit generalization, particularly for tail latency.

## Repository map

| Path | Responsibility |
| --- | --- |
| `src/ragbench_lab/` | CLI, algorithms, runners and offline analysis |
| `configs/` | Experiment settings and execution/analysis protocols |
| `manifests/` | Frozen data, model, selection and study identities |
| `results/stage-b-v4/` | Public aggregate results and figures |
| `data/`, `models/`, `indexes/` | Local input assets and derived search indexes |
| `runs/` | Append-only raw requests and run manifests |
| `reports/` | Local analysis, figures, reviews and dashboard snapshots |
| `artifacts/` | Local archives, verification proofs and environments |

[cli.py](src/ragbench_lab/cli.py) exposes `ragbench` and `python -m ragbench_lab`.
Configuration is separate from algorithms; unsupported combinations fail validation.
The [architecture guide](ARCHITECTURE.md) maps individual modules and their dependencies.

## Source text and evidence mappings

[The adapters](src/ragbench_lab/data/adapters.py) keep questions, reference answers
and supporting annotations outside searchable corpus text. The explicit gold-evidence
baseline is the only path that uses annotations to construct generation context.

For SQuAD, paragraphs are joined in article order and answer spans are mapped into the
reconstructed document. These documents are assembled from the dataset rather than
full Wikipedia articles. For HotpotQA, context passages are deduplicated into a shared
corpus searched by every question, with title variants handled explicitly.

[Preparation](src/ragbench_lab/data/preparation.py) preserves source revisions,
hashes, exclusions and split identities. Question IDs are disjoint across development
and evaluation, with remaining source overlap recorded. The Hotpot corpus is adapted;
official-byte equivalence of its pinned mirror remains unverified.

Offsets are zero-based Python character indices with exclusive ends. Evidence can be
traced from original paragraphs/sentences to chunks and then to packed context.
Coverage therefore measures the supplied text rather than merely checking retrieved IDs.

## Chunking and retrieval

[Chunking](src/ragbench_lab/chunking.py) uses one pinned BGE reference tokenizer to
keep boundaries independent of the embedder and generator. Fixed-token windows are
non-overlapping. Sentence-aware chunking packs complete sentences where possible and
splits overlong sentences with the fixed-token fallback, retaining exact source slices.

[BM25](src/ragbench_lab/retrieval.py) ranks lexical matches through a postings index.
Dense retrieval uses pinned BGE or E5 encoder assets, model-specific prefixes/pooling,
normalized vectors and [exact FAISS search](src/ragbench_lab/dense.py). Token lengths
are checked under each encoder's actual tokenizer so input truncation is detected.

Hybrid retrieval combines BM25 and Dense ranks with reciprocal rank fusion:

```text
RRF(chunk) = sum(1 / (60 + rank_in_each_list))
```

Each constituent retriever returns up to 50 candidates. Hybrid fuses their union and
keeps the best 50 unique chunk IDs, so its initial search work can exceed a single
retriever's. Duplicate chunk IDs must not receive repeated credit within one list.

[The reranker](src/ragbench_lab/reranking.py) scores question/passage pairs using
pinned `cross-encoder/ms-marco-MiniLM-L6-v2` assets. It reorders the same initial
candidates used by the corresponding off condition and detects pair truncation.
The measured cost includes this extra online work.

Indexes contain source chunk records plus lexical postings or Dense vectors.
[Loaders](src/ragbench_lab/pipeline.py) check their corpus, tokenizer, configuration
and model identities. Index reuse is allowed; measured requests still perform fresh
query embedding, search and fusion.

## Packing and generation

[Context packing](src/ragbench_lab/context.py) follows candidate rank order within a
1,024-reference-token budget, counting identifiers and separators. Only the final
included chunk may be partial. Both source offsets and packed-context offsets remain
available after truncation, and evidence scores use the included portions.

The generators receive identical evidence text for each matched question/pipeline.
Their native token counts can differ, so [generation](src/ragbench_lab/generation.py)
checks each full prompt plus the 64-token output allowance against the configured
window. Prompt overflow is rejected rather than silently truncated.

Generation uses temperature zero, pinned artifacts, native chat templates and tokenizer
identities. A short-answer instruction requires grounding in evidence and specifies an
abstention sentinel. Deterministic settings do not guarantee identical outputs on every
backend; output instability and truncation are recorded.

### Cache, timing and memory

[Serving controls](src/ragbench_lab/serving.py) unload/preload models and require
explicit zero cached-prompt counts. Warm model weights are distinct from reusing a
response's computation, and preloaded weights do not establish warm decoder kernels.

The online timer covers query embedding, search/fusion, reranking, packing and
generation. Setup, warmup, cache isolation, scoring and record writes are excluded.
Some instrumentation, including candidate serialization and hashing, remains inside
the measured function. Online latency is therefore different from session wall time.

[Resource sampling](src/ragbench_lab/resources.py) includes the Python worker and
dedicated backend process tree. Unified-memory/GPU counters may overlap process RSS;
these values should not be added as though they represented independent memory pools.

### Diagnostic baselines

No-RAG supplies empty evidence while retaining the grounded-answer instruction.
It measures the empty-evidence control rather than unrestricted parametric knowledge.
Gold context is built from diagnostic SQuAD paragraphs or Hotpot supporting sentences.

[The baseline runner](src/ragbench_lab/baseline_runner.py) constructs and packs context
afresh, then generates without retrieval/reranking. Gold context may truncate at the
common budget and is not a guaranteed numerical upper bound. The two baselines remain
outside the twelve-pipeline factorial, with separately labeled timing paths.

## Records, failures and resume

[RunStore](src/ragbench_lab/run_store.py) writes immutable run manifests and
append-only JSONL records linked by hashes. Each request key combines condition,
question and repetition. An exclusive lock prevents simultaneous writers.

Resume requires compatible source, environment, configuration, model, tokenizer and
index identities. Corrupt chains, partial tails and duplicate successes fail validation.
Failures and retries remain visible; explicit retries append attempts instead of
rewriting unsuccessful records.

Execution uses explicitly bounded request sessions. Main evaluation requires a
compatible failure-free 144-request development gate; baselines require a separate
24-request gate and a completed main parent. A new runner identity or changed study
requires fresh validation before additional compute.

## Scores and uncertainty

[Answer scoring](src/ragbench_lab/answer_metrics.py) reports normalized Exact Match
and token F1. These measure reference-text agreement, not factual correctness.
An answer can contain the correct fact and lose exact-match credit through extra words.

[Evidence scoring](src/ragbench_lab/metrics.py) uses source annotations. SQuAD checks
annotated answer-span coverage, with supporting-paragraph coverage separately available.
Hotpot measures the fraction of supporting sentences covered and whether all required
annotations are present. Overlapping chunks must not inflate coverage.

Top-5/10/50 coverage describes the ranked candidate list; packed coverage describes
the evidence actually supplied. Complete annotations do not establish semantic
sufficiency, and missing annotations do not prove the answer was impossible.

[Paired analysis](src/ragbench_lab/paired_statistics.py) keeps timing repetitions
within question units. Primary answering intervals use 2,000 paired source-cluster
bootstrap draws over 14 SQuAD and 50 Hotpot components, with question-cluster
sensitivity also reported. They are 95% percentile intervals, unadjusted for multiple
comparisons. Retrieval-screening uncertainty uses its own reporting procedure.

Use stored paired intervals to assess differences. Counts of positive/negative point
changes are descriptive signs, not counts of statistically significant wins.

## Results and failure diagnostics

The [study report](report.md) gives the measured quality/latency ranges and baseline
scores. Reranking added 0.13–1.23 seconds across 24 matched comparisons and changed F1
by −3.13 to +13.11 percentage points. Effects vary with dataset, generator and pipeline.

An exploratory saved-response analysis found 404 exact matches among 2,400
first-repetition main responses. Of the 1,996 non-exact responses, 396 had incomplete
top-50 annotations, 285 lost complete candidate evidence during packing, and 1,315
had complete packed annotations. The last group includes 412 zero-F1 responses;
it is not a count of factually wrong answers.

Local reports are `reports/stage-b-failure-diagnostics-v4-50/REPORT.md` and
`reports/stage-b-failure-review-v4-50/REVIEW.md`. Six deterministic paired examples
illustrate evidence bottlenecks and answer/scoring mismatches. Notes are agent-authored,
not independently adjudicated; no new generation was required.

## Public results and local artifacts

The [public bundle](results/stage-b-v4/) contains a condition lookup, the original
cell/contrast/timing CSVs and three unchanged SVG figures. Its unsigned manifest records
source hashes, units, counts and limitations. Question IDs, raw answers, passages and
personal machine provenance are excluded.

```sh
python3 scripts/verify_public_results.py results/stage-b-v4
python3 scripts/build_results_demo.py
```

The verifier uses only the standard library and requires no ignored assets. It checks
hashes, complete matrices, units, interval bounds, contrast arithmetic and reconstruction
of online timing means. It does not audit raw records or recompute bootstraps.

The presentation builder creates `presentations/stage-b-v4.html` from the public
bundle alone, with embedded original SVGs and speaker notes. It refuses existing output;
`--check` compares an existing presentation without writing. Local `DEMO.md` provides
a five-minute walkthrough and fallback steps.

Re-exporting aggregates requires the checked local analysis, figures and proof:

```sh
python3 scripts/export_public_results.py --study v4 --check
```

Use the explicit study selector and paths shown here to target the saved measurements.

| Local path | Contents |
| --- | --- |
| `reports/stage-b-analysis-v4-50/` | 56 conditions, 220 paired contrasts and original intervals |
| `reports/stage-b-figures-v4-50/` | Six plots in SVG/PDF and timing/evidence tables |
| `reports/dashboard-snapshot-v4-50/` | Four saved views, 176 cells and 2,920 examples |
| `artifacts/archives/ragbench-core-v4-50.zip` | Raw records, prepared data and exact measurement source |
| `artifacts/archives/ragbench-analysis-v4-50.zip` | Analysis source, results, figures, viewer snapshot and checks |

Weights and index arrays are excluded from the archives. Raw measurement source and
later analysis source remain separately identified. Archived provenance and earlier
records are preserved unchanged, outside the current presentation narrative.

## Install and open the dashboard

Wide results tables scroll within their own keyboard-focusable regions. Headings
stay on one line, while long configuration names can wrap without widening the page.

For question-level intervals, the source-cluster field reads “Not used — question-level
intervals”; interval notes explain that shared-source dependence was not adjusted.

Question counts remain visible in the main views; source-cluster counts are available
in closed statistics details. The overview derives sample counts from the selected
run. Downloads identify archived figure captions that disagree with saved table
counts, while preserving the original verified files.

The browser tab displays no dashboard favicon.

The viewer uses optional Dash/Plotly dependencies from
[requirements-dashboard.lock](requirements-dashboard.lock). The existing isolated
viewer environment avoids changing the benchmark environment just to inspect results.
The recorded environment is Python 3.14/macOS ARM64; other installations need validation.

With the saved local snapshot and existing viewer environment:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

Open http://127.0.0.1:8050. The viewer provides configuration filters, paired contrasts,
saved question/answer/evidence comparisons and checked downloads. Text is rendered
safely, filtered CSVs neutralize spreadsheet formulas and the server binds to loopback
with debug disabled.

The viewer never loads generators, executes benchmarks or mutates records. It consumes
verified snapshots built offline and must be stopped before timed experiments. The
public aggregate bundle does not include the local snapshot or viewer environment.

## Hosting the original dashboard on Render

`render.yaml` defines a free Python web service using the existing Dash app.
The hosted environment installs only `requirements-render.lock`; it does not
install the benchmark package or model dependencies. `dashboard_wsgi.py` exposes
the original Flask server through one Gunicorn worker with two threads.

The deployment copy in `deployment/dashboard/` contains the unchanged v4 snapshot
as gzip plus its existing figures and CSV. At build time,
`PYTHONPATH=src python scripts/prepare_hosted_dashboard.py` expands the JSON and
checks its byte hash, manifest identity and every asset checksum against
`configs/hosted-dashboard.json`. The original local snapshot stays unchanged.
This copy includes saved questions, generated answers and evidence examples.

After these files are pushed, choose New > Blueprint in Render, connect the
GitHub repository and review the free service described by `render.yaml`.
For manual Web Service creation, select Python, branch main, no root subdirectory,
and the Free instance. Set PYTHON_VERSION=3.14.7 and PYTHONPATH=src. Use these:

```sh
# Build command
pip install -r requirements-render.lock && python scripts/prepare_hosted_dashboard.py
# Start command
gunicorn dashboard_wsgi:server --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
```

The health-check path is `/healthz`. Render supplies PORT and a public URL.
The hosted entry point explicitly permits RENDER_EXTERNAL_HOSTNAME in the viewer
host guard; local CLI defaults still accept only loopback hosts.
No API keys or models are needed.
The free service can sleep when idle; the local CLI continues binding to loopback.

Local checks passed 45 dashboard regressions and nine hosted checks, including
original snapshot bytes, figure download, app routes, corrupt-package rejection
and absence of model imports. Streaming identity verification preserves canonical
hashes while reducing local startup peak from 616,710,144 to 453,836,800 bytes.
Those are macOS memory observations. The deployed health endpoint, page, Dash
layout/dependencies and original CSS/JS assets subsequently passed live checks.
A Linux wheel-resolution check was blocked by DNS failures for files.pythonhosted.org.
The hosted lock pins dependency versions separately from macOS wheel hashes.

## Running and reproducing the study

[requirements.lock](requirements.lock) pins the core Python dependencies. On macOS,
[native.py](src/ragbench_lab/native.py) configures OpenMP library loading before neural
imports; duplicate-runtime error suppression is not the supported remedy.

Inspect configuration and the frozen request matrix without inference:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/stage-a-study.toml
PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-b-plan \
  configs/stage-a-study.toml --study manifests/stage-b-study-v4-50.json
```

These are real CLI identifiers. There is no generic `run` command. A full execution
also needs pinned prepared data, encoder/reranker/generator artifacts, compatible indexes
and fresh development validation, followed by an explicitly bounded request allowance.

Verify the local archives without rerunning models:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab archive-verify \
  artifacts/archives/ragbench-core-v4-50.zip
PYTHONPATH=src .venv/bin/python -m ragbench_lab archive-verify \
  artifacts/archives/ragbench-analysis-v4-50.zip
```

Fresh-workspace numerical replay reproduced observations, clusters and CSV tables
byte-for-byte, with all report fields except recorded analysis provenance/hash matching.
That replay used installed dependencies; it does not demonstrate a fresh installation,
model rerun or cross-platform replication. Local handoff instructions are in
`reports/v4-handoff/START_HERE.md`.

## Validation and limits

```sh
python3 scripts/verify_checkout.py
```

The checkout check uses synthetic fixtures and the standard library to exercise
configuration, factorial enumeration, offsets/split isolation, chunk boundaries,
BM25/RRF, packing/scoring, resume integrity and public-result consistency. Local tests
add detailed algorithm, raw-record, viewer and corruption checks; tests remain ignored.

The evidence budget, output cap, selected embedder/chunker, adapted corpora, source
counts and sequential host measurements bound the conclusions. Alternative generators,
context budgets, candidate depths, overlap and concurrent load need separate controlled
studies with development validation and compute budgets. The completed benchmark
requires no additional requests for its declared evaluation.

AI tools assisted implementation, debugging and writing. Measurements and verification
claims come from the saved records and actual checks, not generated example results.
