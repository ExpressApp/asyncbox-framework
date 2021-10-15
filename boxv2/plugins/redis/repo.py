"""Repository for work with redis."""

import asyncio
import hashlib
import pickle  # noqa: S403
from typing import Any, Callable, Hashable, Optional

import aioredis  # type: ignore


class RedisRepo:  # noqa: WPS214
    redis: aioredis.Redis
    dsn: str
    prefix: Optional[str]
    delimiter: str
    expire: Optional[int]

    def __init__(
        self, dsn: str, prefix: Optional[str] = None, expire: Optional[int] = None
    ) -> None:
        """Init repository object."""

        self.dsn = dsn
        self.prefix = prefix
        self.expire = expire
        self.delimiter = ":"

    @classmethod
    async def init(
        cls, dsn: str, prefix: Optional[str] = None, expire: Optional[int] = None
    ) -> "RedisRepo":
        """Init repository object."""
        repo = cls(dsn=dsn, prefix=prefix, expire=expire)
        repo.redis = await aioredis.create_redis_pool(repo.dsn)
        return repo

    async def close(self) -> None:
        """Close connection to redis."""

        self.redis.close()
        await self.redis.wait_closed()

    async def get(self, key: Hashable, default: Any = None) -> Any:
        """Get value from redis."""

        cached_data = await self.redis.get(self._key(key))
        if cached_data is None:
            return default
        return pickle.loads(cached_data)  # noqa: S301

    async def set(  # noqa: WPS125
        self, key: Hashable, value: Any, expire: Optional[int] = None  # noqa: WPS110
    ) -> None:
        """Set value into redis."""

        if expire is None:
            expire = self.expire
        dumped_value = pickle.dumps(value)
        await self.redis.set(self._key(key), dumped_value, expire=expire)

    async def delete(self, key: Hashable) -> None:
        """Remove value from redis."""

        await self.redis.delete(self._key(key))

    async def rget(self, key: Hashable, default: Any = None) -> Any:
        """Get value and remove it from redis."""

        value = await self.get(key, default)  # noqa: WPS110
        await self.delete(key)
        return value

    def __getitem__(self, item: Hashable) -> Any:  # noqa: WPS110
        """Get item via dictionary syntax."""
        return self._async2sync(self.get, item)

    def __setitem__(self, key: Hashable, value: Any) -> Any:  # noqa: WPS110
        """Set item via dictionary syntax."""
        return self._async2sync(self.set, key, value)

    def __delitem__(self, item: Hashable) -> Any:  # noqa: WPS110,WPS603
        """Delete item via dictionary syntax."""
        return self._async2sync(self.delete, item)

    def _key(self, arg: Hashable) -> str:
        if self.prefix is not None:
            prefix = self.prefix + self.delimiter
        else:
            prefix = ""

        hash_bytes = str(hash(arg)).encode()
        return prefix + hashlib.sha224(hash_bytes).hexdigest()

    def _async2sync(self, function: Callable, *args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return loop.create_task(function(*args, **kwargs))
