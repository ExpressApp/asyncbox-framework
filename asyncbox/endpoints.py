"""Endpoints for communication with botx."""

from botx import Bot, IncomingMessage, Status
from botx.models.status import StatusRecipient
from fastapi import APIRouter, Depends
from starlette.status import HTTP_202_ACCEPTED

from asyncbox.dependencies.status_recipient import get_status_recipient


def get_router(bot: Bot) -> APIRouter:
    """Return router with bot-specific routes."""
    router = APIRouter()

    @router.post("/command", name="botx:command", status_code=HTTP_202_ACCEPTED)
    async def bot_command(message: IncomingMessage) -> None:  # noqa: WPS430
        """Receive commands from users. Max timeout - 5 seconds."""

        await bot.execute_command(message.dict())

    @router.get("/status", name="botx:status", response_model=Status)
    async def bot_status(  # noqa: WPS430
        recipient: StatusRecipient = Depends(get_status_recipient),
    ) -> Status:
        """Send commands with short descriptions."""
        return await bot.status()

    return router
