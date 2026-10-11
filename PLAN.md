# ragbench-lab — implementation plan

## How to use this plan

PRD.md defines requirements. AGENTS.md defines contributor rules. This file owns the ordered task checklist. PROGRESS.md records actual work, verification, decisions, and the next task.

Start with the earliest unblocked task in the authorized phase. Mark a task complete only after its observable output and the phase-relevant checks exist. Update this checklist and PROGRESS.md together. If a task is too large, split it into lettered subtasks while keeping its stable ID.

All implementation tasks below are initially pending. The planning documents have been written; no source implementation or experiment execution has been verified.

## Milestones and dependencies

| Milestone | Phases | Outcome | Target |
| --- | --- | --- | --- |
| M1 | 0–2 | Dataset to BM25 retrieval and evidence scoring | Week 1 |
| M2 | 3–4 | Five retrieval recipes and Stage A selection | Week 2 |
| M3 | 5–6 | Two generators, reranking, measured feasibility | Week 3, early |
| M4 | 7 | Frozen end-to-end experiment records | Week 3 onward |
| M5 | 8 | Analysis and reproducibility export | Week 4 |

These are scheduling targets. Add the task estimates when planning each week; phase labels are rough, not a guarantee that several half-day tasks fit into one day. Unattended compute may overlap analysis preparation.

Phase dependencies: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. A minimal model-access and memory check may happen after Phase 0 to discover hardware problems early. Final sample and model settings must be frozen before Phase 7.

## Experiment sizes

- Stage A: 5 retrieval recipes × 2 chunkers × 3 sizes = 30 configurations per dataset; 60 across both datasets.
- Stage B: 3 retrieval families × 2 sizes × 2 reranking states = 12 configurations; 48 conditions across two datasets and two LLMs.
- Main Stage B workload: 48 × 100 questions × 3 repetitions = 14,400 generation requests. Pilot and diagnostic requests are additional.
- Use the declared smaller-model or sample-size fallback only before study freeze. Keep all resulting changes in the decision log.

## Task sizes and phase gates

XS = 1–2 hours. S = half a day. M = 1–2 days and must be split into S tasks. L = several days and must be split before coding. Estimates describe implementation effort, not unattended benchmark runtime.

Each task should name its input, output, and observable completion check. Complete each phase's gate before depending on it. Do not replace the research pipeline with a demo that returns canned answers.

### Phase 0 — scaffold and constraints (S)

- [x] **P0.1** Create Python package, CLI entry point, dependency setup, and ignore rules. (XS)
- [x] **P0.2** Define configuration schema and small pilot config. (XS)
- [x] **P0.3** Record available CPU, RAM, GPU, disk, and serving backend. (XS)

Gate: the CLI loads and validates a configuration; invalid settings fail clearly. No large download is required.

### Phase 1 — data and evidence (M)

- [ ] **P1.1** Define document, question, evidence-span, and split records. (S)
- [ ] **P1.2** Implement SQuAD ingestion and article reconstruction with offsets. (S)
- [ ] **P1.3** Implement HotpotQA shared-corpus ingestion and sentence provenance. (S)
- [ ] **P1.4** Save deterministic development/evaluation IDs and corpus manifests. (XS)
- [ ] **P1.5** Check evidence presence, duplicate handling, and split leakage. (XS)

Gate: a small sample from each dataset has inspectable source text and correctly mapped evidence. Corpus construction is identical across configurations.

### Phase 2 — chunking and BM25 vertical slice (M)

- [ ] **P2.1** Implement fixed-token chunking with offsets. (S)
- [ ] **P2.2** Implement sentence-aware chunking and long-sentence fallback. (S)
- [ ] **P2.3** Build a BM25 index and return ranked chunk records. (S)
- [ ] **P2.4** Implement reference-token context packing and evidence coverage. (S)

Gate: one command processes a query from either dataset into retrieved chunks, packed context, and evidence metrics. All six chunk profiles can be generated and their actual size distributions inspected.

### Phase 3 — Dense and Hybrid retrieval (M)

- [ ] **P3.1** Add BGE encoding, normalized vectors, and exact FAISS search. (S)
- [ ] **P3.2** Add E5 with its query/passage prefixes and length validation. (S)
- [ ] **P3.3** Add RRF, deterministic tie-breaking, and chunk-ID deduplication. (XS)
- [ ] **P3.4** Save/load indexes with corpus, tokenizer, and model fingerprints. (S)
- [ ] **P3.5** Record query encoding, search/fusion timing, and offline costs. (XS)

