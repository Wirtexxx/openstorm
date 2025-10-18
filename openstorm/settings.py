from pydantic_settings import BaseSettings
from typing import ClassVar
import os


class Settings(BaseSettings):
    DEFAULT_CONTAINER_NAME: ClassVar[str] = "mongodb"
    DEFAULT_BIND_HOST_DIR: ClassVar[str] = os.path.join(os.path.expanduser("~"), "mongo_data")
    MONGO_URI: str = "mongodb://localhost:27017"


settings = Settings()
