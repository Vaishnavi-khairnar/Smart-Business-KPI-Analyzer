from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from api.endpoints.auth import me as get_current_user
from app.schemas.user import User
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def get_dashboard_data(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard data with optional filters"""
    dashboard_service = DashboardService(db)
    
    return dashboard_service.get_dashboard_data(
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )

@router.post("/comparison")
def get_comparison_data(
    current_period: Dict[str, datetime],
    comparison_period: Dict[str, datetime],
    kpi_types: Optional[List[str]] = None,
    business_units: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comparison data between two periods"""
    dashboard_service = DashboardService(db)
    
    return dashboard_service.get_comparison_data(
        current_period=current_period,
        comparison_period=comparison_period,
        kpi_types=kpi_types,
        business_units=business_units
    )

@router.post("/forecast")
def get_forecast_data(
    kpi_type: str,
    periods: int = 12,
    business_units: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get forecast data for a KPI"""
    dashboard_service = DashboardService(db)
    
    return dashboard_service.get_forecast_data(
        kpi_type=kpi_type,
        periods=periods,
        business_units=business_units
    )

@router.get("/insights")
def get_insights(
    kpi_types: Optional[List[str]] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI-generated insights"""
    dashboard_service = DashboardService(db)
    
    return dashboard_service.get_insights(
        kpi_types=kpi_types,
        business_units=business_units
    )

@router.get("/export")
def export_dashboard_data(
    format: str = Query("csv", pattern="^(csv|excel|json)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export dashboard data"""
    dashboard_service = DashboardService(db)
    
    return dashboard_service.export_dashboard_data(
        format=format,
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )