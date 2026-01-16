from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BusinessUnitBase(BaseModel):
    name: str
    description: Optional[str] = None


class BusinessUnitResponse(BusinessUnitBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
