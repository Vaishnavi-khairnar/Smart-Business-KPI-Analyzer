import streamlit as st
from components.reports import ReportComponents
from utils.session import check_authentication

def render_reports_page():
    """Render the reports page"""
    # Check authentication
    if not check_authentication():
        return
    
    st.title("📊 Reports & Exports")
    st.markdown("---")
    
    # Create tabs for different report functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Generate Report", 
        "⏰ Scheduled Reports", 
        "📋 Templates", 
        "📚 History"
    ])
    
    with tab1:
        ReportComponents.report_generator()
    
    with tab2:
        ReportComponents.scheduled_reports()
    
    with tab3:
        ReportComponents.report_templates()
    
    with tab4:
        ReportComponents.report_history()

# Run the reports page
if __name__ == "__main__":
    render_reports_page()