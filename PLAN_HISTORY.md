# ragbench-lab — implementation plan

## How to use this plan

PRD.md defines requirements. AGENTS.md defines contributor rules. This file owns the ordered task checklist. PROGRESS.md records actual work, verification, decisions, and the next task.

Start with the earliest unblocked task in the authorized phase. Mark a task complete only after its observable output and the phase-relevant checks exist. Update this checklist and PROGRESS.md together. If a task is too large, split it into lettered subtasks while keeping its stable ID.

Current status (15 October 2026): Phases 0–8 are complete for reduced v3.
Stage A finished 9,000 development and 18,000 held-out retrieval requests; Stage B
finished 3,600 main and 600 separate baseline requests. Analysis, figures, case
review, synthesis and core delivery have saved verification evidence.

The optional read-only dashboard, XD.10 review improvements and XD.11 text-only
question labels and D.1 documentation refresh are complete. XG and XC
implementation/experiments remain pending; XC.0 is a recorded predeclaration only.
No additional required benchmark compute remains. User authorization is still
required for optional studies, external publication, commits or pushes.

Chronological launches, interruptions and superseded checkpoints belong in
PROGRESS.md. The current statuses below supersede those historical checkpoints.

## Stage B 50-question expansion — 2026-10-17

User selected 50 evaluation questions per dataset. Completed reduced v3 and all
historical exports remain immutable. This is a post-results sample expansion,
not a new untouched confirmatory holdout. Preserve all twelve pipelines, both
generators, three repetitions and the Stage A freeze. No identifier/prompt changes.

- [x] B50.1 — done: support a deterministic nested 50-ID sample, freeze a
  separate v4 plan, validate 7,200 main plus 1,200 baseline identities and preserve
  legacy plans. Fresh measurements only; no imported or pooled historical rows.
- [x] B50.2 — done: local asset preflight and historical runtime estimate;
  exact bounded commands recorded in configs/stage-b-50-protocol.json for a fresh
  compatible 144-request development gate. Model compute requires an explicit bounded allowance; no automatic launch.
- [x] B50.3 — done: execute the development gate, then review its measured
  runtime/resources before authorizing bounded main sessions.
- [x] B50.4 — done: all 7,200 main and 1,200 separate baseline evaluation
  requests plus fresh 144/24 development gates completed without request/setup
  failures. V4 raw archive, paired analysis (56 cells/220 contrasts), six vector
  plots, 2,920-example dashboard snapshot and companion analysis package verified.
  Fresh-workspace replay reproduces numerical tables and all report fields except
  recorded analysis provenance/hash; 43 extracted-workspace tests passed.
  V3 outputs remain separate. Optional qualitative v4 review/synthesis remain unrun.


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
- Active Stage B workload: 48 × 25 questions × 3 repetitions = 3,600 main requests, plus 600 separately labeled baseline requests. Development diagnostics/warmups are additional. Original 14,400-request plans remain historical, not the active target.
- Use the declared smaller-model or sample-size fallback only before study freeze. Keep all resulting changes in the decision log.

## Task sizes and phase gates

### C.1 — behavior-preserving cleanup (2026-10-16)

- [x] C.1a — done: audited source definitions and source/test/script/config/doc references; removed stale CSS, unused comparison variables and redundant cell-ID bookkeeping; shared five dropdown selection paths and disclosure markup; reused prediction token counts and an already loaded tokenizer.
- [x] C.1b — done: all 4,812 serialized behavior fingerprints match; core discovery ran 261 tests (230 passed, 31 optional viewer skips), isolated dashboard suite passed all 45; whole-source Ruff, JavaScript syntax, CLI help/config hash and whitespace checks passed.

Keep public interfaces, CLI/configuration semantics, scientific guards, saved outputs,
compatibility consumers, dependencies and the current dashboard appearance intact.
No experiments, archive rewrites, automatic commits or pushes belong to this task.

### C.2 — conservative frontend cleanup (2026-10-16)

- [x] C.2a — done: reused each facet's available values within the callback in Python/JavaScript, grouped identical width rules and the repeated 850px media block; corrected search focus styling to target Dash's wrapper via focus-within. Existing identity, DOM/hooks and requested motion retained.
- [x] C.2b — done: 500 old/new Python/browser filter cases agree, 4,812 saved rendering/score fingerprints unchanged, all 45 focused tests pass; 18 real-browser tab/viewport style/layout comparisons and focus/filter/reset/motion/idle checks passed without JavaScript errors.

### D.2 — shorter deep dive and AI disclosure (2026-10-16)

- [x] D.2 — done: reduced PROJECT_DEEP_DIVE.md from 1,836 to 997 words, simplified the tone and added first-person AI-use disclosure. Preserved study amendments, controls, interpretation limits, dashboard/replay instructions and the README anchor; local links/module paths, shell syntax and whitespace checked.

### D.3 — concise report and deep dive (2026-10-16)

- [x] D.3 — done: report reduced from 1,947 to 665 words; deep dive from 997 to 482. Findings and operation are separated; essential scope/history/limits and AI disclosures retained. Local links/anchors, module paths, shell syntax, four result ranges, reranking signs/range and saved request counts checked.

### D.4 — publish selected documentation (2026-10-16)

- [x] D.4 — done: explicitly selected PROJECT_DEEP_DIVE.md and report.md only; privacy/content/staged-file review passed, local-only links changed to plain references, committed as 38e8600 and pushed to origin/main. GitHub noreply metadata used; other ignored files remain local.

### D.5 — expanded implementation deep dive (2026-10-16)

- [x] D.5 — done: expanded PROJECT_DEEP_DIVE.md using the supplied CACHEUS document as a structural reference, with current code/data contracts, algorithms, request walkthrough, timing/cache controls, bounded resume, scoring/statistics, outputs, viewer, replay and extension boundaries. Checked links/anchors, shell syntax, real CLI plans, saved counts and result claims, and privacy. Short report, AI wording and README anchor preserved; no experiments or publishing.

### P.1 — public aggregate results and verification (2026-10-16)

