from os import environ

import pytest
from asyncpg import connect
from fastapi import FastAPI
from tortoise import Tortoise

from boxv2 import get_application
from boxv2.settings import BaseAppSettings
from boxv2.tests.fixtures import (
    bot,
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
]

POSTGRES_DSN = environ["TEST_POSTGRES_DSN"]


async def clean_db():
    conn = await connect(dsn=POSTGRES_DSN)
    await conn.fetch("DROP SCHEMA IF EXISTS public CASCADE;")
    await conn.fetch("CREATE SCHEMA public;")
    await conn.close()


@pytest.fixture(scope="function")
async def db_schema():
    await clean_db()
    await Tortoise.init(
        db_url=POSTGRES_DSN,
        modules={"botx": ["boxv2.plugins.tortoise.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    await clean_db()


class AppSettings(BaseAppSettings):
    # do not include plugin here as DB initialization replaced with db_schema()
    # fixture to generate schemas
    PLUGINS = []


@pytest.fixture
def app(db_schema) -> FastAPI:
    return get_application(AppSettings())
