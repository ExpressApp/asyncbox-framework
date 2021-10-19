"""Prometheus client plugin."""

from typing import Any

from asyncbox.plugin import BasePlugin
from asyncbox.plugins.prometheus.endpoint import router
from asyncbox.plugins.prometheus.middleware import PrometheusMiddleware


class PrometheusPlugin(BasePlugin):
    """Prometheus plugin."""

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.bot.add_middleware(PrometheusMiddleware)
        self.application.include_router(router)

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
