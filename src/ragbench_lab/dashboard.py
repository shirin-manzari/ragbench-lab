"""Loopback-only Dash viewer; all measurements/intervals are precomputed offline."""

from __future__ import annotations

import hashlib
import json
import os
from html import escape
from pathlib import Path
from urllib.parse import urlencode

from ragbench_lab.dashboard_snapshot import csv_text, load_snapshot, safe_file, table_rows
from ragbench_lab.data.records import DataError

FILTERS = (
    "dataset",
    "model_family",
    "family",
    "recipe",
    "method",
    "size",
    "reranking",
    "context_budget",
)
LABELS = (
    "Dataset",
    "Generator",
    "Retrieval family",
    "Recipe / baseline",
    "Chunking",
    "Chunk size",
    "Reranking",
    "Context budget",
)
METRICS = {
    "token_f1": "Token F1",
    "exact_match": "Exact match",
    "evidence_coverage": "Packed annotated coverage",
    "abstention": "Abstention rate",
    "output_truncation": "Output truncation rate",
    "latency_mean": "Mean online latency",
    "latency_median": "Median online latency",
    "latency_p95": "95th percentile latency",
}
GRAPH_CONFIG = {
    "showSendToCloud": False,
    "showEditInChartStudio": False,
    "plotlyServerURL": "",
    "modeBarButtonsToRemove": ["sendDataToCloud", "sendChartToCloud", "editInChartStudio"],
    "displaylogo": False,
    "responsive": True,
    "toImageButtonOptions": {"format": "svg", "filename": "ragbench-view"},
}


def value_key(value) -> str:
    return "not_measured" if value is None else str(value)


def selected_cells(run: dict, filters: dict) -> list[dict]:
    return [
        c
        for c in run["cells"]
        if all(v == "all" or value_key(c.get(k)) == v for k, v in filters.items())
    ]


def profile(cell: dict) -> str:
    rr = "n/a" if cell.get("reranking") is None else "on" if cell["reranking"] else "off"
    return (
        f"{cell['dataset']} / {cell.get('model_family') or 'retrieval'} / {cell['recipe']} / "
        f"{cell.get('method') or 'n/a'} / {cell.get('size') or 'n/a'} / rr {rr}"
    )


def linked_filters(run: dict, current: dict | None = None, changed: str | None = None) -> list:
    """Keep the last edited facet, then retain only mutually compatible selections."""
    current = current or {}
    chosen, matching = {}, run["cells"]
    order = ([changed] if changed in FILTERS else []) + [k for k in FILTERS if k != changed]
    for field in order:
        available = {value_key(c.get(field)) for c in matching}
        global_values = {value_key(c.get(field)) for c in run["cells"]}
        value = current.get(field, "all")
        if len(global_values) == 1:
            value = next(iter(global_values))
        elif value not in available:
            value = "all"
        chosen[field] = value
        matching = selected_cells(run, chosen)
    result = []
    for field in FILTERS:
        others = {
            k: v
            for k, v in chosen.items()
            if k != field and not (field == "family" and k == "recipe")
        }
        values = sorted({value_key(c.get(field)) for c in selected_cells(run, others)})
        options = [{"label": "All applicable", "value": "all"}] + [
            {
                "label": "Not measured"
                if v == "not_measured"
                else {"True": "On", "False": "Off"}.get(v, v)
                if field == "reranking"
                else v,
                "value": v,
            }
            for v in values
        ]
        result.extend(
            (options, chosen[field], len({value_key(c.get(field)) for c in run["cells"]}) <= 1)
        )
    return result


def active_writers(root: Path) -> bool:
    return root.exists() and next(root.glob("*/.writer.lock"), None) is not None


