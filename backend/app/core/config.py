from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = Field(default="dev")
    DATABASE_URL: str = Field(default="sqlite:///./dev.db")
    SECRET_KEY: str = Field(default="changeme")
    ACCESS_TOKEN_EXPIRES_MIN: int = Field(default=15)
    REFRESH_TOKEN_EXPIRES_MIN: int = Field(default=7 * 24 * 60)
    INVITES_SECRET: str = Field(default="change-me")
    INVITES_TTL_SECONDS: int = Field(default=604_800)
    INVITE_TOKEN_SECRET: str = Field(default="dev-please-change")
    INVITE_TOKEN_TTL_MIN: int = Field(default=7 * 24 * 60)
    PUBLIC_BASE_URL: str = Field(default="http://localhost:5173")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


# Convenience instance used by modules importing settings
settings = get_settings()
