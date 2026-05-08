import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.core.database import Base
import app.models  # noqa: F401 — registers all models

config = context.config

# DATABASE_URL may be None when the module is imported at app startup before
# Railway has injected environment variables.  Guard against that here so we
# don't raise "TypeError: option values must be strings" at import time.
# The actual URL is resolved (and validated) inside run_migrations_online /
# run_migrations_offline, so migrations will still fail loudly if the variable
# is genuinely missing when alembic is invoked.
_database_url = settings.DATABASE_URL
if _database_url:
    config.set_main_option("sqlalchemy.url", _database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Prefer the already-configured option; fall back to settings so that the
    # URL is always resolved at migration time even if it was None at import.
    url = config.get_main_option("sqlalchemy.url") or settings.get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Ensure the URL is set at migration time even if DATABASE_URL was absent
    # at module-import time (e.g. during Railway container startup).
    if not config.get_main_option("sqlalchemy.url", fallback=None):
        config.set_main_option("sqlalchemy.url", settings.get_database_url())

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
