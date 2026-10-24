# RAGBench Lab — presentation cheat sheet

Use this for an 8–10 minute presentation. Read the quoted sentences aloud; use the
other notes as prompts. Present one completed benchmark, moving from the research
question to the design, results and evidence.

## Before you start

- Open the dashboard at http://127.0.0.1:8050.
- Keep `report.md` and the README dashboard screenshot open as backups.
- Rehearse one configuration comparison and one saved-answer example.
- The demo reads saved measurements. No model requests are needed.

If the dashboard needs starting, run from the project directory:

```sh
PYTHONPATH=src artifacts/dashboard-env/bin/python -m ragbench_lab dashboard \
  --snapshot reports/dashboard-snapshot-v4-50 --port 8050
```

This needs the existing local snapshot and viewer environment. If the dashboard is
already open, reuse it. For a dependency-free fallback, use the README screenshot and public CSVs.

## Dashboard guide — keep beside the demo

### Choose the right saved run

The sidebar's **Study stage** and **Run** select the recorded experiment. The current
internal labels mean:

| Run label | What to call it while presenting |
| --- | --- |
| `Stage A / development / …` | Retrieval screening on development questions |
| `Stage A / evaluation / …` | Held-out retrieval evaluation |
| `Stage B main / evaluation` | The complete answering experiment |
| `Separate baselines / evaluation` | Empty-evidence and gold-evidence controls |

A suffix such as `8aee356a` identifies a saved run. You do not need to read it aloud.
Choose the main answering run for the primary demo. Retrieval-only views do not have
generated-answer scores; their held-out pool also has a different question count.

### Use the sidebar filters

| Control | Meaning / demo advice |
| --- | --- |
| Dataset | Choose `squad` or `hotpot_qa`; explain them as SQuAD and HotpotQA. |
| Generator | Choose Llama or Qwen for answering results. |
| Retrieval family | BM25, Dense or Hybrid. |
| Recipe / baseline | Specific encoder recipe or diagnostic baseline. |
| Chunking | Sentence-aware or fixed-token; the answering experiment fixes sentence-aware. |
| Chunk size | Size of each source chunk, measured in reference tokens. |
| Reranking | On/off; keep **All applicable** when comparing these two settings. |
| Context budget | Total packed evidence allowance, fixed at 1,024 reference tokens here. |
| Metric | The vertical-axis score or the quality metric used in paired comparisons. |
| Latency | Mean, median or p95 online request time. |
| Reset filters | Reset the configuration filters within the selected run. Fixed settings remain fixed. |

Filters only retain compatible settings. A disabled control usually means that the
selected run has one measured value for that setting, rather than a broken control.
**All applicable** means all compatible recorded settings, not unmeasured experiments.

### Know what each tab does

| Tab | Show / explain |
| --- | --- |
| **Overview** | Summary and descriptive findings for the **whole selected run**. Sidebar configuration filters do not narrow these findings. |
| **Results** | Filtered quality/latency charts and request counters. Expand metric or interval notes only if needed. |
| **Compare** | Select two distinct configurations and a shared saved question. The run selector applies, but sidebar configuration filters do not; the view's own selectors keep both conditions in the same dataset. |
| **Questions** | Choose a filtered configuration, search question text or ID, then inspect the saved answer, reference, coverage and exact packed evidence. No new answer is generated. |
| **Paired** | Compare matched conditions on the same questions, using original stored differences and paired intervals. |
| **Downloads** | Export all/filtered result tables or inspect original figures and provenance. Filtered CSV follows the sidebar; archived figures do not. |

### Read the graphs

- **Heatmap — retrieval evaluation:** rows are retrieval/chunking combinations;
  columns are chunk sizes. Darker blue means higher packed evidence coverage.
  Hover for exact values. Color differences alone do not establish significance.
- **Scatter plot — answering evaluation:** each point is a configuration for the
  selected dataset/generator. Horizontal position is latency; vertical position is
  the selected metric. For F1 or coverage, higher scores and lower latency can be
  desirable, but abstention/truncation rates need different interpretation.
