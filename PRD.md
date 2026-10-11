# ragbench-lab — product requirements

Status: implementation specification drafted. No implementation or benchmark execution has been verified.

Repository: `ragbench-lab` (working name).

Description: An academic research project evaluating RAG retrieval, chunking, and performance trade-offs.

Document roles: PRD.md defines what to build and measure; AGENTS.md defines contributor rules; PLAN.md owns task order and completion gates; PROGRESS.md records actual status and evidence.

## Purpose

Build a small, local Python benchmark for a master's software performance evaluation project. Measure how retrieval, chunking, and reranking affect RAG latency, evidence retrieval, answer quality, and resource use.

Research question: how do RAG pipeline configurations affect end-to-end performance across two datasets and two small LLMs?

The deliverable is a reproducible experiment runner, saved measurements, and an analysis. The project should fit roughly four weeks of full-time work, subject to measured hardware performance.

## Goals and boundaries

- Compare five retrieval recipes and six chunking profiles before expensive generation runs.
- Evaluate a controlled set of 12 end-to-end configurations across two datasets and two LLMs.
- Explain quality–latency trade-offs and where time is spent.
- Preserve enough provenance to reproduce each reported result.
- Keep setup and operation practical on one machine, loading one generator at a time.

Exclude model training, a chat UI, distributed serving, agentic retrieval, production deployment, and caching optimization from the required scope. Concurrency and load testing are optional extensions. Sequential measurements do not establish concurrent serving capacity.

## Users and workflow

The researcher prepares datasets, builds indexes, runs a pilot, freezes experiment settings, executes experiments, and exports figures. A professor or reviewer should be able to understand each configuration and trace a plotted value to its measurements.

Planned CLI commands: `prepare`, `index`, `retrieve`, `pilot`, `run`, and `report`. Commands accept a configuration path and support bounded sample sizes. Long runs support safe resumption. These commands are requirements, not claims of existing functionality.

## Experimental design

### Stage A: retrieval screening

| Factor | Levels |
| --- | --- |
| Retrieval | BM25; Dense–BGE; Dense–E5; Hybrid–BGE; Hybrid–E5 |
| Chunking | Fixed-token; sentence-aware |
| Target chunk size | 64, 128, 256 reference tokens |
| Overlap | 0%, fixed |
| Reranking | Off, fixed |

Five retrieval recipes × two chunking methods × three sizes = 30 configurations per dataset, or 60 conditions across two datasets. No generator is required.

Use `BAAI/bge-small-en-v1.5` and `intfloat/e5-small-v2`. Hybrid recipes combine BM25 with the corresponding Dense retriever using reciprocal rank fusion (RRF). Fix the RRF constant at 60 and distinguish it from retrieval depth. Normalize Dense vectors and use exact FAISS search initially; approximation adds an unnecessary variable at this scale.

Retrieve 50 candidates per constituent retriever. For Hybrid, fuse the union and keep the best 50 unique chunk IDs. Do not imply that Hybrid examines the same number of initial candidates as a single retriever; its extra work is part of the measured cost. Fix BM25 parameters and all preprocessing settings in configuration.

Use development data to select one embedding model and one chunking method for Stage B. Score each embedding–method pair by macro-averaged evidence coverage at the fixed context budget, giving each dataset equal weight and averaging its Dense/Hybrid and three size conditions. Freeze this rule before screening. Define “close” as within one absolute percentage point; among close candidates prefer lower retrieval latency, then indexing cost. Preserve all candidate scores.

Evaluate all 30 configurations on held-out questions after freezing the selection. Do not revise Stage B settings using held-out results.

### Stage B: end-to-end evaluation

| Factor | Levels |
| --- | --- |
| Retrieval family | BM25; Dense; Hybrid |
| Chunk size | 128, 256 reference tokens |
| Reranking | Off; On |
| Chunking method and embedder | Selected on development data, then fixed |

Three families × two sizes × two reranking states = 12 pipeline configurations. Two datasets × two generators produce 48 experimental conditions.

The number 12 follows from a factorial design. Papers motivate the factors; they do not prescribe this exact count. The two sizes provide a bounded contrast, not an exhaustive search for an optimum.

Stage B conclusions about answer quality apply to the selected embedder and chunking method. Stage A alone cannot establish their end-to-end answer-quality ranking.

Use `cross-encoder/ms-marco-MiniLM-L-6-v2` as the initial reranker candidate. Pin its revision and verify its supported input length before use. Rerank the same initial candidate list used by the corresponding off condition. Detect pair truncation rather than silently discarding passage text.

### Datasets and splits

