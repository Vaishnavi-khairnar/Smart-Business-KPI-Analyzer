from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pydantic import Field
from typing import Optional, List, Any
from datetime import datetime


class ResponseBase(BaseModel):
       success: bool = True
       message: str
       timestamp: datetime = Field(default_factory=datetime.now)

class KPIResponse(ResponseBase):
       data: Optional[Any] = None

class KPIListResponse(ResponseBase):
       data: List[Any] = []
       count: int = 0

class ErrorResponse(ResponseBase):
       success: bool = False
       error_code: Optional[str] = None
       details: Optional[dict] = None

class HealthResponse(BaseModel):
       status: str
       service: str
       version: str
       timestamp: datetime = Field(default_factory=datetime.now)