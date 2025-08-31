from __future__ import annotations

# Configuration centralisee, sans 'type: ignore' superflu.

# Fallback type-safe pour dotenv en environnement CI.

from os import PathLike
from typing import IO, Any, Callable, TYPE_CHECKING
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    # python-dotenv est optionnel; en CI on peut ne pas l installer.
    from dotenv import load_dotenv as _load_dotenv
except Exception:
    def _load_dotenv(
        dotenv_path: str | PathLike[str] | None = None,
        stream: IO[str] | None = None,
        verbose: bool = False,
        override: bool = False,
        interpolate: bool = True,
        encoding: str | None = None,
    ) -> bool:
        return False

load_dotenv: Callable[..., bool] = _load_dotenv

# Charge .env si present (dev), inoffensif sinon.

load_dotenv()


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRES_MIN: int = 15
    REFRESH_TOKEN_EXPIRES_MIN: int = 7 * 24 * 60

    model_config = SettingsConfigDict(
        env_file=None,
        env_prefix="",
        case_sensitive=True,
    )


if TYPE_CHECKING:
    settings = Settings(DATABASE_URL="")
else:
    settings = Settings()
