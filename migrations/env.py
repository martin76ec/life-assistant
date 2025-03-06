from logging.config import fileConfig
from sqlalchemy import MetaData, create_engine
from alembic import context
from src.providers.sqlalchemy.models import Reminders

config = context.config

if config.config_file_name is not None:
  fileConfig(config.config_file_name)

engine = create_engine("sqlite:///life-assistant.db")
metadata = MetaData()
metadata.reflect(bind=engine)
target_metadata = Reminders.metadata
print(target_metadata.tables.keys())


def run_migrations_offline() -> None:
  context.configure(
    dialect_name=engine.dialect.name,
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
