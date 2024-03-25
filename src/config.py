import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DB_URL')
    db_echo: bool = True


settings = Settings()
