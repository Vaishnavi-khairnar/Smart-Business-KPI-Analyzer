#from pydantic import BaseSettings
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
       app_name: str = "Smart Business KPI Analyzer"
       debug: bool = True
       version: str = "1.0.0"
       api_v1_str: str = "/api/v1"
       
       # Security settings
       secret_key: str = "your-secret-key-here-change-in-production"
       algorithm: str = "HS256"
       access_token_expire_minutes: int = 30
       
       class Config:
           env_file = ".env"

settings = Settings()