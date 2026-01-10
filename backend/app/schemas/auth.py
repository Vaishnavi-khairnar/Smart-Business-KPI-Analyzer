from pydantic import BaseModel
from typing import Any, Dict


class AuthResponse(BaseModel):
    message: str
    data: Dict[str, Any]
