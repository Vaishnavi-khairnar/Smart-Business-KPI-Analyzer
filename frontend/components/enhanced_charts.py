import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class EnhancedCharts:
    """Enhanced chart components with advanced visualization capabilities"""
    
    @staticmethod
    def revenue_trend_chart(data, period='monthly'):
        """
        Create an interactive revenue trend chart with comparison options
        
        Args:
            data: DataFrame with revenue data
            period: 'daily', 'weekly', 'monthly', or 'yearly'
        """
        # Group data by period
        if period == 'daily':
            data['period'] = data['date'].dt.date
        elif period == 'weekly':
            data['period'] = data['date'].dt.to_period('W').dt.start_time
        elif period == 'monthly':
            data['period'] = data['date'].dt.to_period('M').dt.start_time
        else:  # yearly
            data['period'] = data['date'].dt.to_period('Y').dt.start_time
        
        # Aggregate revenue by period
        period_data = data.groupby('period')['revenue'].sum().reset_index()
        
        # Create the chart
        fig = px.line(
            period_data, 
            x='period', 
            y='revenue',
            title=f'Revenue Trend ({period.capitalize()})',
            labels={'revenue': 'Revenue ($)', 'period': period.capitalize()},
            template='plotly_white'
        )
        
        # Add annotations for significant events
        fig.add_annotation(
            x=period_data['period'].iloc[-1],
            y=period_data['revenue'].iloc[-1],
            text=f"${period_data['revenue'].iloc[-1]:,.2f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="gray"
        )
        
        # Add trend line
        fig.update_layout(
            xaxis_title=period.capitalize(),
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def kpi_comparison_chart(kpi_data, kpi_types=None):
        """
        Create a comparison chart for multiple KPIs
        
        Args:
            kpi_data: DataFrame with KPI data
            kpi_types: List of KPI types to include
        """
        if kpi_types is None:
            kpi_types = ['revenue', 'profit', 'cac', 'retention_rate']
        
        # Filter data for selected KPIs
        filtered_data = kpi_data[kpi_data['kpi_type'].isin(kpi_types)]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=tuple([kpi.replace('_', ' ').title() for kpi in kpi_types]),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Add traces for each KPI
        for i, kpi in enumerate(kpi_types):
            kpi_df = filtered_data[filtered_data['kpi_type'] == kpi]
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            fig.add_trace(
                go.Scatter(
                    x=kpi_df['period'],
                    y=kpi_df['value'],
                    mode='lines+markers',
                    name=kpi.replace('_', ' ').title(),
                    line=dict(width=2)
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="KPI Comparison Dashboard",
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def business_unit_performance(data, metric='revenue'):
        """
        Create a business unit performance chart
        
        Args:
            data: DataFrame with business unit data
            metric: Metric to visualize ('revenue', 'profit', 'growth', etc.)
        """
        # Aggregate data by business unit
        unit_data = data.groupby('business_unit')[metric].sum().reset_index()
        unit_data = unit_data.sort_values(metric, ascending=False)
        
        # Create horizontal bar chart
        fig = px.bar(
            unit_data,
            x=metric,
            y='business_unit',
            orientation='h',
            title=f'Business Unit Performance - {metric.title()}',
            labels={metric: metric.title(), 'business_unit': 'Business Unit'},
            color=metric,
            color_continuous_scale='Blues',
            template='plotly_white'
        )
        
        # Add percentage labels
        total = unit_data[metric].sum()
        unit_data['percentage'] = (unit_data[metric] / total * 100).round(1)
        
        fig.update_traces(
            texttemplate='%{x:,.0f} (%{customdata:.1f}%)',
            textposition='outside',
            customdata=unit_data['percentage']
        )
        
        fig.update_layout(
            xaxis_title=metric.title(),
            yaxis_title='Business Unit',
            height=max(400, len(unit_data) * 40),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def customer_segment_analysis(data):
        """
        Create a customer segment analysis chart
        
        Args:
            data: DataFrame with customer segment data
        """
        # Aggregate data by segment
        segment_data = data.groupby('segment').agg({
            'customers': 'sum',
            'revenue': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        # Create bubble chart
        fig = px.scatter(
            segment_data,
            x='customers',
            y='revenue',
            size='profit',
            color='segment',
            title='Customer Segment Analysis',
            labels={
                'customers': 'Number of Customers',
                'revenue': 'Revenue ($)',
                'profit': 'Profit ($)',
                'segment': 'Customer Segment'
            },
            template='plotly_white',
            hover_name='segment',
            hover_data={
                'customers': ':,',
                'revenue': '$:,.2f',
                'profit': '$:,.2f'
            }
        )
        
        fig.update_layout(
            xaxis_title='Number of Customers',
            yaxis_title='Revenue ($)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def trend_analysis_with_forecast(data, periods=12):
        """
        Create a trend analysis chart with forecast
        
        Args:
            data: Historical data
            periods: Number of periods to forecast
        """
        # Simple linear regression for demonstration
        # In production, use more sophisticated forecasting methods
        data['date_ordinal'] = data['date'].apply(lambda x: x.toordinal())
        
        # Fit linear regression
        coeffs = np.polyfit(data['date_ordinal'], data['value'], 1)
        trend_line = np.poly1d(coeffs)
        
        # Create forecast dates
        last_date = data['date'].max()
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=periods,
            freq='M'
        )
        
        # Generate forecast values
        forecast_ordinal = [d.toordinal() for d in forecast_dates]
        forecast_values = trend_line(forecast_ordinal)
        
        # Create the chart
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['value'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Add trend line
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=trend_line(data['date_ordinal']),
            mode='lines',
            name='Trend',
            line=dict(color='lightblue', dash='dash')
        ))
        
        # Add forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_values,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title='Trend Analysis with Forecast',
            xaxis_title='Date',
            yaxis_title='Value',
            template='plotly_white',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def correlation_heatmap(data):
        """
        Create a correlation heatmap for KPIs
        
        Args:
            data: DataFrame with KPI data
        """
        # Pivot data for correlation analysis
        pivot_data = data.pivot_table(
            index='period',
            columns='kpi_type',
            values='value',
            aggfunc='mean'
        )
        
        # Calculate correlation matrix
        corr_matrix = pivot_data.corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            title='KPI Correlation Matrix',
            color_continuous_scale='RdBu_r',
            aspect='auto',
            template='plotly_white'
        )
        
        fig.update_layout(
            xaxis_title='KPI Type',
            yaxis_title='KPI Type'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def performance_gauge(value, title, max_value, thresholds=None):
        """
        Create a performance gauge chart
        
        Args:
            value: Current value
            title: Gauge title
            max_value: Maximum value for the gauge
            thresholds: Dictionary with threshold values and colors
        """
        if thresholds is None:
            thresholds = {
                'low': {'value': max_value * 0.3, 'color': 'red'},
                'medium': {'value': max_value * 0.7, 'color': 'yellow'},
                'high': {'value': max_value, 'color': 'green'}
            }
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, thresholds['low']['value']], 'color': thresholds['low']['color']},
                    {'range': [thresholds['low']['value'], thresholds['medium']['value']], 'color': thresholds['medium']['color']},
                    {'range': [thresholds['medium']['value'], thresholds['high']['value']], 'color': thresholds['high']['color']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)