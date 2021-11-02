"""Dependencies for get bot instance."""

from botx import Bot

from asyncbox.application import get_application


def get_bot() -> Bot:
    """Dependencies for get bot instance."""
    return get_application().state.bot
