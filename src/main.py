from fastapi import FastAPI
from application.reminders import router as reminders_router

app = FastAPI()

app.include_router(reminders_router.router, prefix="/reminders", tags=["reminders"])
