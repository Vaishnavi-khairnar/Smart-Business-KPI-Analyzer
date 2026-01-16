from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class KPIValue(Base):
    __tablename__ = "kpi_values"

    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id"), nullable=False)
    value = Column(Float, nullable=False)

    created_at = Column(DateTime, default=func.now())

    kpi = relationship("KPI", back_populates="values")