- **Point symbols:** blue = BM25, orange = Dense, teal = Hybrid; circles = Llama,
  diamonds = Qwen; open symbols = reranking off; larger symbols = chunk size 256.
- **Stacked bars:** colored sections show mean time spent in each online operation.
  These bars remain **mean seconds**, even if the separate Latency selector is set
  to median or p95. Setup, warmup and scoring are outside online latency.
- **Paired effect plot:** each dot is left minus right; its horizontal interval shows
  uncertainty. Positive F1 means higher overlap; positive latency means slower.
  An interval crossing zero includes no difference among its plausible values;
  it does not establish that the configurations are equivalent.

### Find evidence coverage

In **Metric**, choose **Packed annotated coverage**. This is the evidence-coverage
metric: how much annotated evidence survived packing into the model's context.
It is different from coverage among the top retrieved candidates and is not a
measure of factual correctness. **Questions → Annotated coverage** provides the
saved per-question evidence diagnostics.

### Explain counts and technical details

**Questions** counts unique IDs per configuration. Repetitions and requests across
configurations do not add independent questions. For the answering experiment,
SQuAD has 50 questions across 14 article clusters; HotpotQA has 50 questions across
50 supporting-source groups. **Statistics details** exposes these group counts.

**Not used — question-level intervals** means the retrieval-only results resample
questions rather than source groups. Their interval notes disclose that shared-source
dependence is not adjusted. This is separate from **unadjusted for multiple
comparisons**, which concerns examining many statistical contrasts.

The request cards in **Results** follow filters; **Run details** retains the entire-run
counts. With the main answering run, SQuAD and Llama selected and all twelve pipelines
visible, expect **12 configurations, 1,800 successful requests and 0 failed attempts**.
Zero request failures does not mean all answers were correct.

### A reliable two-minute dashboard route

1. **Overview:** select the main answering run; introduce the completed experiment.
2. **Results:** select SQuAD, Llama, Token F1 and Mean online latency. Leave pipeline
   factors at All applicable. Explain the scatter plot and timing bars.
3. **Paired:** choose Dense, chunk size 128 and reranking-on minus off. Keep the
   Reranking filter at All applicable so both conditions remain included. Use the
   verified comparison in presentation step 7 below.
4. **Compare** or **Questions:** show the ctenophore example from step 8 to explain
   why a non-exact answer is not automatically factually wrong.
5. **Downloads:** point to the checked CSVs if asked about traceability.

If **Paired** says no estimates are available, check that filters include **both**
conditions. For example, a Qwen-minus-Llama contrast needs both generators visible;
choosing only Llama excludes the other side. Only originally saved contrasts are shown.

Wide tables scroll horizontally inside their own region. Source counts, raw IDs and
provenance remain in expandable technical sections; they are available for inspection
without needing to be narrated during the demo.

**Download caveat:** six archived answering SVGs still contain earlier sample-count
captions. Downloads flags them under **Archived figure caption notes**. Use the saved
tables/current interactive charts for the final 50-question counts; do not quote the
old 25-question/75-timing captions as the final experiment's sample size.

## 1. Introduce the project — 30 seconds

**Say:**

> “RAGBench Lab is a local benchmark for evaluating retrieval-augmented generation.
> I measure how retrieval, chunk size and reranking affect the evidence supplied to
> a language model, the quality of its answer and the time it takes.”

**Show:** The README or dashboard **Overview**.

**Remember:** The contribution is a controlled experiment and traceable results.
The dashboard is a viewer for the experiment.

## 2. Explain the research question — 30 seconds

**Say:**

> “Adding retrieval or reranking has a cost. My question is whether a particular
> pipeline improves answer quality enough to justify its extra latency.”

**Remember:** Avoid promising that one configuration is best for every task.

## 3. Explain one request — 45 seconds

Point through this sequence:

```text
Question → retrieve candidates → optional reranking → pack evidence → generate → score
```

**Say:**

> “The system searches source-text chunks, optionally reorders the candidates, and
> packs them into a fixed evidence budget. A local model then answers using that
> context. I save the answer, evidence mappings, scores and timings.”

