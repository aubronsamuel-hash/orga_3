from pydantic import BaseModel
import os


class Settings(BaseModel):
    # SMTP / MailPit
    SMTP_HOST: str = os.environ.get("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "1025"))
    SMTP_USER: str | None = os.environ.get("SMTP_USER")
    SMTP_PASSWORD: str | None = os.environ.get("SMTP_PASSWORD")
    SMTP_FROM: str = os.environ.get("SMTP_FROM", "no-reply@example.test")

    # Telegram
    TELEGRAM_BOT_TOKEN: str | None = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_DEFAULT_CHAT_ID: str | None = os.environ.get("TELEGRAM_DEFAULT_CHAT_ID")

    # Links / signing
    INVITE_LINK_BASE_URL: str = os.environ.get(
        "INVITE_LINK_BASE_URL", "http://localhost:5173/public/invite"
    )
    SIGNING_SECRET: str = os.environ.get("SIGNING_SECRET", "dev-signing-secret-change-me")

    # Rate limit invitations
    INVITE_RATE_LIMIT_COUNT: int = int(
        os.environ.get("INVITE_RATE_LIMIT_COUNT", "5")
    )
    INVITE_RATE_LIMIT_WINDOW_SEC: int = int(
        os.environ.get("INVITE_RATE_LIMIT_WINDOW_SEC", "600")
    )

    # Redis URL (optional)
    REDIS_URL: str | None = os.environ.get("REDIS_URL")

    # Env
    ENV: str = os.environ.get("ENV", "dev")


settings = Settings()
