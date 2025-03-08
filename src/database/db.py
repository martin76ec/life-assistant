import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from constants.env import Envs

# Load environment variables
load_dotenv()

# Create database engine
engine = create_engine(Envs.DB_URL)

# Test connection
with engine.connect() as connection:
    result = connection.execute("SELECT version()")
    print(result.fetchone())  # Should print PostgreSQL version
