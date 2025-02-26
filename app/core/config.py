import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "TailorTalk")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "A self-contained chatbot for the Titanic dataset")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Frontend settings
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "localhost")
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "8501"))
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/titanic.db")
    
    # Data settings
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    VISUALIZATIONS_DIR: str = os.getenv("VISUALIZATIONS_DIR", "./data/visualizations")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()
