"""Database models declarations."""

from typing import Any, Generic, List, TypeVar

from sqlalchemy import Column, Integer, String, insert, update as _update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select

T = TypeVar("T")  # noqa: WPS111

Base = declarative_base()


# This is an example of asynchronous usage of SQLAlchemy.
# You may rewrite this class as need for your models.
class CRUDMixin(Generic[T]):
    """Mixin for CRUD operations for models."""

    id: int  # noqa: WPS125

    @classmethod
    async def create(cls, **kwargs: Any) -> None:
        """Create object."""
        query = insert(cls).values(**kwargs)
        session = get_session()
        async with session.begin():
            await session.execute(query)

    @classmethod
    async def update(cls, id: int, **kwargs: Any) -> None:  # noqa: WPS125
        """Update object by id."""
        query = (
            _update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        session = get_session()
        async with session.begin():
            await session.execute(query)

    @classmethod
    async def get(cls, id: int) -> T:  # noqa: WPS125
        """Get object by id."""
        query = select(cls).where(cls.id == id)
        session = get_session()
        async with session.begin():
            rows = await session.execute(query)
        return rows.scalars().one()

    @classmethod
    async def all(cls) -> List[T]:  # noqa: WPS125
        """Get all objects."""
        query = select(cls)
        session = get_session()
        async with session.begin():
            rows = await session.execute(query)
        return rows.scalars().all()


# This is an example model. You may rewrite it a you need or write any other models.
# After it you may run `alembic revision --autogenerate` to generate migrations
# and `alembic upgrade head` to apply it on database.
# Migrations files will be stored at `app/db/migrations/versions`
class Record(Base, CRUDMixin):
    """Simple database model for example."""

    __tablename__ = "record"

    id: int = Column(Integer, primary_key=True, autoincrement=True)  # noqa: WPS125
    record_data: str = Column(String)

    def __repr__(self) -> str:
        """Show string representation of record."""
        return self.record_data


def get_session() -> AsyncSession:
    from app.main import app  # should not be imported before app initialization

    return app.state.sqlalchemy.session
