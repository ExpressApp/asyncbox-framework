import pytest


@pytest.mark.asyncio
async def test_healthcheck(redis_plugin):
    health_status = await redis_plugin.healthcheck()
    assert health_status.information["server_version"]
    assert health_status.healthy


@pytest.mark.asyncio
async def test_healthcheck_failed(redis_plugin_failed):
    health_status = await redis_plugin_failed.healthcheck()
    assert health_status.information["error"] == "Pool is closed"
    assert health_status.healthy == False
