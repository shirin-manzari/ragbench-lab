# RAGBench Lab: how it works

RAGBench Lab is a local study of retrieval-augmented generation: find relevant text, fit
it into a prompt, and ask a language model to answer from that evidence. The question is
how retrieval, chunking and reranking change answer quality and latency when the
surrounding conditions stay fixed.

This document explains the implementation and the decisions behind it.
[README.md](README.md) has the shortest setup and viewing workflow;
[report.md](report.md) summarizes the completed study and findings.

## Contents

- [What the project includes](#what-the-project-includes)
- [Repository map](#repository-map)
- [The two-stage experiment](#the-two-stage-experiment)
- [From dataset files to searchable documents](#from-dataset-files-to-searchable-documents)
- [Chunking without losing source locations](#chunking-without-losing-source-locations)
- [Retrieval and reranking](#retrieval-and-reranking)
- [Packing the evidence](#packing-the-evidence)
- [One request, from question to record](#one-request-from-question-to-record)
- [Generation and timing controls](#generation-and-timing-controls)
- [Bounded sessions and safe resume](#bounded-sessions-and-safe-resume)
- [Scores, uncertainty and interpretation](#scores-uncertainty-and-interpretation)
- [Saved outputs and analysis](#saved-outputs-and-analysis)
- [Install and open the dashboard](#install-and-open-the-dashboard)
- [Verify and replay](#verify-and-replay)
- [Validation and remaining limits](#validation-and-remaining-limits)
- [Extending the project](#extending-the-project)

## What the project includes

The completed core covers SQuAD v1.1 and an adapted HotpotQA shared corpus. It compares
Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, both quantized as Q4_K_M. Retrieval runs
before generation, so changing the retriever is a measured part of the pipeline rather
than a different collection of prewritten prompts.

There are three useful ways to work with the repository. The command-line tools prepare
data and run controlled experiments; the offline analysis tools turn saved records into
tables and figures; the dashboard lets you inspect those results without running models.
Opening the dashboard does not continue a study.

The current v4 study is complete: 27,000 unchanged Stage A retrieval requests, 7,200
fresh main Stage B requests and 1,200 separate baseline requests. This is 35,400
requests across Stage A and the v4 run set, not a pool of historical Stage B
measurements. Pilots, development gates, warmups and older runs are separate.

## Repository map

Most behavior lives in small Python modules under `src/ragbench_lab/`. Configuration
describes settings; manifests identify the exact frozen study and its inputs. Downloaded
assets and generated outputs stay outside normal Git tracking.

```text
src/ragbench_lab/
  data/                     dataset adapters, records and split preparation
  chunking.py               fixed-token and sentence-aware chunks
  retrieval.py              BM25 and reciprocal-rank fusion
  embeddings.py, dense.py   encoders and exact vector search
  context.py                ranked evidence packing and source mappings
  generation.py             native prompt rendering and backend responses
  execution.py              measured retrieval-to-answer path
  stage_a.py                retrieval screening and evaluation
  stage_b_runner.py         bounded main-generation sessions
  baseline_runner.py        separate No-RAG and gold-evidence sessions
  run_store.py              append-only records and resume checks
  analysis.py               Stage B cells and paired comparisons
  paired_statistics.py      question and source-cluster resampling
  dashboard*.py             offline export, snapshot checks and viewer
  dashboard_assets/         local CSS and JavaScript
configs/                    experiment settings and analysis protocols
manifests/                  frozen selections, identities and amendments
data/, models/, indexes/    local input and derived assets
runs/                       raw request records and run manifests
reports/                    analysis, figures and dashboard snapshots
artifacts/                  archives, verification proofs and environments
```

The tree groups related files; `dashboard*.py` is shorthand, not a directory. The main
entry point is [cli.py](src/ragbench_lab/cli.py), exposed as `ragbench` or `python -m
ragbench_lab`. Algorithms do not depend on the dashboard.

### Environment and dependencies

The recorded environment is Python 3.14 on macOS ARM64. The package declares Python
3.11+, but that is not a claim that every supported Python/platform pair has passed a
full reproduction. Core versions are pinned in [requirements.lock](requirements.lock),
including Torch, Transformers, Tokenizers, FAISS and NumPy.

Dash and Plotly are optional and have a separate
[requirements-dashboard.lock](requirements-dashboard.lock). Keeping the viewer in its
own environment avoids changing the benchmark environment just to browse results. No
cloud model service is required; generation uses a dedicated local Ollama backend.

On macOS, Torch and FAISS can load conflicting OpenMP libraries.
[native.py](src/ragbench_lab/native.py) arranges the CLI's native-library search path
before those imports. Suppressing duplicate-library errors with `KMP_DUPLICATE_LIB_OK`
is not the project's fix.

## The two-stage experiment

### Stage A: choose retrieval components first

Stage A compares five recipes: BM25, Dense with BGE, Dense with E5, Hybrid with BGE and
Hybrid with E5. Each runs with fixed-token and sentence-aware chunking at 64, 128 and
256 reference tokens. Overlap is zero and reranking is off.

```text
5 recipes × 2 chunkers × 3 sizes = 30 conditions per dataset

Development: 30 × 2 datasets × 50 questions × 3 repetitions = 9,000
Held-out:    30 × 2 datasets × 100 questions × 3 repetitions = 18,000
```

Selection uses development data only. For each embedder/chunker pair, it averages
packed-context evidence coverage across Dense and Hybrid at all three sizes, then
averages the two datasets equally. Quality comes from repetition one; latency averages
the repeated measurements within each question.

Candidates within one absolute percentage point of the best coverage are compared by
retrieval latency, then indexing cost, then a deterministic lexical tie-break. A freeze
requires the full successful first-attempt development matrix; diagnostic subsets cannot
select the study. [selection.py](src/ragbench_lab/selection.py) implements this rule.

The selected pair was **E5 with sentence-aware chunking**. The saved decision is
[stage-a-selection-v1.json](manifests/stage-a-selection-v1.json). Held-out Stage A
results evaluate the recipes; they do not reopen that selection.

### Stage B: compare complete answering pipelines

Stage B keeps the selected embedder and chunker and varies three retrieval families, two
sizes and reranking off/on. That gives twelve pipelines per dataset/model, or 48 main
conditions across the two datasets and generators.

```text
Main:      12 pipelines × 2 datasets × 2 models × 50 questions × 3 = 7,200
Baselines:  2 controls  × 2 datasets × 2 models × 50 questions × 3 = 1,200
```

The controls are No-RAG and gold evidence. They have their own plan and runner; they are
not extra retrieval families mixed into the main matrix. All twelve main pipelines, both
generators and all three repetitions stay fixed across the separate reduced v3 and
expanded v4 studies.

### Study versions and sample expansion

The original v1 target was 14,400 main requests, using 100 questions per dataset. It
stopped after 1,405 successful requests and one native/backend prompt-token mismatch.
The Llama tokenizer export had a different `ignore_merges` setting from the backend;
corrected assets and fresh identities produced v2.

V2 stopped at the user's request after 103 successful requests and one recorded
interruption. Reduced v3 then selected 25 question IDs per dataset deterministically
from the existing held-out pools. It did not select the first completed answers or
import successful v1/v2 requests.

Completed v3 contains 3,600 main and 600 baseline requests. The reduction followed
partial execution; it was not a wholly pre-execution protocol. Supervisor acceptance of
that reduced scope has not been verified.

The current definition is
[stage-b-study-v4-50.json](manifests/stage-b-study-v4-50.json). V4 takes the first 50
IDs from the same SHA-256 ranking as v3, preserving the original 25 per dataset.
Selection uses IDs, dataset and frozen seed only. All 7,200 main and 1,200 baseline
measurements are fresh, with no imported or pooled historical aggregates.

This is a post-results expansion of an already used pool, not an untouched confirmatory
holdout. Stage A, prompts, model settings and all pipeline factors remain fixed.
`scripts/prepare_stage_b_50.py` recreates the plan with exclusive output creation.

Some frozen manifests contain status text or feasibility estimates from when they were
written. They are immutable historical definitions, not live progress indicators.
Completion is established from the verified request records and analysis, not by editing
those old fields.

## From dataset files to searchable documents

### Common records

[data/records.py](src/ragbench_lab/data/records.py) defines immutable records rather
than passing dataset-specific dictionaries through every algorithm.

| Record | What it carries |
| --- | --- |
| `Document` | Stable ID, dataset, title, original text and source spans |
| `SourceSpan` | A paragraph or sentence location within a document |
| `Question` | ID, question text, acceptable answers and evidence annotations |
| `EvidenceSpan` | Document/source IDs, character range and exact evidence text |
| `Exclusion` | Question ID and the reason it was rejected |
| `Split` | Development/evaluation IDs, seed and recorded source overlap |

Offsets are zero-based Python character positions, with an exclusive end. A span
`[start, end)` refers to `document.text[start:end]`; these are not byte offsets or token
indices. Keeping this convention across modules makes it possible to trace a scored
answer span back through a packed prompt.

### SQuAD and HotpotQA adapters

The SQuAD adapter joins an article's paragraphs with two newlines and translates
paragraph-local answer offsets into article offsets. It checks the supplied answer text
against the source slice. Invalid annotations exclude the whole question; the adapter
does not search for a convenient replacement occurrence.

HotpotQA is adapted from question-local contexts into a shared searchable corpus. Exact
title/sentence-list matches are deduplicated, while different texts with the same title
remain distinct documents. Supporting facts are resolved against the question's own
context before that context enters the shared pool.

Missing or ambiguous supporting sentences are exclusions, not guessed labels. The
prepared Hotpot corpus is therefore an adaptation, not an untouched official retrieval
benchmark. Byte-equivalence of its pinned mirror to the official distribution remains
unverified.

### Preparation and split isolation

[data/preparation.py](src/ragbench_lab/data/preparation.py) validates exact evidence
slices, span bounds, unique IDs and document references. It writes stable JSONL
documents/questions, exclusions, split information and a manifest containing input and
output hashes. Loading prepared data verifies those bindings again.

Development and evaluation IDs follow a seeded SHA-256 ordering. By default, evaluation
selection excludes documents and titles used by development evidence, not just repeated
question IDs. If the requested split cannot be formed, preparation fails rather than
silently relaxing isolation.

An explicit overlap override records the overlap instead of hiding it. The searchable
corpus is shared; isolation separates labeled question/evidence sources for development
decisions and held-out evaluation, rather than training a different index for every
split. Answer and support labels never become searchable text or generation inputs,
except in the explicit gold baseline.

## Chunking without losing source locations

[chunking.py](src/ragbench_lab/chunking.py) produces chunks with a document ID, source
start/end, original text, method, target size and actual reference-token count. Chunk
IDs derive from those structural coordinates, making boundaries part of the identity.

Fixed-token chunking uses tokenizer offsets to propose boundaries, then counts each
resulting standalone slice again. Tokenization can change at a cut, so a nominal
boundary is shortened if the actual slice exceeds the target. It fails if it cannot make
progress within the declared limit.

Sentence-aware chunking packs consecutive sentences until the next one would exceed the
target. Hotpot uses preserved sentence spans; other text uses punctuation and paragraph
heuristics, not a learned sentence model. An oversized sentence falls back to
fixed-token splitting, with the fallback counted.

Both methods preserve source characters and use zero overlap. A size of 128 is a
per-chunk target, not a promise that every chunk is full or that a prompt contains
exactly eight chunks. Whitespace-only or otherwise zero-token regions need not become
searchable chunks.

## Retrieval and reranking

### BM25

[retrieval.py](src/ragbench_lab/retrieval.py) uses Unicode word matching and case
folding, without a separate stemmer or stop-word list. The index stores term
frequencies, document frequencies and chunk lengths. Here, the retrieval documents are
chunks rather than entire source articles.

For each query term, the score uses the following form:

```text
idf(t) = log(1 + (N - df(t) + 0.5) / (df(t) + 0.5))

score(q, d) = sum over query terms t:
  qtf(t) × idf(t) × tf(t,d) × (k1 + 1)
  / (tf(t,d) + k1 × (1 - b + b × length(d) / average_length))
```

There is no separate TF-IDF retrieval pipeline. The frozen settings are `k1 = 1.5` and
`b = 0.75`. Repeated query terms keep their query frequency. Scores and stable chunk-ID
tie-breaks determine order; saved postings are validated rather than treated as an
opaque cache.

In the formula, `N` is the number of chunks, `df` counts chunks containing the term, and
`tf`/`qtf` count occurrences in the chunk/query. If fewer than 50 chunks match, the
candidate list can include deterministic zero-score entries. Being returned as a
candidate therefore does not itself establish relevance.

### Dense search

[embeddings.py](src/ragbench_lab/embeddings.py) supports the pinned BGE-small and
E5-small models. Both produce 384-dimensional normalized vectors, but their input
conventions differ.

| Encoder | Query prefix | Passage prefix | Pooling |
| --- | --- | --- | --- |
| BGE | `Represent this sentence for searching relevant passages: ` | None | CLS |
| E5 | `query: ` | `passage: ` | Attention-mask mean |

Embedding runs on CPU in float32 with pinned seeds, deterministic settings and four
Torch threads. Inputs are checked for truncation instead of silently letting the model
shorten them.

[dense.py](src/ragbench_lab/dense.py) uses FAISS `IndexFlatIP`: exact inner-product
search over normalized vectors, not an approximate neighbor index. Ties at the candidate
cutoff are resolved deterministically. Corpus vectors are built offline; a measured
query still computes a fresh query embedding.

### Hybrid search

Hybrid runs BM25 and Dense at depth 50, then combines their rankings using
reciprocal-rank fusion. For each chunk, it adds `1 / (60 + rank)` from each constituent
list, using one-based ranks.

The same chunk contributes at most once per list. Fusion uses rank rather than adding
incompatible BM25 and vector scores, deduplicates by chunk ID and returns the top 50
fused candidates. Constituent rankings are retained so the combined result can be
inspected later.

### Optional reranking

[reranking.py](src/ragbench_lab/reranking.py) scores each question/chunk pair with the
pinned `cross-encoder/ms-marco-MiniLM-L6-v2` model. Unlike Dense search, the
cross-encoder reads the pair together and produces a relevance score.

Reranking reorders the existing candidate list; it cannot add, remove or replace chunks.
The runner checks candidate membership before and after. Pair lengths are checked
against the model's 512-token limit, and deterministic tie-breaks keep equal scores
stable.

### What an index contains

[pipeline.py](src/ragbench_lab/pipeline.py) ties chunks, sparse postings and vector
files to corpus, tokenizer, configuration and model-file hashes. It records build time
and persisted size separately from online query time.

Loading checks the manifest and file hashes, then validates chunk identities, source
slices and token counts. Reusing a persisted corpus index is expected; reusing saved
query results in place of measured retrieval is not.

## Packing the evidence

[context.py](src/ragbench_lab/context.py) walks the final ranked list in order and
builds one evidence string. The budget is 1,024 tokens under the pinned BGE reference
tokenizer, regardless of which generator will read it.

Each included chunk has a `[chunk_id]` header, with blank lines between chunks. Headers
and separators count toward the budget. The packer counts the complete candidate string
after concatenation rather than assuming that separately counted pieces add up.

If the next full chunk does not fit, the packer tries the longest fitting prefix at a
tokenizer boundary. Only the final included chunk can be partial. If no text from the
next ranked chunk fits, packing stops; it does not jump ahead to a smaller lower-ranked
chunk.

Each included segment retains both source offsets and its position in the final context.
Evidence coverage is recomputed from those surviving source intervals, not from the
original full chunk. A useful sentence retrieved at rank one can still be absent from
the actual prompt after truncation.

For a synthetic example, suppose a chunk covers source characters `[100, 240)` but only
its prefix through character 180 fits. A gold span at `[190, 210)` is present in the
retrieved chunk but absent from the packed evidence. The context score must reflect the
latter.

The shared reference budget controls evidence length, not the entire native chat prompt.
Each generator separately counts its rendered prompt and reserves space for output.
Paired model requests must have identical evidence strings and compatible candidate
identities; model-specific chat framing may differ.

## One request, from question to record

Consider an illustrative Stage B condition: Dense, size 128, reranking enabled, with the
frozen E5/sentence-aware pair. This is a walkthrough of the code path, not a new
measured example.

```text
Checked condition + prepared question
  → fresh query embedding and Dense top-50 search
  → cross-encoder reorders the same candidates
  → ranked packing under the shared 1,024-token budget
  → native chat rendering and local generation
  → cache/count/context validation and scoring
  → append the result to the run's hash chain
```

Before the request, the runner verifies identities, prepares the block and isolates the
backend cache. [execution.py](src/ragbench_lab/execution.py) then starts the online
timer immediately before retrieval. It saves initial candidates, reranked IDs, input
lengths, packed evidence and context identity as the request moves through the pipeline.

The generator returns an answer plus prompt/output counts, backend statistics, stream
information and truncation state. The online timer stops when generation returns. Cache
validation, answer scoring, evidence scoring and disk writes happen afterward, outside
that total.

If a stage fails, the result identifies that stage and the error instead of pretending
an empty answer was a successful request. Available partial generation details are
retained. The outer runner records the attempt and stops the session on failure rather
than silently carrying on with a different matrix.

## Generation and timing controls

### Prompting and model identity

[generation.py](src/ragbench_lab/generation.py) applies each model's pinned native chat
template to the same grounding instruction, question and packed evidence. The
instruction asks for a short evidence-based answer or exactly `INSUFFICIENT_EVIDENCE`
when the evidence is insufficient.

The frozen settings use a 4,096-token native context window, at most 64 output tokens,
temperature zero, seed 20261011 and four backend threads. Backend version, model digest,
quantization, tokenizer files and template identity are checked. A mutable model tag
alone is not enough to identify a measured model.

The rendered native prompt plus output allowance must fit the model window. The native
prompt count must also match the backend's reported count, with model-specific
beginning-of-sequence handling applied once. A count mismatch is a failure, as the
historical v1 stop demonstrated.

Stream handling has a bounded deadline and validates final response metadata. The
recorded first-visible-output time is observed by the client; it should not be relabeled
as a server-internal time-to-first-token measurement. An output stopped by the token
limit is retained and marked truncated.

### Cache isolation and warm state

[serving.py](src/ragbench_lab/serving.py) unloads the selected model, requires the
dedicated server to be empty, and preloads that model with an empty prompt before each
measured request. Residency checks require the expected digest and context size, with
only one generator loaded.

The response must explicitly report zero cached prompt tokens. A missing, boolean or
nonzero value is not accepted as proof of an uncached request. Isolation and preload are
outside online latency but contribute to real session wall time.

This policy prevents prompt reuse from bypassing measured work. It does not guarantee
that all decoder kernels remain warm after fresh decoder creation. The feasibility notes
and result interpretation keep that distinction visible.

### Time and memory are scoped measurements

Online latency includes fresh retrieval, reranking when enabled, context packing and the
generation call, including its native prompt handling. It excludes index/model setup,
block warmup, cache isolation, scoring and record writes. Reported stage timers need not
exhaust the total; remaining overhead is kept rather than forced into a misleading
stage.

[resources.py](src/ragbench_lab/resources.py) samples process RSS for the caller and
dedicated backend process tree. Sampling can miss short peaks. Runtime device allocation
is a separate counter and may overlap RSS on unified-memory hardware, so the two are not
added into a supposed total.

Requests run sequentially, with seeded randomized block order and one generator at a
time. A resumed study is still a single-host, multi-session measurement, not a
concurrency or sustained-load benchmark. Online seconds also should not be used as a
direct estimate of whole-session duration.

### The two baseline paths

No-RAG sends an empty evidence context but retains the grounding/abstention instruction.
It is not an unrestricted test of a model's memorized knowledge.

Gold evidence takes SQuAD diagnostic paragraphs or Hotpot supporting sentences,
deduplicates and orders their source spans, then uses the same context packer. It can
still lose text to the budget, and isolated supporting sentences can omit coreference
context. Gold is a diagnostic control, not a guaranteed upper bound.

Baseline and main runs also have distinct execution paths and source identities. Their
contrasts are reported with that limitation, not treated as perfectly isolated estimates
of retrieval cost alone.

## Bounded sessions and safe resume

### Attempts, not just a progress counter

[run_store.py](src/ragbench_lab/run_store.py) identifies a request by its condition,
question ID and repetition. Attempts for that request are numbered; successful requests
cannot be appended again. Warmup and lifecycle events are separate records and do not
increase the request count.

A run manifest binds source, configuration, models, study definition, environment and
source-code provenance. Records form an append-only SHA-256 chain starting from that
manifest, with consecutive sequence numbers. Writes flush and sync; an exclusive writer
lock prevents two sessions from appending concurrently.

Hashes detect mismatches and corruption relative to the saved identities; they are not a
substitute for trusted backups or signed provenance. The code records dirty source state
rather than claiming every measurement came from a clean commit.

### What a pause or resume does

Stage B sessions require an explicit positive `--max-requests` bound. That limit counts
attempts in the current invocation, not a new total target. For example, a bound of 500
permits up to 500 more attempts; it does not mean “stop when the study reaches 500.”

With `--resume`, the runner first validates the existing manifest and chain, then skips
completed successes. Failed requests are not silently erased or replaced: retrying
requires `--retry-failures`, and the earlier attempt stays in the log. A failure ends
the current session.

Identity changes, a damaged or incomplete JSONL tail, and incompatible paired contexts
are rejected. Resume does not automatically repair the log or migrate results to a new
study. A leftover lock needs investigation of the actual writer, not an assumption that
deleting it is safe.

### Development gates

A new runner/source/study identity needs a compatible development diagnostic before
held-out execution. V4 passed a fresh 144-request main diagnostic across all 48
conditions and three repetitions, using one development question per dataset. After the
completed main parent was verified, baselines passed their own fresh 24-request
diagnostic. Both finished without request/setup failures.

Gates validate orchestration and compatibility, not held-out answer quality. A
successful old diagnostic cannot authorize a changed implementation.

## Scores, uncertainty and interpretation

### Answer scores and evidence scores answer different questions

[answer_metrics.py](src/ragbench_lab/answer_metrics.py) normalizes case, punctuation,
English articles and whitespace. Exact match compares normalized answers; token F1 uses
multiset token overlap. Each metric takes its best score over the acceptable references,
with special handling for Hotpot yes/no/noanswer.

These are text-match metrics. A correct but verbose explanation may score below a
concise reference, while lexical agreement alone does not establish factual correctness.
Abstention is counted only when the stripped output exactly equals the sentinel;
free-form statements of uncertainty are not silently reclassified.

[metrics.py](src/ragbench_lab/metrics.py) merges overlapping source intervals before
checking evidence. SQuAD coverage accepts a fully covered alternative answer span, with
paragraph coverage tracked separately. Hotpot coverage measures the fraction of complete
supporting sentences and whether all are covered.

Top-5, top-10 and top-50 evidence scores describe the ranked list being evaluated. Stage
B computes them after any reranking. Packed-context coverage instead uses only the
source intervals actually sent to generation; the two should not be used
interchangeably.

### Repetitions are not extra questions

Stage B quality uses successful first attempts from repetition one. Three timing
repetitions are repeated measurements of the same question, not three independent
quality samples. The 8,400 v4 main/baseline requests cover 100 distinct question IDs,
shared across every pipeline, generator and repetition.

The primary v4 intervals use 14 SQuAD article clusters and 50 Hotpot supporting-source
components. Hotpot clustering connects questions that share supporting document IDs or
normalized titles, including transitive connections and same-title variants.

[paired_statistics.py](src/ragbench_lab/paired_statistics.py) uses 2,000 seeded
bootstrap draws and 95% percentile intervals. Paired comparisons share resampling
weights, and dataset-macro results give each dataset equal weight. Repetitions stay
attached to their question; question-only intervals are a separately labeled sensitivity
analysis.

Intervals are withheld with fewer than two source clusters. Macro medians or p95 values
average dataset-level statistics rather than pretending to be a percentile of pooled
requests. Stage A reporting uses its own question-level procedure; its uncertainty
should not be mistaken for the Stage B source analysis.

### What the completed results support

Reranking increased mean online latency in all 24 matched main comparisons, by 0.13–1.23
seconds. F1 changed by −3.13 to +13.11 percentage points: fourteen paired changes were
positive and ten negative. These are descriptive signs, not significance counts.

Llama had higher SQuAD F1 point estimates in all twelve matched profiles. Qwen had
higher Hotpot F1 in five and lower in seven. Qwen's mean online latency was higher in
all 24 matched main profiles.

Those are descriptive observations, not proof of a universal winner. The intervals are
unadjusted for multiple comparisons, and the small, source-dependent sample limits tail
estimates and superiority claims. [report.md](report.md) keeps the numerical ranges and
examples together.

## Saved outputs and analysis

[analysis.py](src/ragbench_lab/analysis.py) checks run completeness, record identities,
protocol bindings and archive evidence before producing the complete Stage B report. It
recomputes scores from saved answers and packed source spans rather than trusting only
the per-request summary fields.

The analysis keeps 48 main cells and eight baseline cells separate. It exports both
per-dataset and equal-dataset macro results, with paired model, reranking, size,
retrieval-family and baseline contrasts. Changing display filters does not create a new
inferential analysis.

The main local outputs are:

| Directory | Useful files |
| --- | --- |
| `reports/stage-b-analysis-v4-50/` | 56 cells, 220 paired contrasts, original intervals and observations |
| `reports/stage-b-figures-v4-50/` | Six SVG/PDF plots, `stage-times.csv`, `stage-evidence.json` |
| `reports/dashboard-snapshot-v4-50/` | Four separate run views, 176 cells and 2,920 examples |
| `reports/v4-handoff/` | Verification and replay guidance |

These generated directories are local artifacts, not files supplied by a normal Git
checkout. Each export has a manifest tying its inputs and outputs together. Independent
verification helpers and proofs are retained with the local delivery materials.

The current v4 public subset is [results/stage-b-v4/](results/stage-b-v4/): a
condition lookup, the original cell/contrast/stage CSVs and three unchanged SVG figures.
Its manifest records source hashes, units, counts and interpretation limits without
exporting question IDs, question/answer text, source passages or personal provenance.
Join metric tables to `conditions.csv` by condition ID to read their configurations.

Run `python3 scripts/verify_public_results.py results/stage-b-v4` from a checkout to check the public
inventory, complete factorial/contrast matrices, units, interval bounds, contrast
arithmetic and reconstruction of online stage means. The script uses only the standard
library and does not require ignored inputs. These are aggregate consistency checks, not
raw-run audits or recomputed confidence intervals.

[export_public_results.py](scripts/export_public_results.py) creates a new bundle only
from the checked local analysis, figure manifest and analysis proof; it refuses to
overwrite an existing directory. Its `--check` option instead compares the existing
bundle byte-for-byte with those inputs without writing. Historical checkers and full
replay materials stay local; this export does not change them. Select v4 explicitly with
`--study v4`; the default remains historical v3, preserved byte-for-byte under
`results/stage-b-v3/`. Each profile rejects mixed sample counts, notes and cluster counts.

The offline [presentation](presentations/stage-b-v4.html) is built by
`python3 scripts/build_results_demo.py` using only the verified public v4 bundle.
It embeds the original quality–latency and stage-time SVGs, calculates descriptive
ranges/sign counts from exported CSVs, includes speaker notes and prints to PDF.
`--check` compares the generated presentation byte-for-byte. The ignored local
`DEMO.md` supplies a five-minute script, exact viewer command and offline fallback.

[figures.py](src/ragbench_lab/figures.py) preserves the original estimates and intervals
rather than computing new uncertainty for the plots. Its generation share is
generation-call mean divided by online-total mean, not the average of per-request ratios
or a share of full session wall time.

The v3 failure review selected six illustrative units by declared strata and seeded ID
ranking, saving selection before loading their answer texts. V4 now has an exhaustive exploratory failure breakdown and six paired case notes in
`reports/stage-b-failure-diagnostics-v4-50/` and
`reports/stage-b-failure-review-v4-50/`. These use saved responses without new model
requests; extended narrative synthesis remains unproduced. The v3 notes are agent-authored
interpretations, not independent human adjudication or a prevalence estimate. Historical
`reports/stage-b-failure-review-v1/` and `reports/study-synthesis-v1/` remain unchanged
and describe v3. The current [report.md](report.md) summarizes measured v4 findings.

## Install and open the dashboard

### Use the saved local viewer

With the snapshot and isolated environment already available:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

Open http://127.0.0.1:8050. If the environment or snapshot is missing, the command is
not a self-contained installation. The offline installation instructions are in the
local `reports/dashboard-handoff-v2/README.md`; its bundled wheels were checked on
Python 3.14/macOS ARM64.

The repository's current UI is newer than the immutable viewer ZIP. Do not replace an
archived package and keep its old identity just to incorporate a visual change.

### How the viewer stays separate

[dashboard_export.py](src/ragbench_lab/dashboard_export.py) builds a checked snapshot
offline. [dashboard_snapshot.py](src/ragbench_lab/dashboard_snapshot.py) validates it,
and [dashboard.py](src/ragbench_lab/dashboard.py) renders the saved data. The viewer
path does not load models, call the backend or launch a runner.

The current snapshot includes four run sets: Stage A development/evaluation, v4 Stage B
main and its baselines. It contains 176 cells, metadata for 35,400 requests and 2,920
saved examples. Stage A examples are a deterministic subset; Stage B examples cover all
repetition-one main and baseline responses.

The six tabs are Overview, Results, Compare, Questions, Paired and Downloads. Filters
stay within compatible runs and available configurations. Side-by-side examples use
shared saved questions; stored paired intervals are shown only for supported
comparisons, with the original contrast direction preserved.

Source text is rendered as text with safe annotations, not interpreted as HTML.
Downloads use checked assets, CSV exports neutralize spreadsheet formulas, and filtered
exports are produced in memory. The server binds to loopback with debug off; it is a
local viewer, not an authenticated public service.

Active-writer guards reject conflicts at startup and during use. They do not stop an
experiment for you, and browsing can still consume host resources. Stop the viewer
before timed work.

## Verify and replay

### Current archives and historical delivery

| Archive under `artifacts/archives/` | Purpose |
| --- | --- |
| `ragbench-core-v4-50.zip` | Verified raw v4 records, Stage A lineage, prepared data and exact measurement source |
| `ragbench-analysis-v4-50.zip` | Later analysis source, reports, figures, snapshot, local checks and replay proof |
| `ragbench-core-v1.zip`, `ragbench-analysis-v1.zip` | Historical v3 raw and analysis delivery |
| `ragbench-dashboard-v2.zip` | Historical reviewed viewer package and offline installation wheels |

Keep the two v4 archives together. Verify each inventory and member checksum:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab archive-verify \
  artifacts/archives/ragbench-core-v4-50.zip
PYTHONPATH=src .venv/bin/python -m ragbench_lab archive-verify \
  artifacts/archives/ragbench-analysis-v4-50.zip
```

The analysis package inventory pins the exact required raw companion.
`artifacts/analysis-package-independent-verification-v4-50.json` records its separate
verification. `delivery-verify` applies to the older structured v3 bundle; the v4 local
analysis package uses `archive-verify`.

The archiver accepts an explicitly declared saved local source snapshot only when its
revision and fingerprint match the measurement provenance exactly. Missing, extra,
changed or symlinked fingerprint inputs fail validation. The v4 measurement snapshot is
distinct from the later `src/` in the analysis package. These packages omit weights,
indexes and virtual environments.

The local `reports/v4-handoff/START_HERE.md` describes raw-first, analysis-second
extraction into a fresh checkout. A fresh-workspace v4 replay reproduced observations,
clusters, `cells.csv` and `contrasts.csv` byte-for-byte, and all report fields except
recorded analysis provenance/hash. All 43 focused archive/analysis/figure tests passed
there, using the existing installed environment. The replay proof is
`artifacts/analysis-replay-verification-v4-50.json`.

The earlier v3 rehearsal and offline viewer installation have separate historical
proofs. Current Markdown updates are newer than both immutable v4 ZIPs; editing a guide
does not regenerate a package or change its checksum.

Those checks establish specific replay results. They do not establish a new model
installation, cross-platform replication, off-device backup or clearance to publish the
underlying data. Review licenses, private paths and exported question/answer content
before sharing archives.

## Validation and remaining limits

### Inspect before launching compute

The following commands validate or describe settings; they do not run the study:

```sh
PYTHONPATH=src .venv/bin/python -m ragbench_lab validate configs/stage-a-study.toml
PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-a-plan configs/stage-a-study.toml
PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-b-plan \
  configs/stage-a-study.toml --study manifests/stage-b-study-v4-50.json
PYTHONPATH=src .venv/bin/python -m ragbench_lab stage-b-run --help
```

Actual execution needs the matching prepared sources, local model assets, indexes,
dedicated backend and development-gate records. The CLI deliberately has separate
commands for planning, diagnostic runs, held-out runs and reporting; there is no generic
“run everything” command.

### What gets checked

Run `python3 scripts/verify_checkout.py` from a fresh checkout with Python 3.11+. It
uses only the standard library and needs no package installation or ignored assets.
Eight named checks cover source syntax, configuration/factorials, synthetic dataset
preparation and splits, chunk boundaries, BM25/RRF, packed evidence/scoring, append-only
resume and the existing public aggregate verifier. Scratch inputs and records are
automatically removed; checkout contents are read-only.

The command's synthetic character counter checks algorithm contracts and Unicode source
offsets, not the frozen BGE/native tokenizers. Runtime guards reject model and viewer
numerical imports, network calls and subprocess launches. Use `python3 -I -S -B
scripts/verify_checkout.py --json` for an isolated machine-readable summary; failures
return status 1, including with `-O`.

The workflow in `.github/workflows/verify.yml` runs on pushes, pull requests and manual
dispatch, with Linux Python 3.11/3.14 and macOS/Windows Python 3.14 jobs. It installs no
project dependencies and uses the same command outside the checkout working directory,
with site packages disabled. Action revisions are pinned; checkout credentials are not
retained. Workflow setup can access the network. Cross-platform CI results are
established only when those jobs actually run. `configs/checkout-verification.json`
records the command, invariants and limits.

Focused local tests cover source offsets, split isolation, chunk boundaries, RRF
deduplication, context budgets, scoring, factorial enumeration and resume integrity.
Dashboard checks cover snapshot validation, compatible selection, safe text/download
handling and client/server filter agreement.

Tests and generated fixtures are intentionally ignored in normal Git tracking, so a
checkout alone does not contain the full local validation suite. Critical dashboard
commands and invariants are recorded in
[dashboard-validation.json](configs/dashboard-validation.json); replay packages retain
explicitly selected validation assets.

The local `PROGRESS.md` records actual commands, results and failed rehearsals. A
previously passed suite is historical evidence, not a claim that an unrelated future
change has been tested.

### Limits that remain

The main constraints are the 50-question-per-dataset Stage B sample, shared evidence
sources, resumed single-host timing, quantized small models and the short output cap.
Text-match scores and annotated span coverage do not replace semantic answer assessment.

The corpus adaptations, post-start budget amendment and post-collection analysis choices
also limit interpretation. Optional experiments remain unrun, and no extra measurements
are needed for the completed v4 expansion. Broader claims need a separately defined
study, not more confident wording.

## Extending the project

Start with the layer that owns the change. A dataset adapter must produce valid common
records and source mappings; a retriever must preserve stable chunk identities; a
generator must validate its prompt accounting and response metadata. A new dashboard
view should consume saved data without importing execution code.

Add one controlled factor at a time, declare its questions and budget, and write a new
manifest/run set. Changes to measurement code or study identity require a fresh
compatible development gate before bounded held-out execution. Keep the v1/v2 history
and completed v3/v4 outputs intact.

Candidate extensions include depth 20 versus 50, overlap, a third end-to-end chunk size,
concurrent load, caching, a larger corpus, and the planned SmolLM3-3B or 512/1,024/2,048
context-budget comparisons. SmolLM would need verified `no_think` behavior and
original-generator regressions for backend changes.

These are plans, not completed results or instructions to launch compute. Because main
held-out results have already been inspected, subsequent choices informed by them must
be labeled exploratory or evaluated on new held-out data.

## AI use

I used AI tools throughout this project to help with planning, coding, debugging, and
writing documentation.
