from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    cost_date = Column(Date, nullable=False)

    business_unit_id = Column(Integer, ForeignKey("business_units.id"))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Cost(id={self.id}, amount={self.amount})>"
