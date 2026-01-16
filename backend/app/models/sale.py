from sqlalchemy import Column, Integer, Float, Date, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False)

    business_unit_id = Column(Integer, ForeignKey("business_units.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Sale(id={self.id}, amount={self.amount})>"
