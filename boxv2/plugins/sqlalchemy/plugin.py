"""Postgresql database plugin."""

from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from boxv2.plugin import BasePlugin, BasePluginSettings, HealtCheckData
from boxv2.plugins.sqlalchemy.url_scheme_utils import make_url_async


class Settings(BasePluginSettings):
    """Settings for Tortoise ORM plugin."""

    POSTGRES_DSN: str
    SQL_DEBUG: bool = False


class SQLAlchemyPlugin(BasePlugin):
    """Tortoise ORM plugin."""

    settings_class = Settings
    _session: Optional[AsyncSession]
    engine: Optional[AsyncEngine]

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.engine = create_async_engine(
            make_url_async(self.settings.POSTGRES_DSN), echo=self.settings.SQL_DEBUG
        )

        make_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self._session = make_session()

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""
        if self.session is not None:
            await self.session.close()

    async def healthcheck(self) -> HealtCheckData:
        """Healthcheck function."""
        try:
            async with self.session.begin():
                rows = await self.session.execute("select version()")
        except Exception as exc:
            return HealtCheckData(healthy=False, information={"error": str(exc)})
        return HealtCheckData(
            healthy=True,
            info={
                "server_version": rows.scalars().one(),
                "dsn": self.settings.POSTGRES_DSN,
            },
        )

    @property
    def session(self) -> AsyncSession:
        """Return an SQLAlchemy session instance."""
        if self._session is None:
            raise RuntimeError("Plugin not yet initialized!")
        return self._session
