# RAGBench Lab: study report

This study measures how retrieval, chunk size and reranking affect evidence coverage,
answer quality and online latency in a local RAG system. Reranking increased mean
latency in every matched comparison, while its answer-quality effects had both signs.
The results do not establish a universal winning pipeline.

## Research design

The benchmark uses SQuAD v1.1 and an adapted HotpotQA shared corpus. Generators are
Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct in Q4_K_M on macOS ARM64.

Retrieval screening compares five recipes, two chunking methods and three sizes.
Development-only packed-evidence coverage selected E5 and sentence-aware chunking;
that choice was frozen before held-out retrieval evaluation. Screening completed
9,000 development and 18,000 held-out retrieval requests.

The answering experiment varies BM25/Dense/Hybrid retrieval, chunk sizes 128/256 and
reranking off/on. These twelve pipelines are evaluated on two datasets and two
generators, producing 48 main conditions. Each condition uses 50 questions and three
timing repetitions, with repetition one reserved for answer quality.

The completed evaluation contains **7,200 main requests and 1,200 separate
No-RAG/gold-evidence requests**, covering 100 distinct question IDs. Request/setup
failures were zero. Development validation, warmups and screening are separate from
these answering measurements.

## Main results

Ranges span the twelve pipeline point estimates within each dataset/model. They are
not confidence intervals. Token F1 measures reference-token overlap; latency is mean
online request time.

| Dataset | Generator | Token F1 | Mean online latency |
| --- | --- | --- | --- |
| SQuAD | Llama | 42.39–57.54% | 4.52–5.88 s |
| SQuAD | Qwen | 37.07–48.39% | 5.05–6.05 s |
| HotpotQA | Llama | 15.92–23.75% | 4.55–5.58 s |
| HotpotQA | Qwen | 13.63–21.57% | 5.35–6.39 s |

Across 24 matched comparisons, reranking changed F1 by **−3.13 to +13.11 percentage
points** and added **0.13–1.23 seconds** to mean online latency. F1 rose in 14 and fell
in 10. These are descriptive signs, not counts of statistically significant wins.

Llama had higher SQuAD F1 point estimates in all twelve matched profiles. On HotpotQA,
Qwen was higher in five and lower in seven. Qwen had higher mean online latency in all
24 matched main profiles. Retrieval and chunk-size effects also varied.

## Diagnostic baselines

| Dataset | Generator | No-RAG token F1 | Gold-evidence token F1 |
| --- | --- | --- | --- |
| SQuAD | Llama | 4.29% | 64.93% |
| SQuAD | Qwen | 0.00% | 52.08% |
| HotpotQA | Llama | 5.20% | 31.52% |
| HotpotQA | Qwen | 0.00% | 33.08% |

No-RAG retains the grounding and abstention instruction, so it is an empty-evidence
control rather than an unrestricted knowledge test. Gold evidence is a diagnostic
reference; it can truncate at the common budget and is not a guaranteed upper bound.
Baseline timing paths differ from main and remain separately labeled.

## Failure diagnostics

An exploratory review classified 2,400 first-repetition main responses. There were
404 exact matches and 1,996 responses that did not exactly match the reference.
The earliest observed evidence bottleneck gives this descriptive breakdown:

| Diagnostic category | Responses | Share of non-exact responses |
| --- | ---: | ---: |
| Incomplete annotated evidence among the top 50 candidates | 396 | 19.8% |
| Complete candidate evidence lost during packing | 285 | 14.3% |
| Non-exact answer with complete packed annotations | 1,315 | 65.9% |

The last category is not a count of factually wrong answers. It contains 903 responses
with positive token F1 and 412 with zero token F1. Complete annotations can coexist
with reasoning failures, abstention, or correct answers expressed with extra wording.
Six paired case notes illustrate these possibilities; they are agent-authored and
not independently adjudicated.

## Uncertainty and limitations

Paired 95% intervals use 2,000 whole-source-cluster bootstrap draws over 14 SQuAD
article clusters and 50 Hotpot supporting-source components. Question-cluster
sensitivity is also reported. Intervals are unadjusted for multiple comparisons;
repeated timings do not increase the number of independent questions or sources.

The final sample was expanded after earlier results were inspected. Selection used a
deterministic ID-only ranking, and all reported measurements were freshly collected
without pooling earlier runs. This is not an untouched confirmatory holdout.

EM/F1 measure text agreement, not factuality. Annotated coverage does not establish
semantic sufficiency. The 1,024-reference-token evidence budget, 64-token output cap,
adapted corpora and resumed single-host timings constrain generalization, especially
for tail latency. Official-byte equivalence of the Hotpot mirror remains unverified;
analysis choices were not prospectively preregistered.

## Results and verification

The [public results](results/stage-b-v4/) contain the original cell/contrast CSVs,
online timing breakdowns, SVG plots and a checksum manifest. Check them with:

```sh
python3 scripts/verify_public_results.py results/stage-b-v4
```

[README.md](README.md) covers setup and viewing. The local analysis lives in
`reports/stage-b-analysis-v4-50/`; failure diagnostics and illustrative notes live in
`reports/stage-b-failure-diagnostics-v4-50/` and
`reports/stage-b-failure-review-v4-50/`. Raw data and analysis archives retain the exact
source and provenance used for measurement and reporting.

Archive verification and fresh-workspace numerical replay passed using the installed
environment. They do not establish a fresh dependency installation, model rerun or
cross-platform replication. AI tools assisted implementation and writing; numerical
claims above come from saved verified measurements.
