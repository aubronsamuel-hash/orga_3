import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "CoulissesCrew")
    env: str = os.getenv("ENV", "dev")
    tz: str = os.getenv("TZ", "UTC")
    host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    port: int = int(os.getenv("BACKEND_PORT", "8000"))
    request_id_header: str = os.getenv("REQUEST_ID_HEADER", "X-Request-ID")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
