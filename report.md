# RAGBench Lab: study report

Updated 19 October 2026. This report describes the completed **v4, 50-question Stage B
expansion**. It measures how retrieval, chunk size and reranking affect answer quality
and latency on one local machine. Reranking added time in every matched comparison,
while its answer-quality changes had both signs.

## Study and completion

The datasets are SQuAD v1.1 and an adapted HotpotQA shared corpus. Generators are
Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, both Q4_K_M, on macOS ARM64.

Stage A completed 9,000 development and 18,000 held-out retrieval requests, using 50/100
questions per dataset. Development evidence coverage selected E5 with sentence-aware
chunking; that choice stayed frozen for Stage B.

Stage B compares BM25, Dense and Hybrid retrieval, chunk sizes 128/256, and reranking
off/on: twelve pipelines across two datasets and two generators. With 50 questions per
dataset and three repetitions, v4 completed **7,200 main and 1,200 separate
No-RAG/gold-evidence requests**. Both fresh development gates (144 main and 24 baseline
requests) passed. All v4 matrices completed with zero request/setup failures;
diagnostics and warmups are excluded from results.

## Main results

Ranges span the twelve pipeline point estimates within each dataset/model. They are not
confidence intervals or a selection of winning configurations. Token F1 is
reference-token overlap; latency is mean online request time.

| Dataset | Generator | Token F1 | Mean online latency |
| --- | --- | --- | --- |
| SQuAD | Llama | 42.39–57.54% | 4.52–5.88 s |
| SQuAD | Qwen | 37.07–48.39% | 5.05–6.05 s |
| HotpotQA | Llama | 15.92–23.75% | 4.55–5.58 s |
| HotpotQA | Qwen | 13.63–21.57% | 5.35–6.39 s |

Reranking changed F1 by −3.13 to +13.11 percentage points and added 0.13–1.23 seconds
across 24 matched comparisons. F1 rose in 14 and fell in 10. These are descriptive
signs, not counts of statistically significant wins.

Llama had higher SQuAD F1 point estimates in all twelve matched profiles. HotpotQA model
differences varied: Qwen was higher in five and lower in seven. Qwen had higher mean
online latency in all 24 matched main profiles. Retrieval and chunk-size effects also
varied; the results do not establish a universal best pipeline.

## Separate baselines

| Dataset | Generator | No-RAG token F1 | Gold-evidence token F1 |
| --- | --- | --- | --- |
| SQuAD | Llama | 4.29% | 64.93% |
| SQuAD | Qwen | 0.00% | 52.08% |
| HotpotQA | Llama | 5.20% | 31.52% |
| HotpotQA | Qwen | 0.00% | 33.08% |

No-RAG retains the grounded-answer/abstention instruction, so it is not an unrestricted
parametric-knowledge test. Gold evidence is a diagnostic reference, not a guaranteed
upper bound. Baseline and main timing paths differ and remain separately labeled.

## Uncertainty and limits

The 8,400 measurements cover 100 distinct question IDs. Quality uses repetition one; all
three repetitions contribute to timing. Paired 95% intervals use 2,000
whole-source-cluster bootstrap draws over 14 SQuAD article clusters and 50 Hotpot
supporting-source components, with question-cluster sensitivity also reported. Intervals
are descriptive and unadjusted for multiple comparisons. Repetitions do not increase the
number of questions or independent evidence sources.

V4 expands a previously used evaluation pool after v3 results were inspected. Its
ID-only sample includes the earlier 25 questions per dataset, with fresh measurements
and no historical aggregate pooling. It is not an untouched confirmatory holdout. V1
stopped on a tokenizer mismatch; corrected v2 stopped at the user's request; completed
reduced v3 remains a separate study. The local ignored `REPORT_V3.md` preserves
its original findings.

EM/F1 measure text agreement, not factuality. Annotated evidence coverage does not
guarantee sufficient context. The 1,024-reference-token evidence budget, 64-token output
cap, adapted corpora, resumed single-host timing and limited source counts constrain
generalization, especially for tail latency. Hotpot mirror equivalence and supervisor
acceptance of the earlier reduction remain unverified. Analysis choices were not
prospectively preregistered.

## Saved work and verification

[README.md](README.md) covers setup and viewing;
[PROJECT_DEEP_DIVE.md](PROJECT_DEEP_DIVE.md) explains the implementation. The v4 tables
and original intervals are in `reports/stage-b-analysis-v4-50/`, figures in
`reports/stage-b-figures-v4-50/`, and the saved viewer in
`reports/dashboard-snapshot-v4-50/`. The published `results/stage-b-v3/` remains v3.

The separate v4 raw and analysis ZIPs passed member/checksum verification.
Fresh-workspace offline replay reproduced four numerical files byte-for-byte and all
report fields except recorded provenance/hash; 43 focused tests passed there. Replay
used existing installed dependencies. It does not establish a fresh installation, model
rerun, cross-platform replication or remote backup. V4 qualitative case review and
extended narrative synthesis remain unproduced; optional model, context and load
experiments remain unrun.

AI tools helped with planning, implementation, debugging and documentation. Numerical
claims above come from the saved verified v4 measurements.
