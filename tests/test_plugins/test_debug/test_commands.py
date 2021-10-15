from os import environ

import pytest
from botx import Bot
from botx.testing import MessageBuilder, TestClient as BotXClient


@pytest.mark.asyncio
async def test_debug_command(
    builder: MessageBuilder,
    bot: Bot,
    botx_client: BotXClient,
):
    environ["COMMIT_SHA"] = "test_commit_sha"
    builder.body = "/_debug:commit_sha"
    await botx_client.send_command(builder.message)

    body = botx_client.notifications[0].result.body
    assert body == "test_commit_sha"
