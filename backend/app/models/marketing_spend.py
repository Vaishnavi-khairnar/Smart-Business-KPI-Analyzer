from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class MarketingSpend(Base):
    __tablename__ = "marketing_spend"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    spend_date = Column(Date, nullable=False)

    business_unit_id = Column(Integer, ForeignKey("business_units.id"))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<MarketingSpend(id={self.id}, channel='{self.channel}', amount={self.amount})>"
