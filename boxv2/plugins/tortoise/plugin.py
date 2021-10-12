"""Postgresql database plugin."""

from typing import Any, Dict, List, Optional

from pydantic import PostgresDsn
from tortoise import Tortoise

from boxv2.plugin import BasePlugin, BasePluginSettings
from boxv2.plugins.tortoise.dependencies import auto_models_update


class Settings(BasePluginSettings):
    """Settings for Tortoise ORM plugin."""

    POSTGRES_DSN: PostgresDsn
    EXTRA_MODELS: Optional[Dict[str, List[str]]] = {}  # noqa: WPS234
    SQL_DEBUG: bool = False


class Plugin(BasePlugin):
    """Tortoise ORM plugin."""

    settings_class = Settings
    dependencies = [auto_models_update]

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        extra_models = self.settings.EXTRA_MODELS or {}
        await Tortoise.init(
            db_url=str(self.settings.POSTGRES_DSN),
            modules={"botx": ["boxv2.plugins.tortoise.models"], **extra_models},
        )

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
        await Tortoise.close_connections()
