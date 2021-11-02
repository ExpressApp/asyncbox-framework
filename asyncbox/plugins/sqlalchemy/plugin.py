"""Postgresql database plugin."""

from typing import Any, Optional, Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from asyncbox.plugin import BasePlugin, BasePluginSettings, HealtCheckData
from asyncbox.plugins.sqlalchemy.url_scheme_utils import make_url_async


class Settings(BasePluginSettings):
    """Settings for SQLAlchemy ORM plugin."""

    POSTGRES_DSN: str
    SQL_DEBUG: bool = False


class SQLAlchemyPlugin(BasePlugin):
    """SQLAlchemy ORM plugin."""

    settings_class = Settings
    make_session: Optional[Callable]
    engine: Optional[AsyncEngine]

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""
        self.engine = create_async_engine(
            make_url_async(self.settings.POSTGRES_DSN), echo=self.settings.SQL_DEBUG
        )

        self.make_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def healthcheck(self) -> HealtCheckData:
        """Healthcheck function."""
        try:
            session = self.make_session()
            async with session.begin():
                rows = await session.execute("select version()")  # type: ignore
        except Exception as exc:
            return HealtCheckData(healthy=False, information={"error": str(exc)})
        return HealtCheckData(
            healthy=True,
            information={
                "server_version": rows.scalars().one(),
                "dsn": self.settings.POSTGRES_DSN,
            },
        )
