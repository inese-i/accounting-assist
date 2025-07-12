from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    PROJECT_NAME: str = "API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # LangSmith Configuration
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: Optional[str] = os.getenv("LANGSMITH_PROJECT")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    
    # Database Configuration (for future use)
    DATABASE_URL: str = "sqlite:///./hgb_accountant.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