**Remember:** Search retrieves up to 50 final candidates. Evidence is packed into
1,024 reference tokens; output is capped at 64 native model tokens. Chunk size and
context budget are different settings.

## 4. Explain the experiment — 60 seconds

**Say:**

> “I compare BM25, Dense and Hybrid retrieval, two chunk sizes, and reranking off
> or on. That gives twelve pipelines. I test them on SQuAD and an adapted HotpotQA
> corpus using Qwen and Llama 3B models.”

| Factor | Settings |
| --- | --- |
| Retrieval | BM25 / Dense / Hybrid |
| Chunk size | 128 / 256 reference tokens |
| Reranking | Off / on |
| Generators | Qwen2.5-3B-Instruct / Llama-3.2-3B-Instruct, Q4_K_M |
| Fixed components | E5 embeddings, sentence-aware chunks, zero overlap |

**Add:**

> “The embedder and chunker were selected using development-only evidence coverage
> and then frozen. Matched generators receive identical evidence text.”

**Remember:** BM25 uses lexical matching; Dense uses embeddings; Hybrid combines
rankings with reciprocal rank fusion. Reranking rescores question/passage pairs.

## 5. Explain the counts and metrics — 60 seconds

**Say:**

> “There are fifty evaluation questions per dataset: one hundred distinct question
> IDs. The twelve pipelines, two generators and three timing repetitions produce
> 7,200 main requests. Another 1,200 requests evaluate diagnostic baselines.”

```text
12 pipelines × 2 datasets × 2 generators × 50 questions × 3 repetitions = 7,200
2 baselines × 2 datasets × 2 generators × 50 questions × 3 repetitions = 1,200
```

| Metric | Plain explanation |
| --- | --- |
| Exact Match | Does the normalized answer match a reference exactly? |
| Token F1 | How much do the answer and reference overlap in tokens? |
| Packed evidence coverage | How much annotated evidence actually reached the model? |
| Online latency | Time through retrieval, optional reranking, packing and generation |

**Remember:** Quality uses the first repetition. Three timings do not triple the
question sample. Zero request/setup failures means the requests completed; it does
not mean every answer was correct. Setup, warmup, cache isolation and scoring are
outside online latency.

## 6. Present the main finding — 60 seconds

**Say:**

> “Reranking increased mean latency in all twenty-four matched comparisons.
> Token F1 improved in fourteen comparisons and decreased in ten. Its value depends
> on the dataset, generator and pipeline.”

**Numbers to quote:** Added latency **0.13–1.23 seconds**; F1 change **−3.13 to +13.11
percentage points**. These are ranges of point estimates, not confidence intervals.
The fourteen/ten split does not count statistically significant wins.

**Show:** **Results**. Select the completed main-answering run, SQuAD and Llama.
Use **Token F1** and **Mean online latency**. Keep all retrieval families visible
initially so the audience can see the trade-off.

## 7. Demonstrate one matched comparison — 60 seconds

**Do:**

1. In **Results**, select SQuAD, Llama, Dense retrieval and chunk size 128.
2. Leave **Reranking** at **All applicable** to keep both conditions visible.
3. Open **Paired** and select the reranking-on minus reranking-off contrast.
4. Point to the difference and its stored paired interval.

| SQuAD / Llama / Dense / 128 | Token F1 | Mean online latency |
| --- | ---: | ---: |
| Reranking off | 50.84% | 5.100 s |
| Reranking on | 57.54% | 5.227 s |
| On minus off | +6.70 percentage points | +0.128 s |

**Say:**

> “Here, reranking raises F1 by about 6.70 percentage points and adds about
> 0.128 seconds. This illustrates one measured trade-off. The paired interval
> helps show its uncertainty.”

**Remember:** Use the displayed interval before discussing statistical uncertainty.
Do not infer significance from overlapping individual-condition error bars. This
example illustrates the method; it does not establish a universal winner.

## 8. Show why inspecting evidence matters — 60 seconds

**Do:** Open **Compare**. Its selectors compare conditions within the same run and
dataset; sidebar filters do not control this view. Choose SQuAD, with BM25, size 256,
reranking off for both generators: one Llama condition and one Qwen condition.

