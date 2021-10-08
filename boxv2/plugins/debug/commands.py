"""Handlers for default bot commands and system events."""

from os import environ

from botx import Bot, Collector, Message

collector = Collector()


@collector.hidden(command="/_debug:commit_sha")
async def commit_sha(message: Message, bot: Bot) -> None:
    """Show git commit SHA."""
    await bot.answer_message(environ.get("COMMIT_SHA"), message)
