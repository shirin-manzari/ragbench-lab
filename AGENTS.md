# ragbench-lab — agent instructions

## Mission

Build the project described in PRD.md: a local, reproducible RAG benchmark focused on retrieval, chunking, reranking, latency, and answer quality. Preserve the two-stage experiment and its scientific controls.

Read PRD.md, PLAN.md, PROGRESS.md, and the existing implementation before editing. Treat planned features as planned until verified. When requirements conflict or a change alters the experiment, explain the conflict and record the decision rather than silently changing the study.

## Working rules

- Work in small, independently reviewable tasks. Split work larger than half a day before implementation.
- Implement the current requested phase. A roadmap is not an instruction to launch the whole experiment immediately.
- Finish a usable vertical slice early, then extend it.
- Prefer plain Python functions, typed records, and small modules. Avoid speculative frameworks, plugin systems, services, or a UI.
- Keep configuration separate from algorithms. Validate settings and reject unsupported combinations.
- Add dependencies only when required, and update the lockfile.
- Preserve unrelated changes. Never fabricate measurements, citations, or completed checks.
- Report what changed, what was checked, and any remaining limitation in a short handoff.

## Git rules — required

Commit messages must be natural, short, and entirely lowercase. Aim for 3–8 words and no more than 50 characters. Use one clear change per commit. Do not use conventional-commit prefixes, emojis, uppercase acronyms, or generic messages such as `update stuff`.

Good examples: `add bm25 retrieval`, `preserve evidence offsets`, `fix context budget counting`, `record generation latency`.

Keep README and project deep dive files local and ignored by Git. Use the canonical names `README.md` and `PROJECT_DEEP_DIVE.md`. If a different spelling or format is introduced, add its exact path to .gitignore before writing it.

Keep tests local and ignored by Git, including fixtures and test reports. This rule controls versioning; it does not remove the obligation to validate important behavior. Never force-add ignored documentation or tests.

Keep source, configs, dependency files, PRD.md, AGENTS.md, PLAN.md, PROGRESS.md, and the .gitignore tracked. Use explicit paths when staging; inspect the staged diff and file list before committing. Do not auto-commit unless requested or the active workflow authorizes it.

If a prohibited file is already tracked, .gitignore alone is insufficient. Remove only that file from the index using `git rm --cached` while preserving its local contents. Do not rewrite history or delete unrelated files.

## Local documentation style

Write README and project deep dive in a natural, human tone. Explain what the tool does, why a choice exists, and how to run it. Use direct sentences and concrete examples. Keep paragraphs to 2–4 short sentences. Avoid long walls of text, marketing language, filler, and repetitive summaries.

README covers setup and the shortest working workflow. PROJECT_DEEP_DIVE explains architecture, the experimental design, decisions, and limitations. Update them locally when behavior changes. Do not claim unimplemented commands work.

## Validation policy

Create focused local tests for consequential behavior: evidence offsets, split isolation, chunk boundaries, RRF deduplication, context budgets, scoring, factorial enumeration, and resume integrity. Keep all tests in ignored `tests/` or `test/` directories, or ignored test filenames. Use tiny synthetic local fixtures where possible.

Run the checks relevant to each change. Prefer a small smoke run before a model-backed check. Do not repeatedly download models or run the complete benchmark for routine edits. Report exact checks and failures honestly.

Because tests are intentionally untracked, document critical validation commands and invariants in tracked technical specifications or configuration metadata. Never make a clean checkout's normal run depend on ignored test fixtures.

## Scientific rules

- Keep development decisions separate from held-out evaluation.
- Pin model revisions, dataset revisions, tokenizer, dependencies, seeds, and hardware settings.
- Stage A is 5 retrieval recipes × 2 chunking methods × 3 sizes = 30 per dataset.
- Stage B is 3 retrieval families × 2 sizes × 2 reranking states = 12 per dataset/model.
- Freeze the selected embedder and chunker using the declared development rule in PRD.md.
- Use a shared context-budget tokenizer and identical evidence text for paired LLM comparisons.
- Preserve source offsets and score the evidence actually included after context truncation.
- Detect embedding/reranker input truncation and generator context overflow.
- Keep corpus evidence labels out of searchable text and generation inputs except in the explicit gold-evidence baseline.
- Time the real online path; cached query results must not bypass measured work.
- Treat repeated timing runs as repeated measurements of the same question.
- Record failures and retries. Never discard bad runs silently.
- Export raw results and provenance before claiming conclusions.
- Any change to the frozen study creates a new manifest and clearly separate run set.

## Repository layout

| Path | Responsibility | Git |
| --- | --- | --- |
| `src/ragbench_lab/` | Pipeline and CLI implementation | Tracked |
| `configs/` | Pilot, screening, final experiment settings | Tracked |
| `manifests/` | Compact frozen experiment definitions and hashes | Tracked; review for private paths |
| `pyproject.toml`, lockfile | Package and environment | Tracked |
| `PRD.md`, `AGENTS.md`, `PLAN.md`, `PROGRESS.md` | Requirements, rules, tasks, and work evidence | Tracked |
| `README.md`, `PROJECT_DEEP_DIVE.md` | Human-readable local guidance | Ignored |
| `tests/`, `test/` | Local validation and fixtures | Ignored |
| `data/`, `models/`, `indexes/` | Downloaded and derived assets | Ignored |
| `runs/`, `reports/`, `artifacts/` | Measurements and generated outputs | Ignored; explicitly archive |

## Phase overview

PLAN.md owns the detailed task checklist and phase gates. Keep it synchronized with the implementation; record evidence and current status in PROGRESS.md.

| Phase | Goal | Typical task size |
| --- | --- | --- |
| 0 | Package, configuration, hardware inventory | XS |
| 1 | Dataset adapters and evidence mappings | S |
| 2 | Chunking and BM25 vertical slice | S |
| 3 | Dense and Hybrid retrieval | XS–S |
| 4 | Stage A runner, selection, and retrieval evaluation | XS–S |
| 5 | Local generators, reranking, answer scoring | XS–S |
| 6 | Pilot and study freeze | XS–S |
| 7 | Stage B experiments and archive | S plus compute |
| 8 | Analysis, failure review, and delivery | S |

XS means 1–2 hours; S means roughly half a day. Split larger work into these sizes before coding. Estimates exclude unattended compute.

## Progress maintenance

At the start of a task, read PRD.md, PLAN.md, and PROGRESS.md. Check existing code before assuming the progress log is current. Update the active task and status only for work actually started.

At the end of meaningful work, update PLAN.md checkboxes and PROGRESS.md with changed files, actual verification commands/results, blockers, and the next task ID. Use `pending`, `in_progress`, `blocked`, or `done` consistently. A done task needs observable evidence. Planning documents alone do not complete scaffold or experiment tasks.

Keep a short dated decision log for changes to scope, datasets, models, and measurement settings. Do not overwrite earlier benchmark records. Record run IDs and artifact locations when experiments exist; never invent them.

## Optional extensions — after the core study

Candidate depth 20 versus 50; overlap 0% versus 20%; a third chunk size in end-to-end runs; concurrent load; caching; a larger corpus; an additional generator. Add one controlled factor at a time with a separate manifest and budget. Do not expand the required matrix accidentally.

## Handoff checklist

- State the completed phase/tasks and the next smallest task.
- List changed behavior and relevant local verification.
- Confirm ignored docs/tests are absent from the staged diff.
- Identify measured results separately from estimates and planned work.
- Record blockers and unresolved experimental decisions without hiding them.
