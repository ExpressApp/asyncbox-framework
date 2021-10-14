"""Redis plugin."""

from typing import Any, Optional

from pydantic import RedisDsn

from boxv2.plugin import BasePlugin, BasePluginSettings
from boxv2.plugins.redis.repo import RedisRepo


class Settings(BasePluginSettings):
    REDIS_DSN: RedisDsn
    REDIS_PREFIX: Optional[str]
    REDIS_EXPIRE: Optional[int]


class RedisPlugin(BasePlugin):
    """Redis plugin."""

    redis_repo: RedisRepo
    settings_class = Settings

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        prefix = self.settings.REDIS_PREFIX or self.settings.NAME
        expire = self.settings.REDIS_EXPIRE or 0
        self.redis_repo = await RedisRepo.init(
            dsn=str(self.settings.REDIS_DSN), prefix=prefix, expire=expire
        )
        self.application.state.redis = self.redis_repo

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
        await self.redis_repo.close()