Gate: all five retrieval recipes run on the same corpus and return the same record schema. A stale or mismatched index is rejected.

### Phase 4 — Stage A runner and selection (M)

- [ ] **P4.1** Generate exactly 30 unique conditions per dataset. (XS)
- [ ] **P4.2** Add query-level JSONL records, manifests, and safe resume. (S)
- [ ] **P4.3** Run development screening and produce the declared selection table. (S)
- [ ] **P4.4** Freeze the embedder/chunker choice and held-out plan. (XS)
- [ ] **P4.5** Evaluate held-out retrieval and produce latency/coverage summaries. (S)

Gate: all choices have a recorded development basis. Each aggregate can be traced to per-question records. Interrupted work resumes without duplicate successful request keys.

### Phase 5 — generation and reranking (M)

- [ ] **P5.1** Integrate one local LLM with timeout/error handling and timing. (S)
- [ ] **P5.2** Add the second model through the same adapter. (XS)
- [ ] **P5.3** Add the fixed cross-encoder and on/off paths. (S)
- [ ] **P5.4** Add answer scoring, abstention, and truncation reporting. (S)
- [ ] **P5.5** Add No-RAG and gold-evidence diagnostic conditions. (XS)

Gate: a handful of questions completes on both models; the prompt, context, output, token counts, metrics, and timings are inspectable. Reranking changes order without changing the initial candidate set.

### Phase 6 — feasibility pilot and study freeze (S–M)

- [ ] **P6.1** Run 20 development questions spanning both datasets and representative conditions. (S)
- [ ] **P6.2** Estimate total runtime and memory from measurements. (XS)
- [ ] **P6.3** Verify warmup, cache behavior, model residency, and timer boundaries. (S)
- [ ] **P6.4** Freeze models, quantization, sample size, prompts, and run manifest. (XS)

Gate: the intended 14,400 main requests have a measured runtime estimate. Any reduced sample or smaller-model fallback is recorded before held-out generation begins.

### Phase 7 — Stage B experiments (L; mostly compute)

- [ ] **P7.1** Enumerate 12 pipeline configurations and 48 dataset/model conditions. (XS)
- [ ] **P7.2** Execute randomized, sequential blocks with three timing repetitions. (S orchestration, plus compute)
- [ ] **P7.3** Run diagnostic baselines and record failures separately. (XS orchestration, plus compute)
- [ ] **P7.4** Check completeness and archive raw measurements with manifests. (S)

Gate: each planned request is completed or explicitly marked failed. No model/configuration changes are mixed into the frozen run set.

### Phase 8 — analysis and delivery (M)

- [ ] **P8.1** Generate paired quality and latency comparisons with confidence intervals. (S)
- [ ] **P8.2** Produce stage-time breakdowns, evidence-retrieval charts, and quality–latency plots. (S)
- [ ] **P8.3** Inspect a small declared sample of retrieval and generation failures. (S)
- [ ] **P8.4** Summarize dataset/model dependence and validity limits. (S)
- [ ] **P8.5** Refresh ignored local docs and export a reproducibility bundle. (S)

Gate: conclusions answer the research questions, identify sample sizes and failures, and link to measurements. The export includes enough non-Git artifacts to reproduce the analysis; Git alone is not claimed to contain the full study.


## Optional extensions — after the core study

Candidate depth 20 versus 50; overlap 0% versus 20%; a third chunk size in end-to-end runs; concurrent load; caching; a larger corpus; an additional generator. Add one controlled factor at a time with a separate manifest and budget. Do not expand the required matrix accidentally.


## Final delivery checklist

- [ ] All required phase gates have evidence in PROGRESS.md.
- [ ] Configuration counts, sample sizes, and actual completion totals agree.
- [ ] Reports disclose failures, exclusions, adapted corpus scope, and selection limitations.
- [ ] Source/configuration files are ready for Git; ignored docs/tests are absent from staging.
- [ ] Ignored raw results, indexes or reconstruction instructions, and environment metadata are archived outside Git.
- [ ] A fresh environment can reproduce the documented small workflow and analysis export.
