from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

from verify_public_results import (
    CONDITION_FIELDS,
    METRIC_FIELDS,
    ROOT,
    STUDY_V4,
    table,
    verify,
)

DEFAULT_OUTPUT = ROOT / "presentations/stage-b-v4.html"


def build(bundle: Path) -> str:
    verify(bundle)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    if manifest["study"] != STUDY_V4:
        raise ValueError("presentation requires the separate v4 bundle")
    conditions = {c["condition_id"]: c for c in table(
        (bundle / "conditions.csv").read_bytes(), CONDITION_FIELDS)}
    cells = table((bundle / "cells.csv").read_bytes(), METRIC_FIELDS)
    contrasts = table((bundle / "contrasts.csv").read_bytes(), METRIC_FIELDS)
    values = {(r["left_id"], r["metric"]): float(r["estimate"]) for r in cells}
    names = {"squad": "SQuAD", "hotpot_qa": "HotpotQA", "llama": "Llama", "qwen": "Qwen"}
    rows, baselines = [], []
    for dataset in ("squad", "hotpot_qa"):
        for model in ("llama", "qwen"):
            subset = [c for c in conditions.values()
                      if c["dataset"] == dataset and c["model"] == model]
            main = [c["condition_id"] for c in subset if c["role"] == "rag"]
            f1 = [100 * values[c, "token_f1"] for c in main]
            latency = [values[c, "latency_mean"] for c in main]
            label = f'<th scope="row">{names[dataset]} / {names[model]}</th>'
            rows.append(f'<tr>{label}<td>{min(f1):.2f}–{max(f1):.2f}%</td>'
                        f'<td>{min(latency):.2f}–{max(latency):.2f} s</td></tr>')
            baseline = {c["role"]: values[c["condition_id"], "token_f1"] * 100
                        for c in subset if c["role"] != "rag"}
            baselines.append(f'<tr>{label}<td>{baseline["no_rag"]:.2f}%</td>'
                             f'<td>{baseline["gold"]:.2f}%</td></tr>')
    reranking = [r for r in contrasts if r["condition_or_contrast"] == "reranking_on_minus_off"]
    f1 = [float(r["estimate"]) * 100 for r in reranking if r["metric"] == "token_f1"]
    latency = [float(r["estimate"]) for r in reranking if r["metric"] == "latency_mean"]
    positive, negative = sum(v > 0 for v in f1), sum(v < 0 for v in f1)
    charts = {}
    for name, label in (("quality_latency.svg", "Quality and latency across the twelve pipelines"),
                        ("stage_times_main.svg", "Mean online latency by stage")):
        # The verifier rejects active/external SVG content. Inline figures keep the deck standalone.
        svg = (bundle / name).read_text(encoding="utf-8")
        svg = svg[svg.index("<svg"):]
        charts[name] = f'<figure aria-label="{label}">{svg}<figcaption>{label}; original ' \
                       'source-cluster intervals are preserved where plotted.</figcaption></figure>'
    deck = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Offline presentation of verified RAGBench Lab Stage B v4