- [x] P.1a — done: aggregate-only results/stage-b-v3 has 56-condition lookup, unchanged cell/contrast/stage CSVs, three original SVGs and a source/hash/method manifest (637,007 bytes). Explicit ignore allowlist and byte-preserving Git attributes prevent private extras and newline-induced integrity failures; original records/archives remain local and unchanged.
- [x] P.1b — done: standalone standard-library export and verification scripts, short README/deep-dive usage, and 24 passing ignored focused tests. Exact source/interval parity, isolated public-only execution, privacy/SVG checks, factorial/contrast/timer integrity, overwrite rejection, Git filters, lint and whitespace verified. No staging, commit or push; next is user review.

### V.1 — fresh-checkout verification (2026-10-16)

- [x] V.1a — done: standard-library-only scripts/verify_checkout.py runs eight
  named groups covering source syntax/configuration, exact study factorials,
  synthetic adapters/splits, chunk/source offsets, BM25/RRF, packed evidence/scoring,
  append-only resume and existing public aggregate verification. Temporary inputs
  are cleaned and dependencies/network/subprocesses guarded; no ignored assets needed.
- [x] V.1b — done: read-only pinned-action CI for Linux Python 3.11/3.14 and
  macOS/Windows 3.14; 13 local regressions pass on both installed Python versions,
  including isolated checkout, corruption/mutation guards and no checkout writes.
  Workflow structure, Ruff, optimized runs and whitespace pass. Hosted CI run
  38932496632 completed successfully after push; native/model replication is excluded.

Decision: operational smoke scenarios belong to the explicit verification command;
local unittest modules/fixtures/reports remain ignored. This does not change the
frozen study, authorize benchmark requests, or establish native/model replication.
Critical scope/commands/invariants are in configs/checkout-verification.json.
Committed/pushed as 9145e27 after explicit authorization; first hosted CI passed.
No further work remains for V.1; native/model replication remains separate.

XS = 1–2 hours. S = half a day. M = 1–2 days and must be split into S tasks. L = several days and must be split before coding. Estimates describe implementation effort, not unattended benchmark runtime.

Each task should name its input, output, and observable completion check. Complete each phase's gate before depending on it. Do not replace the research pipeline with a demo that returns canned answers.

### Phase 0 — scaffold and constraints (S)

- [x] **P0.1** Create Python package, CLI entry point, dependency setup, and ignore rules. (XS)
- [x] **P0.2** Define configuration schema and small pilot config. (XS)
- [x] **P0.3** Record available CPU, RAM, GPU, disk, and serving backend. (XS)

Gate: the CLI loads and validates a configuration; invalid settings fail clearly. No large download is required.

### Phase 1 — data and evidence (M)

- [x] **P1.1** Define document, question, evidence-span, and split records. (S)
- [x] **P1.2** Implement SQuAD ingestion and article reconstruction with offsets. (S)
- [x] **P1.3** Implement HotpotQA shared-corpus ingestion and sentence provenance. (S)
- [x] **P1.4a** Implement deterministic splits and source/corpus/evaluation manifests. (XS)
- [x] **P1.4b** Prepare and pin real source pools for both datasets. (XS; SQuAD and pinned HotpotQA mirror pilots verified)
- [x] **P1.5a** Validate evidence presence, duplicates, split isolation, and saved identities locally. (XS)
- [x] **P1.5b** Inspect and verify prepared samples from both real datasets. (XS)

Gate: a small sample from each dataset has inspectable source text and correctly mapped evidence. Corpus construction is identical across configurations.

### Phase 2 — chunking and BM25 vertical slice (M)

- [x] **P2.1** Implement fixed-token chunking with offsets. (S)
- [x] **P2.2** Implement sentence-aware chunking and long-sentence fallback. (S)
- [x] **P2.3** Build a BM25 index and return ranked chunk records. (S)
- [x] **P2.4** Implement reference-token context packing and evidence coverage. (S)

Gate: one command processes a query from either dataset into retrieved chunks, packed context, and evidence metrics. All six chunk profiles can be generated and their actual size distributions inspected.

### Phase 3 — Dense and Hybrid retrieval (M)

- [x] **P3.1** Add BGE encoding, normalized vectors, and exact FAISS search. (S)
- [x] **P3.2** Add E5 with its query/passage prefixes and length validation. (S)
- [x] **P3.3** Add RRF, deterministic tie-breaking, and chunk-ID deduplication. (XS)
- [x] **P3.4** Save/load indexes with corpus, tokenizer, and model fingerprints. (S)
- [x] **P3.5** Record query encoding, search/fusion timing, and offline costs. (XS)

Gate: all five retrieval recipes run on the same corpus and return the same record schema. A stale or mismatched index is rejected.

### Phase 4 — Stage A runner and selection (M)

- [x] **P4.1** Generate exactly 30 unique conditions per dataset. (XS)
- [x] **P4.2** Add query-level JSONL records, manifests, and safe resume. (S)
- [x] **P4.3a** Implement and validate development selection tables on synthetic runs. (XS)
- [x] **P4.3b** Resolve 10/10 pilot versus PRD 50/100 samples and full-corpus compute budget. (XS; separate 50/100 preparations verified; full profile/native-length preflight and explicit planning allowances recorded)
- [x] **P4.3c** Run full development screening and preserve all candidate scores. (S plus compute; done, 9,000 successes and all four candidate scores verified)
- [x] **P4.4a** Implement diagnostic/incomplete-run guards and frozen held-out identities. (XS)
- [x] **P4.4b** Freeze the real development-selected embedder/chunker and held-out plan. (XS; done, verified selection manifest and full held-out run identity)
- [x] **P4.5a** Implement saved-record coverage/timing summaries with clustered uncertainty. (XS)
- [x] **P4.5b** Evaluate held-out retrieval and produce final summaries. (S plus compute; done, 18,000 successes and final report verified)

P4.3–P4.5 are split into implementation and measured study work. Bounded
diagnostics do not complete screening, freeze, or held-out evaluation.

The completed Stage A scope is `configs/stage-a-study.toml`, with separate
50/100 full-corpus preparations. Development run
`8aee356a-46ae-4af2-9fc0-496a74d40a64` completed 9,000 requests; held-out run
`7b44f0dd-5dac-4553-a442-0f58e197f946` completed 18,000. Both summaries and all
candidate scores are preserved.

