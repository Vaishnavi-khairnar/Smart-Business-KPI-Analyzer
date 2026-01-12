import streamlit as st
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List


   
def kpi_trend_chart(data: pd.DataFrame, title: str, x_col: str, y_col: str):
       """Create a line chart showing KPI trends over time."""
       fig = px.line(data, x=x_col, y=y_col, title=title)
       
       # Customize chart appearance
       fig.update_layout(
           title_font_size=16,
           title_x=0.02,
           title_y=0.02,
           xaxis_title_font_size=12,
           yaxis_title_font_size=12,
           legend=dict(
               orientation="h",
               yanchor="bottom",
               xanchor="left",
               font=dict(size=10)
           )
       )
       
       # Add hover information
       fig.update_traces(
           hovertemplate="<b>%{y}</b><br>Date: %{x}</br><extra></extra>",
           hoverlabel=dict(
               font=dict(size=10)
           )
       )
       
       return fig
   
def kpi_gauge_chart(value: float, title: str, threshold: Dict[str, Any]):
       """Create a gauge chart for current KPI value."""
       # Determine color based on threshold
       if value >= threshold.get("good", float('inf')):
           color = "green"
       elif value >= threshold.get("warning", float('inf')):
           color = "orange"
       else:
           color = "red"
       
       # Create gauge chart
       fig = px.funnel_area(
           y=[0, value, max(data.max(), value)],
           textposition="inside",
           marker_colors=["red", "orange", "green"]
       )
       
       # Customize appearance
       fig.update_layout(
           title_font_size=16,
           title_x=0.02,
           title_y=0.02,
           font=dict(color="white", size=10)
       )
       
       # Add value and threshold annotations
       fig.add_annotation(
           x=1,
           y=value,
           text=f"{title}: {value}",
           showarrow=True,
           arrowhead=1,
           arrowsize=1,
           arrowcolor="black"
       )
       
       # Add threshold lines
       for threshold_name, threshold_value in threshold.items():
           fig.add_hline(
               y0=threshold_value,
               y1=threshold_value,
               line_dash="dash",
               line_color="gray"
           )
           fig.add_annotation(
               x=0.5,
               y=threshold_value,
               text=threshold_name,
               showarrow=False,
               font=dict(color="gray", size=8)
           )
       
       return fig
   
def kpi_comparison_chart(data: pd.DataFrame, metrics: List[str]):
       """Create a bar chart comparing multiple KPIs."""
       fig = px.bar(data, x=metrics, y="value", title="KPI Comparison")
       
       # Customize appearance
       fig.update_layout(
           title_font_size=16,
           title_x=0.02,
           title_y=0.02,
           xaxis_title_font_size=12,
           yaxis_title_font_size=12,
           legend=dict(
               orientation="h",
               yanchor="bottom",
               xanchor="left",
               font=dict(size=10)
           )
       )
       
       return fig
   
def kpi_pie_chart(data: pd.DataFrame, names_col: str, values_col: str):
       """Create a pie chart for KPI distribution."""
       fig = px.pie(data, names=names_col, values=values_col, title="KPI Distribution")
       
       # Customize appearance
       fig.update_traces(
           textposition="inside",
           textfont=dict(size=10),
           marker=dict(colors=data[names_col])
       )
       
       return fig