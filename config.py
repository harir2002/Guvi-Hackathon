from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_KEY: str
    GROQ_API_KEY: str
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_data"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
