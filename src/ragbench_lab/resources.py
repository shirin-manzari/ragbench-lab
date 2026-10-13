"""Sample resident process memory for the caller and a dedicated model-server tree."""

import os
import subprocess
from threading import Event, Thread
from time import perf_counter


def tree_memory(rows: list[tuple[int, int, int]], roots: set[int]) -> dict:
    selected = set(roots)
    while True:
        children = {pid for pid, parent, _ in rows if parent in selected}
        if children <= selected:
            break
        selected.update(children)
    present = [(pid, rss) for pid, _, rss in rows if pid in selected]
    return {"rss_bytes": sum(rss for _, rss in present),
            "processes": [{"pid": pid, "rss_bytes": rss} for pid, rss in present]}


class MemorySampler:
    def __init__(self, server_pid: int, interval: float = .5):
        self.roots = {os.getpid(), server_pid}
        self.interval, self.samples, self.errors = interval, [], []
        self.stop = Event()

    def _sample(self):
        while not self.stop.is_set():
            try:
                result = subprocess.run(["ps", "-axo", "pid=,ppid=,rss="],
                                        capture_output=True, text=True, timeout=5, check=True)
                rows = [tuple(int(value) for value in line.split())
                        for line in result.stdout.splitlines()]
                rows = [(pid, parent, rss * 1024) for pid, parent, rss in rows]
                self.samples.append({"monotonic": perf_counter(),
                                     **tree_memory(rows, self.roots)})
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                self.errors.append(str(error))
            self.stop.wait(self.interval)

    def __enter__(self):
        self.thread = Thread(target=self._sample, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.stop.set()
        self.thread.join(timeout=6)

    def summary(self):
        return {"method": "sampled summed RSS; caller and dedicated server descendants",
                "peak_rss_bytes": max((r["rss_bytes"] for r in self.samples), default=None),
                "sample_count": len(self.samples), "interval_seconds": self.interval,
                "errors": self.errors, "samples": self.samples,
                "device_memory": "record API size_vram separately; unified memory may overlap RSS"}