E5 sentence-aware selection is frozen in `manifests/stage-a-selection-v1.json`,
identity `0ef5eef4ba57f109f4edd9539243e3f617f735f292576cec2da82ec948614f2b`.
Held-out results did not change it. Preparation/capacity manifests retain original
source checks and planning estimates; session-by-session history stays in PROGRESS.md.

Gate: done. Choices have a declared development basis; summaries trace to
per-question records, and resume preserves successful request identity.

### Phase 5 — generation and reranking (M)

- [x] **P5.1** Integrate one local LLM with timeout/error handling and timing. (S; done, verification in PROGRESS.md)
- [x] **P5.2** Add the second model through the same adapter. (XS; done, verification in PROGRESS.md)
- [x] **P5.3** Add the fixed cross-encoder and on/off paths. (S; done, verification in PROGRESS.md)
- [x] **P5.4** Add answer scoring, abstention, and truncation reporting. (S; done, verification in PROGRESS.md)
- [x] **P5.5** Add No-RAG and gold-evidence diagnostic conditions. (XS; done, verification in PROGRESS.md)

Gate: a handful of questions completes on both models; the prompt, context, output, token counts, metrics, and timings are inspectable. Reranking changes order without changing the initial candidate set.

Phase 5 gate is done: corrected attempt 5 passed all sixteen real-model
diagnostics on pinned Qwen/Llama 3B Q4_K_M artifacts. Paired contexts and
native/backend token counts matched, with failed earlier attempts preserved.
Subsequent Phase 6 cache/pilot validation is also complete.

### Phase 6 — feasibility pilot and study freeze (S–M)

- [x] **P6.1** Run 20 development questions spanning both datasets and representative conditions. (S; done, all 40 paired-model requests verified)
- [x] **P6.1a** Verify repeated-prompt cache behavior and an explicit isolation procedure. (XS; six baseline and six isolated probes saved)
- [x] **P6.1b** Complete the bounded paired pilot and preserve timings/resources/failures. (XS plus compute; done)
- [x] **P6.2** Estimate total runtime and memory from measurements. (XS; done, 27.7 hours main/setup projection, 41.5 hours planning allowance, 5.2 GiB sampled RSS)
- [x] **P6.3** Verify warmup, cache behavior, model residency, and timer boundaries. (S; done, zero cache counts and paired contexts verified; decoder warmth limitation recorded)
- [x] **P6.4** Freeze scientific models, quantization, sample size, prompts, and prospective study manifest. (XS; done, execution runner provenance must be pinned in Phase 7)

Gate: the intended 14,400 main requests have a measured runtime estimate. Any reduced sample or smaller-model fallback is recorded before held-out generation begins.

Pilot plan: ten deterministic development questions per dataset, paired across both
models (40 requests, 20 independent questions), six representative profiles covering
all factor levels. Profile interactions are not exhaustively measured. Explicit
unload/empty-prompt preload before every request clears prompt reuse; isolation cost
is separate from online latency and included in planning. Retrieval/reranker warmup
is offline. Loaded weights do not guarantee warm decoder kernels after reset.
Freeze requires all 40 successes, zero cached prompt tokens, matching paired evidence,
valid memory samples under 12 GiB RSS, and a 1.5x-headroom runtime allowance under
48 hours. These planning thresholds are predeclared, not measured conclusions.
The prospective study plan retains 100 held-out questions, preferred 3B models and
the full 12-pipeline/48-condition/14,400-request design. Phase 7 execution provenance
must still be pinned after its runner is implemented; no Stage B request starts here.

Phase 6 gate is done. Pilot run `c4686f55-6779-4127-87c6-1e1465095e8f` completed
40/40 without failures; prospective freeze identity
`ca0b183f7dd84cfe3ea43c27ec425493f82736850fb2e7d68feac95f5a1e7fe6`.
The scientific freeze is separate from execution provenance. P7.1/P7.2a/P7.2b
are complete. Reduced v3 held-out execution and baselines are also complete;
the original Phase 6 100-question plan remains preserved as historical context.

### Phase 7 — Stage B experiments (L; mostly compute)

### Approved reduction — 14 October 2026

- [x] **P7.R1** Freeze the outcome-blind reduced sample and preserve prior records. (done: separate v3 manifest, 25 IDs per dataset, 3,600 unique main requests; preservation audit; no old requests imported)
- [x] **P7.R2** Support the explicit frozen subset in planning and execution preflight. (done: original 100-question plans remain supported; reduced samples must match the exact ID-only rule; local validation recorded in PROGRESS.md)
- [x] **P7.R3** Commit stable source and pass a fresh compatible 144-request development diagnostic. (done: 144/144, zero failures, four-request pause/resume, compatible source `9d48ed8`, released lock and verified backend shutdown)
- [x] **P7.R4** Execute reduced v3 in explicitly bounded sessions. (done: 3,600/3,600 successes, zero failures, all paired controls verified, checkpoint saved and backend stopped)
- [x] **P7.R5** Execute and label the 600 reduced baseline requests. (done: 600/600 successes, 300 per baseline, zero failures, saved checkpoint and stopped backend)
- [x] **P7.R5a** Implement and locally validate separate baseline planning/execution. (done: frozen 600-slot parent-linked plan, CLI, 24-slot development gate, synthetic pause/resume/failure/offset checks and real local input preflight; 151 tests passed)
- [x] **P7.R5b** Commit stable baseline source and pass its own 24-request development diagnostic. (done: 24/24, zero failures, four-request pause/resume, compatible source `239734b`, released lock and verified dedicated backend shutdown)
- [x] **P7.R5c** Execute 600 separately labeled baseline requests in authorized bounded sessions. (done: complete failure-free separate evaluation, released lock and verified backend shutdown)

Manifest: `manifests/stage-b-study-v3-reduced.json`. Sampling and invariants:
`configs/reduced-study-protocol.json`. Stage A still uses the complete 50/100
prepared pools and its existing selection freeze; the source config is not edited.
Every pipeline/model/repetition uses the same selected IDs. Do not use existing
completion order or answer/latency scores to select questions. This is a declared
budget amendment after partial execution, with only 50 independent question units
and weaker tail estimates; professor approval is not claimed.

