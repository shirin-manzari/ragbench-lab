import os
from pathlib import Path

from ragbench_lab.dashboard import create_app

hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
app = create_app(
    Path(__file__).resolve().parent / "deployment/dashboard",
    allowed_hosts=frozenset({hostname}) if hostname else frozenset(),
)
server = app.server


@server.get("/healthz")
def healthz():
    return {"status": "ok"}
