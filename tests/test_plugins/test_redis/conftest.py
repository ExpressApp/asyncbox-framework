from os import environ

import pytest

from boxv2.plugins.redis.plugin import RedisPlugin as Plugin, Settings

REDIS_DSN = environ["TEST_REDIS_DSN"]


class StateMock:
    redis = None


class AppMock:
    state = StateMock()


@pytest.fixture()
async def redis():
    app = AppMock()
    settings = Settings(REDIS_DSN=REDIS_DSN, REDIS_PREFIX="boxv2_test")
    plugin = Plugin(settings, app, None)
    await plugin.on_startup()
    yield plugin.redis_repo
    await plugin.on_shutdown()