V1 retains 1,405 successes and its tokenizer failure; v2 retains 103 successes and
one user interruption, with its 144-request validation complete. New subset runner
code changes execution provenance, so no old timings/quality aggregates are imported
or pooled. No measurements are deleted or relabeled. Original phase/extension counts
below are historical unless explicitly revised here. Optional extensions remain deferred.

- [x] **P7.1** Enumerate 12 pipeline configurations and 48 dataset/model conditions. (XS; `stage-b-plan` validates the frozen study and emits 144 blocks/14,400 unique request identities; 117 tests passed)
- [x] **P7.2** Execute randomized, sequential blocks with three timing repetitions. (done for approved reduced v3: 3,600 main slots verified; original full-size v1/v2 remain preserved incomplete)
- [x] **P7.2a** Implement block-scoped setup, warmup, measured execution, and safe bounded resume with preserved failures. (S; `stage-b-run`, synthetic resume/failure tests and real local identity preflight passed; model-backed runner validation remains P7.2b)
- [x] **P7.2b** Verify tiny model-backed development diagnostics, interruption/resume, cache counts, paired contexts, and execution-manifest integrity. (XS plus bounded compute; 144/144 successes, no failures, real four-request pause/resume and final gate verified)
- [x] **P7.2c** Execute the frozen held-out matrix in explicitly authorized bounded sessions and verify three repetitions. (done for reduced v3: 3,600 success, 48 conditions and three repetitions; raw chain/pairing/checkpoint verified)

Historical v1 exception, resolved in a separate lineage: a session stopped at
1,405 successes plus a native/backend token-count mismatch (1,112/1,110).
The Llama export's merge policy differed from the backend. The exact-count guard
was retained; corrected assets, fresh validation and v2 received separate identities.
V2 later stopped at the user's request. Completed reduced v3 never pools those runs.

- [x] **P7.2d1** Diagnose the prompt-count discrepancy without changing frozen assets. (XS; four isolated backend probes reproduced it and verified an in-memory candidate; all 1,405 earlier token sequences unchanged)
- [x] **P7.2d2** Correct Llama export in a new asset set and add focused regressions. (XS; seven focused asset tests and full 137-test suite passed; exact-count guard unchanged)
- [x] **P7.2d3** Freeze a separate corrected study/execution identity and decide existing-result compatibility. (XS; v2 study/plan and explicit v1 lineage created; no timing/quality pooling or imported request rows; execution manifests remain gated on development validation)
- [x] **P7.2d4** Validate corrected assets on development diagnostics before bounded continuation. (done: 144/144 corrected diagnostics, zero failures, verified pause/resume and compatible evaluation gate under source `2a83c4a`; subsequent held-out session stopped by user at 103 successes plus one interrupted attempt)

Correction artifacts: `models/stage-b-corrected-v2`,
`manifests/stage-b-study-v2.json` (hash
`243b356e2c5e9b20d65be484458fda00e88b8c8a1dfb38e99b1f5ef73fca9bb1`),
`artifacts/stage-b-v2-compatibility-audit.json`, and
`artifacts/corrected-assets-smoke-v2`. Audit shows all 1,405 prior token sequences
match, but native counting algorithm cost can change inside online timing.
Therefore preserve v1 as separate historical evidence and plan all 14,400 new
v2 request slots after revalidation. No old success is reclassified or silently
discarded, and no new held-out request is launched here. Original Phase 6
capacity projections remain estimates, not newly measured v2 pilot findings.
- [x] **P7.3** Run diagnostic baselines and record failures separately. (done: 24 development and 600 held-out baseline successes; zero failures, no retries)
- [x] **P7.4** Check completeness and archive raw measurements with manifests. (done: all declared matrices/links/chains verified; 477-file local ZIP with prepared data, raw results, historical failures and five matching core source snapshots; independent SHA-256 verification passed)

Gate: each planned request is completed or explicitly marked failed. No model/configuration changes are mixed into the frozen run set.

P7.1's original plan is preserved in `artifacts/phase7-plan-v1.json`; it
enumerates conditions, not an execution run. The active completed identity is
`manifests/stage-b-study-v3-reduced.json`, with its own stopped execution manifest.

Runner gates: full compatible 144-request main development diagnostics and
24-request baseline diagnostics passed before evaluation. Each source/study
identity has its own provenance. Requests are bounded explicitly, failures stop
execution, retries are explicit, and compatible resume never changes a frozen plan.

Gate: done for reduced v3. All 3,600 main and 600 baseline requests succeeded;
raw chains, pairing and completeness are verified and archived. Future runner,
asset or study changes require new identity/gate evidence before bounded compute.
The original 14,400-slot descriptions do not authorize more work.

### Phase 8 — analysis and delivery (M)

- [x] **P8.1** Generate paired quality and latency comparisons with confidence intervals. (done: real 56-cell/220-contrast report, source-cluster and question-sensitivity intervals, independent exports/point checks)
- [x] **P8.1a** Record analysis protocol and validate paired estimators/cluster units. (done: source-cluster bootstrap, question sensitivity, explicit all-factor contrasts, no prospective-preregistration claim; fourteen focused tests passed)
- [x] **P8.1b** Verify archived input bindings, recompute scores and export real paired reports. (done: 4,200 raw-linked observations, 28 dataset macro cells/110 macro contrasts, CSV/JSON and independent verification proof)
- [x] **P8.2** Produce stage-time breakdowns, evidence-retrieval charts, and quality–latency plots. (done: six four-facet figures, SVG/PDF, verified 56-cell stage/evidence tables, independent raw-linked check and visual previews; 191 tests passed)
- [x] **P8.3** Inspect a small declared sample of retrieval and generation failures. (done: declared deterministic six-unit sample, twelve paired main/twenty-four matching baseline responses, source-offset/score checks, agent-authored qualitative notes and independent selection/export proof; 199 tests passed)
- [x] **P8.4** Summarize dataset/model dependence and validity limits. (done: four dataset/model profile summaries, 22 contrast groups retaining 120 original paired intervals, separate controls and bounded validity discussion; independent arithmetic proof and 208 tests passed)
- [x] **P8.5** Refresh ignored local docs and export a reproducibility bundle. (done: verified two-part raw/analysis delivery, refreshed local guides, 23 byte-identical fresh-workspace replay outputs and 65 packaged tests; full suite 216 passed; final archive proof stored externally)

