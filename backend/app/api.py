from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1")

@router.get("/ping")
def ping(request: Request):
    rid = request.headers.get("X-Request-ID", "")
    return {"status":"ok","request_id":rid}
