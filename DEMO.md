# Five-minute v4 demo

Open `presentations/stage-b-v4.html` in a browser. It is self-contained and needs no
server, models, downloads or dashboard dependencies. Use the section links or left/right
arrows; expand speaker notes during rehearsal. Browser Print → Save as PDF creates a
handout. Keep the original SVG figures for publication-quality exports.

## Before presenting

Run these from the repository; all checks are offline and use no inference:

```sh
python3 scripts/verify_public_results.py results/stage-b-v4
python3 scripts/build_results_demo.py --check
python3 scripts/verify_checkout.py
```

The public bundle and presentation work in a checkout without raw records. Rebuilding
the bundle itself requires the local verified analysis/proof/figures. To create a fresh
copy rather than overwrite the reviewed directory:

```sh
python3 scripts/export_public_results.py --study v4 --output /tmp/ragbench-public-v4-demo
python3 scripts/build_results_demo.py --output /tmp/ragbench-v4-demo.html
```

Choose unused paths; builders refuse existing outputs. The exporter with no study flag
retains historical v3 behavior, so always specify `--study v4` here.

## The talk

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:30 | Overview | We measured how retrieval, chunk size and reranking affect answer overlap and online latency. There are 100 distinct question IDs, not 8,400 independent samples. |
| 0:30–1:15 | Design | Stage A selected E5/sentence-aware chunking on development data. Stage B freezes that selection and compares twelve pipelines on two datasets and two 3B generators. |
| 1:15–2:15 | Results | Read within one dataset/model. The twelve point estimates span a quality/latency trade-off; cell error bars are source-cluster intervals. |
| 2:15–3:00 | Trade-offs | Reranking increases latency in all 24 matched comparisons. F1 rises in 14 and falls in 10; these are descriptive signs, not significance counts. |
| 3:00–3:30 | Baselines | No-RAG retains grounding instructions. Gold evidence is a diagnostic reference and may truncate; it does not guarantee a correct answer. |
| 3:30–4:00 | Limits | V4 is a post-results nested expansion. Timing repetitions, EM/F1 and annotated coverage each have specific limits. |
| 4:00–5:00 | Demo | Verify the public bundle, trace a condition ID between CSVs, or show one saved dashboard example. |

The deck calculates all numerical ranges and reranking sign counts directly from the
public CSVs. Do not claim a universal winning pipeline or concurrent serving capacity.
The public export excludes question IDs, question/answer text and source passages.

## Optional dashboard walkthrough

Use the existing local snapshot and isolated viewer environment:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

Open http://127.0.0.1:8050. If that port already serves the verified v4 snapshot, reuse
it; if another process occupies it, use `--port 8051` and the matching URL. The optional
viewer needs Dash/Plotly and the saved snapshot, which are not included in the public
aggregate bundle. This walkthrough reads recorded results; it does not generate answers.

1. Select Stage B main/evaluation and one dataset/model. Identify chunk size, retrieval
   family and reranking state before comparing points.
2. Open paired comparisons and inspect a reranking-on minus off contrast. Read both
   the point difference and original paired source interval; do not infer significance
   from overlapping cell intervals.
3. Open the saved question/configuration view. Compare paired generator answers and
   the evidence actually packed into context. Explain that full annotations can coexist
   with an exact-match failure, including correct answers with extra wording.
4. Use Downloads/provenance to show the checked export and study identity.

If the dashboard is unavailable, stay in the offline deck and public CSVs. No new
inference is needed. Stop the viewer before any future timed experiment.

## Failure-analysis follow-up, if asked

The local `reports/stage-b-failure-diagnostics-v4-50/REPORT.md` diagnoses 2,400
repetition-one main responses. Of 1,996 non-exact matches, 396 have incomplete top-50
annotations, 285 lose complete candidate annotations during packing, and 1,315 have
full packed annotations. The last group is not a factual-error count. Six paired case
notes are in `reports/stage-b-failure-review-v4-50/REVIEW.md`; they are agent-authored,
not independently adjudicated. These local text-bearing reports are separate from the
public aggregate bundle and immutable earlier ZIPs.

## Shareable copy

`artifacts/archives/ragbench-public-v4.zip` contains only the v4 aggregate bundle,
standalone HTML/PDF presentation, standard-library checker/builder, an unsigned
file inventory and START_HERE.txt. It is 364,566 bytes; SHA-256:
`e7fa2b932c28cbcbda2cf99b57cf4e4647bf2bc4545c4af57204145a597ca91e`.
It excludes this local walkthrough, internal planning files and all saved question text.
The ZIP was independently extracted and checked without raw data or installed packages.
It has been prepared locally; it has not been uploaded or pushed.
