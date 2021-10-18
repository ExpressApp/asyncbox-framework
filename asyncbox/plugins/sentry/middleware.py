"""Sentry middleware."""

from botx import Message
from botx.concurrency import callable_to_coroutine
from botx.middlewares.base import BaseMiddleware
from botx.typing import Executor
from loguru import logger
from sentry_sdk import capture_exception  # type: ignore
from sentry_sdk import push_scope


class SentryMiddleware(BaseMiddleware):
    async def dispatch(self, message: Message, call_next: Executor) -> None:
        """Send exception to sentry and log traceback."""
        with push_scope() as scope:
            msg = message.incoming_message.copy()
            scope.set_user({"user_huid": msg.user.user_huid})

            if msg.file:
                scope.set_extra("file_in_message", value=True)

                msg.file = None  # noqa: WPS110

            scope.set_extra("command", msg.command.command)
            scope.set_extra("message", msg.dict())
            try:
                await callable_to_coroutine(call_next, message)
            except Exception as exc:

                capture_exception(exc)

                logger.exception("catch exception that was sent to Sentry")
