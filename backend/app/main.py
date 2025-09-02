from __future__ import annotations

import logging
import os
import uuid
from typing import Any, Dict

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text

from .settings import settings
from .logging_setup import configure_logging
from .observability import setup_metrics
from .db import set_database_url


logger = logging.getLogger("app.main")


SAFE_MODE = os.environ.get("SAFE_MODE", "0") == "1"


# Middleware request_id + logs JSON
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get(settings.request_id_header) or uuid.uuid4().hex
    request.state.request_id = req_id
    request.state.trace_id = req_id
    logger = logging.getLogger("app.request")
    response: Response
    try:
        response = await call_next(request)
    finally:  # noqa: WPS100
        pass
    try:
        duration_ms = getattr(request.state, "_duration_ms", None)
    except Exception:  # pragma: no cover - defensive
        duration_ms = None
    logger.info(
        "http_request",
        extra={
            "request_id": req_id,
            "trace_id": req_id,
            "method": request.method,
            "path": request.url.path,
            "status": getattr(response, "status_code", None),
            "duration_ms": duration_ms,
        },
    )
    response.headers[settings.request_id_header] = req_id
    return response


# Middleware pour mesurer la duree en ms (pour logs)
async def add_timer(request: Request, call_next):
    import time

    start = time.perf_counter()
    response = await call_next(request)
    request.state._duration_ms = int((time.perf_counter() - start) * 1000)
    return response


def _readiness_check() -> Dict[str, Any]:
    url = os.getenv("DATABASE_URL") or os.getenv("DB_URL")
    if not url:
        return {"db": "missing-url", "ok": False}
    try:
        eng = create_engine(url, future=True)
        with eng.connect() as c:
            c.execute(text("SELECT 1"))
        return {"db": "ok", "ok": True}
    except Exception as e:  # pragma: no cover (rare)
        return {"db": f"error:{type(e).__name__}", "ok": False}


def create_app() -> FastAPI:
    configure_logging()
    # Rebind DB a chaque creation d app (prend en compte DATABASE_URL courant)
    url = os.getenv("DATABASE_URL", "sqlite:///./backend/dev.db")
    set_database_url(url)
    os.environ.pop("DATABASE_URL", None)

    app = FastAPI(title=settings.app_name)

    # Observabilite
    app.middleware("http")(add_timer)
    app.middleware("http")(add_request_id)
    metrics_enabled = os.getenv("METRICS_ENABLED", "true").lower() == "true"
    setup_metrics(app, enabled=metrics_enabled)

    @app.get("/healthz", tags=["meta"])
    @app.get("/health", tags=["meta"])
    def healthz() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/livez")
    def livez() -> Dict[str, str]:
        return {"status": "live"}

    @app.get("/readyz")
    def readyz() -> JSONResponse:
        status = _readiness_check()
        code = 200 if status.get("ok") else 503
        return JSONResponse({"status": status}, status_code=code)

    if not SAFE_MODE:
        try:
            from .api import router as api_router
            from .api_auth import router as auth_router
            from .api_rbac_demo import router as rbac_demo_router
            from .api_v1_assignments import router as assignments_router
            from .api_v1_availability import router as availability_router
            from .api.v1 import conflicts as conflicts_api
            from .api_v1_invitations import router as invitations_router
            from .api_v1_missions import router as missions_router
            from .api_v1_orgs import router as orgs_router
            from .api_v1_projects import router as projects_router
            from .api_v1_rates import router as rates_router
            from .api_v1_users import router as users_router
            from .api.v1 import availabilities as avail_api
            from .api.v1 import users_profile as users_profile_api
            from .api.v1 import reports as reports_api
            from .api.v1 import exports as exports_api
            from .routers import notifications_router

            app.include_router(api_router)
            app.include_router(auth_router)
            app.include_router(rbac_demo_router)
            app.include_router(projects_router)
            app.include_router(missions_router)
            app.include_router(assignments_router)
            # Invitations (create, verify, accept)
            app.include_router(invitations_router)
            app.include_router(users_router)
            app.include_router(
                avail_api.router,
                prefix="/api/v1/availabilities",
                tags=["availabilities"],
            )
            app.include_router(
                users_profile_api.router, prefix="/api/v1/users", tags=["users"]
            )
            app.include_router(availability_router)
            app.include_router(conflicts_api.router)
            app.include_router(reports_api.router)
            app.include_router(exports_api.router)
            app.include_router(rates_router)
            app.include_router(orgs_router)
            app.include_router(notifications_router)
            logger.info("Routes API chargees (mode complet).")
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(
                "Chargement des routes en echec (mode degrade). Raison: %s", exc
            )
    else:
        logger.info("Mode SAFE actif : routes API non chargees.")

    return app


app = create_app()

if __name__ == "__main__":  # pragma: no cover - manual execution
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        reload=False,
    )
