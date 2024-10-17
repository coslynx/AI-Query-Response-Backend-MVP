from pydantic import BaseSettings
import os
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    #  Cache Settings
    CACHE_TTL: int = 60 * 5 # 5 minutes
    CACHE_SIZE: int = 100

    # OpenAI model configurations (you can add more models here)
    OPENAI_MODELS: List[str] = [
        "text-davinci-003",
        "text-curie-001",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache(maxsize=Settings().CACHE_SIZE)
def get_settings():
    return Settings()