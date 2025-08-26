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

from .api_v1_projects import router as projects_router
from .api_v1_missions import router as missions_router
from .api_v1_assignments import router as assignments_router
from .api_v1_invitations import router as invitations_router
from .api_v1_users import router as users_router
from .api_v1_availability import router as availability_router
from .api_v1_conflicts import router as conflicts_router
from .api_v1_rates import router as rates_router
from .api_v1_orgs import router as orgs_router

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

    app.include_router(projects_router)
    app.include_router(missions_router)
    app.include_router(assignments_router)
    app.include_router(invitations_router)
    app.include_router(users_router)
    app.include_router(availability_router)
    app.include_router(conflicts_router)
    app.include_router(rates_router)
    app.include_router(orgs_router)
    return app


app = create_app()
