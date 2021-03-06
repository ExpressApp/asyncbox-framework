import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# init config
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from asyncbox.application import get_app_settings  # isort:skip
from asyncbox.plugins.sqlalchemy.url_scheme_utils import make_url_sync  # isort:skip
from app.db.models import Base  # isort:skip

postgres_dsn = make_url_sync(get_app_settings().POSTGRES_DSN)
context_config = context.config
fileConfig(context_config.config_file_name)
target_metadata = Base.metadata
context_config.set_main_option("sqlalchemy.url", postgres_dsn)


def run_migrations_online() -> None:
    connectable = engine_from_config(
        context_config.get_section(context_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
