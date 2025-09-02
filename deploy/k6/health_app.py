from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Health App (SAFE_MODE)")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/healthz")
def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})
