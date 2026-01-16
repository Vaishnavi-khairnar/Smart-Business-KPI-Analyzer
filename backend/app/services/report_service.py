    
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import BytesIO
import csv
import json
from pathlib import Path
import os


def __init__(self, db: Session):
        self.db = db
        self.kpi_service = KPIService(db)
    
def generate_kpi_report_data(self, start_date: datetime = None, end_date: datetime = None,
                               business_units: List[str] = None, kpi_types: List[str] = None) -> Dict[str, Any]:
        """Generate KPI data for reports"""
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get KPI data
        kpi_query = self.db.query(KPI).filter(
            KPI.period >= start_date,
            KPI.period <= end_date
        )
        
        if business_units:
            kpi_query = kpi_query.filter(KPI.business_unit.in_(business_units))
        
        if kpi_types:
            kpi_query = kpi_query.filter(KPI.kpi_type.in_(kpi_types))
        
        kpis = kpi_query.all()
        
        # Convert to DataFrame
        kpi_data = []
        for kpi in kpis:
            kpi_data.append({
                'id': kpi.id,
                'kpi_type': kpi.kpi_type,
                'value': kpi.value,
                'period': kpi.period,
                'business_unit': kpi.business_unit,
                'created_at': kpi.created_at
            })
        
        df = pd.DataFrame(kpi_data)
        
        # Generate summary statistics
        summary_stats = self._generate_summary_stats(df)
        
        # Generate trend analysis
        trend_analysis = self._generate_trend_analysis(df)
        
        # Generate business unit comparison
        bu_comparison = self._generate_bu_comparison(df)
        
        return {
            'kpi_data': kpi_data,
            'summary_stats': summary_stats,
            'trend_analysis': trend_analysis,
            'bu_comparison': bu_comparison,
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'period_start': start_date.isoformat(),
                'period_end': end_date.isoformat(),
                'business_units': business_units or [],
                'kpi_types': kpi_types or []
            }
        }
    
def export_to_csv(self, report_data: Dict[str, Any], include_summary: bool = True) -> bytes:
        """Export report data to CSV format"""
        output = BytesIO()
        
        # Create main KPI data CSV
        kpi_df = pd.DataFrame(report_data['kpi_data'])
        
        with output as f:
            writer = csv.writer(f)
            
            # Write header with metadata
            writer.writerow(['KPI Analyzer Report'])
            writer.writerow([f"Generated: {report_data['report_metadata']['generated_at']}"])
            writer.writerow([f"Period: {report_data['report_metadata']['period_start']} to {report_data['report_metadata']['period_end']}"])
            writer.writerow([])
            
            # Write main data
            writer.writerow(['KPI Data'])
            writer.writerow(['ID', 'KPI Type', 'Value', 'Period', 'Business Unit', 'Created At'])
            
            for _, row in kpi_df.iterrows():
                writer.writerow([
                    row['id'],
                    row['kpi_type'],
                    row['value'],
                    row['period'],
                    row['business_unit'],
                    row['created_at']
                ])
            
            # Include summary statistics if requested
            if include_summary and 'summary_stats' in report_data:
                writer.writerow([])
                writer.writerow(['Summary Statistics'])
                writer.writerow(['Metric', 'Value'])
                
                for metric, value in report_data['summary_stats'].items():
                    writer.writerow([metric, value])
            
            # Include business unit comparison if available
            if include_summary and 'bu_comparison' in report_data:
                writer.writerow([])
                writer.writerow(['Business Unit Comparison'])
                writer.writerow(['Business Unit', 'KPI Type', 'Total', 'Average', 'Min', 'Max'])
                
                for bu_data in report_data['bu_comparison']:
                    writer.writerow([
                        bu_data['business_unit'],
                        bu_data['kpi_type'],
                        bu_data['total'],
                        bu_data['average'],
                        bu_data['min'],
                        bu_data['max']
                    ])
        
        return output.getvalue()
    
