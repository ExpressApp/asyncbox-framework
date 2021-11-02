"""Endpoints for communication with botx."""

from botx import Bot, IncomingMessage, Status
from botx.models.status import StatusRecipient
from fastapi import APIRouter, Depends
from starlette.status import HTTP_202_ACCEPTED

from asyncbox.dependencies.bot import get_bot
from asyncbox.dependencies.status_recipient import get_status_recipient

router = APIRouter()


@router.post("/command", name="botx:command", status_code=HTTP_202_ACCEPTED)
async def bot_command(
    message: IncomingMessage, bot: Bot = Depends(get_bot)
) -> None:  # noqa: WPS430
    """Receive commands from users. Max timeout - 5 seconds."""

    await bot.execute_command(message.dict())


@router.get("/status", name="botx:status", response_model=Status)
async def bot_status(  # noqa: WPS430
    recipient: StatusRecipient = Depends(get_status_recipient),
    bot: Bot = Depends(get_bot),
) -> Status:
    """Send commands with short descriptions."""
    return await bot.status()
