from __future__ import annotations

import os
import sys
from importlib.metadata import distribution
from pathlib import Path

from ragbench_lab.data.records import DataError


def shared_openmp_directory() -> Path | None:
    if sys.platform != "darwin":
        return None
    directory = Path(distribution("torch").locate_file("torch/lib")).resolve()
    if not (directory / "libomp.dylib").is_file():
        raise DataError("expected pinned PyTorch OpenMP runtime is missing")
    return directory


def require_native_environment() -> None:
    if os.environ.get("KMP_DUPLICATE_LIB_OK", "").casefold() in {"true", "1", "yes"}:
        raise DataError("unsafe duplicate OpenMP suppression is forbidden")
    directory = shared_openmp_directory()
    if (directory is not None
            and os.environ.get("DYLD_LIBRARY_PATH", "").split(":")[0] != str(directory)):
        raise DataError("macOS library API requires DYLD_LIBRARY_PATH to start with "
                        "the pinned torch/lib directory before Python starts; use the CLI")


def configure_cli_native_environment(arguments: list[str]) -> None:
    """Restart once before native imports: dyld reads its search path at process startup."""
    directory = shared_openmp_directory()
    if (directory is not None
            and os.environ.get("DYLD_LIBRARY_PATH", "").split(":")[0] != str(directory)):
        environment = dict(os.environ)
        previous = environment.get("DYLD_LIBRARY_PATH", "")
        environment["DYLD_LIBRARY_PATH"] = str(directory) + (":" + previous if previous else "")
        os.execve(sys.executable, [sys.executable, "-m", "ragbench_lab", *arguments], environment)
    require_native_environment()