Use SQuAD v1.1 and HotpotQA. Start with 50 development questions and 100 held-out evaluation questions per dataset. Save IDs, source revisions, sampling seeds, and corpus hashes. Keep development and evaluation question IDs disjoint; avoid shared source articles where feasible and record remaining document overlap.

For SQuAD, reconstruct documents by joining the available paragraphs for an article in source order. Preserve original paragraph IDs, answer spans, and mapped document offsets. These are reconstructed dataset documents, not necessarily full Wikipedia articles.

For HotpotQA, create a frozen shared corpus from deduplicated context passages in a declared validation pool. Search the same corpus for every query, rather than each query's private distractor list. Preserve source titles and sentence IDs; handle differing passages with the same title explicitly. Describe this as an adapted HotpotQA corpus, not the official full-Wikipedia benchmark.

Index source text only. Questions, answers, and supporting-fact labels belong in evaluation records, never embedded into searchable text. Check that all annotated evidence is present. Record missing-evidence cases and a declared exclusion policy before running experiments.

### Chunking and context control

Use one pinned reference tokenizer for corpus chunking and context budgeting, initially the BGE tokenizer. This keeps chunk boundaries independent of the embedder or generator being compared. Check actual input lengths under both embedding tokenizers, including prefixes and special tokens.

Fixed-token chunking creates non-overlapping windows. Sentence-aware chunking packs sentences up to the target size; split overlong sentences with the fixed-token fallback. Preserve character offsets in both methods. Report actual lengths, chunk counts, fallback counts, and the percentage of documents affected by each size.

Pack ranked chunks into a 1,024-reference-token evidence budget, including evidence separators and identifiers. Append in rank order and truncate the final chunk to the remaining budget with exact provenance. Score evidence coverage on the text actually supplied. Record any underfilled contexts.

The two LLMs receive identical context text for a given query and pipeline configuration. Their native token counts may differ; record both. Check the full prompt and output allowance against each model's configured context window. Do not silently truncate prompts.

### Generators and baselines

Preferred models: Qwen2.5-3B-Instruct and Llama-3.2-3B-Instruct, using one local serving backend and comparable quantization. Verify access, memory, and runtime during the pilot. Pin exact model artifacts or digests, chat templates, quantization, and backend version.

If the pilot makes 3B impractical, use Qwen2.5-1.5B and Llama-3.2-1B before freezing the study. Record that size and family then vary together. Do not substitute models midway through a result set.

Use the same instruction text, temperature 0, and initially a 64-token output cap. Ask for a short answer grounded in context, with an explicit abstention token when evidence is insufficient. Record output length and truncation. Deterministic settings do not guarantee identical outputs on every backend.

Add No-RAG and gold-evidence-context diagnostic baselines. Gold evidence is a diagnostic reference, not a guaranteed numerical upper bound. Run baselines separately from the 12-configuration factorial and identify them in outputs.

## Measurement requirements

| Area | Required measurements |
| --- | --- |
| Retrieval | Evidence coverage at k = 5, 10, 50; coverage inside packed context |
| SQuAD evidence | Whether the annotated answer span is covered; supporting-paragraph coverage as a separate diagnostic |
| HotpotQA evidence | Fraction of annotated supporting sentences covered; all-required-evidence success |
| Answers | Dataset-appropriate normalized Exact Match and token F1; abstention and truncation rates |
| Online timing | Query embedding, search/fusion, reranking, packing, generation, total request latency |
| Summaries | Median and p95 latency, with sample counts and uncertainty |
| Offline costs | Chunking/embedding/indexing time, index size, chunk count |
| Resources | Python plus model-server memory; GPU memory if available |

Map retrieved text to original evidence using offsets and IDs. Overlapping chunks must not inflate evidence counts. Answer-string matching alone is insufficient evidence scoring, especially for yes/no HotpotQA questions.

Use monotonic timers and synchronize accelerator work when necessary for isolated stage timings. Measure total latency from receipt of a query through receipt of the complete answer. Offline indexing is reported separately. A client streaming timestamp may be reported as time to first visible output; label it accurately rather than claiming exact server TTFT.

Warm each model and index before measured runs. Keep requests sequential and randomize configuration order in recorded blocks. Recompute the full online retrieval path during measured requests. Reusing indexes is allowed; precomputed query embeddings or retrieval results must not silently bypass timed work.

Disable reusable response/KV caching where supported. Otherwise document backend behavior and use a verified isolation procedure. Warm model weights and warm indexes are distinct from reusing a previous response's computation.

Run three timing repetitions per question/configuration. Predeclare the first repetition as the answer-quality observation, and report output instability separately. Repeated runs do not increase the independent question count. Use paired bootstrap confidence intervals over questions; cluster by source document when appropriate. Treat p95 estimates from small samples cautiously.

