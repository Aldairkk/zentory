from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Zentory ERP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    DATABASE_URL: str = "sqlite:///./zentory.db"
    
    SECRET_KEY: str = "zentory-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    ADMIN_EMAIL: str = "admin@zentory.com"
    ADMIN_PASSWORD: str = "Admin123!"
    
    class Config:
        env_file = ".env"


settings = Settings()