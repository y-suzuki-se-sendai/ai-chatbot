import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "./data/chroma")
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-1.5-pro"

settings = Settings()