## Run records and reproducibility

Write append-only JSONL records with schema version, run ID, condition ID, query ID, repetition, status, timestamps, config hash, model/index identifiers, retrieved chunk IDs, evidence mappings, prompt/context hashes, answer, metrics, token counts, and timings. Preserve full prompts/context in a local artifact or reconstruct them exactly from frozen IDs and templates.

Every run has a manifest containing the Git revision and dirty-state flag, package versions, hardware, thread settings, seeds, corpus hashes, quantization, cache policy, and the resolved configuration. Checkpoint completed requests and resume only when manifest identities match.

Record failures, timeouts, retries, and partial outputs. Never silently remove failed requests or mix retries with successful first attempts. Report successful-request latency alongside failure rate. Flush records promptly and avoid overwriting prior runs.

## Implementation shape

Use Python 3.11+, a standard `src/ragbench_lab` package, typed data records, configuration files, and thin CLI commands. Suggested dependencies are Hugging Face Datasets, SentenceTransformers, FAISS, rank_bm25, an HTTP client for Ollama, psutil, pandas, and matplotlib. Use pytest locally and a linter; pin the resolved environment.

Suggested modules: `data`, `chunking`, `retrieval`, `reranking`, `context`, `generation`, `metrics`, `runner`, and `reporting`. Keep interfaces small. Add a library only when an implemented requirement needs it.

Track source, configs, lockfile, this PRD, AGENTS.md, PLAN.md, PROGRESS.md, and compact non-sensitive run manifests. Keep raw datasets, models, indexes, logs, generated results, local tests, README, and project deep dive outside Git. Provide explicit export commands so ignored research artifacts can still be archived with the final report.

## Delivery sizes and schedule

| Size | Deliverable | Estimate |
| --- | --- | --- |
| XS | One bounded task with one observable outcome | 1–2 hours |
| S | One module or CLI capability | Half a day |
| M | One integrated pipeline stage | 1–2 days; split into S tasks |
| L | Complete experiment stage | Several days; split before coding |

Week 1 covers setup, data, chunking, and a BM25 vertical slice. Week 2 adds Dense/Hybrid retrieval and Stage A. Week 3 adds generation, reranking, and the frozen Stage B runs. Week 4 covers analysis, failure inspection, and reporting. Unattended compute time is separate from implementation time.

At 100 questions per dataset and three repetitions, Stage B requires 12 × 2 × 2 × 100 × 3 = 14,400 main generation requests. Pilot 20 questions before committing to the full workload. A mean of 10 seconds implies about 40 hours; 30 seconds implies 120 hours, excluding setup and diagnostics.

If compute is excessive, reduce the evaluation sample consistently before freezing the study and report wider uncertainty. Preserve the factorial structure. Never choose the final sample size based on whether a desired result becomes significant.

## Acceptance criteria

- A small command-line run completes from prepared corpus through scored answer and report.
- Both dataset adapters preserve verifiable evidence mappings and deterministic splits.
- Stage A enumerates exactly 30 unique configurations per dataset; Stage B exactly 12 per dataset/model.
- Every plotted number traces to records and a frozen manifest.
- Held-out evaluation does not influence setting selection.
- Resume produces no duplicate successful request keys or mixed configurations.
- Latency charts separate offline work, retrieval, reranking, and generation.
- Reports include quality–latency plots, configuration comparisons, sample sizes, failures, and limitations.
- No performance claim is presented as a result before it has been measured.

## Research references

These motivate the design; exact project values remain explicit engineering choices.

- Wang et al., Searching for Best Practices in Retrieval-Augmented Generation, EMNLP 2024: https://aclanthology.org/2024.emnlp-main.981/ — retrieval families, reranking, chunk-size comparisons.
- Rethinking Chunk Size for Long-Document Retrieval, 2025: https://arxiv.org/abs/2505.21700 — chunk-size and dataset dependence.
- A Systematic Analysis of Chunking Strategies for Reliable Question Answering, 2026 preprint: https://arxiv.org/abs/2601.14123 — chunking methods and context budgeting.
- RAGPerf, 2026: https://arxiv.org/abs/2603.10765 — component-level and end-to-end measurement.
- RAG-Stack, 2026: https://arxiv.org/abs/2608.03487 — performance/quality trade-offs.

## Repository and writing policy

Use natural, short, lowercase commit messages. Keep README, project deep dive, and test files local and ignored by Git. Write local explanatory documentation in a human, conversational tone with short paragraphs. AGENTS.md defines the exact contributor workflow and ignore patterns.
