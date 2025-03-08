from dotenv import load_dotenv
import os

load_dotenv()

class Envs:
    DB_URL = os.getenv('DB_URL') or ""
