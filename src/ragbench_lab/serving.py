"""Explicit prompt-cache isolation with loaded weights; never operate on another model."""

from time import perf_counter

from ragbench_lab.data.records import DataError


def resident_model(generator) -> dict:
    rows = generator._json("/api/ps")["models"]
    settings = generator.settings
    if (len(rows) != 1 or rows[0].get("digest") != settings.model_digest
            or rows[0].get("context_length") != settings.context_window):
        raise DataError("expected exactly the pinned model resident at the configured context")
    return rows[0]


def isolate_request(generator) -> dict:
    """Unload KV/weights, preload weights without a prompt, then verify residency.

    This preparation is outside online timing but its wall cost must be budgeted.
    Reloading decoder state may still affect kernel warmth; record this limitation.
    """
    settings = generator.settings
    started = perf_counter()
    generator._json("/api/generate", {"model": settings.model, "stream": False,
                                      "keep_alive": 0})
    if generator._json("/api/ps")["models"]:
        raise DataError("dedicated backend did not unload; refusing unknown cache state")
    preloaded = generator._json("/api/generate", {
        "model": settings.model, "stream": False, "keep_alive": "10m",
        "options": {"temperature": 0, "seed": settings.seed,
                    "num_predict": settings.maximum_output_tokens,
                    "num_thread": settings.threads,
                    "num_ctx": settings.context_window},
    })
    if preloaded.get("response", ""):
        raise DataError("empty-prompt preload unexpectedly generated text")
    return {"policy": "unload_then_empty_prompt_preload_per_request",
            "seconds": perf_counter() - started, "preload": preloaded,
            "resident_before": resident_model(generator),
            "limitation": "weights preloaded; fresh decoder may have cold kernel state"}


def verify_uncached(result: dict) -> None:
    if (result.get("status") != "success"
            or type(result.get("cached_prompt_tokens")) is not int
            or result["cached_prompt_tokens"] != 0):
        raise DataError("zero cached prompt tokens required; missing counts are not proof")
