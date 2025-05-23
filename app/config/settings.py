from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Pier2 Imports"
    version: str = "0.0.1"
    # database_url: str = "postgresql://postgres:changemeinprod!@localhost:5432/pier2imports"
    database_name: str = "pier2imports"
    database_username: str = "postgres"
    database_password: str = "changemeinprod!"
    database_host: str = "localhost"
    database_port: int = 5432


@lru_cache
def get_settings():
    return Settings()