Gate: conclusions answer the research questions, identify sample sizes and failures, and link to measurements. The export includes enough non-Git artifacts to reproduce the analysis; Git alone is not claimed to contain the full study.


## Optional extensions — after the core study

### Scope, status, and execution boundaries

The extension plan was written on 13 October 2026. Model and context work
(XG/XC) remains unimplemented/unrun, except the recorded XC.0 predeclaration.
The separately authorized local dashboard and review improvements are complete.

Original v1, corrected v2 and completed reduced v3 remain immutable and separate.
The extension workload tables retain their original 100-question reference scope;
they neither expand the 3,600-request core nor authorize acquisition or execution.
A future choice of different extension sampling needs its own explicit decision.

Use new extension manifests and separate run/output directories. Link their
parent study hash rather than editing v1. Each manifest must declare factors,
question IDs, scientific and execution settings, artifacts, provenance, quality
repetition, failure/retry policy, pairing rules, budget, and stop controls. Freeze
extension settings before held-out execution; changes create another run set.

XS tasks estimate 1–2 hours; S tasks estimate 3–4 hours of implementation or
verification effort. Downloads, pilots, and unattended compute are additional.
Split any task that proves larger before implementation. Dependencies listed
below are gates, not claims that the dependent features already exist.

| Separate study | Profiles per dataset/model | Conditions | Main requests |
| --- | --- | --- | --- |
| Original v1, unchanged | 12 | 48 | 14,400 |
| SmolLM-only replication | 12 | 24 | 7,200 additional |
| Original plus SmolLM replication | 12 | 72 | 21,600 combined |
| Independent context study, Qwen/Llama | 18 | 72 | 21,600 |
| Independent context study, three models | 18 | 108 | 32,400 |

Every count uses 100 questions per dataset and three repetitions. Pilots, warmups,
baselines, and retries are excluded. These are workload counts, not runtime
estimates or authorization to execute. The original pilot's 48-hour allowance
does not automatically cover either extension.

### XG — third-generator replication: SmolLM3-3B

Target `HuggingFaceTB/SmolLM3-3B` in explicitly verified `no_think` mode. Support
in the pinned Ollama 0.34.1 backend, an appropriate Q4_K_M artifact, the exact
mode switch, tokenizer framing, and answer extraction are **unverified**. Do not
invent a download tag or assume that prompt text alone disables thinking.

Keep the shared QA instruction, evidence text, reference tokenizer, selected E5
sentence-aware retrieval, both chunk sizes, candidate depth, reranker, seed,
temperature zero, and initial 64-token output cap. Pin model-specific framing and
mode controls separately. Any thinking markers, hidden output, or extraction
policy must be recorded and validated, not silently stripped from measurements.

| Task (all pending) | Dependency | Effort | Observable completion gate |
| --- | --- | --- | --- |
| [ ] **XG.1** Review backend architecture, template, and `no_think` support | P6.4; explicit implementation authorization | XS | Publisher/backend evidence documents the proposed exact disabling mechanism, expected raw output, and compatibility decision for Ollama 0.34.1; unresolved support blocks acquisition approval, and actual runtime mode verification remains required in XG.3. |
| [ ] **XG.2** Acquire and pin model inputs | XG.1 passes; acquisition authorized | XS | Suitable Q4_K_M artifact, source revision/digest, all blob hashes, native tokenizer, chat template, and mode controls are verified in a separate asset set; no unverified model substitution. |
| [ ] **XG.3** Add model framing and extraction validation | XG.2 | S | Focused tests and tiny development probes preserve shared instructions and validate `no_think`, exact native/backend prompt counts, full context plus output allowance, extraction, abstention, and output truncation. |
| [ ] **XG.4** Verify cache controls and backend regressions | XG.3; P7.2b | S | Explicit zero cached-prompt counts and pinned residency pass; missing counts fail. If backend/template changes were necessary, Qwen/Llama integration and cache/count regressions pass in separate run sets, with no changed-backend records merged into v1. |
| [ ] **XG.5** Repeat integration diagnostics | XG.4 | S | Both datasets, RAG reranking off/on, No-RAG, and gold-evidence checks preserve raw prompts/outputs/failures; paired contexts and initial candidate membership match. Model integration is not claimed from a single prompt. |
| [ ] **XG.6** Run development-only feasibility pilot | XG.5 | XS + compute | Existing Phase 6 twenty representative question/profile assignments are reused by ID (ten per dataset, six profiles); fresh SmolLM work records RSS, separate device allocation, online latency, isolation overhead, setup, and failures without reusing timed query work. |
| [ ] **XG.7** Resolve budget and freeze extension plan | XG.6; P7.2b | XS | Measured pilot projects 7,200 added main requests plus setup/baselines; explicit compute, memory, disk, headroom, and stop allowances are approved. New extension manifest pins settings and compatible comparison policy; v1 is unchanged. |
| [ ] **XG.8** Execute bounded replication and archive | XG.7; P7.4; explicit compute authorization | XS orchestration + compute | Twelve pipelines × two datasets × 100 questions × three repetitions produce 7,200 accounted-for requests in separate records; failures/retries and compatibility-aware Qwen/Llama comparisons are exported with provenance. |

XG gate: no held-out replication until support, integration, cache, pilot, and
budget gates pass. A required backend upgrade is a protocol change; obtain a new
extension identity and regression evidence rather than replacing the original
backend or extrapolating its feasibility unchanged.

### XC — context-budget experiment

Research question: does increasing the evidence budget improve evidence coverage
and answer quality enough to justify additional latency? Compare **512, 1,024,
and 2,048 reference tokens**. Fix chunk size at 256; compare BM25, Dense–E5,
Hybrid–E5, reranking off/on, both datasets, and Qwen/Llama initially.

This is 3 families × 2 reranking states × 3 budgets = 18 profiles. Independent
execution is 18 × 2 datasets × 2 models × 100 questions × 3 repetitions = 21,600
requests. A separately validated and budgeted SmolLM replication would add 10,800
requests, making 32,400 for the three-model context matrix. Do not conflate this
with XG's separate twelve-pipeline, 7,200-request replication.

