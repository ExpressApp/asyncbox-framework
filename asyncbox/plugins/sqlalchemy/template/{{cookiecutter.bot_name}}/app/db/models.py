"""Database models declarations."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base

# All models in project must be inherited from this class
Base = declarative_base()


# This is an example model. You may rewrite it a you need or write any other models.
# After it you may run `alembic revision --autogenerate` to generate migrations
# and `alembic upgrade head` to apply it on database.
# Migrations files will be stored at `app/db/migrations/versions`
class Record(Base):
    """Simple database model for example."""

    __tablename__ = "record"

    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: WPS125
    record_data = Column(String, nullable=False)

    def __repr__(self) -> str:
        """Show string representation of record."""
        return f"<{self.id}> {self.record_data}"


def get_session() -> AsyncSession:
    #  should not be imported before app initialization
    from app.main import app  # noqa: WPS433

    return app.state.sqlalchemy.session
