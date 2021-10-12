"""Plugin for check that message was send from bot's cts."""

from typing import Any

from botx import DependencyFailure, Depends, Message

from boxv2.plugin import BasePlugin, BasePluginSettings
from boxv2.utils.import_utils import import_object


class CheckExtCts:

    text = (
        "Bot have been registered on another CTS.\n"
        "To keep working with the bot text to it from your CTS.\n"
        "You can find it in via contacts search."
    )

    async def __call__(self, message: Message) -> None:  # noqa: WPS610
        """Check that user write from bot's cts."""
        if message.is_system_event:
            return

        if not (message.user.ad_domain and message.ad_login):
            await message.bot.answer_message(self.text, message)
            raise DependencyFailure


class Settings(BasePluginSettings):

    FORBID_EXT_CTS_TEXT: str = (
        "app.resources.strings:BOT_CANT_COMMUNICATE_WITH_OTHERS_CTS"
    )


class Plugin(BasePlugin):
    """Forbid external CTS plugin."""

    settings_class = Settings
    function = CheckExtCts()
    dependencies = [Depends(function)]

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        try:
            text = import_object(self.settings.FORBID_EXT_CTS_TEXT)
        except (ImportError, AttributeError):
            text = None
        if text is not None:
            self.function.text = text
