from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.kpi_value import KPIValue


# =========================
# KPI BASE
# =========================
class KPIBase(BaseModel):
    name: str = Field(..., description="Name of the KPI")
    description: Optional[str] = Field(
        None, description="Description of the KPI"
    )
    unit: str = Field(..., description="Unit of measurement for the KPI")
    formula: Optional[str] = Field(
        None, description="Formula used to calculate the KPI"
    )


class KPICreate(KPIBase):
    pass


class KPIUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    formula: Optional[str] = None


# =========================
# KPI RESPONSE
# =========================
class KPI(KPIBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# KPI VALUE
# =========================
class KPIValue(BaseModel):
    kpi_id: int
    value: float
    period_start: datetime
    period_end: datetime
    calculated_at: datetime
    extra_data: Optional[dict] = None

    class Config:
        from_attributes = True


class KPIValueCreate(BaseModel):
    kpi_id: int
    value: float
    period_start: datetime
    period_end: datetime
    extra_data: Optional[dict] = None


# =========================
# KPI WITH VALUES
# =========================
class KPIWithValues(KPI):
    values: List[KPIValue] = Field(default_factory=list)
