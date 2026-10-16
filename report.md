# RAGBench Lab: study report

Updated: 16 October 2026.

This project measures how retrieval, chunk size and reranking affect RAG answer
quality and latency on one local machine. The reduced core study and its analysis
are complete. The main finding is that quality gains depend on the dataset and
generator: reranking consistently cost time, but did not consistently improve answers.

## Study

The datasets are SQuAD v1.1 and an adapted HotpotQA shared corpus. The generators
are Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, both Q4_K_M, on macOS ARM64.

Stage A compared five retrieval recipes, two chunkers and three sizes. It completed
9,000 development requests and 18,000 held-out retrieval requests, using 50/100
questions per dataset. E5 with sentence-aware chunking was selected on development
evidence coverage and frozen before held-out evaluation.

Stage B kept twelve pipelines: BM25/Dense/Hybrid × sizes 128/256 × reranking off/on.
Across both datasets and generators, 25 questions per dataset and three repetitions
produced 3,600 main requests and 600 separate No-RAG/gold requests. These active
matrices completed without request failures; pilots and historical attempts are separate.

Stage B originally targeted 14,400 main requests. V1 stopped on a tokenizer
mismatch; corrected v2 was later stopped at my request. Reduced v3 used a fixed
ID-only sample after partial execution; earlier results were preserved separately
and never pooled.

## Results

Ranges span the twelve main profiles. They are point-estimate ranges, not
confidence intervals or a selection of winning configurations.

| Dataset | Generator | Token F1 | Mean online latency |
| --- | --- | --- | --- |
| SQuAD | Llama | 37.36–58.69% | 4.44–5.67 s |
| SQuAD | Qwen | 30.24–50.64% | 5.05–6.04 s |
| HotpotQA | Llama | 9.38–23.02% | 4.38–5.41 s |
| HotpotQA | Qwen | 10.65–20.06% | 5.23–6.19 s |

Reranking added about 0.33–1.03 seconds in all 24 matched mean-latency comparisons,
while F1 changes had both signs. Llama had higher SQuAD F1 point estimates in all
matched profiles; HotpotQA model differences varied. Qwen had higher mean online
latency in every matched main profile. Chunk-size and retrieval-family effects
also varied; no universal best pipeline was established.

## How to read the findings

The 4,200 main/baseline measurements cover fifty source-dependent questions.
Quality uses repetition one; three timing repetitions do not triple the sample.
Paired intervals use 2,000 source-cluster bootstrap draws over twelve SQuAD articles
and 25 Hotpot source components. Intervals are descriptive and unadjusted for
multiple comparisons; small-sample p95 estimates need particular caution.

For BM25/128 without reranking, the Qwen-minus-Llama F1 source intervals cross
zero on both datasets: SQuAD −18.51 to +4.40 percentage points, Hotpot −6.34 to
+8.73. Point-estimate signs alone do not establish superiority.

EM/F1 measure text agreement, not factuality. Annotated evidence coverage does not
guarantee sufficient context. No-RAG retains grounding/abstention instructions;
gold evidence can omit context or be truncated. Both are separate diagnostics.

The shared evidence budget is 1,024 reference tokens, with identical paired context
and verified native prompt counts. Timing includes fresh retrieval through
generation, excluding setup, warmup, cache isolation and scoring. Fresh decoder
state may affect kernel warmth. One host, adapted corpora, the small sample and
64-token output cap limit generalization. Hotpot mirror equivalence and supervisor
acceptance of the reduction remain unverified; detailed analysis choices were
finalized after collection.

## Code and saved work

The project includes preparation, retrieval, generation, resumable runners,
analysis, figures and a local read-only results dashboard. [README.md](README.md)
covers setup; [PROJECT_DEEP_DIVE.md](PROJECT_DEEP_DIVE.md) explains the code and controls.

Numerical results are in `reports/stage-b-analysis-v1/` and
`reports/study-synthesis-v1/`; figures are in `reports/stage-b-figures-v1/`.
The two core ZIPs under `artifacts/archives/` support offline analysis replay,
which previously matched 23 output files byte-for-byte using the installed environment.
They exclude weights/index arrays and do not establish a fresh model replication.
The local `PROGRESS.md` records checks; `PRD.md` contains background references.
Optional model, context and load studies remain unrun.

## AI use

I used AI tools throughout this project to help with planning, coding, debugging,
testing, and writing documentation.
