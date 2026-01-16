from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import BytesIO
import json

from app.models import KPI, BusinessUnit, Customer, Sale, Cost, MarketingSpend
from app.services.kpi_service import KPIService

class DashboardService:
    """Service for dashboard data aggregation and analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.kpi_service = KPIService(db)
    
    def get_dashboard_data(self, start_date: datetime = None, end_date: datetime = None,
                          business_units: List[str] = None, kpi_types: List[str] = None) -> Dict[str, Any]:
        """Get aggregated dashboard data"""
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
        
        # Convert to DataFrame for easier manipulation
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
        
        # Get business units and customer segments
        business_units_list = self.db.query(BusinessUnit.name).all()
        business_units_list = [bu[0] for bu in business_units_list]
        
        # Get customer segments
        customer_segments = self.db.query(Customer.segment).distinct().all()
        customer_segments = [cs[0] for cs in customer_segments if cs[0]]
        
        # Calculate summary metrics
        summary_metrics = self._calculate_summary_metrics(df)
        
        return {
            'kpis': kpi_data,
            'summary_metrics': summary_metrics,
            'business_units': business_units_list,
            'customer_segments': customer_segments
        }
    
    def get_comparison_data(self, current_period: Dict[str, datetime],
                           comparison_period: Dict[str, datetime],
                           kpi_types: List[str] = None,
                           business_units: List[str] = None) -> Dict[str, Any]:
        """Get comparison data between two periods"""
        # Get current period data
        current_data = self.get_dashboard_data(
            start_date=current_period['start_date'],
            end_date=current_period['end_date'],
            business_units=business_units,
            kpi_types=kpi_types
        )
        
        # Get comparison period data
        comparison_data = self.get_dashboard_data(
            start_date=comparison_period['start_date'],
            end_date=comparison_period['end_date'],
            business_units=business_units,
            kpi_types=kpi_types
        )
        
        # Calculate comparisons
        comparisons = {}
        
        current_df = pd.DataFrame(current_data['kpis'])
        comparison_df = pd.DataFrame(comparison_data['kpis'])
        
        if not current_df.empty and not comparison_df.empty:
            # Group by KPI type and calculate averages
            current_by_type = current_df.groupby('kpi_type')['value'].mean()
            comparison_by_type = comparison_df.groupby('kpi_type')['value'].mean()
            
            for kpi_type in current_by_type.index:
                current_value = current_by_type[kpi_type]
                comparison_value = comparison_by_type.get(kpi_type, 0)
                
                if comparison_value != 0:
                    change_percent = ((current_value - comparison_value) / comparison_value) * 100
                else:
                    change_percent = 0
                
                comparisons[kpi_type] = {
                    'current_value': current_value,
                    'comparison_value': comparison_value,
                    'change_percent': change_percent,
                    'trend': 'up' if change_percent > 0 else 'down' if change_percent < 0 else 'flat'
                }
        
        return {
            'current_period': current_data,
            'comparison_period': comparison_data,
            'comparisons': comparisons
        }
    
    def get_forecast_data(self, kpi_type: str, periods: int = 12,
                         business_units: List[str] = None) -> Dict[str, Any]:
        """Get forecast data for a KPI"""
        # Get historical data for the KPI
        # Use last 12 periods as training data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Last year
        
        kpi_data = self.get_dashboard_data(
            start_date=start_date,
            end_date=end_date,
            business_units=business_units,
            kpi_types=[kpi_type]
        )
        
        df = pd.DataFrame(kpi_data['kpis'])
        
        if df.empty:
            return {
                'kpi_type': kpi_type,
                'forecast': [],
                'confidence_intervals': [],
                'model_accuracy': 0
            }
        
        # Simple linear regression for demonstration
        # In production, use more sophisticated forecasting methods
        df['date_ordinal'] = df['period'].apply(lambda x: x.toordinal())
        
        # Fit linear regression
        coeffs = np.polyfit(df['date_ordinal'], df['value'], 1)
        trend_line = np.poly1d(coeffs)
        
        # Generate forecast dates
        last_date = df['period'].max()
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=periods,
            freq='M'
        )
        
        # Generate forecast values
        forecast_ordinal = [d.toordinal() for d in forecast_dates]
        forecast_values = trend_line(forecast_ordinal)
        
        # Calculate confidence intervals (simplified)
        residuals = df['value'] - trend_line(df['date_ordinal'])
        std_error = np.std(residuals)
        
        forecast_data = []
        confidence_intervals = []
        
        for i, date in enumerate(forecast_dates):
            forecast_value = forecast_values[i]
            lower_bound = forecast_value - 1.96 * std_error  # 95% confidence interval
            upper_bound = forecast_value + 1.96 * std_error
            
            forecast_data.append({
                'date': date.isoformat(),
                'value': forecast_value
            })
            
            confidence_intervals.append({
                'date': date.isoformat(),
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            })
        
        # Calculate model accuracy (R-squared)
        y_pred = trend_line(df['date_ordinal'])
        ss_res = np.sum((df['value'] - y_pred) ** 2)
        ss_tot = np.sum((df['value'] - np.mean(df['value'])) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            'kpi_type': kpi_type,
            'forecast': forecast_data,
            'confidence_intervals': confidence_intervals,
            'model_accuracy': r_squared
        }
    
    def get_insights(self, kpi_types: List[str] = None,
                    business_units: List[str] = None) -> Dict[str, Any]:
        """Generate AI-powered insights from KPI data"""
        # Get recent data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)  # Last 3 months
        
        kpi_data = self.get_dashboard_data(
            start_date=start_date,
            end_date=end_date,
            business_units=business_units,
            kpi_types=kpi_types
        )
        
        df = pd.DataFrame(kpi_data['kpis'])
        
        insights = []
        
        if df.empty:
            return {'insights': insights}
        
        # Generate insights based on data patterns
        # Revenue trend insight
        revenue_data = df[df['kpi_type'] == 'revenue']
        if len(revenue_data) > 1:
            revenue_growth = (
                (revenue_data.iloc[-1]['value'] - revenue_data.iloc[0]['value']) / 
                revenue_data.iloc[0]['value'] * 100
            )
            
            if revenue_growth > 10:
                insights.append({
                    'type': 'positive',
                    'title': 'Strong Revenue Growth',
                    'description': f"Revenue has grown by {revenue_growth:.1f}% over the last 3 months.",
                    'recommendation': 'Consider investing in growth initiatives to maintain this momentum.'
                })
            elif revenue_growth < -10:
                insights.append({
                    'type': 'negative',
                    'title': 'Revenue Decline',
                    'description': f"Revenue has declined by {abs(revenue_growth):.1f}% over the last 3 months.",
                    'recommendation': 'Review sales strategy and market conditions to address the decline.'
                })
        
        # Profit margin insight
        profit_data = df[df['kpi_type'] == 'profit']
        revenue_data = df[df['kpi_type'] == 'revenue']
        
        if not profit_data.empty and not revenue_data.empty:
            latest_profit = profit_data.iloc[-1]['value']
            latest_revenue = revenue_data.iloc[-1]['value']
            
            if latest_revenue > 0:
                profit_margin = (latest_profit / latest_revenue) * 100
                
                if profit_margin < 5:
                    insights.append({
                        'type': 'warning',
                        'title': 'Low Profit Margin',
                        'description': f"Current profit margin is {profit_margin:.1f}%, which is below industry average.",
                        'recommendation': 'Review cost structure and pricing strategy to improve profitability.'
                    })
                elif profit_margin > 25:
                    insights.append({
                        'type': 'positive',
                        'title': 'Strong Profitability',
                        'description': f"Current profit margin is {profit_margin:.1f}%, indicating strong profitability.",
                        'recommendation': 'Consider reinvesting profits into growth opportunities.'
                    })
        
        # Customer acquisition cost insight
        cac_data = df[df['kpi_type'] == 'cac']
        if not cac_data.empty:
            latest_cac = cac_data.iloc[-1]['value']
            avg_cac = cac_data['value'].mean()
            
            if latest_cac > avg_cac * 1.2:
                insights.append({
                    'type': 'warning',
                    'title': 'Rising Customer Acquisition Cost',
                    'description': f"Current CAC (${latest_cac:.2f}) is 20% higher than the 3-month average.",
                    'recommendation': 'Review marketing channels and optimize acquisition strategy.'
                })
        
        return {'insights': insights}
    
    def export_dashboard_data(self, format: str = "csv", start_date: datetime = None,
                             end_date: datetime = None, business_units: List[str] = None,
                             kpi_types: List[str] = None) -> bytes:
        """Export dashboard data in specified format"""
        # Get dashboard data
        dashboard_data = self.get_dashboard_data(
            start_date=start_date,
            end_date=end_date,
            business_units=business_units,
            kpi_types=kpi_types
        )
        
        df = pd.DataFrame(dashboard_data['kpis'])
        
        if format == "csv":
            output = BytesIO()
            df.to_csv(output, index=False)
            return output.getvalue()
        
        elif format == "excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='KPI Data', index=False)
                
                # Add summary sheet
                summary_df = pd.DataFrame([dashboard_data['summary_metrics']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            return output.getvalue()
        
        elif format == "json":
            return json.dumps(dashboard_data).encode('utf-8')
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _calculate_summary_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate summary metrics from KPI data"""
        if df.empty:
            return {}
        
        summary = {}
        
        # Latest values for each KPI type
        latest_kpis = df.groupby('kpi_type')['value'].last()
        
        for kpi_type, value in latest_kpis.items():
            summary[kpi_type] = value
        
        # Growth rates
        for kpi_type in df['kpi_type'].unique():
            kpi_data = df[df['kpi_type'] == kpi_type].sort_values('period')
            
            if len(kpi_data) > 1:
                first_value = kpi_data.iloc[0]['value']
                last_value = kpi_data.iloc[-1]['value']
                
                if first_value != 0:
                    growth_rate = ((last_value - first_value) / first_value) * 100
                    summary[f"{kpi_type}_growth_rate"] = growth_rate
        
        return summary