/* Local label associations; no network, storage or benchmark work. */
(() => {
  const fields = ["dataset", "model_family", "family", "recipe", "method", "size", "reranking", "context_budget"];
  const keyOf = value => value == null ? "not_measured" : typeof value === "boolean" ? (value ? "True" : "False") : String(value);
  const matching = (cells, values) => cells.filter(c => Object.entries(values).every(([k,v]) => v === "all" || keyOf(c[k]) === v));
  window.dash_clientside = Object.assign({}, window.dash_clientside);
  window.dash_clientside.ragbench = {
    filters: function(key, reset, ...args) {
      const metadata = args.pop() || {}, cells = metadata[key] || [];
      const changed = (window.dash_clientside.callback_context?.triggered?.[0]?.prop_id || "").split(".")[0];
      const current = Object.fromEntries(fields.map((field, i) => [field, changed === "reset-filters" ? "all" : args[i]]));
      const order = [...(fields.includes(changed) ? [changed] : []), ...fields.filter(k => k !== changed)];
      const chosen = {};
      for (const field of order) {
        const available = new Set(matching(cells, chosen).map(c => keyOf(c[field])));
        const global = new Set(cells.map(c => keyOf(c[field])));
        chosen[field] = global.size === 1 ? [...global][0] : available.has(current[field]) ? current[field] : "all";
      }
      return fields.flatMap(field => {
        const others = Object.fromEntries(Object.entries(chosen).filter(([k]) => k !== field && !(field === "family" && k === "recipe")));
        const values = [...new Set(matching(cells, others).map(c => keyOf(c[field])))].sort();
        const options = [{label:"All applicable", value:"all"}, ...values.map(value => ({value, label:value === "not_measured" ? "Not measured" : field === "reranking" ? ({True:"On", False:"Off"}[value] || value) : value}))];
        return [options, chosen[field], new Set(cells.map(c => keyOf(c[field]))).size <= 1];
      });
    }
  };
  // Selection still belongs to Dash. This only positions a decorative CSS pill.
  // Motion reference (independent implementation): codepen.io/flavio_amaral/pen/xxgYGrR
  const sliders = new WeakSet();
  function installSlider(track) {
    if (sliders.has(track)) return;
    sliders.add(track);
    let frame = null;
    function update() {
      frame = null;
      const active = track.querySelector(".tab--selected");
      if (!active) {
        if (track.classList.contains("tab-slider-ready")) {
          track.classList.remove("tab-slider-ready");
        }
        return;
      }
      const rect = active.getBoundingClientRect(), bounds = track.getBoundingClientRect();
      const values = {
        "--tab-x": rect.left - bounds.left - track.clientLeft + track.scrollLeft,
        "--tab-y": rect.top - bounds.top - track.clientTop + track.scrollTop,
        "--tab-width": rect.width,
        "--tab-height": rect.height
      };
      Object.entries(values).forEach(([key, value]) => track.style.setProperty(key, value + "px"));
      if (!track.classList.contains("tab-slider-ready")) track.classList.add("tab-slider-ready");
    }
    function schedule() {
      if (frame === null) frame = requestAnimationFrame(update);
    }
    new MutationObserver(schedule).observe(track, {
      subtree: true, childList: true, attributes: true, attributeFilter: ["class"]
    });
    const resize = new ResizeObserver(schedule);
    resize.observe(track);
    track.querySelectorAll(".tab").forEach(tab => resize.observe(tab));
    schedule();
  }
  function adapt() {
    document.querySelectorAll("label[for][id]").forEach(label => {
      const control = document.getElementById(label.htmlFor);
      if (!control || !control.classList.contains("dash-dropdown")) return;
      const value = document.getElementById(control.id + "-value");
      const ids = label.id + (value ? " " + value.id : "");
      if (control.getAttribute("aria-labelledby") !== ids) {
        control.setAttribute("aria-labelledby", ids);
      }
    });
    document.querySelectorAll(".view-tab-list").forEach(installSlider);
  }
  new MutationObserver(adapt).observe(document.documentElement, {childList: true, subtree: true});
  document.addEventListener("DOMContentLoaded", adapt);
  adapt();
})();
