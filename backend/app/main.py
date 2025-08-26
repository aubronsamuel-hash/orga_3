from fastapi import FastAPI, Request
from .settings import settings
from .logging_conf import setup as setup_logging
from .api import router as api_router
from .api_auth import router as auth_router
import uuid

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.app_name)

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        rid = request.headers.get(settings.request_id_header) or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers[settings.request_id_header] = rid
        return response

    app.include_router(api_router)
    app.include_router(auth_router)
    return app


app = create_app()
