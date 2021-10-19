"""Handlers for default bot commands and system events."""

from os import environ

from botx import Bot, Collector, Message

collector = Collector()


@collector.hidden(command="/_debug:commit_sha")
async def commit_sha(message: Message, bot: Bot) -> None:
    """Show git commit SHA."""
    await bot.answer_message(str(environ.get("COMMIT_SHA")), message)


@collector.hidden(command="/_debug:plugins")
async def plugins(message: Message, bot: Bot) -> None:
    """Show git commit SHA."""
    names_and_status = [
        (plugin.get_name(), (await plugin.healthcheck()).json(indent=2))
        for plugin in bot.state.plugins
    ]
    template = "**{name}**\n ```json\n{status}\n```"
    text = "\n\n".join(
        [template.format(name=name, status=status) for name, status in names_and_status]
    )
    await bot.answer_message(text, message)
