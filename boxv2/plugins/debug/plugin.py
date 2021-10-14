"""Debug plugin."""

from typing import Any

from boxv2.plugin import BasePlugin
from boxv2.plugins.debug.commands import collector


class DebugPlugin(BasePlugin):
    """Debug plugin."""

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.bot.include_collector(collector)
