from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from datetime import datetime

from app.models.database import (
    SalesData,
    CostData,
    MarketingData,
    CustomerData,
)
from .base import CRUDBase


# =====================================================
# SALES DATA CRUD
# =====================================================
class CRUDSalesData(CRUDBase[SalesData, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[SalesData]:
        """
        Get sales data within a date range (DATE-safe).
        """
        return (
            db.query(SalesData)
            .filter(
                func.date(SalesData.date) >= start_date.date(),
                func.date(SalesData.date) <= end_date.date(),
            )
            .order_by(SalesData.date)
            .all()
        )


# =====================================================
# COST DATA CRUD
# =====================================================
class CRUDCostData(CRUDBase[CostData, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[CostData]:
        """
        Get cost data within a date range (DATE-safe).
        """
        return (
            db.query(CostData)
            .filter(
                func.date(CostData.date) >= start_date.date(),
                func.date(CostData.date) <= end_date.date(),
            )
            .order_by(CostData.date)
            .all()
        )


# =====================================================
# MARKETING DATA CRUD
# =====================================================
class CRUDMarketingData(CRUDBase[MarketingData, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[MarketingData]:
        """
        Get marketing data within a date range (DATE-safe).
        """
        return (
            db.query(MarketingData)
            .filter(
                func.date(MarketingData.date) >= start_date.date(),
                func.date(MarketingData.date) <= end_date.date(),
            )
            .order_by(MarketingData.date)
            .all()
        )


# =====================================================
# CUSTOMER DATA CRUD
# =====================================================
class CRUDCustomerData(CRUDBase[CustomerData, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[CustomerData]:
        """
        Get customers created within a date range (DATE-safe).
        """
        return (
            db.query(CustomerData)
            .filter(
                func.date(CustomerData.signup_date) >= start_date.date(),
                func.date(CustomerData.signup_date) <= end_date.date(),
            )
            .order_by(CustomerData.signup_date)
            .all()
        )

    def get_active_at_date(
        self,
        db: Session,
        *,
        date: datetime,
    ) -> List[CustomerData]:
        """
        Get customers active at a specific date.
        """
        return (
            db.query(CustomerData)
            .filter(func.date(CustomerData.signup_date) <= date.date())
            .all()
        )


# =====================================================
# CRUD INSTANCES
# =====================================================
crud_sales_data = CRUDSalesData(SalesData)
crud_cost_data = CRUDCostData(CostData)
crud_marketing_data = CRUDMarketingData(MarketingData)
crud_customer_data = CRUDCustomerData(CustomerData)
