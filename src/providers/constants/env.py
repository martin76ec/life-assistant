import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENV") or "dev"
DB_URL = os.getenv("DB_TEST_URL") if ENVIRONMENT == "dev" else os.getenv("DB_URL") or ""
