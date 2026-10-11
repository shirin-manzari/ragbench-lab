# ragbench-lab — progress

Last updated: 2026-10-11 (Asia/Tehran).

## Current state

Status: Phase 0 complete and locally verified.

Active phase: none. Next phase: Phase 1 — data and evidence.

Next task: **P1.1 — define document, question, evidence-span, and split records.**

This record covers work verified in this conversation. No external repository has been inspected. If implementation already exists elsewhere, inspect it and reconcile this record before marking tasks complete.

## Completed planning

| Item | Status | Evidence |
| --- | --- | --- |
| Project goals and scope | done | PRD.md |
| Two-stage experimental design | done | PRD.md and PLAN.md |
| Contributor, Git, and writing rules | done | AGENTS.md |
| Task breakdown and phase gates | done | PLAN.md |
| Local ignore template | done | .gitignore in the planning bundle; exclusion patterns checked during document preparation |
| Runtime feasibility | pending | Requires measured pilot on target hardware |

## Phase status

| Phase | Status | Evidence / next gate |
| --- | --- | --- |
| 0 — scaffold | done | Editable install, configuration checks, local tests, and hardware inventory verified |
| 1 — data | pending | No prepared corpus or evidence mapping verified |
| 2 — chunking and BM25 | pending | No retrieval output verified |
| 3 — Dense and Hybrid | pending | No model/index integration verified |
| 4 — Stage A | pending | No screening or selection results |
| 5 — generation and reranking | pending | No local LLM integration verified |
| 6 — pilot and freeze | pending | No measured runtime estimate |
| 7 — Stage B | pending | No benchmark runs |
| 8 — analysis | pending | No measured findings or report |

## Decisions

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-10-11 | Working repo name: ragbench-lab | Describes the evaluation scope; alternatives have not been selected |
| 2026-10-11 | Broad retrieval screening before end-to-end runs | Expands retrieval coverage while controlling generation cost |
| 2026-10-11 | Stage A: 30 configurations per dataset | Five recipes, two chunkers, three sizes |
| 2026-10-11 | Stage B: 12 configurations per dataset/model | Three families, two sizes, reranking off/on |
| 2026-10-11 | Two datasets and two small local generators | Check whether results depend on dataset and generator |
| 2026-10-11 | README, project deep dive, and tests stay out of Git | User's repository policy; local validation remains required |
| 2026-10-11 | PLAN.md owns task checkboxes | Avoid conflicting completion states across documents |

The experiment design is proposed; the measured pilot and development selection are not complete. Exact model revisions, quantization, hardware, corpus pool, and frozen manifests remain unset.

## Open items

| Item | Resolve by | Impact |
| --- | --- | --- |
| Target machine and available memory/accelerator | Phase 0 | Model size and runtime feasibility |
| Exact model artifacts, access, and package versions | Phases 0–5 | Reproducibility and setup |
| Dataset revisions, corpus pool, and split IDs | Phase 1 | Valid evidence evaluation |
| Embedder and chunker selection | Phase 4 | Stage B fixed settings |
| Backend cache behavior and timing boundaries | Phase 6 | Valid latency comparisons |
| Final sample size and compute budget | Phase 6 | Runtime and statistical uncertainty |
| External archive destination for ignored artifacts | Before Phase 7 | Preservation of measurements |

These items do not block writing the scaffold. Resolve them at their phase gates.

## Verification record

Phase 0 application checks were run on 2026-10-11. No model runs or performance measurements have been executed.

| Date | Task | Command / inspection | Result | Artifact |
| --- | --- | --- | --- | --- |
| 2026-10-11 | P0.1 | `python -m pip install -e .` | passed; editable package and CLI installed | `pyproject.toml`, `src/ragbench_lab/` |
| 2026-10-11 | P0.2 | `python -m ragbench_lab validate configs/pilot.toml` | passed; config hash recorded and 30 Stage A conditions confirmed | `configs/pilot.toml` |
| 2026-10-11 | P0.2 | `python -m unittest discover -s tests -v` | passed; 2 tests including invalid candidate-depth rejection | ignored `tests/test_phase0.py` |
| 2026-10-11 | P0.3 | `python -m ragbench_lab hardware --workspace .` plus Windows and `nvidia-smi` inspection | passed; CPU, RAM, GPU, disk, Python, and backend availability recorded | `manifests/hardware.json` |
| 2026-10-11 | P0.1 | `git check-ignore -v README.md PROJECT_DEEP_DIVE.md tests/test_phase0.py` | passed; local docs and tests ignored | `.gitignore` |

For subsequent work, append an entry containing date, task ID, command or inspection, result, and relevant artifact path. Use exact commands only after they exist and have been run.

## Experiment ledger

No experiments run yet. The expected main Stage B workload is 14,400 requests at the proposed sample size; this is an estimate of work, not completed progress.

| Run ID | Stage | Config/manifest | Planned / completed / failed | Artifact location |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

## Session handoff template

Copy this structure for each meaningful implementation session:

- Date:
- Task IDs and resulting status:
- Changed behavior and files:
- Verification performed and result:
- Decisions or deviations:
- Blockers:
- Next smallest task:

Keep entries short and factual. Only mark tasks done when their completion checks pass. Preserve failed experiment records and describe retries explicitly.

## Session handoff

- Date: 2026-10-11
- Task IDs and resulting status: P0.1, P0.2, and P0.3 done; Phase 0 gate passed.
- Changed behavior and files: added installable package and CLI, strict TOML configuration records, pilot config, hardware probe and inventory; corrected ignore rules so required planning files can be tracked.
- Verification performed and result: editable install, valid config CLI, hardware CLI, compile check, and 2 focused tests passed. Invalid candidate depth raises a clear configuration error.
- Decisions or deviations: TOML and standard-library validation avoid premature runtime dependencies. Dataset/tokenizer revisions remain explicit placeholders until their download phases.
- Blockers: Ollama is not installed or reachable. This does not block Phase 0; model feasibility remains a Phase 6 measurement.
- Next smallest task: P1.1, define typed data and evidence records.