def export_to_excel(self, report_data: Dict[str, Any], include_charts: bool = True) -> bytes:
        """Export report data to Excel format with multiple sheets"""
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Create main data sheet
            kpi_df = pd.DataFrame(report_data['kpi_data'])
            kpi_df.to_excel(writer, sheet_name='KPI Data', index=False)
            
            # Create summary sheet
            if 'summary_stats' in report_data:
                summary_df = pd.DataFrame(list(report_data['summary_stats'].items()), 
                                     columns=['Metric', 'Value'])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Create business unit comparison sheet
            if 'bu_comparison' in report_data:
                bu_df = pd.DataFrame(report_data['bu_comparison'])
                bu_df.to_excel(writer, sheet_name='Business Units', index=False)
            
            # Create trend analysis sheet
            if 'trend_analysis' in report_data:
                trend_dfs = {}
                for kpi_type, trend_data in report_data['trend_analysis'].items():
                    trend_dfs[kpi_type] = pd.DataFrame(trend_data)
                
                for kpi_type, df in trend_dfs.items():
                    sheet_name = f"Trend - {kpi_type.replace('_', ' ').title()}"[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Create metadata sheet
            metadata_df = pd.DataFrame(list(report_data['report_metadata'].items()),
                                   columns=['Property', 'Value'])
            metadata_df.to_excel(writer, sheet_name='Report Info', index=False)
        
        return output.getvalue()
    
def export_to_pdf(self, report_data: Dict[str, Any], template: str = 'standard') -> bytes:
        """Export report data to PDF format"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.graphics.shapes import Drawing
            from reportlab.graphics.charts.lineplots import LinePlot
            from reportlab.graphics.charts.barcharts import VerticalBarChart
        except ImportError:
            # Fallback to simple text-based PDF if reportlab is not available
            return self._export_to_pdf_fallback(report_data)
        
        output = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(output, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        story.append(Paragraph("KPI Analyzer Report", title_style))
        story.append(Spacer(1, 12))
        
        # Report metadata
        metadata = report_data['report_metadata']
        story.append(Paragraph(f"<b>Generated:</b> {metadata['generated_at']}", styles['Normal']))
        story.append(Paragraph(f"<b>Period:</b> {metadata['period_start']} to {metadata['period_end']}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Summary Statistics
        if 'summary_stats' in report_data:
            story.append(Paragraph("Summary Statistics", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            summary_data = [['Metric', 'Value']]
            for metric, value in report_data['summary_stats'].items():
                summary_data.append([metric, str(value)])
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 12))
        
        # Business Unit Comparison
        if 'bu_comparison' in report_data:
            story.append(PageBreak())
            story.append(Paragraph("Business Unit Comparison", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            bu_data = [['Business Unit', 'KPI Type', 'Total', 'Average', 'Min', 'Max']]
            for bu in report_data['bu_comparison']:
                bu_data.append([
                    bu['business_unit'],
                    bu['kpi_type'],
                    str(bu['total']),
                    str(bu['average']),
                    str(bu['min']),
                    str(bu['max'])
                ])
            
            bu_table = Table(bu_data)
            bu_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(bu_table)
            story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        return output.getvalue()
    
def _export_to_pdf_fallback(self, report_data: Dict[str, Any]) -> bytes:
        """Fallback PDF export using basic text formatting"""
        # This is a simplified fallback when reportlab is not available
        # In production, ensure reportlab is installed
        text_content = []
        
        # Add title and metadata
        text_content.append("KPI Analyzer Report")
        text_content.append("=" * 50)
        text_content.append(f"Generated: {report_data['report_metadata']['generated_at']}")
        text_content.append(f"Period: {report_data['report_metadata']['period_start']} to {report_data['report_metadata']['period_end']}")
        text_content.append("")
        
        # Add summary statistics
        if 'summary_stats' in report_data:
            text_content.append("Summary Statistics")
            text_content.append("-" * 30)
            for metric, value in report_data['summary_stats'].items():
                text_content.append(f"{metric}: {value}")
            text_content.append("")
        
        # Add business unit comparison
        if 'bu_comparison' in report_data:
            text_content.append("Business Unit Comparison")
            text_content.append("-" * 30)
            for bu in report_data['bu_comparison']:
                text_content.append(f"{bu['business_unit']} - {bu['kpi_type']}")
                text_content.append(f"  Total: {bu['total']}, Average: {bu['average']}")
                text_content.append("")
        
        # Return as bytes
        return "\n".join(text_content).encode('utf-8')
    
def _generate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics from KPI data"""
        if df.empty:
            return {}
        
        summary = {}
        
        # Overall statistics
        summary['total_records'] = len(df)
        summary['unique_kpi_types'] = df['kpi_type'].nunique()
        summary['unique_business_units'] = df['business_unit'].nunique()
        summary['date_range_start'] = df['period'].min().isoformat()
        summary['date_range_end'] = df['period'].max().isoformat()
        
        # Statistics by KPI type
        for kpi_type in df['kpi_type'].unique():
            kpi_df = df[df['kpi_type'] == kpi_type]
            summary[f'{kpi_type}_avg'] = kpi_df['value'].mean()
            summary[f'{kpi_type}_total'] = kpi_df['value'].sum()
            summary[f'{kpi_type}_min'] = kpi_df['value'].min()
            summary[f'{kpi_type}_max'] = kpi_df['value'].max()
        
        return summary
    
def _generate_trend_analysis(self, df: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
        """Generate trend analysis for each KPI type"""
        if df.empty:
            return {}
        
        trend_data = {}
        
        for kpi_type in df['kpi_type'].unique():
            kpi_df = df[df['kpi_type'] == kpi_type].sort_values('period')
            
            # Calculate period-over-period change
            kpi_df['prev_value'] = kpi_df['value'].shift(1)
            kpi_df['change_pct'] = ((kpi_df['value'] - kpi_df['prev_value']) / kpi_df['prev_value'] * 100).fillna(0)
            
            trend_data[kpi_type] = []
            
            for _, row in kpi_df.iterrows():
                trend_data[kpi_type].append({
                    'period': row['period'].isoformat(),
                    'value': row['value'],
                    'change_pct': row['change_pct']
                })
        
        return trend_data
    
def _generate_bu_comparison(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate business unit comparison data"""
        if df.empty:
            return []
        
        bu_data = []
        
        # Group by business unit and KPI type
        grouped = df.groupby(['business_unit', 'kpi_type'])['value'].agg(['sum', 'mean', 'min', 'max']).reset_index()
        
        for _, row in grouped.iterrows():
            bu_data.append({
                'business_unit': row['business_unit'],
                'kpi_type': row['kpi_type'],
                'total': row['sum'],
                'average': row['mean'],
                'min': row['min'],
                'max': row['max']
            })
        
        return bu_data
    
def schedule_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a report for automatic generation"""
        # This is a placeholder for report scheduling
        # In a real implementation, you would use a task queue like Celery
        scheduled_report = {
            'id': f"report_{datetime.now().timestamp()}",
            'config': report_config,
            'status': 'scheduled',
            'next_run': self._calculate_next_run(report_config['schedule']),
            'created_at': datetime.now().isoformat()
        }
        
        return scheduled_report
    
def _calculate_next_run(self, schedule_config: Dict[str, Any]) -> str:
        """Calculate the next run time for a scheduled report"""
        now = datetime.now()
        
        if schedule_config['frequency'] == 'daily':
            next_run = now + timedelta(days=1)
        elif schedule_config['frequency'] == 'weekly':
            next_run = now + timedelta(weeks=1)
        elif schedule_config['frequency'] == 'monthly':
            next_run = now + timedelta(days=30)
        else:
            next_run = now + timedelta(days=1)
        
        return next_run.isoformat()