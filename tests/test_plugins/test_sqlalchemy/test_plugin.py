import pytest


@pytest.mark.asyncio
async def test_healthcheck(sqlalchemy_plugin):
    health_status = await sqlalchemy_plugin.healthcheck()
    assert health_status.information["server_version"].startswith("PostgreSQL")
    assert health_status.healthy


@pytest.mark.asyncio
async def test_healthcheck_failed(sqlalchemy_plugin_failed):
    health_status = await sqlalchemy_plugin_failed.healthcheck()
    assert health_status.healthy is False


@pytest.mark.asyncio
async def test_uninitialized(sqlalchemy_plugin_uninitialized):
    with pytest.raises(RuntimeError):
        sqlalchemy_plugin_uninitialized.make_session()
