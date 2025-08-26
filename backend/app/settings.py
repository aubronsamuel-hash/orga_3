from __future__ import annotations

from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "CoulissesCrew")
    env: str = os.getenv("ENV", "dev")
    tz: str = os.getenv("TZ", "UTC")
    host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    port: int = int(os.getenv("BACKEND_PORT", "8000"))
    request_id_header: str = os.getenv("REQUEST_ID_HEADER", "X-Request-ID")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    # Auth/JWT
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-not-for-prod")
    jwt_algorithm: str = os.getenv("JWT_ALG", "HS256")
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
    refresh_token_days: int = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))


settings = Settings()
