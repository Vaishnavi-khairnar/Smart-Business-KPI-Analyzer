import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------
# IMPORT COMPONENTS
# -------------------------
from components.enhanced_charts import EnhancedCharts
from components.filters import AdvancedFilters
from utils.api import APIClient
from utils.session import (
    is_authenticated,
    get_token,
    logout
)

# =========================
# STREAMLIT PAGE ENTRY (REQUIRED)
# =========================
def show():
    """
    Entry point required by app router
    """
    render_dashboard()


# =========================
# MAIN DASHBOARD RENDER
# =========================
def render_dashboard():
    """Render the enhanced dashboard page"""

    st.title("📊 Enhanced KPI Dashboard")
    st.markdown("---")

    # -------------------------
    # AUTH CHECK
    # -------------------------
    if not is_authenticated():
        st.error("🔒 Please login to access the dashboard.")
        st.stop()

    # -------------------------
    # INIT API CLIENT
    # -------------------------
    api_client = APIClient()

    # -------------------------
    # SIDEBAR FILTERS
    # -------------------------
    with st.sidebar:
        st.header("🔍 Filters")

        # Logout button
        if st.button("🚪 Logout"):
            logout()
            st.rerun()

        st.markdown("---")

        # Date range filter
        start_date, end_date = AdvancedFilters.date_range_filter()

        # Business unit filter
        business_units = api_client.get_business_units()
        selected_units = (
            AdvancedFilters.business_unit_filter(business_units)
            if business_units else []
        )

        # KPI type filter
        kpi_types = api_client.get_kpi_types()
        selected_kpis = (
            AdvancedFilters.kpi_type_filter(kpi_types)
            if kpi_types else []
        )

        # Comparison filter
        comparison_settings = AdvancedFilters.comparison_filter()

        # Advanced options
        advanced_options = AdvancedFilters.advanced_options_filter()

    # -------------------------
    # REFRESH BUTTON
    # -------------------------
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    st.markdown("---")

    # -------------------------
    # FETCH DATA
    # -------------------------
    try:
        kpi_data = api_client.get_kpis(
            start_date=start_date,
            end_date=end_date,
            business_units=selected_units,
            kpi_types=selected_kpis
        )

        if kpi_data is None or kpi_data.empty:
            st.warning("⚠️ No KPI data available for selected filters.")
            return

        # -------------------------
        # DASHBOARD TABS
        # -------------------------
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview",
            "📊 Detailed Analysis",
            "🏢 Business Units",
            "👥 Customer Segments",
            "🔮 Advanced Analytics"
        ])

        with tab1:
            render_overview_tab(kpi_data, comparison_settings, advanced_options)

        with tab2:
            render_detailed_analysis_tab(kpi_data, advanced_options)

        with tab3:
            render_business_units_tab(kpi_data)

        with tab4:
            render_customer_segments_tab(kpi_data)

        with tab5:
            render_advanced_analytics_tab(kpi_data)

    except Exception as e:
        st.error("❌ Failed to load dashboard data")
        st.exception(e)


# =========================
# OVERVIEW TAB
# =========================
def render_overview_tab(kpi_data, comparison_settings, advanced_options):
    st.header("📈 KPI Overview")

    metrics = calculate_kpi_metrics(kpi_data)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Revenue", f"${metrics.get('revenue', 0):,.2f}")

    with col2:
        st.metric("Profit", f"${metrics.get('profit', 0):,.2f}")

    with col3:
        st.metric("CAC", f"${metrics.get('cac', 0):,.2f}")

    with col4:
        st.metric("Retention Rate", f"{metrics.get('retention_rate', 0):.1f}%")

    st.markdown("---")

    st.subheader("Revenue Trend")
    EnhancedCharts.revenue_trend_chart(
        kpi_data[kpi_data["kpi_type"] == "revenue"]
    )


# =========================
# DETAILED ANALYSIS TAB
# =========================
def render_detailed_analysis_tab(kpi_data, advanced_options):
    st.header("📊 Detailed KPI Analysis")

    EnhancedCharts.kpi_comparison_chart(kpi_data)
    EnhancedCharts.correlation_heatmap(kpi_data)


# =========================
# BUSINESS UNITS TAB
# =========================
def render_business_units_tab(kpi_data):
    st.header("🏢 Business Unit Performance")

    if "business_unit" not in kpi_data.columns:
        st.warning("Business unit data not available.")
        return

    EnhancedCharts.business_unit_performance(kpi_data, metric="revenue")
    EnhancedCharts.business_unit_performance(kpi_data, metric="profit")


# =========================
# CUSTOMER SEGMENTS TAB
# =========================
def render_customer_segments_tab(kpi_data):
    st.header("👥 Customer Segment Analysis")

    if "segment" not in kpi_data.columns:
        st.warning("Customer segment data not available.")
        return

    EnhancedCharts.customer_segment_analysis(kpi_data)


# =========================
# ADVANCED ANALYTICS TAB
# =========================
def render_advanced_analytics_tab(kpi_data):
    st.header("🔮 Advanced Analytics")

    revenue_data = kpi_data[kpi_data["kpi_type"] == "revenue"]
    EnhancedCharts.trend_analysis_with_forecast(revenue_data)


# =========================
# HELPERS
# =========================
def calculate_kpi_metrics(kpi_data):
    return kpi_data.groupby("kpi_type")["value"].last().to_dict()