Keep the pinned reference tokenizer, source offsets, packing/provenance rules,
selected E5 sentence-aware chunking, candidate depth 50, scoring, QA instructions,
seed, and output allowance fixed. Count identifiers and separators in the budget.
Evidence text must match across models for each question/configuration/budget;
different budgets deliberately contain different text. Check every full native
prompt plus the unchanged 64-token output cap against the configured model window.
Overflow must fail; do not trim evidence further for one model or enlarge only
one model's window silently.

Predeclare paired comparisons on the same questions for evidence coverage,
Exact Match, token F1, abstention, final-chunk and output truncation, generation
latency, total latency, and resource use. Report reference/native counts and
underfilled contexts. First repetition is the quality observation; cluster timing
repetitions by question and predeclare source-document clustering where appropriate.
Do not count three repetitions as three independent questions.

| Task (implementation/experiments pending) | Dependency | Effort | Observable completion gate |
| --- | --- | --- | --- |
| [x] **XC.0** Finalize context research protocol before answer-quality inspection | P6.4; before inspecting P7.2c held-out answer-quality findings | XS | Done: dated protocol below predeclares matrix, comparisons, metrics, clustering, overflow/failure policy, and reuse criteria before held-out generation begins; no extension feature or run is implemented. |
| [ ] **XC.1** Add separate context configuration and enumeration | XC.0; P7.2a | S | Extension-only settings accept exactly 512/1,024/2,048 and size 256; tests enumerate 18 profiles/72 conditions/21,600 identities. Existing core validation remains fixed at 1,024 and v1 counts remain unchanged. |
| [ ] **XC.2** Validate packing, provenance, and native limits | XC.1; P7.2b | S | Synthetic and tiny development checks cover separators/IDs, exact final offsets, reference/native counts, underfill, evidence-after-truncation scoring, shared paired text, reranker inputs, and full-prompt overflow without relaxing guards. |
| [ ] **XC.3** Decide compatibility and reuse policy | XC.0; P7.2b; actual saved v1 records if reuse is proposed | XS | Recorded audit compares manifests, scientific settings, execution/cache/timing protocols, artifacts, sample/repetition keys, source/environment/backend fingerprints, and completeness. Incompatible or unavailable records mean independent reruns, not assumed reuse. |
| [ ] **XC.4** Run development-only budget pilot | XC.2; XC.3 | XS + compute | Fresh measurements span both datasets/models, all three budgets, retrieval families and reranking states; paired evidence and cache/count checks pass, with failure, memory, setup, generation, online and isolation costs preserved. |
| [ ] **XC.5** Resolve runtime budget and freeze extension | XC.4 | XS | Pilot-based full workload estimate, memory/disk/headroom and explicit stop allowances are approved; a new separate context manifest records counts, window/output settings, pairing and reuse decision before held-out execution. |
| [ ] **XC.6** Execute and archive the two-model matrix | XC.5; P7.4; explicit compute authorization | XS orchestration + compute | All 21,600 independent request slots, or explicitly audited compatible reused slots plus new work, are accounted for by provenance; missing requests, failures and retries remain visible and cannot be merged away. |
| [ ] **XC.7** Produce paired budget comparisons | XC.6; P8.1 | S | Same-question evidence/quality/latency/resource contrasts have independent sample counts, clustered uncertainty, truncation/failure rates, and clear confirmatory/exploratory labels. |
| [ ] **XC.8** Budget optional SmolLM context replication | XG.7; XC.5; separately authorized pilot | XS planning + pilot compute | SmolLM passes every budget's native-limit/cache/pairing checks; a new budget/manifest explicitly covers 10,800 added requests. Execution is a separately authorized follow-up, not automatically part of XC.6. |

The 1,024-budget, size-256 cells overlap v1 scientifically: six profiles × two
datasets × two models × 100 questions × three repetitions = 7,200 request slots.
Reuse is permitted only after XC.3's documented compatibility audit. It must retain
original record/run identifiers and measurement lineage, never duplicate samples
or merge incompatible environments. Without validated reuse, plan all 21,600
requests; no saved time or reduced runtime is assumed.

#### XC.0 predeclaration — 2026-10-13, before first held-out generation

The previously declared eighteen-profile, two-model matrix and 100 frozen
evaluation IDs per dataset are retained. The directional research hypothesis is
that larger evidence budgets improve coverage and short-answer quality, but may
increase generation/total latency; improvements are not assumed or guaranteed.
Record contrasts 1,024 minus 512 and 2,048 minus 1,024 as primary paired contrasts;
2,048 minus 512 is a secondary contrast. Report each dataset/model/family/reranking
cell, with an equal-dataset macro summary, without selecting favorable cells.

Primary outcomes are packed evidence coverage and normalized answer token F1;
Exact Match, abstention, final evidence/output truncation, generation and total
latency, memory, native/reference counts and underfill are required secondary
outcomes. Quality uses repetition one, attempt one; timing preserves three
measurements per question. Report all failed slots and retry history separately;
never substitute retries silently into first-attempt quality or paired timing.

Use 2,000 seeded paired bootstrap resamples (seed 20261011) and 95% percentile
intervals on same-question contrasts. Retain repetitions within question, stratify
by dataset, and preserve shared evidence-source dependencies: cluster by SQuAD
article; for HotpotQA use connected components of shared annotated supporting
document IDs. Declare the component count and withhold intervals when there are
fewer than two independent clusters. Report question-cluster sensitivity results
as such. Use matched successful first-attempt slots for conditional timing, with
missing-pair counts and failures alongside it. No significance-based pruning,
post-hoc factor tuning or independence claim from repeated measurements.

Keep all pinned retrieval/context/prompt/cache controls and the 64-token output
cap. A native context overflow is a preserved failure, not permission to trim
one model's evidence or change its window/output cap. Development-only pilot
problems must be resolved and frozen in a separate extension identity before any
extension evaluation. Any held-out-informed change to this protocol is explicitly
exploratory or uses new evaluation data, not a revision of these predictions.

Plan independent execution of all 21,600 slots. Reuse only the overlapping
1,024-budget/size-256 cells after XC.3 verifies scientific settings, sample IDs,
repetition/attempt keys, execution/timing/cache protocols, source/model/tokenizer/
artifact/environment identities and complete raw lineage. Otherwise rerun into
a separate compatible set. XC.5 must still freeze final assets/protocol/budget
after the development pilot; this predeclaration is not an execution manifest,
extension implementation, measured result, or authorization to launch it.

