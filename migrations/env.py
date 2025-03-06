from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from src.providers.sqlalchemy.models.models import Reminders  # Ensure all models are imported here if needed

config = context.config

if config.config_file_name is not None:
  fileConfig(config.config_file_name)

engine = create_engine("sqlite:///life-assistant.db")

# Use the metadata defined on your Reminders model (and any others sharing the same base)
target_metadata = Reminders.metadata


def run_migrations_offline() -> None:
  context.configure(
    url="sqlite:///life-assistant.db",
    target_metadata=target_metadata,
    literal_binds=True,
    dialect_opts={"paramstyle": "named"},
  )
  with context.begin_transaction():
    context.run_migrations()


def run_migrations_online() -> None:
  with engine.connect() as connection:
    context.configure(
      connection=connection,
      target_metadata=target_metadata,
      compare_type=True,
    )
    with context.begin_transaction():
      context.run_migrations()


if context.is_offline_mode():
  run_migrations_offline()
else:
  run_migrations_online()
