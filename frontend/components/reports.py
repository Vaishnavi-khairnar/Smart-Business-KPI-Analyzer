import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import io
import base64

from utils.api import APIClient
from utils.session import get_auth_token

class ReportComponents:
    """Components for report generation and management"""
    
    @staticmethod
    def report_generator():
        """Display report generation interface"""
        st.header("📄 Report Generator")
        st.markdown("Generate custom reports in various formats.")
        
        # Get available filters
        api_client = APIClient()
        
        # Get business units and KPI types
        try:
            business_units = api_client.get_business_units()
            kpi_types = api_client.get_kpi_types()
        except:
            business_units = []
            kpi_types = []
        
        # Report configuration
        with st.form("report_config"):
            st.subheader("Report Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Date range
                st.subheader("Date Range")
                start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
                end_date = st.date_input("End Date", value=datetime.now())
                
                # Business units
                st.subheader("Business Units")
                selected_bus = st.multiselect(
                    "Select Business Units",
                    options=business_units,
                    default=business_units[:3] if business_units else []
                )
            
            with col2:
                # KPI types
                st.subheader("KPI Types")
                selected_kpis = st.multiselect(
                    "Select KPI Types",
                    options=kpi_types,
                    default=kpi_types[:3] if kpi_types else []
                )
                
                # Report options
                st.subheader("Report Options")
                include_summary = st.checkbox("Include Summary Statistics", value=True)
                include_charts = st.checkbox("Include Charts", value=True)
            
            # Export format
            st.subheader("Export Format")
            export_format = st.selectbox(
                "Select Format",
                options=["CSV", "Excel", "PDF"],
                index=1  # Default to Excel
            )
            
            # Generate button
            submitted = st.form_submit_button("Generate Report", type="primary")
            
            if submitted:
                if not selected_bus:
                    st.error("Please select at least one business unit.")
                elif not selected_kpis:
                    st.error("Please select at least one KPI type.")
                else:
                    # Generate report
                    with st.spinner("Generating report..."):
                        try:
                            # Prepare parameters
                            params = {
                                'start_date': start_date.isoformat(),
                                'end_date': end_date.isoformat(),
                                'business_units': selected_bus,
                                'kpi_types': selected_kpis
                            }
                            
                            if export_format == "CSV":
                                params['include_summary'] = include_summary
                                response = requests.get(
                                    f"{api_client.base_url}/reports/export/csv",
                                    params=params,
                                    headers=api_client._get_auth_headers()
                                )
                            elif export_format == "Excel":
                                params['include_charts'] = include_charts
                                response = requests.get(
                                    f"{api_client.base_url}/reports/export/excel",
                                    params=params,
                                    headers=api_client._get_auth_headers()
                                )
                            else:  # PDF
                                params['template'] = 'standard'
                                response = requests.get(
                                    f"{api_client.base_url}/reports/export/pdf",
                                    params=params,
                                    headers=api_client._get_auth_headers()
                                )
                            
                            if response.status_code == 200:
                                # Provide download link
                                st.success("Report generated successfully!")
                                
                                # Create download button
                                filename = f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}"
                                st.download_button(
                                    label=f"Download {export_format} Report",
                                    data=response.content,
                                    file_name=filename,
                                    mime=self._get_mime_type(export_format)
                                )
                            else:
                                st.error(f"Error generating report: {response.text}")
                        
                        except Exception as e:
                            st.error(f"Error generating report: {str(e)}")
    
    @staticmethod
    def scheduled_reports():
        """Display scheduled reports management"""
        st.header("⏰ Scheduled Reports")
        st.markdown("Manage your scheduled reports.")
        
        api_client = APIClient()
        
        # Get scheduled reports
        try:
            scheduled_reports = api_client.get_scheduled_reports()
        except:
            scheduled_reports = []
        
        if scheduled_reports:
            # Display existing scheduled reports
            for report in scheduled_reports:
                with st.expander(f"{report['name']} ({report['frequency']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Status", report['status'])
                    
                    with col2:
                        st.metric("Next Run", report['next_run'][:10])
                    
                    with col3:
                        if st.button(f"Delete {report['id']}", key=f"delete_{report['id']}"):
                            try:
                                api_client.delete_scheduled_report(report['id'])
                                st.success(f"Report {report['id']} deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting report: {str(e)}")
        else:
            st.info("No scheduled reports found.")
        
        # Add new scheduled report
        st.subheader("Schedule New Report")
        
        with st.form("schedule_report"):
            col1, col2 = st.columns(2)
            
            with col1:
                report_name = st.text_input("Report Name")
                frequency = st.selectbox(
                    "Frequency",
                    options=["daily", "weekly", "monthly"]
                )
            
            with col2:
                recipients = st.text_area("Email Recipients (one per line)")
                export_format = st.selectbox(
                    "Export Format",
                    options=["CSV", "Excel", "PDF"]
                )
            
            # Report configuration (same as generator)
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
            end_date = st.date_input("End Date", value=datetime.now())
            
            try:
                business_units = api_client.get_business_units()
                kpi_types = api_client.get_kpi_types()
            except:
                business_units = []
                kpi_types = []
            
            selected_bus = st.multiselect(
                "Select Business Units",
                options=business_units,
                default=business_units[:3] if business_units else []
            )
            
            selected_kpis = st.multiselect(
                "Select KPI Types",
                options=kpi_types,
                default=kpi_types[:3] if kpi_types else []
            )
            
            # Schedule button
            submitted = st.form_submit_button("Schedule Report", type="primary")
            
            if submitted:
                if not report_name:
                    st.error("Please enter a report name.")
                elif not selected_bus:
                    st.error("Please select at least one business unit.")
                elif not selected_kpis:
                    st.error("Please select at least one KPI type.")
                else:
                    # Create report configuration
                    report_config = {
                        'name': report_name,
                        'frequency': frequency,
                        'recipients': [r.strip() for r in recipients.split('\n') if r.strip()],
                        'export_format': export_format,
                        'filters': {
                            'start_date': start_date.isoformat(),
                            'end_date': end_date.isoformat(),
                            'business_units': selected_bus,
                            'kpi_types': selected_kpis
                        }
                    }
                    
                    try:
                        scheduled_report = api_client.schedule_report(report_config)
                        st.success(f"Report '{report_name}' scheduled successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error scheduling report: {str(e)}")
    
    @staticmethod
    def report_templates():
        """Display available report templates"""
        st.header("📋 Report Templates")
        st.markdown("Choose from predefined report templates.")
        
        api_client = APIClient()
        
        # Get available templates
        try:
            templates = api_client.get_report_templates()
        except:
            templates = []
        
        if templates:
            # Display templates in a grid
            cols = st.columns(min(3, len(templates)))
            
            for i, template in enumerate(templates):
                with cols[i % 3]:
                    st.markdown(f"### {template['name']}")
                    st.markdown(template['description'])
                    
                    # Show available formats
                    formats_str = ", ".join(template['formats'])
                    st.markdown(f"**Formats:** {formats_str}")
                    
                    # Use template button
                    if st.button(f"Use Template", key=f"use_template_{template['id']}"):
                        # Store template selection in session state
                        st.session_state['selected_template'] = template
                        st.success(f"Template '{template['name']}' selected!")
        else:
            st.info("No report templates available.")
    
    @staticmethod
    def report_history():
        """Display report generation history"""
        st.header("📚 Report History")
        st.markdown("View and download previously generated reports.")
        
        # This is a placeholder - in a real implementation, you would
        # fetch from a database table of generated reports
        report_history = [
            {
                "id": "report_1",
                "name": "Monthly KPI Report",
                "format": "Excel",
                "generated_at": "2023-01-31T14:30:00",
                "generated_by": "john.doe@example.com",
                "size": "2.5 MB"
            },
            {
                "id": "report_2",
                "name": "Weekly Executive Summary",
                "format": "PDF",
                "generated_at": "2023-01-30T09:15:00",
                "generated_by": "jane.smith@example.com",
                "size": "1.2 MB"
            }
        ]
        
        if report_history:
            # Display history as a table
            for report in report_history:
                with st.expander(f"{report['name']} ({report['format']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Generated", report['generated_at'][:10])
                    
                    with col2:
                        st.metric("By", report['generated_by'])
                    
                    with col3:
                        st.metric("Size", report['size'])
                    
                    # Download button
                    if st.button(f"Download {report['id']}", key=f"download_{report['id']}"):
                        st.success(f"Downloading {report['name']}...")
                        # In a real implementation, you would fetch and download the file
        else:
            st.info("No report history found.")
    
    @staticmethod
    def _get_mime_type(format: str) -> str:
        """Get MIME type for export format"""
        mime_types = {
            "CSV": "text/csv",
            "Excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "PDF": "application/pdf"
        }
        return mime_types.get(format, "application/octet-stream")