XC gate: protocol predeclaration precedes answer-quality inspection, followed by
development validation, a measured pilot, explicit compute allowance, a separate
manifest, and execution authorization. Failure at 2,048 native-prompt fit is a
decision to resolve before freeze, not permission to alter the original study.

### XD — local read-only Dash + Plotly dashboard

This is an explicitly requested optional UI exception, not a replacement for the
CLI or a benchmark execution service. Build Stage A views first from existing
saved records; show honest empty/pending states for missing Stage B or extension
data. Implementation and local validation are complete (2026-10-15); the optional
dependency lock and isolated viewer environment leave the benchmark environment
unchanged. Packaging evidence is recorded separately in PROGRESS.md.

Dashboard callbacks must never start benchmarks, load models, change manifests,
or mutate measurement records. Use offline exported snapshots and precomputed
Python aggregates/intervals; do not run dashboard aggregation or rendering on the
benchmark machine during timed experiments. Bind locally by default and render
dataset/model text as untrusted plain content, without raw HTML or executable text.

Required views and filters:

- Overview: completion/failure counts, run IDs, hardware, frozen settings, and provenance.
- Retrieval: Stage A coverage heatmaps, chunk-size comparisons, and retrieval latency.
- End-to-end: quality–latency plots, stage breakdowns, reranking, and model comparisons.
- Context budget: paired evidence coverage, answer quality, and latency across budgets.
- Question explorer: retrieved chunks, packed evidence/mappings, reference and generated answers, scores, and failures.
- Filters: dataset, model, retrieval family, chunk size, reranking, context budget, stage, and compatible run set; inapplicable filters are explicitly disabled rather than inferred.

| Task | Dependency | Effort | Observable completion gate |
| --- | --- | --- | --- |
| [x] **XD.1** Define versioned read-only export schema | P4.5b; explicit dashboard implementation authorization | XS | Schema covers run/manifest provenance, compatibility keys, split/purpose, conditions, requests/attempts, question/source IDs, metrics, units, counts, uncertainty, text-artifact references, and absent-field states; example synthetic export is labeled synthetic. |
| [x] **XD.2** Build offline Python aggregation and export | XD.1; P4.5b | S | Stage A aggregates reproduce saved summaries with failure/retry counts and question-cluster intervals; paired comparisons use matched questions and declared source clustering. Export retains lineage and never recomputes benchmark work. |
| [x] **XD.3** Add validating snapshot loader | XD.2 | S | Missing/corrupt/incomplete exports and incompatible run sets are detected; incomplete runs are explicitly labeled, incompatible sets cannot be pooled, and development/held-out/pilot/diagnostic/extension purposes stay separate. |
| [x] **XD.4** Build local Dash shell, overview, and retrieval views | XD.3 | S | Dash/Plotly dependencies are added and locked only now; Stage A heatmaps, chunk-size and latency views show sample counts, 95% interval availability, units and failures; missing Stage B data displays no invented points. |
| [x] **XD.5** Add linked filters and configuration details | XD.4 | S | Selecting a configuration consistently updates overview/details and question examples; all required filters preserve compatible-run boundaries, valid selections, and empty states without model loading or execution callbacks. |
| [x] **XD.6** Add safe question explorer | XD.5 | S | Source chunks, included evidence offsets, references, model answers, scores, truncation and failures trace to raw artifacts; script/HTML-like synthetic inputs render harmlessly, and unvalidated artifact paths are rejected. |
| [x] **XD.7** Populate end-to-end and context views | XD.5; P7.4/P8.1 for main data; XC.7 for budget comparisons; XG.8 for optional SmolLM | S | Available core studies have quality–latency/model/reranking plots and stage breakdowns; unrun model/budget studies retain pending views, not fabricated comparisons. |
| [x] **XD.8** Export tables and publication figures | XD.2; XD.4; P8.2 when applicable | S | CSV and SVG/PDF exports match verified aggregates with units/counts/uncertainty/provenance. Decision 2026-10-14: reuse the existing standard-library vector renderer rather than add Matplotlib; format and scientific contracts unchanged. CSV formulas neutralized. |
| [x] **XD.9** Validate local operation and handoff | XD.4–XD.6; XD.8; XD.7 for populated later views | XS | 21 isolated tests and live Chrome checks pass; Stage A-only/incomplete/incompatible/unsafe text/exports covered. No model/runner/exporter modules load in the viewer. Local startup and timing exclusion documented. |

XD gate: a usable Stage A vertical slice can finish XD.1–XD.6/XD.8–XD.9 before
Stage B data exists. XD.7 waits for actual validated results. The dashboard never
competes with timed work; a clean checkout's normal commands do not depend on
ignored synthetic tests. Add dependencies only during approved implementation
and update the lockfile then. Publication outputs and snapshots remain ignored
and are explicitly archived.

XD evidence: `reports/dashboard-snapshot-v2` has four run sets, 176 cells and
1,520 examples; `artifacts/dashboard-snapshot-verification-v2.json` independently
checks saved aggregates, original intervals, all example offsets and vector bars.
See `reports/dashboard-handoff-v1/README.md` and the dated PROGRESS entry.

### XD.10 — dashboard review fixes and improvements (2026-10-15)

User authorized recording all review findings here and fixing/improving them.
Scope is presentation and read-only validation only: no new benchmark requests,
study changes, held-out tuning, dependency changes, or overwriting old outputs.
Each item is an independently reviewable slice; implementation proceeds in order.

