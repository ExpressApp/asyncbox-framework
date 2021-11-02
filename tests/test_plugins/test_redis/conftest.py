from os import environ

import pytest

from asyncbox.plugins.redis.plugin import RedisPlugin as Plugin, Settings

REDIS_DSN = environ["REDIS_DSN"]


class StateMock:
    redis = None


class AppMock:
    state = StateMock()


@pytest.fixture()
async def redis_plugin():
    app = AppMock()
    settings = Settings(REDIS_DSN=REDIS_DSN, REDIS_PREFIX="asyncbox_test")
    plugin = Plugin(settings, app, None)
    await plugin.on_startup()
    yield plugin
    await plugin.on_shutdown()


@pytest.fixture()
async def redis_plugin_failed():
    app = AppMock()
    settings = Settings(REDIS_DSN=REDIS_DSN, REDIS_PREFIX="asyncbox_test")
    plugin = Plugin(settings, app, None)
    await plugin.on_startup()
    await plugin.redis_repo.close()
    yield plugin
    await plugin.on_shutdown()
