"""Sentry plugin."""

from typing import Any

import sentry_sdk  # type: ignore
from pydantic import AnyHttpUrl
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware  # type: ignore

from asyncbox.plugin import BasePlugin, BasePluginSettings
from asyncbox.plugins.sentry.middleware import SentryMiddleware


class Settings(BasePluginSettings):
    """Settings for sentry plugin."""

    SENTRY_DSN: AnyHttpUrl


class SentryPlugin(BasePlugin):
    """Sentry plugins."""

    settings_class = Settings

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        sentry_sdk.init(dsn=self.settings.SENTRY_DSN)
        self.application.add_middleware(SentryAsgiMiddleware)
        self.bot.add_middleware(SentryMiddleware)

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
