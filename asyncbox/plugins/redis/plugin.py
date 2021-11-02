"""Redis plugin."""

from typing import Any, Optional

from pydantic import RedisDsn

from asyncbox.plugin import BasePlugin, BasePluginSettings, HealtCheckData
from asyncbox.plugins.redis.repo import RedisRepo


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
        prefix = self._get_prefix()
        expire = self.settings.REDIS_EXPIRE or 0
        self.redis_repo = await RedisRepo.init(
            dsn=str(self.settings.REDIS_DSN), prefix=prefix, expire=expire
        )
        self.application.state.redis = self.redis_repo

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
        await self.redis_repo.close()

    async def healthcheck(self) -> HealtCheckData:
        """Healthcheck."""
        try:
            information = await self.redis_repo.redis.info()
        except Exception as exc:
            return HealtCheckData(healthy=False, information={"error": str(exc)})
        return HealtCheckData(
            healthy=True,
            information={
                "server_version": information["server"]["redis_version"],
                "dsn": self.settings.REDIS_DSN,
                "prefix": self._get_prefix(),
            },
        )

    def _get_prefix(self) -> str:
        return self.settings.REDIS_PREFIX or self.settings.NAME