| Task | Status | Completion gate |
| --- | --- | --- |
| [x] XD.10a — local-only charts and stricter validation | done | Cloud actions/destination disabled for all charts; stage metrics, counts/totals, links/text/offsets validated; explicit unavailable states tested. |
| [x] XD.10b — consistent filters, counts and names | done | Dataset-qualified names; scoped counters/run totals; compatible family/recipe and run/contrast choices; preserve/reset selections. Rapid-click race found in browser QA: synchronous configuration-only client normalization replaces server writes. |
| [x] XD.10c — readable question and evidence explorer | done | ID/text search and question retention; readable reference/answer/coverage cards; safe offset-based highlights; expandable original JSON/lineage retained. |
| [x] XD.10d — readable comparisons and metric selection | done | Original paired table/effect plots show counts/source intervals and pp/second units; quality/rate and latency selectors; no recomputed inference or pooling. |
| [x] XD.10e — mobile layout and accessible controls | done | 390px layout without overflow; collapsible filters and associated control labels verified in Chrome; reset/search work. |
| [x] XD.10f — scoped downloads and complete figure captions | done | In-memory filtered CSV plus full export with uncertainty/count metadata; fresh snapshot v3 preserves all run data, 12 core vectors and Stage A bar geometry; captions disclose n. |
| [x] XD.10g — regressions, live review and handoff | done | 35 isolated tests; core 251 discovered/230 passed/21 optional viewer skips; final Chrome/rapid-click/mobile checks; independent 808-row check; separate 126-payload archive and fresh offline installation/replay verified. See current PROGRESS.md and external proofs. |

Review findings: cloud-share action enabled by default; malformed/null metrics can
pass validation then crash rendering; filtered cell counts mixed with run totals;
duplicate dataset-ambiguous labels; incompatible family/recipe and contrast choices;
per-question retrieval scores hidden; Stage A publication captions omit explicit n.
Improvements: readable cards/tables with raw JSON retained, paired evidence context,
metric selector, reset/search, collapsible mobile filters, accessible labels and
filtered CSV. These items do not authorize additional experiment factors.

### XD.11 — question-text-only dropdown (2026-10-15)

- [x] done: saved-question dropdown labels show only question text. Internal IDs,
  ID search and expandable raw lineage remain unchanged. All 35 focused tests pass;
  the assertion checks exact question-text labels. Viewer-only change; old packages
  and measurement exports remain preserved.

### XD.12 — guided dashboard and two-configuration comparison

Authorized 2026-10-15: presentation only; saved snapshots and original intervals
remain immutable. No benchmark requests, new inference, dependencies or publishing.

- [x] XD.12a — done: default overview tab with research question, run-scoped
  study counts, three saved-data observations and visible limitations.
- [x] XD.12b — done: accessible metric explanations and nearby uncertainty/count
  guidance; distinguish repeated timings from question units and source clusters.
- [x] XD.12c — done: same-run/same-dataset side-by-side configurations, shared
  saved question, answers/evidence and original paired intervals when available.
- [x] XD.12d — done: 42 focused tests; core 258 discovered/230 passed/28 optional
  viewer skips; four real run overviews and all 248 stored pair directions passed.
  Desktop/390px browser checks verified exact saved answers, highlights, local-only
  plots and no overflow/JavaScript exceptions. Synthetic regressions, real-snapshot smoke and local UI
  verification; update local guidance and tracked validation invariants.

### XD.13 — sidebar text removal (2026-10-15)

- [x] done: removed only the RESULTS LAB label and its introductory sentence at
  the user's request. Other dashboard features/styles remain unchanged; 42 focused
  tests passed and whitespace checks passed. Documentation/tests remain local.

### D.1 — concise documentation refresh (2026-10-15)

Navigation/content order: done. Tab bar precedes shared summary and separate view
panels for all six tabs. 45 focused tests and desktop/mobile motion/layout checks
passed; summaries never push the tab bar down. Mobile grid/link overflow corrected.

Reference tab motion: done. Independently implemented a sliding selection
pill and jelly settle inspired by the supplied CodePen xxgYGrR; preserve native
Dash selection, local-only assets, scrolling/resizing alignment and reduced motion.
Real clicks, rapid changes, mobile overflow, idle observer stability and reduced
motion passed local Chrome checks. All 44 focused tests and syntax/whitespace pass.

Dashboard copy reduction: done. Shorter visible copy; detailed metric, uncertainty
and validity explanations preserved in expandable notes. Counts, units, original
intervals and interactions unchanged. 44 focused tests, Ruff and whitespace pass.

Sidebar scroll fix: done. Desktop sidebar is viewport-height and sticky, with
independent scrolling to the last filter; mobile retains normal flow. Scoped
footer CSS to prevent padding Dash's empty framework footer. Browser checks
passed at 1440×900, 1440×600 and 390px; all 43 focused tests passed.

Sidebar follow-up: done, user requested filters directly visible rather than a
"Filters & display" menu. Replaced Details/Summary with a normal container and
removed viewport-driven collapsing. 43 focused tests passed; no scientific changes.

- [x] done: README rewritten as a 350-word practical guide; deep dive and research
  report refreshed; PRD/PLAN/PROGRESS/AGENTS current status synchronized. Existing
  contributor/scientific rules and chronological evidence preserved. Local links/
  anchors, shell syntax, real CLI flags, artifact paths and four measured result
  ranges verified; reference metadata checked on primary sites. No benchmark run,
  dependency changes, staging, commit, push or archive rewriting.

### Other optional factors

Candidate depth 20 versus 50, overlap 0% versus 20%, a third end-to-end chunk size,
concurrent load, caching optimization, and a larger corpus remain optional and
unstarted. Add one controlled factor at a time with its own manifest and budget;
do not expand the required matrix accidentally.


## Final delivery checklist

- [x] Required core phase gates have evidence in PROGRESS.md.
- [x] Active matrix counts, sample sizes and completion totals agree.
- [x] Reports disclose historical failures, exclusions, corpus adaptation and inference limits.
- [x] Implemented source/configs remain local for review; ignored docs/tests are unstaged.
- [x] Raw records, provenance and offline-analysis reconstruction assets are archived locally.
- [x] Fresh-workspace analysis replay and fresh offline viewer installation/replay passed.

These checks do not claim a fresh benchmark dependency/model installation, a full
model rerun, cross-platform replication, off-device backup or public sharing clearance.
Current docs and the final question-label edit are newer than immutable release ZIPs.

## D.4 — local architecture guide (2026-10-18)

- [x] done: added ignored ARCHITECTURE.md with component/request diagrams, source
  module map, data contracts, study/run boundaries, timing/cache/resume controls,
  offline analysis and viewer flow, and completed-v3 versus ongoing-v4 status.
  Local links, diagram fences, whitespace, ignore rule and unstaged state checked.
  No source/settings changes, model requests, experiment launches or interruptions.
