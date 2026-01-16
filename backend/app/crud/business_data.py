from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from datetime import datetime

from app.models.sale import Sale
from app.models.cost import Cost
from app.models.marketing_spend import MarketingSpend
from app.models.customer import Customer
from .base import CRUDBase


# =====================================================
# SALES DATA CRUD
# =====================================================
class CRUDSalesData(CRUDBase[Sale, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Sale]:
        """
        Get sales data within a date range (DATE-safe).
        """
        return (
            db.query(Sale)
            .filter(
                func.date(Sale.sale_date) >= start_date.date(),
                func.date(Sale.sale_date) <= end_date.date(),
            )
            .order_by(Sale.sale_date)
            .all()
        )


# =====================================================
# COST DATA CRUD
# =====================================================
class CRUDCostData(CRUDBase[Cost, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Cost]:
        """
        Get cost data within a date range (DATE-safe).
        """
        return (
            db.query(Cost)
            .filter(
                func.date(Cost.cost_date) >= start_date.date(),
                func.date(Cost.cost_date) <= end_date.date(),
            )
            .order_by(Cost.cost_date)
            .all()
        )


# =====================================================
# MARKETING DATA CRUD
# =====================================================
class CRUDMarketingData(CRUDBase[MarketingSpend, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[MarketingSpend]:
        """
        Get marketing data within a date range (DATE-safe).
        """
        return (
            db.query(MarketingSpend)
            .filter(
                func.date(MarketingSpend.spend_date) >= start_date.date(),
                func.date(MarketingSpend.spend_date) <= end_date.date(),
            )
            .order_by(MarketingSpend.spend_date)
            .all()
        )


# =====================================================
# CUSTOMER DATA CRUD
# =====================================================
class CRUDCustomerData(CRUDBase[Customer, dict, dict]):
    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Customer]:
        """
        Get customers created within a date range (DATE-safe).
        """
        return (
            db.query(Customer)
            .filter(
                func.date(Customer.created_at) >= start_date.date(),
                func.date(Customer.created_at) <= end_date.date(),
            )
            .order_by(Customer.created_at)
            .all()
        )

    def get_active_at_date(
        self,
        db: Session,
        *,
        date: datetime,
    ) -> List[Customer]:
        """
        Get customers active at a specific date.
        """
        return (
            db.query(Customer)
            .filter(func.date(Customer.created_at) <= date.date())
            .all()
        )


# =====================================================
# CRUD INSTANCES
# =====================================================
crud_sales_data = CRUDSalesData(Sale)
crud_cost_data = CRUDCostData(Cost)
crud_marketing_data = CRUDMarketingData(MarketingSpend)
crud_customer_data = CRUDCustomerData(Customer)
