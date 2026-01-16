from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import io

from app.core.database import get_db
from api.endpoints.auth import get_current_user
from app.schemas import User
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/data")
def get_report_data(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get report data with optional filters"""
    report_service = ReportService(db)
    
    return report_service.generate_kpi_report_data(
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )

@router.get("/export/csv")
def export_csv(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    include_summary: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export report data as CSV"""
    report_service = ReportService(db)
    
    # Generate report data
    report_data = report_service.generate_kpi_report_data(
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )
    
    # Export to CSV
    csv_data = report_service.export_to_csv(report_data, include_summary=include_summary)
    
    # Create filename with timestamp
    filename = f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        io.BytesIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/export/excel")
def export_excel(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    include_charts: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export report data as Excel"""
    report_service = ReportService(db)
    
    # Generate report data
    report_data = report_service.generate_kpi_report_data(
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )
    
    # Export to Excel
    excel_data = report_service.export_to_excel(report_data, include_charts=include_charts)
    
    # Create filename with timestamp
    filename = f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return StreamingResponse(
        io.BytesIO(excel_data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/export/pdf")
def export_pdf(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    business_units: Optional[List[str]] = Query(None),
    kpi_types: Optional[List[str]] = Query(None),
    template: str = Query("standard"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export report data as PDF"""
    report_service = ReportService(db)
    
    # Generate report data
    report_data = report_service.generate_kpi_report_data(
        start_date=start_date,
        end_date=end_date,
        business_units=business_units,
        kpi_types=kpi_types
    )
    
    # Export to PDF
    pdf_data = report_service.export_to_pdf(report_data, template=template)
    
    # Create filename with timestamp
    filename = f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_data),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/schedule")
def schedule_report(
    report_config: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Schedule a report for automatic generation"""
    report_service = ReportService(db)
    
    # Schedule the report
    scheduled_report = report_service.schedule_report(report_config)
    
    # In a real implementation, you would add this to a task queue
    # background_tasks.add_task(generate_and_email_report, scheduled_report)
    
    return scheduled_report

@router.get("/templates")
def get_report_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available report templates"""
    templates = [
        {
            "id": "standard",
            "name": "Standard Report",
            "description": "Basic KPI report with summary statistics",
            "formats": ["csv", "excel", "pdf"]
        },
        {
            "id": "executive",
            "name": "Executive Summary",
            "description": "High-level summary for executive audience",
            "formats": ["pdf", "excel"]
        },
        {
            "id": "detailed",
            "name": "Detailed Analysis",
            "description": "Comprehensive report with trend analysis",
            "formats": ["excel", "pdf"]
        },
        {
            "id": "comparison",
            "name": "Comparison Report",
            "description": "Period-over-period comparison analysis",
            "formats": ["excel", "pdf"]
        }
    ]
    
    return templates

@router.get("/scheduled")
def get_scheduled_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of scheduled reports"""
    # This is a placeholder - in a real implementation, you would
    # fetch from a database table of scheduled reports
    scheduled_reports = [
        {
            "id": "report_1",
            "name": "Weekly KPI Report",
            "frequency": "weekly",
            "next_run": "2023-02-01T09:00:00",
            "last_run": "2023-01-25T09:00:00",
            "status": "active"
        },
        {
            "id": "report_2",
            "name": "Monthly Executive Summary",
            "frequency": "monthly",
            "next_run": "2023-02-01T09:00:00",
            "last_run": "2023-01-01T09:00:00",
            "status": "active"
        }
    ]
    
    return scheduled_reports

@router.delete("/scheduled/{report_id}")
def delete_scheduled_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a scheduled report"""
    # This is a placeholder - in a real implementation, you would
    # delete from a database table of scheduled reports
    return {"message": f"Report {report_id} deleted successfully"}