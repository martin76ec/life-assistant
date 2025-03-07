from fastapi import APIRouter

from application.reminders.create import Create

router = APIRouter()


@router.get("/reminders")
async def reminders_get():
  return {"message": "List of items"}


@router.post("/")
async def reminders_create(data: dict):
  await Create.run(data)
