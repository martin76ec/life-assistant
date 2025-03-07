from os import getenv
from dotenv import load_dotenv
from dotenv.main import os


load_dotenv()

ENVIRONMENT = os.getenv("ENV") or "dev"
DB_URL = os.getenv("DB_TEST_URL") if ENVIRONMENT == "dev" else os.getenv("DB_URL") or ""
