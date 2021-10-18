"""Handlers for default bot commands and system events."""

from botx import Collector

collector = Collector()


@collector.default(include_in_status=False)
async def default_handler() -> None:
    """Run if command not found."""
