from __future__ import annotations
import os
import uuid
from fastapi import FastAPI, Request
from .settings import settings
from .logging_conf import setup as setup_logging
from .api import router as api_router
from .api_auth import router as auth_router
from .api_rbac_demo import router as rbac_demo_router
from .db import set_database_url

def create_app() -> FastAPI:
    setup_logging()
    # Rebind DB a chaque creation d app (prend en compte DATABASE_URL courant)
    url = os.getenv("DATABASE_URL", "sqlite:///./backend/dev.db")
    set_database_url(url)
    os.environ.pop("DATABASE_URL", None)

    app = FastAPI(title=settings.app_name)

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        rid = request.headers.get(settings.request_id_header) or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers[settings.request_id_header] = rid
        return response

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_router)
    app.include_router(auth_router)
    app.include_router(rbac_demo_router)
    return app


# Instance module-level pour /healthz etc. (tests auth utilisent create_app())
app = create_app()
