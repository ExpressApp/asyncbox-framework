"""Debug plugin."""

from typing import Any

from asyncbox.plugin import BasePlugin
from asyncbox.plugins.debug.commands import collector


class DebugPlugin(BasePlugin):
    """Debug plugin."""

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.bot.include_collector(collector)
