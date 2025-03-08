from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from providers.constants.env import DB_URL


class EngineSingleton:
  _instance: Any = None

  @staticmethod
  def instance_get() -> AsyncEngine:
    if EngineSingleton._instance == None:
      EngineSingleton._instance = create_async_engine(DB_URL)
    return EngineSingleton._instance
