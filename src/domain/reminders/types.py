from typing import Optional

from pydantic import BaseModel


class ReminderModel(BaseModel):
  message: str
  reminder_date: str
  status: Optional[str]
  recurrence: Optional[str]
