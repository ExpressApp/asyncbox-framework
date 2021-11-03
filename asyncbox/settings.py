"""Default settings for bot application."""

from typing import Any, Optional

from botx import BotXCredentials
from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator


class BaseAppSettings(BaseSettings):
    """Main settings for application."""

    class Config:  # noqa: WPS431
        env_file = ".env"
        json_loads = lambda x: x  # noqa: E731,WPS111

    NAME = "asyncbox"

    PLUGINS: list[str] = []
    COLLECTORS: list[str] = []
    DEFAULT_ROUTER = "asyncbox.endpoints:router"

    # base kwargs
    DEBUG: bool = False
    BOT_CREDENTIALS: list[BotXCredentials]

    # PostgreSQL settings
    POSTGRES_DSN: Optional[PostgresDsn]
    SQL_DEBUG: bool = False

    # Redis settings
    REDIS_DSN: Optional[RedisDsn]
    REDIS_PREFIX: Optional[str]
    REDIS_EXPIRE: Optional[int]

    # metrics
    SENTRY_DSN: Optional[str] = None

    @validator("BOT_CREDENTIALS", pre=True)
    @classmethod
    def parse_bot_credentials(cls, raw_credentials: Any) -> list[BotXCredentials]:
        """Parse bot credentials separated by comma.

        Each entry must be separated by "@".
        """

        if not raw_credentials:
            raise ValueError("`BOT_CREDENTIALS` can't be empty")
        return [
            _build_credentials_from_string(credentials_str)
            for credentials_str in raw_credentials.replace(",", " ").split()
        ]


def _build_credentials_from_string(credentials_str: str) -> BotXCredentials:
    assert (  # noqa: S101
        credentials_str.count("@") == 2
    ), "Have you forgot to add `bot_id`?"

    host, secret_key, bot_id = [
        str_value.strip() for str_value in credentials_str.split("@")
    ]
    return BotXCredentials(host=host, secret_key=secret_key, bot_id=bot_id)
