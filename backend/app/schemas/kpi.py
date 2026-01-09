from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# =========================
# KPI Base Schema
# =========================

class KPIBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    formula: Optional[str] = None


# =========================
# KPI Schemas
# =========================

class KPICreate(KPIBase):
    pass


class KPIUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    formula: Optional[str] = None


class KPIRead(KPIBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # ✅ REQUIRED (Pydantic v2)


class KPIResponse(BaseModel):
    id: int
    name: str
    value: float
    description: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# KPI Value Schemas
# =========================

class KPIValueBase(BaseModel):
    value: float
    period_start: datetime
    period_end: datetime


class KPIValueCreate(KPIValueBase):
    kpi_id: int


class KPIValueRead(KPIValueBase):
    id: int
    kpi_id: int

    class Config:
        from_attributes = True


# =========================
# KPI Calculation Requests
# =========================

class KPICalculationRequest(BaseModel):
    kpi_type: str = Field(..., description="Type of KPI to calculate")
    period_start: datetime
    period_end: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "kpi_type": "revenue",
                "period_start": "2023-01-01T00:00:00",
                "period_end": "2023-01-31T23:59:59"
            }
        }


class AllKPICalculationRequest(BaseModel):
    period_start: datetime
    period_end: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "period_start": "2023-01-01T00:00:00",
                "period_end": "2023-01-31T23:59:59"
            }
        }
