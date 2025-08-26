from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Coulisses Crew")


@app.get("/healthz")
async def healthz() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"}, status_code=200)
