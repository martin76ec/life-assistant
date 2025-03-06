# todo: create a function that imports Reminders model from src.providers.sqlalchemy.models.models and creates a new row
# context: if try except needed use a general try except in the main thread
# context: define dataclasses for params if needed
# context: for function naming always use entity_action template
# context: don't put unncessary comments

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.providers.sqlalchemy.models.models import Reminders


async def create_reminder(reminder: Reminders, session: AsyncSession) -> Optional[Reminders]:
  """Creates a new reminder."""
  try:
    session.add(reminder)
    await session.commit()
    await session.refresh(reminder)
    return reminder
  except Exception as e:
    print(f"Error creating reminder: {e}")
    await session.rollback()
    return None
