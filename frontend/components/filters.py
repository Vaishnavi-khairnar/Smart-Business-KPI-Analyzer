import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

class AdvancedFilters:
    """Advanced filtering components for dashboard"""
    
    @staticmethod
    def date_range_filter(key_prefix="date"):
        """
        Create an advanced date range filter with preset options
        
        Args:
            key_prefix: Prefix for widget keys
            
        Returns:
            tuple: (start_date, end_date)
        """
        st.subheader("📅 Date Range Filter")
        
        # Preset options
        preset_options = {
            "Last 7 Days": 7,
            "Last 30 Days": 30,
            "Last 90 Days": 90,
            "Last 6 Months": 180,
            "Last 12 Months": 365,
            "Year to Date": None,
            "Custom Range": None
        }
        
        selected_preset = st.selectbox(
            "Select Preset",
            options=list(preset_options.keys()),
            key=f"{key_prefix}_preset"
        )
        
        # Calculate dates based on preset
        end_date = datetime.now()
        
        if selected_preset == "Year to Date":
            start_date = datetime(end_date.year, 1, 1)
        elif selected_preset == "Custom Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=end_date - timedelta(days=30),
                    key=f"{key_prefix}_start"
                )
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=end_date,
                    key=f"{key_prefix}_end"
                )
        else:
            days = preset_options[selected_preset]
            start_date = end_date - timedelta(days=days)
        
        if selected_preset != "Custom Range":
            st.info(f"Selected Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        return start_date, end_date
    
    @staticmethod
    def business_unit_filter(business_units, key_prefix="bu"):
        """
        Create a business unit filter with search functionality
        
        Args:
            business_units: List of available business units
            key_prefix: Prefix for widget keys
            
        Returns:
            list: Selected business units
        """
        st.subheader("🏢 Business Unit Filter")
        
        # Search functionality
        search_term = st.text_input(
            "Search Business Units",
            key=f"{key_prefix}_search"
        )
        
        # Filter business units based on search
        if search_term:
            filtered_units = [bu for bu in business_units if search_term.lower() in bu.lower()]
        else:
            filtered_units = business_units
        
        # Multi-select with select all option
        select_all = st.checkbox("Select All", key=f"{key_prefix}_select_all")
        
        if select_all:
            selected_units = filtered_units
        else:
            selected_units = st.multiselect(
                "Select Business Units",
                options=filtered_units,
                default=filtered_units[:5],  # Default to first 5
                key=f"{key_prefix}_multiselect"
            )
        
        return selected_units
    
    @staticmethod
    def kpi_type_filter(kpi_types, key_prefix="kpi"):
        """
        Create a KPI type filter with grouping
        
        Args:
            kpi_types: List of available KPI types
            key_prefix: Prefix for widget keys
            
        Returns:
            list: Selected KPI types
        """
        st.subheader("📊 KPI Type Filter")
        
        # Group KPIs by category
        kpi_categories = {
            "Financial": ["revenue", "profit", "profit_margin", "roi"],
            "Customer": ["cac", "retention_rate", "customer_lifetime_value", "churn_rate"],
            "Operational": ["inventory_turnover", "order_fulfillment_time", "production_efficiency"],
            "Marketing": ["conversion_rate", "marketing_roi", "lead_to_customer_rate"]
        }
        
        selected_kpis = []
        
        for category, kpis in kpi_categories.items():
            with st.expander(f"{category} KPIs"):
                # Filter available KPIs for this category
                available_kpis = [kpi for kpi in kpis if kpi in kpi_types]
                
                if available_kpis:
                    category_selected = st.multiselect(
                        f"Select {category} KPIs",
                        options=available_kpis,
                        default=available_kpis[:2],  # Default to first 2
                        key=f"{key_prefix}_{category.lower()}"
                    )
                    selected_kpis.extend(category_selected)
                else:
                    st.info(f"No {category.lower()} KPIs available")
        
        return selected_kpis
    
    @staticmethod
    def numeric_range_filter(min_value, max_value, label, key_prefix="numeric"):
        """
        Create a numeric range filter with slider
        
        Args:
            min_value: Minimum possible value
            max_value: Maximum possible value
            label: Label for the filter
            key_prefix: Prefix for widget keys
            
        Returns:
            tuple: (selected_min, selected_max)
        """
        st.subheader(f"🔢 {label}")
        
        # Slider for range selection
        selected_range = st.slider(
            f"Select {label} Range",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
            key=f"{key_prefix}_slider"
        )
        
        # Display selected values
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Min", f"{selected_range[0]:,.2f}")
        with col2:
            st.metric("Max", f"{selected_range[1]:,.2f}")
        
        return selected_range
    
    @staticmethod
    def comparison_filter(key_prefix="comparison"):
        """
        Create a comparison period filter
        
        Args:
            key_prefix: Prefix for widget keys
            
        Returns:
            dict: Comparison settings
        """
        st.subheader("📈 Comparison Settings")
        
        # Enable comparison
        enable_comparison = st.checkbox(
            "Enable Period Comparison",
            key=f"{key_prefix}_enable"
        )
        
        comparison_settings = {
            'enabled': enable_comparison
        }
        
        if enable_comparison:
            # Comparison type
            comparison_type = st.selectbox(
                "Comparison Type",
                options=["Previous Period", "Same Period Last Year", "Custom Period"],
                key=f"{key_prefix}_type"
            )
            
            comparison_settings['type'] = comparison_type
            
            if comparison_type == "Custom Period":
                col1, col2 = st.columns(2)
                with col1:
                    comp_start = st.date_input(
                        "Comparison Start Date",
                        value=datetime.now() - timedelta(days=60),
                        key=f"{key_prefix}_comp_start"
                    )
                with col2:
                    comp_end = st.date_input(
                        "Comparison End Date",
                        value=datetime.now() - timedelta(days=30),
                        key=f"{key_prefix}_comp_end"
                    )
                
                comparison_settings['start_date'] = comp_start
                comparison_settings['end_date'] = comp_end
        
        return comparison_settings
    
    @staticmethod
    def advanced_options_filter(key_prefix="advanced"):
        """
        Create advanced options filter
        
        Args:
            key_prefix: Prefix for widget keys
            
        Returns:
            dict: Advanced options
        """
        st.subheader("⚙️ Advanced Options")
        
        with st.expander("Display Options"):
            # Chart type
            chart_type = st.selectbox(
                "Chart Type",
                options=["Line", "Bar", "Area", "Scatter"],
                key=f"{key_prefix}_chart_type"
            )
            
            # Aggregation level
            aggregation = st.selectbox(
                "Aggregation Level",
                options=["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"],
                key=f"{key_prefix}_aggregation"
            )
            
            # Show trend line
            show_trend = st.checkbox(
                "Show Trend Line",
                value=True,
                key=f"{key_prefix}_trend"
            )
            
            # Show forecast
            show_forecast = st.checkbox(
                "Show Forecast",
                value=False,
                key=f"{key_prefix}_forecast"
            )
        
        with st.expander("Data Options"):
            # Include outliers
            include_outliers = st.checkbox(
                "Include Outliers",
                value=True,
                key=f"{key_prefix}_outliers"
            )
            
            # Data smoothing
            smoothing = st.slider(
                "Data Smoothing",
                min_value=0,
                max_value=10,
                value=0,
                help="Higher values create smoother lines",
                key=f"{key_prefix}_smoothing"
            )
            
            # Confidence interval
            show_confidence = st.checkbox(
                "Show Confidence Interval",
                value=False,
                key=f"{key_prefix}_confidence"
            )
        
        return {
            'chart_type': chart_type.lower(),
            'aggregation': aggregation.lower(),
            'show_trend': show_trend,
            'show_forecast': show_forecast,
            'include_outliers': include_outliers,
            'smoothing': smoothing,
            'show_confidence': show_confidence
        }