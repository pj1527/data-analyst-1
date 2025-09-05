import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application Settings
    STAGE: str = os.getenv("STAGE", "local")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    
    # LLM Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    
    # API Configuration
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost,http://localhost:3000"
    ).split(",")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()
