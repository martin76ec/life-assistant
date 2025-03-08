# todo: create a function to update a reminder giving (reminder_id, partial[remidner], session)
# context: if try except needed use a general try except in the main thread
# context: define dataclasses for params if needed
# context: for function naming always use entity_action template
# context: don't put unncessary comments

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.providers.sqlalchemy.models.models import Reminders


async def update_reminder(reminder_id: int, reminder: Reminders, session: AsyncSession) -> Optional[Reminders]:
  """Updates an existing reminder."""
  try:
    stmt = select(Reminders).where(Reminders.id == reminder_id)
    existing_reminder = (await session.execute(stmt)).scalar_one_or_none()
    if existing_reminder:
      for key, value in reminder.model_dump(exclude_unset=True).items():
        setattr(existing_reminder, key, value)
      await session.commit()
      await session.refresh(existing_reminder)
      return existing_reminder
    else:
      return None
  except Exception as e:
    print(f"Error updating reminder: {e}")
    await session.rollback()
    return None
