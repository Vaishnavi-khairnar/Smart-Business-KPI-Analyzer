import os
from typing import Dict, Any
   
def get_api_url() -> str:
       """Get API URL from environment or default."""
       return os.getenv("API_URL", "http://localhost:8000/api/v1")
   
def get_setting(key: str, default: Any = None) -> Any:
       """Get a setting from file or return default."""
       # In a real app, this would load from a file
       return os.getenv(key.upper(), default)
   
def save_setting(key: str, value: Any) -> None:
       """Save a setting to file."""
       # In a real app, this would save to a file
       os.environ[key.upper()] = str(value)
   
def get_all_settings() -> Dict[str, Any]:
       """Get all settings."""
       # In a real app, this would load from a file
       return {
           "API_URL": get_api_url(),
           # Add other settings here
       }