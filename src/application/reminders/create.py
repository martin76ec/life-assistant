from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from domain.reminders.types import ReminderModel
from providers.sqlalchemy.engine import EngineSingleton
from src.providers.sqlalchemy.models.models import Reminders
from src.infrastructure.database.reminders.reminders_ds import RemindersDS


class Create:
  @staticmethod
  async def run(reminder: dict) -> Optional[Reminders]:
    """Creates a new reminder."""
    engine = EngineSingleton.instance_get()
    session = AsyncSession(engine)

    try:
      valid_reminder = ReminderModel.model_validate(reminder, strict=True)
      await RemindersDS.create_reminder(valid_reminder, session)
    except Exception as e:
      print(f"Error creating reminder: {e}")
      await session.rollback()
    finally:
      await session.close()
