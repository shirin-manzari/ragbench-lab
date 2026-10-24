from pathlib import Path

from ragbench_lab.dashboard import create_app

app = create_app(Path(__file__).resolve().parent / "deployment/dashboard")
server = app.server


@server.get("/healthz")
def healthz():
    return {"status": "ok"}