def create_app(directory: Path, benchmark_root: Path = Path("runs")):
    # Optional imports are isolated here. The viewer never imports export/runner/model code.
    try:
        import plotly.graph_objects as go
        from dash import ClientsideFunction, Dash, Input, Output, State, dcc, html
        from flask import Response, request, send_file
    except ImportError as error:
        raise DataError(
            "install the optional requirements-dashboard.lock in a separate venv"
        ) from error
    if active_writers(benchmark_root):
        raise DataError("stop the dashboard/active benchmark; do not compete with timed work")
    snapshot = load_snapshot(directory)
    runs = {r["key"]: r for r in snapshot["runs"]}
    if not runs:
        raise DataError("snapshot has no available runs")
    assets = Path(__file__).with_name("dashboard_assets")
    app = Dash(
        __name__,
        assets_folder=str(assets),
        serve_locally=True,
        title="ragbench | results",
        update_title=None,
    )
    first = next((k for k, r in runs.items() if r["stage"] == "B"), next(iter(runs)))

    def graph(figure):
        return dcc.Graph(figure=figure, config=GRAPH_CONFIG)

    def empty_figure(message):
        f = go.Figure()
        f.add_annotation(
            text=escape(message), x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False
        )
        return f.update_layout(template="plotly_white", height=350)

    def interval(f, x, y, mx, my):
        # Draw endpoints directly: percentile intervals need not contain the estimate.
        if mx.get("ci95"):
            f.add_trace(
                go.Scatter(
                    x=mx["ci95"],
                    y=[y, y],
                    mode="lines",
                    showlegend=False,
                    line=dict(color="#a0afc0", width=1),
                    hoverinfo="skip",
                )
            )
        if my.get("ci95"):
            scale = 100 if my["unit"] == "fraction" else 1
            f.add_trace(
                go.Scatter(
                    x=[x, x],
                    y=[v * scale for v in my["ci95"]],
                    mode="lines",
                    showlegend=False,
                    line=dict(color="#a0afc0", width=1),
                    hoverinfo="skip",
                )
            )

    def figures(run, cells, metric="token_f1", latency_metric="latency_mean"):
        if not cells:
            return [graph(empty_figure("No configurations match these filters"))]
        available = cells[0]["metrics"]
        if metric not in available:
            metric = "evidence_coverage"
        if latency_metric not in available:
            latency_metric = "latency_median"
        result = []
        for dataset in sorted({c["dataset"] for c in cells}):
            chosen = [c for c in cells if c["dataset"] == dataset]
            f = go.Figure()
            if run["stage"] == "A":
                sizes = sorted({c["size"] for c in chosen})
                recipes = sorted({(c["recipe"], c["method"]) for c in chosen})
                lookup = {(c["recipe"], c["method"], c["size"]): c for c in chosen}
                f.add_trace(
                    go.Heatmap(
                        x=sizes,
                        y=[escape(f"{a} / {b}") for a, b in recipes],
                        z=[
                            [
                                100 * lookup[(a, b, s)]["metrics"]["evidence_coverage"]["estimate"]
                                if (a, b, s) in lookup
                                and lookup[(a, b, s)]["metrics"]["evidence_coverage"]["estimate"]
                                is not None
                                else None
                                for s in sizes
                            ]
                            for a, b in recipes
                        ],
                        zmin=0,
                        zmax=100,
                        colorscale="Blues",
                        colorbar=dict(title="Coverage %"),
                        hovertemplate="%{y}<br>Chunk %{x}<br>Coverage %{z:.2f}%<extra></extra>",
                    )
                )
                f.update_layout(
                    title=f"{escape(dataset)} · packed annotated coverage",
                    xaxis_title="Chunk size (reference tokens)",
                    xaxis_type="category",
                    height=440,
                )
                latency = go.Figure()
                for recipe, method in recipes:
                    rows = sorted(
                        [c for c in chosen if (c["recipe"], c["method"]) == (recipe, method)],
                        key=lambda c: c["size"],
                    )
                    latency.add_trace(
                        go.Scatter(
                            x=[c["size"] for c in rows],
                            y=[c["metrics"][latency_metric]["estimate"] for c in rows],
                            mode="lines+markers",
                            name=escape(f"{recipe}/{method}"),
                        )
                    )
                    for c in rows:
                        m = c["metrics"][latency_metric]
                        if m["estimate"] is not None:
                            interval(latency, c["size"], m["estimate"], {"ci95": None}, m)
                latency.update_layout(
                    title=f"{escape(dataset)} · retrieval latency",
                    xaxis_title="Chunk size (reference tokens)",
                    xaxis=dict(tickmode="array", tickvals=sizes),
                    yaxis_title=f"{METRICS.get(latency_metric, latency_metric)} (seconds)",
                    height=440,
                    legend=dict(font=dict(size=10)),
                )
                if all(c["metrics"]["evidence_coverage"]["estimate"] is None for c in chosen):
                    f = empty_figure("Annotated coverage unavailable; no zero values substituted")
                if all(c["metrics"][latency_metric]["estimate"] is None for c in chosen):
                    latency = empty_figure(
                        "Selected latency unavailable; no zero values substituted"
                    )
                result += [
                    graph(f.update_layout(template="plotly_white")),
                    graph(latency.update_layout(template="plotly_white")),
                ]
            else:
                for c in chosen:
                    mx, my = c["metrics"][latency_metric], c["metrics"][metric]
                    if mx["estimate"] is None or my["estimate"] is None:
                        continue
                    x, y = mx["estimate"], my["estimate"] * 100
                    interval(f, x, y, mx, my)
                    f.add_trace(
                        go.Scatter(
                            x=[x],
                            y=[y],
                            mode="markers",
                            name=escape(profile(c)),
                            marker=dict(
                                size=11 if c.get("size") == 256 else 8,
                                color={
                                    "bm25": "#2876b6",
                                    "dense": "#e87542",
                                    "hybrid": "#13a89e",
                                    "gold": "#a777cf",
                                    "no_rag": "#8292a6",
                                }.get(c.get("family") or c.get("baseline"), "#2876b6"),
                                symbol=("diamond" if c.get("model_family") == "qwen" else "circle")
                                + ("-open" if c.get("reranking") is False else ""),
                            ),
                            hovertemplate=escape(profile(c)) + f"<br>n={c['questions']} questions; "
                            f"{c['timing_measurements']} timings<br>Latency %{{x:.3f}} s"
                            f"<br>{escape(METRICS.get(metric, metric))} %{{y:.2f}}%<extra></extra>",
                        )
                    )
                f.update_layout(
                    title=f"{escape(dataset)} · quality / latency",
                    xaxis_title=f"{METRICS.get(latency_metric, latency_metric)} (seconds)",
                    yaxis_title=f"{METRICS.get(metric, metric)} (%)",
                    height=500,
                    showlegend=False,
                    yaxis_range=[0, 100],
                    template="plotly_white",
                )
                stages = go.Figure()
                for stage in sorted({s for c in chosen for s in c["stage_seconds"]}):
                    if not any(c["stage_seconds"].get(stage) for c in chosen):
                        continue
                    stages.add_bar(
                        x=[
                            escape(
                                f"{c['model_family'][0].upper()} {c['recipe']} "
                                f"{c.get('size') or ''} "
                                f"{'+' if c.get('reranking') else '-'}"
                            )
                            for c in chosen
                        ],
                        y=[c["stage_seconds"].get(stage) for c in chosen],
                        name=stage.replace("_", " "),
                    )
                stages.update_layout(
                    title=f"{escape(dataset)} · disjoint online stage means",
                    barmode="stack",
                    yaxis_title="Mean seconds (setup/isolation excluded)",
                    xaxis_tickangle=-45,
                    height=550,
                    template="plotly_white",
                )
                if not f.data:
                    f = empty_figure("Selected metrics unavailable; no zero values substituted")
                if not stages.data:
                    stages = empty_figure("Stage timings unavailable")
                result += [graph(f), graph(stages)]
        return result

    def plain(value):
        return html.Pre(
            value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2),
            className="plain",
        )

    def raw(title, value):
        return html.Details([html.Summary(title), plain(value)], className="raw-details")

    def table(headers, rows):
        return html.Div(
            html.Table(
                [
                    html.Thead(html.Tr([html.Th(h, scope="col") for h in headers])),
                    html.Tbody([html.Tr([html.Td(v) for v in row]) for row in rows]),
                ]
            ),
            className="table-scroll",
            tabIndex=0,
            role="region",
            **{"aria-label": " / ".join(headers)},
        )

    def number(value, unit="fraction", *, delta=False):
        if value is None:
            return "Unavailable"
        return (
            f"{value * 100:.2f} {'pp' if delta else '%'}"
            if unit == "fraction"
            else f"{value:.4f} s"
        )

    def metric_table(metrics):
        return table(
            ["Metric", "Estimate", "95% interval", "Source clusters"],
            [
                [
                    METRICS.get(name, name.replace("_", " ")),
                    number(m["estimate"], m["unit"]),
                    " – ".join(number(v, m["unit"]) for v in m["ci95"])
                    if m.get("ci95")
                    else "Unavailable",
                    json.dumps(m.get("source_clusters", "not adjusted")),
                ]
                for name, m in metrics.items()
            ],
        )

    def highlighted(text, spans):
        boundaries = sorted(
            {0, len(text), *(max(0, min(len(text), x)) for span in spans for x in span)}
        )
        return [
            html.Mark(text[a:b]) if any(lo <= a < hi for lo, hi in spans) else text[a:b]
            for a, b in zip(boundaries, boundaries[1:])
            if b > a
        ]

    def annotated_chunk(chunk, question):
        spans = [
            (
                max(0, e["start"] - chunk["start"]),
                min(len(chunk["text"]), e["end"] - chunk["start"]),
            )
            for e in question.get("evidence", [])
            if e["document_id"] == chunk["document_id"]
            and e["end"] > chunk["start"]
            and e["start"] < chunk["end"]
        ]
        return html.Div(highlighted(chunk["text"], spans), className="evidence-text")

    def dropdown(identifier, label, options=None, value=None):
        return html.Div(
            [
                html.Label(label, id=f"{identifier}-label", htmlFor=identifier),
                dcc.Dropdown(id=identifier, clearable=False, options=options or [], value=value),
            ],
            className="filter",
        )

    app.layout = html.Div(
        [
            dcc.Store(
                id="filter-conditions",
                storage_type="memory",
                data={
                    key: [{field: c.get(field) for field in FILTERS} for c in run["cells"]]
                    for key, run in runs.items()
                },
            ),
            html.Aside(
                [
                    html.Div("ragbench", className="brand"),
                    html.Div("RESULTS LAB", className="eyebrow"),
                    html.P("A view into the frozen study. No models. No new requests."),
                    html.Details(
                        [
                            html.Summary("Filters & display"),
                            html.Div(
                                [
                                    dropdown(
                                        "stage",
                                        "Study stage",
                                        [
                                            {"label": "All measured stages", "value": "all"},
                                            *[
                                                {"label": s, "value": s}
                                                for s in sorted({r["stage"] for r in runs.values()})
                                            ],
                                        ],
                                        "all",
                                    ),
                                    dropdown("run", "Compatible run set"),
                                    *[
                                        dropdown(k, label)
                                        for k, label in zip(FILTERS, LABELS, strict=True)
                                    ],
                                    dropdown("metric", "Quality / rate metric"),
                                    dropdown("latency-metric", "Latency statistic"),
                                    html.Button(
                                        "Reset filters",
                                        id="reset-filters",
                                        n_clicks=0,
                                        className="reset-button",
                                    ),
                                ],
                                className="filter-body",
                            ),
                        ],
                        id="filter-panel",
                        className="filter-panel",
                    ),
                    html.Div("LOCAL · READ ONLY", className="readonly"),
                ]
            ),
            html.Main(
                [
                    html.Header(
                        [
                            html.Div("EXPERIMENT EXPLORER", className="eyebrow"),
                            html.H1("Evidence, answers & time"),
                            html.P("Explore saved measurements without changing the experiment."),
                        ]
                    ),
                    html.Div(id="overview", className="panel"),
                    dcc.Tabs(
                        [
                            dcc.Tab(
                                label="Results", children=[html.Div(id="plots", className="plots")]
                            ),
                            dcc.Tab(
                                label="Configuration & questions",
                                children=[
                                    html.Div(
                                        [
                                            dropdown("condition", "Configuration"),
                                            html.Div(id="details"),
                                            html.Label(
                                                "Find a saved question", htmlFor="question-search"
                                            ),
                                            dcc.Input(
                                                id="question-search",
                                                type="search",
                                                placeholder="Search question text or ID",
                                                debounce=True,
                                                className="search-input",
                                            ),
                                            dropdown("question", "Saved question"),
                                            html.Div(id="example"),
                                        ],
                                        className="panel",
                                    )
                                ],
                            ),
                            dcc.Tab(
                                label="Paired comparisons",
                                children=[
                                    dropdown(
                                        "contrast",
                                        "Left minus right",
                                    ),
                                    html.Div(id="paired", className="panel"),
                                ],
                            ),
                            dcc.Tab(
                                label="Context & extensions",
                                children=[
                                    html.Div(
                                        [
                                            html.H3("No extra study is implied"),
                                            html.P(
                                                "Only the frozen 1,024-token budget is measured "
                                                "here. SmolLM and 512/2,048 comparisons are "
                                                "pending, not zero-valued results."
                                            ),
                                            plain(snapshot.get("missing_studies", [])),
                                        ],
                                        className="panel",
                                    )
                                ],
                            ),
                            dcc.Tab(
                                label="Downloads & provenance",
                                children=[
                                    html.Div(
                                        [
                                            html.H3("Offline exports"),
                                            html.A(
                                                "All snapshot cells · CSV",
                                                href="/exports/tables.csv",
                                            ),
                                            html.P(
                                                html.A(
                                                    "Selected run and filters · CSV",
                                                    id="filtered-download",
                                                    href="/filtered.csv",
                                                )
                                            ),
                                            html.P(
                                                "Downloads preserve run boundaries and original "
                                                "units/intervals. Core SVG/PDF figures are copied "
                                                "unchanged; they do not follow filters."
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li(html.A(name, href=f"/exports/{name}"))
                                                    for name in snapshot["files"]
                                                    if name != "tables.csv"
                                                ]
                                            ),
                                            raw(
                                                "Raw export provenance",
                                                {
                                                    k: snapshot[k]
                                                    for k in (
                                                        "manifest_sha256",
                                                        "raw_archive_sha256",
                                                        "provenance",
                                                    )
                                                },
                                            ),
                                        ],
                                        className="panel",
                                    )
                                ],
                            ),
                        ]
                    ),
                    html.Footer(
                        "Stop this viewer before timed experiments. Scores and intervals are "
                        "descriptive; repeated timings are not independent questions."
                    ),
                ]
            ),
        ],
        className="shell",
    )

    @app.callback(
        Output("run", "options"),
        Output("run", "value"),
        Input("stage", "value"),
        State("run", "value"),
    )
    def run_options(stage, current):
        options = [
            {"label": r["label"], "value": k}
            for k, r in runs.items()
            if stage in {None, "all", r["stage"]}
        ]
        values = {o["value"] for o in options}
        return options, (
            current
            if current in values
            else first
            if first in values
            else options[0]["value"]
            if options
            else None
        )

    app.clientside_callback(
        ClientsideFunction(namespace="ragbench", function_name="filters"),
        *[
            out
            for key in FILTERS
            for out in (Output(key, "options"), Output(key, "value"), Output(key, "disabled"))
        ],
        Input("run", "value"),
        Input("reset-filters", "n_clicks"),
        *[Input(k, "value") for k in FILTERS],
        State("filter-conditions", "data"),
    )

    def filter_options(key, current=None, changed=None):
        return linked_filters(runs.get(key, {"cells": []}), current, changed)

    @app.callback(
        Output("contrast", "options"),
        Output("contrast", "value"),
        Input("run", "value"),
        State("contrast", "value"),
    )
    def contrast_options(key, current):
        names = sorted({p["contrast"] for p in runs.get(key, {}).get("paired_contrasts", [])})
        return (
            [{"label": n.replace("_minus_", " − ").replace("_", " "), "value": n} for n in names],
            current if current in names else next(iter(names), None),
        )

    @app.callback(
        Output("metric", "options"),
        Output("metric", "value"),
        Output("latency-metric", "options"),
        Output("latency-metric", "value"),
        Input("run", "value"),
        State("metric", "value"),
        State("latency-metric", "value"),
    )
    def metric_options(key, current, latency):
        cells = runs.get(key, {}).get("cells", [])
        names = sorted({m for c in cells for m in c["metrics"]})
        quality = [n for n in names if not n.startswith("latency_")]
        timings = [n for n in names if n.startswith("latency_")]

        def options(items):
            return [{"label": METRICS.get(n, n), "value": n} for n in items]

        return (
            options(quality),
            current
            if current in quality
            else "token_f1"
            if "token_f1" in quality
            else next(iter(quality), None),
            options(timings),
            latency
            if latency in timings
            else "latency_mean"
            if "latency_mean" in timings
            else next(iter(timings), None),
        )

    @app.callback(
        Output("overview", "children"),
        Output("plots", "children"),
        Output("condition", "options"),
        Output("condition", "value"),
        Input("run", "value"),
        *[Input(k, "value") for k in FILTERS],
        Input("metric", "value"),
        Input("latency-metric", "value"),
        State("condition", "value"),
    )
    def render_results(key, *values):
        return update_results(
            key, *values[: len(FILTERS)], values[-1], metric=values[-3], latency_metric=values[-2]
        )

    def update_results(key, *values, metric="token_f1", latency_metric="latency_mean"):
        run = runs.get(key)
        if run is None:
            return [html.P("No compatible run selected")], [], [], None
        filters = dict(zip(FILTERS, [v or "all" for v in values[:-1]], strict=True))
        cells = selected_cells(run, filters)
        options = [{"label": profile(c), "value": c["condition_id"]} for c in cells]
        current = values[-1]
        chosen = (
            current
            if current in {o["value"] for o in options}
            else (options[0]["value"] if options else None)
        )
        completion = run["completion"]
        cids = {c["condition_id"] for c in cells}
        requests = [r for r in run.get("requests", []) if r["condition_id"] in cids]
        successes = (
            sum(r["status"] == "success" for r in requests)
            if run.get("requests")
            else sum(c["timing_measurements"] for c in cells)
        )
        failures = (
            sum(r["status"] == "failed" for r in requests)
            if run.get("requests")
            else sum(c.get("failures", 0) for c in cells)
        )
        overview = [
            html.H2(run["label"]),
            html.Div(
                [
                    html.Div([html.Strong(str(len(cells))), html.Span("visible configurations")]),
                    html.Div(
                        [
                            html.Strong(str(successes)),
                            html.Span("successful requests in view"),
                        ]
                    ),
                    html.Div(
                        [
                            html.Strong(str(failures)),
                            html.Span("failed attempts in view"),
                        ]
                    ),
                ],
                className="cards",
            ),
            html.P(f"{completion['status'].upper()} · {run['purpose']} · {run['uncertainty']}"),
            html.P(
                f"Entire run: {completion.get('successful_requests', 'unavailable')} successes; "
                f"{completion.get('failed_attempts', 'unavailable')} failed attempts. "
                "The cards and plots above follow your filters.",
                className="muted",
            ),
            html.P(
                "Repetition-one quality; repeat timings stay within question. "
                "Select a configuration for counts, intervals and source details."
            ),
            html.P(run["example_scope"], className="muted"),
            html.P(
                "Plot key: blue BM25, orange Dense, teal Hybrid; circles Llama, "
                "diamonds Qwen; open = reranking off; larger = size 256."
                if run["stage"] == "B"
                else "Unavailable fields are not zero measurements.",
                className="muted",
            ),
        ]
        return overview, figures(run, cells, metric, latency_metric), options, chosen

    @app.callback(
        Output("details", "children"),
        Output("question", "options"),
        Output("question", "value"),
        Input("run", "value"),
        Input("condition", "value"),
        Input("question-search", "value"),
        State("question", "value"),
    )
    def configuration(key, cid, search="", previous=None):
        run = runs.get(key, {"cells": [], "examples": []})
        cell = next((c for c in run["cells"] if c["condition_id"] == cid), None)
        if cell is None:
            return html.P("No configuration selected"), [], None
        search = (search or "").casefold().strip()
        examples = [
            e
            for e in run["examples"]
            if e["condition_id"] == cid
            and (
                search in e["question_id"].casefold()
                or search in e["question"].get("text", "").casefold()
            )
        ]
        options = [
            {
                "label": e["question"].get("text") or "Question text unavailable",
                "value": e["question_id"],
            }
            for e in examples
        ]
        return (
            [
                html.H3(profile(cell)),
                html.P(
                    f"{cell['questions']} repetition-one questions; "
                    f"{cell['timing_measurements']} timings. {run['uncertainty']}"
                ),
                metric_table(cell["metrics"]),
                raw(
                    "Raw configuration & provenance",
                    {
                        "condition": cell,
                        "run_id": run["run_id"],
                        "compatibility_key": run["compatibility_key"],
                        "provenance": run["provenance"],
                    },
                ),
            ],
            options,
            previous
            if previous in {o["value"] for o in options}
            else options[0]["value"]
            if options
            else None,
        )

    @app.callback(
        Output("example", "children"),
        Input("run", "value"),
        Input("question", "value"),
        Input("condition", "value"),
    )
    def question_example(key, request, cid=None):
        run = runs.get(key, {"examples": []})
        record = next(
            (
                e
                for e in run["examples"]
                if e["request_key"] == request
                or (e["question_id"] == request and e["condition_id"] == cid)
            ),
            None,
        )
        if not record:
            return html.P("No saved example for this selection; no question will be executed.")
        question, context = record["question"], record["context"]
        annotations = []
        for included in context.get("evidence", []):
            for evidence in question.get("evidence", []):
                if evidence["document_id"] == included["document_id"]:
                    lo, hi = (
                        max(evidence["start"], included["source_start"]),
                        min(evidence["end"], included["source_end"]),
                    )
                    if lo < hi:
                        annotations.append(
                            (
                                included["context_start"] + lo - included["source_start"],
                                included["context_start"] + hi - included["source_start"],
                            )
                        )
        retrieval_rows = [
            [name.replace("_", " "), number(m["evidence_coverage"])]
            for name, m in (record.get("metrics") or {}).items()
            if isinstance(m, dict) and "evidence_coverage" in m
        ]
        chunks = [
            html.Article(
                [
                    html.H4(
                        f"Final rank {i + 1} · {item['chunk'].get('reference_tokens', '?')} tokens"
                    ),
                    html.P(
                        f"Source {item['chunk']['document_id']} · "
                        f"characters {item['chunk']['start']}–{item['chunk']['end']}"
                    ),
                    annotated_chunk(item["chunk"], question),
                    html.P(
                        f"Original retrieval score: {item.get('score', 'unavailable')}. "
                        "Not a reranker score.",
                        className="muted",
                    ),
                ],
                className="evidence-card",
            )
            for i, item in enumerate(record["retrieved_top5"])
        ]
        return [
            html.H3("Saved question & references"),
            html.P(question.get("text", "Question text unavailable"), className="question-text"),
            html.P([html.Strong("Reference answers: "), " / ".join(question.get("answers", []))]),
            html.H3("Generated answer"),
            html.Div(
                record["answer"]
                if record["answer"] is not None
                else "Not measured in Stage A"
                if run.get("stage") == "A"
                else "Unavailable — no saved successful answer",
                className="answer-card",
            ),
            html.P(
                f"Status: {record['status']} · Output truncated: "
                f"{record.get('output_truncated', 'not measured')}"
            ),
            html.P(record.get("error") or "No recorded error"),
            table(
                ["Answer score", "Value"],
                [
                    [METRICS.get(k, k), number(v)]
                    for k, v in (record.get("answer_metrics") or {}).items()
                ],
            ),
            html.H3("Per-question annotated retrieval coverage"),
            table(["Evidence included", "Coverage"], retrieval_rows)
            if retrieval_rows
            else html.P("Retrieval coverage not measured for this baseline."),
            html.H3("Exact packed evidence and source offsets"),
            html.P(
                "Highlighted spans match dataset annotations, not an independent factuality "
                "judgment. The text and offsets are unchanged."
            ),
            html.Div(highlighted(context.get("text", ""), annotations), className="evidence-text"),
            table(
                ["Source document", "Source characters", "Packed characters", "Truncated"],
                [
                    [
                        e["document_id"],
                        f"{e['source_start']}–{e['source_end']}",
                        f"{e['context_start']}–{e['context_end']}",
                        str(e.get("truncated", False)),
                    ]
                    for e in context.get("evidence", [])
                ],
            ),
            html.H3(
                "No retrieval in this baseline"
                if record.get("baseline")
                else "First five retrieved chunks"
            ),
            *chunks,
            raw("Raw question, scores, context, chunks & record lineage", record),
        ]

    @app.callback(
        Output("paired", "children"),
        Input("run", "value"),
        Input("contrast", "value"),
        *[Input(k, "value") for k in FILTERS],
        Input("metric", "value"),
        Input("latency-metric", "value"),
    )
    def render_paired(key, contrast, *values):
        return paired(
            key, contrast, *values[: len(FILTERS)], metric=values[-2], latency_metric=values[-1]
        )

    def paired(key, contrast, *values, metric="token_f1", latency_metric="latency_mean"):
        run = runs.get(key, {"cells": [], "paired_contrasts": []})
        filters = dict(zip(FILTERS, [v or "all" for v in values], strict=True))
        cids = {c["condition_id"] for c in selected_cells(run, filters)}
        rows = [
            p
            for p in run["paired_contrasts"]
            if p["contrast"] == contrast
            and p["left_condition_id"] in cids
            and p["right_condition_id"] in cids
        ]
        if not rows:
            return html.P(
                "No paired estimates available for this run/contrast; no pooling or recomputation."
            )
        lookup = {c["condition_id"]: c for c in run["cells"]}
        table_data, plots = [], []
        for name in dict.fromkeys([metric, latency_metric]):
            plot = go.Figure()
            for index, row in enumerate(rows):
                m = row["metrics"].get(name)
                if m is None or m["estimate"] is None:
                    continue
                left, right = lookup[row["left_condition_id"]], lookup[row["right_condition_id"]]
                unit = left["metrics"][name]["unit"]
                ci = m.get("source_ci95")
                table_data.append(
                    [
                        index + 1,
                        profile(left),
                        profile(right),
                        METRICS.get(name, name),
                        number(m["estimate"], unit, delta=True),
                        " – ".join(number(v, unit, delta=True) for v in ci)
                        if ci
                        else "Unavailable",
                        json.dumps(m.get("questions", "unavailable")),
                        json.dumps(m.get("source_clusters", "unavailable")),
                    ]
                )
                y = f"{index + 1}. {row['dataset']}"
                scale = 100 if unit == "fraction" else 1
                if ci:
                    plot.add_trace(
                        go.Scatter(
                            x=[v * scale for v in ci],
                            y=[y, y],
                            mode="lines",
                            showlegend=False,
                            line=dict(color="#8093aa"),
                            hoverinfo="skip",
                        )
                    )
                plot.add_trace(
                    go.Scatter(
                        x=[m["estimate"] * scale],
                        y=[y],
                        mode="markers",
                        marker=dict(color="#12677b", size=9),
                        showlegend=False,
                        hovertemplate=escape(profile(left) + " minus " + profile(right))
                        + "<br>Effect %{x:.4f}<extra></extra>",
                    )
                )
            if plot.data:
                plot.add_vline(x=0, line_dash="dot", line_color="#748295")
                plot.update_layout(
                    template="plotly_white",
                    height=max(340, 160 + len(rows) * 25),
                    title=METRICS.get(name, name),
                    yaxis_title="Pair (see table)",
                    xaxis_title="Left − right (percentage points)"
                    if scale == 100
                    else "Left − right (seconds)",
                )
                plots.append(graph(plot))
        return [
            html.P(
                "Original paired estimates; positive latency means slower. "
                "Positive rate/coverage differences mean higher, not necessarily better. "
                "95% source intervals are unadjusted; pp means percentage points. "
                "Cross-run/baseline pairs are not pooled. Only the selected metrics are shown."
            ),
            html.Div(plots, className="plots"),
            table(
                [
                    "Pair",
                    "Left configuration",
                    "Right configuration",
                    "Metric",
                    "Difference",
                    "95% source interval",
                    "Distinct questions",
                    "Source clusters",
                ],
                table_data,
            ),
            raw("All original paired metrics & provenance", rows),
        ]

    @app.callback(
        Output("filtered-download", "href"),
        Input("run", "value"),
        *[Input(k, "value") for k in FILTERS],
    )
    def filtered_link(key, *values):
        return "/filtered.csv?" + urlencode({"run": key or "", **dict(zip(FILTERS, values))})

    @app.server.before_request
    def refuse_timed_work():
        from urllib.parse import urlsplit

        if urlsplit(request.host_url).hostname not in {"127.0.0.1", "localhost", "::1"}:
            return Response("Local dashboard accepts only loopback hosts", status=403)
        if active_writers(benchmark_root):
            return Response(
                "A benchmark writer is active. Stop the dashboard before timed work.",
                status=503,
                content_type="text/plain",
            )

    @app.server.get("/filtered.csv")
    def filtered_csv():
        run = runs.get(request.args.get("run"))
        if run is None or set(request.args) - {"run", *FILTERS}:
            return Response("Select a known run and filters", status=400)
        filters = {k: request.args.get(k, "all") for k in FILTERS}
        for field, value in filters.items():
            if value != "all" and value not in {value_key(c.get(field)) for c in run["cells"]}:
                return Response("Unknown filter value", status=400)
        rows = table_rows(run, selected_cells(run, filters))
        response = Response(
            csv_text(rows or [{"status": "no matching configurations", "run_key": run["key"]}]),
            mimetype="text/csv",
        )
        response.headers["Content-Disposition"] = 'attachment; filename="ragbench-filtered.csv"'
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.server.get("/exports/<path:name>")
    def download(name):
        if name not in snapshot["files"]:
            return Response("Unknown export", status=404)
        path = safe_file(directory, name)
        with path.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != snapshot["files"][name]:
                return Response("Export bytes changed; reload a verified snapshot", status=409)
        response = send_file(path.resolve(), as_attachment=True, download_name=Path(name).name)
        response.headers["Content-Security-Policy"] = "sandbox"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    # Exposed only for local unit tests; this object is never sent to the browser.
    app.viewer_functions = {
        "run_options": run_options,
        "filter_options": filter_options,
        "update_results": update_results,
        "configuration": configuration,
        "question_example": question_example,
        "paired": paired,
        "contrast_options": contrast_options,
        "metric_options": metric_options,
        "filtered_link": filtered_link,
    }
    return app


def serve_dashboard(directory: Path, port: int = 8050) -> None:
    if not 1024 <= port <= 65535:
        raise DataError("dashboard port must be between 1024 and 65535")
    app = create_app(directory)
    print(
        f"Read-only dashboard PID {os.getpid()}; http://127.0.0.1:{port}; stop before timed work",
        flush=True,
    )
    app.run(
        host="127.0.0.1",
        port=port,
        debug=False,
        use_reloader=False,
        dev_tools_ui=False,
        dev_tools_hot_reload=False,
        dev_tools_disable_version_check=True,
    )
