# updated: 2026-05-07
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/institute_db"
    OPENAI_API_KEY: str = ""
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()
