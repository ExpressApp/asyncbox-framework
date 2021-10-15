import pytest
from fastapi import FastAPI

from boxv2 import get_application
from boxv2.settings import BaseAppSettings
from boxv2.tests.fixtures import (
    bot,
    botx_client,
    builder,
    chat_created_data,
    credentials,
    environment,
    group_chat_id,
    http_client,
)

__all__ = [
    "builder",
    "bot",
    "chat_created_data",
    "group_chat_id",
    "credentials",
    "environment",
    "http_client",
    "botx_client",
]


class AppSettings(BaseAppSettings):
    PLUGINS = ["boxv2.plugins.debug"]


@pytest.fixture
def app() -> FastAPI:
    app = get_application(AppSettings())
    return app
