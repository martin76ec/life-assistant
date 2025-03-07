from fastapi import FastAPI
from application.reminders import router as reminders_router
import uvicorn

app = FastAPI()

app.include_router(reminders_router.router, prefix="/reminders", tags=["reminders"])


def start():
  """Launched with `poetry run start` at root level"""
  uvicorn.run("src.main:app", host="0.0.0.0", port=9090, reload=True)