aggregates">
<title>RAGBench Lab · Stage B v4</title>
<style>
:root{color-scheme:light;--ink:#152b32;--muted:#52646c;--teal:#087f78;--paper:#f2f5f2}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);
font:18px/1.55 system-ui,sans-serif}a{color:var(--teal)}
nav{position:sticky;top:0;background:#fff;z-index:2;border-bottom:1px solid #ccd8d3;
padding:12px 5vw;display:flex;gap:20px;flex-wrap:wrap;font-size:14px}
nav a{text-decoration:none}a:focus-visible,summary:focus-visible{outline:3px solid #c77c23}
main{max-width:1280px;margin:auto;padding:0 4vw}section{padding:64px 0;
border-bottom:1px solid #cbd7d1;scroll-margin-top:100px;min-height:80vh}
h1{font-size:clamp(42px,7vw,82px);line-height:1.05;max-width:900px;letter-spacing:-.05em}
h2{font-size:clamp(30px,4vw,48px);line-height:1.15;letter-spacing:-.03em}
h3{font-size:22px}.eyebrow{color:var(--teal);font-size:14px;letter-spacing:.12em;text-transform:uppercase}
p{max-width:900px}.lede{font-size:24px}.muted,figcaption{color:var(--muted);font-size:15px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:32px 0}
.card{background:white;border:1px solid #d5dfd9;border-radius:12px;padding:24px}
.card strong{display:block;font-size:38px;color:var(--teal)}
.flow{padding:20px;background:#e3eeea;border-left:4px solid var(--teal)}
table{border-collapse:collapse;width:100%;background:white;font-variant-numeric:tabular-nums}
th,td{padding:14px;text-align:left;border-bottom:1px solid #d5dfd9}thead{background:#dce9e4}
figure{margin:30px 0;background:white;padding:12px;border:1px solid #d5dfd9}
figure svg{width:100%;height:auto;display:block}figcaption{padding:12px}
details{margin-top:24px;padding:16px;background:#fff}summary{cursor:pointer;font-weight:600}
code{font-size:.85em;overflow-wrap:anywhere}.hash{font-size:12px;overflow-wrap:anywhere}
li{margin:10px 0}footer{padding:24px 4vw}.table-wrap{overflow-x:auto}
@media(max-width:650px){.cards{grid-template-columns:1fr}
section{padding:36px 0}
th,td{padding:9px}
nav{gap:12px}
}
@media print{nav,details{display:none}
body{font-size:12pt;background:white}
main{max-width:none;padding:0}
section{min-height:0;break-before:page;padding:12mm 0;border:0}
section:first-child{break-before:auto}
h1{font-size:44pt}h2{font-size:28pt}.cards{gap:10px}.card strong{font-size:24pt}
figure,table,.cards{break-inside:avoid}figure{padding:0}footer{font-size:9pt}}
</style></head><body>
<nav aria-label="Presentation sections"><a href="#intro">Overview</a><a href="#design">Design</a>
<a href="#results">Results</a><a href="#tradeoffs">Trade-offs</a><a href="#baselines">Baselines</a>
<a href="#limits">Limits</a><a href="#demo">Demo</a></nav><main>
<section id="intro"><p class="eyebrow">RAGBench Lab / Stage B v4 / 19 October 2026</p>
<h1>Where does a RAG pipeline spend its time?</h1>
<p class="lede">A local study of retrieval, chunk size and reranking, measuring the evidence
supplied to two small generators and the answers they produce.</p>
<div class="cards"><div class="card"><strong>7,200</strong>main timing measurements</div>
<div class="card"><strong>1,200</strong>separate baseline measurements</div>
<div class="card"><strong>100</strong>distinct question IDs</div></div>
<p>Reranking added latency in every matched comparison. Its answer-quality changes had both
signs.</p>
<p class="muted">Saved measurements only. No inference, model downloads or network access is needed
for this presentation. Scroll, use the section links or press ← / →. Print to PDF for handouts.</p>
<details><summary>Speaker notes · 30 seconds</summary><p>Introduce the question: which pipeline
choices improve reference answer overlap enough to justify their online cost? Clarify that 8,400
measurements do not mean 8,400 independent questions.</p></details></section>
<section id="design"><p class="eyebrow">01 / Design</p><h2>Screen retrieval, then freeze the
choice</h2>
<p><b>Stage A:</b> five retrieval recipes × two chunkers × three sizes. Development evidence
coverage selected E5 and sentence-aware chunking before held-out evaluation.</p>
<p><b>Stage B:</b> BM25 / Dense / Hybrid × 128 / 256 reference-token chunks × reranking off / on.
Twelve pipelines × two datasets × two generators = 48 main conditions.</p>
<p class="flow">Question → retrieve 50 candidates → optional rerank → pack evidence into
1,024 reference tokens → generate up to 64 native output tokens → score saved answer and
evidence</p>
<p>SQuAD v1.1 and adapted shared-corpus HotpotQA; Qwen2.5-3B-Instruct and
Llama-3.2-3B-Instruct in Q4_K_M on one macOS ARM64 host. Each condition uses 50 questions
and three sequential timing repetitions. Quality uses repetition one.</p>
<details><summary>Speaker notes · 45 seconds</summary><p>The evidence text is paired across
generators. Chunking and evidence budgets share one reference tokenizer; native prompt counts are
checked separately. Stage A has 9,000 development and 18,000 held-out retrieval requests;
these are separate from Stage B counts.</p></details></section>
<section id="results"><p class="eyebrow">02 / Results</p><h2>Quality and cost depend on the
task</h2>
<div class="table-wrap"><table><caption>Ranges across twelve main pipeline point estimates</caption>
<thead><tr><th>Dataset / generator</th><th>Token F1</th><th>Mean online latency</th></tr></thead>
<tbody>@@ROWS@@</tbody></table></div>
<p class="muted">Ranges are not confidence intervals. F1 is reference-token overlap, not
factuality.</p>
@@QUALITY@@
<details><summary>Speaker notes · 60 seconds</summary><p>Read within each dataset/model group.
Use the plot to discuss quality versus mean latency rather than declare a universal winner.
Error bars retain the original source-cluster 95% bootstrap intervals; use the exported paired
contrasts for differences, rather than infer significance from cell interval
overlap.</p></details></section>
<section id="tradeoffs"><p class="eyebrow">03 / Matched comparisons</p>
<h2>Reranking adds cost; quality changes vary</h2>
<div class="cards"><div class="card"><strong>@@LATENCY@@ s</strong>change in mean online
latency</div>
<div class="card"><strong>@@F1@@ pp</strong>change in token F1</div>
<div class="card"><strong>@@SIGNS@@</strong>positive / negative F1 changes</div></div>
<p>These are 24 matched reranking-on minus reranking-off point estimates. Signs are descriptive;
they are not counts of statistically significant wins. No universal best pipeline is
established.</p>
@@STAGES@@
<details><summary>Speaker notes · 45 seconds</summary><p>Locate the reranking segment in the
time breakdown. Online latency includes embedding, search/fusion, reranking, packing and generation.
Setup, warmup, cache isolation, scoring and record writes are excluded. Concurrent serving capacity
was not measured.</p></details></section>
<section id="baselines"><p class="eyebrow">04 / Diagnostic baselines</p><h2>Better evidence helps;
it does not guarantee an answer</h2>
<div class="table-wrap"><table><caption>Separate baseline token F1 point estimates</caption>
<thead><tr><th>Dataset / generator</th><th>No-RAG</th><th>Gold evidence</th></tr></thead>
<tbody>@@BASELINES@@</tbody></table></div>
<p>No-RAG retains the grounding and abstention instruction. It is an empty-evidence control,
not an unrestricted knowledge test. Gold context can truncate at the common budget and is a
diagnostic reference, not a guaranteed upper bound. Baseline timing paths differ from main.</p>
<details><summary>Speaker notes · 30 seconds</summary><p>Explain why low No-RAG scores should
not be read as the models' general knowledge ability. All eight baseline conditions remain outside
the twelve-pipeline main factorial.</p></details></section>
<section id="limits"><p class="eyebrow">05 / Interpretation</p><h2>What these results support</h2>
<ul><li>V4 is a post-results nested expansion after v3 inspection. It uses fresh measurements
without pooling earlier aggregates; it is not an untouched confirmatory holdout.</li>
<li>The 100 IDs span 14 SQuAD article clusters and 50 Hotpot supporting-source components.
Repeated timings do not create new independent questions.</li>
<li>95% source-cluster percentile intervals use 2,000 draws and are unadjusted for multiple
comparisons. Source dependence, small samples and single-host timings limit generalization and
tails.</li>
<li>EM/F1 measure text agreement. Complete annotated evidence does not establish semantic
sufficiency. Neither metric alone measures factual correctness.</li>
<li>Model/context/load extensions remain unmeasured. Aggregate consistency checks do not
recompute bootstraps, audit raw runs or demonstrate independent replication.</li></ul>
<details><summary>Speaker notes · 30 seconds</summary><p>State these limits before inviting
questions about generalization. The public bundle excludes raw question and answer content.
Detailed provenance and offline replay materials remain in the separate local
archive.</p></details></section>
<section id="demo"><p class="eyebrow">06 / Live walkthrough</p><h2>A demo that works without
inference</h2>
<ol><li>Explain the frozen design and open the quality–latency plot above.</li>
<li>Show <code>conditions.csv</code>, then join a condition ID to <code>cells.csv</code>.
Scores use fractions; latency uses seconds.</li>
<li>Open <code>contrasts.csv</code>: the direction is left minus right, with the original paired
interval.</li>
<li>If the local snapshot is available, open the read-only dashboard to compare saved answers
and packed evidence. It requires local assets and the optional viewer environment.</li></ol>
<p>From the repository, verify the public bundle with:</p>
<pre><code>python3 scripts/verify_public_results.py results/stage-b-v4</code></pre>
<p class="muted">The standalone HTML is the fallback when dashboard dependencies or local data
are unavailable. The local ignored DEMO.md supplies the timed script and exact viewer command.</p>
<p>Source bundle inventory: <code class="hash">@@MANIFEST@@</code></p>
<p class="muted">Built deterministically from verified aggregate CSVs and unchanged SVGs.
AI tools assisted implementation and writing; numerical claims come from saved
measurements.</p></section>
</main><footer>RAGBench Lab · Stage B v4 · Offline presentation · Public aggregates only</footer>
<script>
document.addEventListener('keydown',event=>{
 if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||
 event.target.closest('a,button,input,select,textarea,summary,[contenteditable]'))return;
 const direction=event.key==='ArrowRight'?1:event.key==='ArrowLeft'?-1:0;if(!direction)return;
 const sections=[...document.querySelectorAll('main>section')];
 const current=sections.reduce(
  (index,section,i)=>section.getBoundingClientRect().top<=150?i:index,0);
 const target=sections[Math.max(0,Math.min(sections.length-1,current+direction))];
 location.hash=target.id;event.preventDefault();
});
</script></body></html>
'''
    replacements = {
        "@@ROWS@@": "".join(rows), "@@BASELINES@@": "".join(baselines),
        "@@LATENCY@@": f"{min(latency):.2f}–{max(latency):.2f}",
        "@@F1@@": f"{min(f1):+.2f} to {max(f1):+.2f}",
        "@@SIGNS@@": f"{positive} / {negative}",
        "@@QUALITY@@": charts["quality_latency.svg"],
        "@@STAGES@@": charts["stage_times_main.svg"],
        "@@MANIFEST@@": html.escape(manifest["manifest_sha256"]),
    }
    for key, value in replacements.items():
        deck = deck.replace(key, value)
    return deck


def main() -> int:
    parser = argparse.ArgumentParser(description=(
        'Build an offline v4 presentation from the verified aggregate bundle;'
        ' no models.'
    ))
    parser.add_argument("--bundle", type=Path, default=ROOT / "results/stage-b-v4")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    try:
        content = build(args.bundle).encode("utf-8")
        if args.check:
            if args.output.read_bytes() != content:
                raise ValueError("presentation differs from verified aggregate inputs")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("xb") as stream:
                stream.write(content)
        print(json.dumps({"presentation": args.output.name, "bytes": len(content),
                          "sections": 7, "model_requests": 0}))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"presentation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
