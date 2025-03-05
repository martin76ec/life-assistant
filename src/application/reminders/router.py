from fastapi import APIRouter

router = APIRouter()


@router.get("/reminders")
async def reminders_get():
  return {"message": "List of items"}
