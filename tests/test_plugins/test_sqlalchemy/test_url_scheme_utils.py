from asyncbox.plugins.sqlalchemy.url_scheme_utils import make_url_async, make_url_sync

async_url = "postgresql+asyncpg://postgres:postgres@postgres/postgres"
sync_url = "postgresql://postgres:postgres@postgres/postgres"


def test_make_url_async():
    assert make_url_async(sync_url) == async_url


def test_make_url_sync():
    assert make_url_sync(async_url) == sync_url
