from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    success: bool = True
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class KPIResponse(ResponseBase):
    data: Optional[Any] = None


class KPIListResponse(ResponseBase):
    data: List[Any] = Field(default_factory=list)
    count: int = 0
