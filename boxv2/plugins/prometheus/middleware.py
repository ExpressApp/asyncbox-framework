"""Prometheus client middleware."""

from botx import Message
from botx.concurrency import callable_to_coroutine
from botx.middlewares.base import BaseMiddleware
from botx.typing import Executor
from prometheus_client import Counter  # type: ignore

COMMANDS = Counter(
    "botx_commands_total",
    "Total count of commands by user, command.",
    ["command", "user_huid"],
)
BOT_USERS = Counter(
    "botx_users_total",
    "Total count of bot users by user_huid and cts",
    ["user_huid", "cts"],
)
COMMAND_IN_CHATS = Counter(
    "botx_commands_in_chats_total",
    "Total count of commands in different chats by command and chat type",
    ["command", "chat_type"],
)


class PrometheusMiddleware(BaseMiddleware):
    async def dispatch(self, message: Message, call_next: Executor) -> None:
        """Execute middleware logic.

        Arguments:
            message: incoming message.
            call_next: next executor in middleware chain.
        """
        COMMANDS.labels(
            command=message.command.command,
            user_huid=str(message.user_huid),
        ).inc()
        COMMAND_IN_CHATS.labels(
            command=message.command.command,
            chat_type=message.chat_type,
        ).inc()
        BOT_USERS.labels(user_huid=str(message.user_huid), cts=message.host).inc()
        await callable_to_coroutine(call_next, message)
