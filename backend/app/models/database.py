from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
   
class User(Base):
       __tablename__ = "users"
       
       id = Column(Integer, primary_key=True, index=True)
       username = Column(String(50), unique=True, index=True)
       email = Column(String(100), unique=True, index=True)
       hashed_password = Column(String(255))
       is_active = Column(Boolean, default=True)
       created_at = Column(DateTime, default=func.now())
       updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
   
class KPI(Base):
       __tablename__ = "kpis"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False)
       description = Column(Text)
       unit = Column(String(50), nullable=False)
       formula = Column(Text)
       is_active = Column(Boolean, default=True)
       created_at = Column(DateTime, default=func.now())
       updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
       
       # Relationships
       values = relationship("KPIValue", back_populates="kpi")
   
class KPIValue(Base):
       __tablename__ = "kpi_values"
       
       id = Column(Integer, primary_key=True, index=True)
       kpi_id = Column(Integer, ForeignKey("kpis.id"), nullable=False)
       value = Column(Float, nullable=False)
       period_start = Column(DateTime, nullable=False)
       period_end = Column(DateTime, nullable=False)
       calculated_at = Column(DateTime, default=func.now())
       extra_data = Column(Text)  # JSON string for additional extra_data
       
       # Relationships
       kpi = relationship("KPI", back_populates="values")
   
class SalesData(Base):
       __tablename__ = "sales_data"
       
       id = Column(Integer, primary_key=True, index=True)
       date = Column(DateTime, nullable=False, index=True)
       amount = Column(Float, nullable=False)
       product_id = Column(String(50))
       customer_id = Column(Integer)
       region = Column(String(50))
       created_at = Column(DateTime, default=func.now())
   
class CostData(Base):
       __tablename__ = "cost_data"
       
       id = Column(Integer, primary_key=True, index=True)
       date = Column(DateTime, nullable=False, index=True)
       amount = Column(Float, nullable=False)
       cost_category = Column(String(50))
       department = Column(String(50))
       description = Column(Text)
       created_at = Column(DateTime, default=func.now())
   
class MarketingData(Base):
       __tablename__ = "marketing_data"
       
       id = Column(Integer, primary_key=True, index=True)
       date = Column(DateTime, nullable=False, index=True)
       amount = Column(Float, nullable=False)
       campaign_type = Column(String(50))
       campaign_name = Column(String(100))
       channel = Column(String(50))
       created_at = Column(DateTime, default=func.now())
   
class CustomerData(Base):
       __tablename__ = "customer_data"
       
       id = Column(Integer, primary_key=True, index=True)
       customer_id = Column(Integer, nullable=False, unique=True, index=True)
       name = Column(String(100))
       email = Column(String(100))
       signup_date = Column(DateTime, nullable=False, index=True)
       last_activity_date = Column(DateTime, index=True)
       total_purchases = Column(Float, default=0.0)
       total_value = Column(Float, default=0.0)
       region = Column(String(50))
       created_at = Column(DateTime, default=func.now())