Choose the question “Where do ctenophores be found in large numbers?” If needed,
use **Questions**, select the corresponding configuration and search for `ctenophores`.
Its ID is `5725c69738643c19005accbc`.

**Show this saved Llama response:**

```text
Reference: In bays / bays
Answer:    In bays where they occur in very high numbers.
```

**Say:**

> “The response contains the reference fact but is longer than the reference,
> so Exact Match is zero. This is why an exact-match failure alone is not proof
> of a factual error.”

**Optional failure-analysis follow-up:** Among 1,996 non-exact responses, 396 had
incomplete top-50 annotations, 285 lost complete candidate evidence during packing,
and 1,315 had complete packed annotations. The last group mixes answer problems and
scoring limitations; it is not a count of factually wrong answers. These are response
counts across configurations, not independent question counts.

## 9. Explain controls, limitations and conclude — 60 seconds

**Say:**

> “The experiment pins model and dataset identities, preserves source offsets and
> measures fresh online retrieval. Results remain traceable to saved records.”

> “The limits are the sample size and shared sources, adapted corpora, text-match
> metrics and sequential timing on one machine. The sample was expanded after
> earlier results were inspected, using fresh measurements without pooling earlier
> records, so it is not an untouched confirmatory holdout.”

> “The main finding is that additional retrieval processing has a measurable cost,
> while its answer-quality benefit depends on the configuration. Evidence coverage,
> answer scores and latency need to be assessed together.”

## Questions you may be asked

| Question | Short answer |
| --- | --- |
| BM25 or TF-IDF? | BM25 is the lexical retriever. Dense embeddings and Hybrid retrieval are also evaluated. |
| Why twelve pipelines? | Three retrieval families × two chunk sizes × two reranking settings. |
| Why E5 and sentence-aware chunking? | The declared development-only evidence-coverage selection rule chose them before held-out retrieval evaluation. |
| Are there 8,400 questions? | No. There are 100 distinct evaluation question IDs, measured across conditions and timing repetitions. |
| Did you separate the original fifty IDs from the added fifty? | No. Final results use all fifty questions per dataset, grouped by dataset/model/pipeline. Every reported measurement was freshly collected. |
| What are the baselines? | Empty evidence and gold-evidence context, separately measured. Empty evidence retains grounding instructions; gold context can truncate and is not a guaranteed upper bound. |
| Which generator won? | Llama has higher SQuAD F1 point estimates in all twelve matched profiles. Hotpot model comparisons vary; there is no universal winner. |
| Are the differences significant? | Consult the original paired source-cluster intervals. Sign counts alone do not establish significance; intervals are unadjusted for multiple comparisons. |
| What does the dashboard do live? | It filters and displays saved results, answers and evidence. It does not run new inference. |
| Can someone reproduce it? | Public aggregates have a standalone checker. A full rerun also needs pinned assets, the environment and validated execution settings. Offline numerical replay passed using installed dependencies. |
| What comes next without more inference? | Manually review the 412 zero-F1 responses with complete annotations to distinguish answer errors from scoring limitations. |
| What would you extend? | One separately controlled factor, such as context budget, with its own manifest, validation and compute allowance. |
| Did AI tools help? | Yes, with implementation, debugging and writing. Numerical claims come from saved measurements and verification checks. |

## Last-minute memory card

**Purpose:** evidence, quality and latency.

**Design:** 3 retrieval families × 2 sizes × 2 reranking settings = 12 pipelines.

**Sample:** 50 questions per dataset; 100 distinct IDs; 3 timing repetitions.

**Workload:** 7,200 main + 1,200 separate baseline requests.

**Main finding:** reranking costs time; quality changes vary.

**Demo order:** Overview → Results → Paired → Compare.

**Be precise:** F1 is text overlap; repetitions are not new questions; complete
annotations do not guarantee a correct answer.

Verified references: [study report](report.md), [public results](results/stage-b-v4/),
[methods](PROJECT_DEEP_DIVE.md), and the local case-review files under
`reports/stage-b-failure-review-v4-50/`. Dashboard labels follow the current source.
