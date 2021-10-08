import pytest


@pytest.mark.asyncio
async def test_repo(redis):
    await redis.set("one", 1)
    assert await redis.get("one") == 1
    assert await redis.rget("one") == 1
    assert await redis.rget("one") is None

    redis["two"] = 2
    assert await redis["two"] == 2
    del redis["two"]
    assert await redis["two"] is None
