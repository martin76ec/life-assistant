from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from domain.reminders.types import ReminderModel
from providers.sqlalchemy.models.dataclasses import Reminders


class RemindersDS:
  @staticmethod
  async def create_reminder(reminder: ReminderModel, session: AsyncSession):
    """Creates a new reminder."""
    data = Reminders(
      id=None,
      message=reminder.message,
      recurrence=reminder.recurrence,
      reminder_date=datetime.strptime(reminder.reminder_date, "%Y-%m-%d %H:%M"),
      created_at=None,
      updated_at=None,
      status=None,
      is_deleted=None,
    )
    session.add(data)
    await session.commit()
    await session.refresh(data)
    return data
