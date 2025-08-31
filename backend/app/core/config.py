from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

# Chargement .env **sans** import statique (evite les erreurs mypy si python-dotenv n'est pas installe)
_load = None
try:  # importlib renvoie Any, mypy ne tente pas de resoudre le paquet
    _mod = importlib.import_module("dotenv")
    _load = getattr(_mod, "load_dotenv", None)
except Exception:
    _load = None

if callable(_load):
    try:
        _load()
    except Exception:
        pass  # best-effort : si ca echoue en CI, on continue


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRES_MIN: int = 15
    REFRESH_TOKEN_EXPIRES_MIN: int = 7 * 24 * 60
    INVITES_SECRET: str = "change-me"
    INVITES_TTL_SECONDS: int = 604800

    model_config = SettingsConfigDict(
        env_file=None,
        env_prefix="",
        case_sensitive=True,
    )


if TYPE_CHECKING:
    settings = Settings(DATABASE_URL="")
else:
    settings = Settings()
