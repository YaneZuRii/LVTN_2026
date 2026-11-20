"""http://127.0.0.1:8080"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"

app = FastAPI(title="NNKH Web")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


if __name__ == "__main__":
    import uvicorn

    print("Mo trinh duyet: http://127.0.0.1:8080")
    print("Cho phep camera khi trinh duyet hoi.")
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")