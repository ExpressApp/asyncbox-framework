import re

import pytest
from botx import Bot
from botx.testing import MessageBuilder, TestClient as BotXClient
from fastapi import FastAPI
from httpx import AsyncClient, codes

command_regexp = r'botx_commands_total{command="/test",user_huid="[0-9a-f\-]+"}'


@pytest.mark.asyncio
async def test_prometheus_endpoint(
    builder: MessageBuilder,
    botx_client: BotXClient,
    app: FastAPI,
    http_client: AsyncClient,
    bot: Bot,
):

    # check there is no information about command in metrics
    url = app.url_path_for("prometheus:metrics")
    response = await http_client.get(url)
    assert response.status_code == codes.OK
    assert re.search(command_regexp, response.text) is None

    # send command
    builder.body = "/test"
    await botx_client.send_command(builder.message)

    # check there is information about command in metrics
    response = await http_client.get(url)
    assert response.status_code == codes.OK
    assert re.search(command_regexp, response.text)
