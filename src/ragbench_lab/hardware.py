"""Small, dependency-free hardware and local backend inventory."""

from __future__ import annotations

import ctypes
import json
import os
import platform
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class _MemoryStatus(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_ulong),
        ("memory_load", ctypes.c_ulong),
        ("total_physical", ctypes.c_ulonglong),
        ("available_physical", ctypes.c_ulonglong),
        ("total_page_file", ctypes.c_ulonglong),
        ("available_page_file", ctypes.c_ulonglong),
        ("total_virtual", ctypes.c_ulonglong),
        ("available_virtual", ctypes.c_ulonglong),
        ("available_extended_virtual", ctypes.c_ulonglong),
    ]


def _ram_bytes() -> int | None:
    if platform.system() == "Darwin":
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5, check=False
        )
        return int(result.stdout.strip()) if result.returncode == 0 else None
    if os.name != "nt":
        return None
    status = _MemoryStatus()
    status.length = ctypes.sizeof(status)
    return (
        status.total_physical
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
        else None
    )


def _nvidia() -> list[dict[str, Any]]:
    executable = shutil.which("nvidia-smi")
    if not executable:
        return []
    result = subprocess.run(
        [
            executable,
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if result.returncode != 0:
        return []
    devices = []
    for line in result.stdout.splitlines():
        name, memory_mib, driver = (part.strip() for part in line.split(",", maxsplit=2))
        devices.append({"name": name, "memory_mib": int(memory_mib), "driver": driver})
    return devices


def _ollama() -> dict[str, Any]:
    executable = shutil.which("ollama")
    api_version = None
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=1) as response:
            api_version = json.load(response).get("version")
    except (OSError, ValueError, urllib.error.URLError):
        pass
    return {
        "name": "ollama",
        "executable_available": executable is not None,
        "api_available": api_version is not None,
        "version": api_version,
    }


def collect_inventory(workspace: str | Path = ".") -> dict[str, Any]:
    usage = shutil.disk_usage(Path(workspace).resolve())
    return {
        "schema_version": 1,
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
        },
        "python": platform.python_version(),
        "cpu": {"processor": platform.processor(), "logical_cores": os.cpu_count()},
        "memory": {"total_bytes": _ram_bytes()},
        "gpu": _nvidia(),
        "workspace_disk": {"total_bytes": usage.total, "free_bytes": usage.free},
        "serving_backend": _ollama(),
    }
