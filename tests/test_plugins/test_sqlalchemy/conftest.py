from os import environ

import pytest

from asyncbox.plugins.sqlalchemy.plugin import Settings, SQLAlchemyPlugin as Plugin

POSTGRES_DSN = environ["POSTGRES_DSN"]


class StateMock:
    sqlalchemy = None


class AppMock:
    state = StateMock()


@pytest.fixture()
async def sqlalchemy_plugin():
    app = AppMock()
    settings = Settings(POSTGRES_DSN=POSTGRES_DSN)
    plugin = Plugin(settings, app, None)
    await plugin.on_startup()
    yield plugin
    await plugin.on_shutdown()


@pytest.fixture()
async def sqlalchemy_plugin_failed():
    app = AppMock()
    settings = Settings(POSTGRES_DSN="postgresql://user:pass@non_existant_server/base")
    plugin = Plugin(settings, app, None)
    await plugin.on_startup()
    yield plugin
    await plugin.on_shutdown()


@pytest.fixture()
async def sqlalchemy_plugin_uninitialized():
    app = AppMock()
    settings = Settings(POSTGRES_DSN=POSTGRES_DSN)
    plugin = Plugin(settings, app, None)
    yield plugin
