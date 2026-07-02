"""
Enterprise LMS Dashboard - Main Application
Built with Streamlit for interactive training compliance tracking
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    APP_NAME, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE,
    DATA_FILE, ALERT_THRESHOLDS, FEATURES
)
from data_manager import get_data_manager
from dashboard_components import DashboardComponents
from generate_data import DataGenerator

# ============= LOGGING SETUP =============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= PAGE CONFIGURATION =============
st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)

# ============= CUSTOM STYLING =============
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0066CC;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066CC;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# ============= SESSION STATE INITIALIZATION =============
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = get_data_manager()

if 'df' not in st.session_state:
    st.session_state.df = None

if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None

if 'filters' not in st.session_state:
    st.session_state.filters = {}

# ============= SIDEBAR NAVIGATION =============
def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown(f"# {APP_NAME}")
        st.divider()
        
        # Navigation
        page = st.radio(
            "Select Page",
            options=['📊 Dashboard', '📋 Training Tracker', '📈 Analytics', '📄 Reports', '⚙️ Settings'],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Data management
        st.subheader("📁 Data Management")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.df = None
            st.rerun()
        
        if st.button("📥 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating data..."):
                generator = DataGenerator(num_records=500)
                generator.save_to_csv(DATA_FILE)
                st.session_state.df = None
                st.success("Sample data generated successfully!")
                st.rerun()
        
        st.divider()
        
        # Info
        st.caption("**Version:** 1.0.0")
        st.caption("**Last Updated:** " + datetime.now().strftime("%B %d, %Y"))
        
        return page

# ============= MAIN DASHBOARD PAGE =============
def render_dashboard():
    """Render main dashboard page"""
    st.markdown('<h1 class="main-header">📊 Training Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available. Please generate sample data from the sidebar.")
        return
    
    # Filters
    with st.sidebar:
        st.subheader("🔍 Filters")
        
        search = st.text_input("Search by name or ID", "")
        departments = st.multiselect("Department", options=dm.get_departments(df), default=[])
        statuses = st.multiselect("Status", options=dm.get_statuses(df), default=[])
        
        filters = {
            'search': search,
            'department': departments if departments else None,
            'status': statuses if statuses else None
        }
    
    # Apply filters
    df_filtered = dm.apply_filters(df, filters)
    
    # Metrics
    metrics = dm.get_summary_metrics(df_filtered)
    
    # KPI Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total Trainings",
            metrics.get('total_records', 0),
            delta=f"Employees: {metrics.get('unique_employees', 0)}"
        )
    
    with col2:
        st.metric(
            "✅ Completion Rate",
            f"{metrics.get('completion_rate', 0)}%",
            delta=f"Completed: {metrics.get('completed', 0)}"
        )
    
    with col3:
        st.metric(
            "🎯 Compliance Rate",
            f"{metrics.get('compliance_rate', 0)}%",
            delta=f"Compliant: {metrics.get('unique_employees', 0)}"
        )
    
    with col4:
        st.metric(
            "⚠️ Overdue",
            metrics.get('overdue', 0),
            delta=f"Failed: {metrics.get('failed', 0)}"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Status Distribution")
        DashboardComponents.render_status_distribution(df_filtered)
    
    with col2:
        st.subheader("Compliance Status Distribution")
        DashboardComponents.render_compliance_distribution(df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Completion Rate by Department")
        DashboardComponents.render_department_performance(df_filtered)
    
    with col2:
        st.subheader("Completion Rate by Category")
        DashboardComponents.render_training_category_performance(df_filtered)
    
    # Additional metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alert Distribution")
        DashboardComponents.render_alert_distribution(df_filtered)
    
    with col2:
        st.subheader("Score Distribution")
        DashboardComponents.render_score_distribution(df_filtered)

# ============= TRAINING TRACKER PAGE =============
def render_training_tracker():
    """Render training tracker page"""
    st.markdown('<h1 class="main-header">📋 Training Tracker</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Overdue Trainings", "Expiring Certifications", "All Trainings"])
    
    with tab1:
        st.subheader("🔴 Overdue Trainings")
        overdue_df = dm.get_overdue_trainings(df)
        
        if len(overdue_df) == 0:
            st.success("No overdue trainings! ✅")
        else:
            st.warning(f"⚠️ {len(overdue_df)} overdue trainings found")
            DashboardComponents.render_data_table(overdue_df, "Overdue Trainings")
    
    with tab2:
        st.subheader("📅 Expiring Certifications (30 days)")
        expiring_df = dm.get_expiring_certifications(df, days=30)
        
        if len(expiring_df) == 0:
            st.success("No certifications expiring soon! ✅")
        else:
            st.warning(f"⚠️ {len(expiring_df)} certifications expiring within 30 days")
            DashboardComponents.render_data_table(expiring_df, "Expiring Certifications")
    
    with tab3:
        st.subheader("📋 All Training Records")
        
        # Filters
        with st.sidebar:
            st.subheader("🔍 Filters")
            
            search = st.text_input("Search", key="tracker_search")
            departments = st.multiselect("Department", options=dm.get_departments(df), key="tracker_dept")
            statuses = st.multiselect("Status", options=dm.get_statuses(df), key="tracker_status")
            
            filters = {
                'search': search,
                'department': departments if departments else None,
                'status': statuses if statuses else None
            }
        
        df_filtered = dm.apply_filters(df, filters)
        DashboardComponents.render_data_table(df_filtered, f"All Trainings ({len(df_filtered)} records)", max_rows=100)

# ============= ANALYTICS PAGE =============
def render_analytics():
    """Render analytics page"""
    st.markdown('<h1 class="main-header">📈 Analytics</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Department Analysis", "Location Analysis", "Timeline"])
    
    with tab1:
        st.subheader("🏢 Department Analysis")
        
        dept_summary = dm.get_department_summary(df)
        st.dataframe(dept_summary, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Completion Rate by Department")
            DashboardComponents.render_department_performance(df)
        
        with col2:
            st.subheader("Average Score by Department")
            dept_scores = df.groupby('Department')['Score'].mean().sort_values(ascending=False)
            st.bar_chart(dept_scores)
    
    with tab2:
        st.subheader("📍 Location Analysis")
        
        loc_summary = dm.get_location_summary(df)
        st.dataframe(loc_summary, use_container_width=True)
        
        st.subheader("Performance by Location")
        DashboardComponents.render_location_performance(df)
    
    with tab3:
        st.subheader("📅 Timeline Analysis")
        
        # Monthly statistics
        monthly_stats = df.groupby(df['Planned Date'].dt.to_period('M')).size()
        st.subheader("Training Volume Over Time")
        st.line_chart(monthly_stats)
        
        # Completion trends
        completion_trends = df.groupby(df['Completion Date'].dt.to_period('M')).size()
        st.subheader("Completion Trends")
        st.line_chart(completion_trends)

# ============= REPORTS PAGE =============
def render_reports():
    """Render reports page"""
    st.markdown('<h1 class="main-header">📄 Reports</h1>', unsafe_allow_html=True)
    
    dm = st.session_state.data_manager
    df = dm.load_data(DATA_FILE)
    
    if df is None or len(df) == 0:
        st.warning("No data available.")
        return
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Compliance Summary",
            "Training Status",
            "Department Performance",
            "Employee Compliance",
            "Expiry Calendar"
        ]
    )
    
    if report_type == "Compliance Summary":
        st.subheader("📋 Compliance Summary Report")
        metrics = dm.get_summary_metrics(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", metrics.get('total_records', 0))
        with col2:
            st.metric("Completion Rate %", f"{metrics.get('completion_rate', 0)}")
        with col3:
            st.metric("Compliance Rate %", f"{metrics.get('compliance_rate', 0)}")
        with col4:
            st.metric("Avg Score", f"{metrics.get('average_score', 0)}")
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv,
            file_name="compliance_summary.csv",
            mime="text/csv"
        )
    
    elif report_type == "Training Status":
        st.subheader("📊 Training Status Report")
        
        status_counts = df['Status'].value_counts()
        st.dataframe(status_counts, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Status Distribution")
            DashboardComponents.render_status_distribution(df)
        with col2:
            st.write("Status Details")
            status_df = df.groupby('Status').agg({
                'Employee ID': 'count',
                'Score': 'mean'
            }).round(2)
            status_df.columns = ['Count', 'Avg Score']
            st.dataframe(status_df, use_container_width=True)
    
    elif report_type == "Department Performance":
        st.subheader("🏢 Department Performance Report")
        dept_summary = dm.get_department_summary(df)
        st.dataframe(dept_summary, use_container_width=True)
        
        csv = dept_summary.to_csv()
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv,
            file_name="department_performance.csv",
            mime="text/csv"
        )
    
    elif report_type == "Employee Compliance":
        st.subheader("👥 Employee Compliance Report")
        
        employee_id = st.selectbox("Select Employee", options=dm.get_employee_list(df))
        
        if employee_id:
            emp_compliance = dm.get_compliance_detail(df, employee_id)
            st.dataframe(emp_compliance, use_container_width=True)
            
            csv = emp_compliance.to_csv(index=False)
            st.download_button(
                label="📥 Download Employee Report as CSV",
                data=csv,
                file_name=f"employee_{employee_id}_compliance.csv",
                mime="text/csv"
            )
    
    elif report_type == "Expiry Calendar":
        st.subheader("📅 Certificate Expiry Calendar")
        expiring_df = dm.get_expiring_certifications(df, days=90)
        
        if len(expiring_df) > 0:
            st.dataframe(expiring_df, use_container_width=True)
        else:
            st.success("No certifications expiring in the next 90 days!")

# ============= SETTINGS PAGE =============
def render_settings():
    """Render settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["General", "Data", "About"])
    
    with tab1:
        st.subheader("General Settings")
        
        st.write("**Application Settings**")
        auto_refresh = st.checkbox("Enable Auto-Refresh", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)
        
        theme = st.selectbox("Theme", options=["Light", "Dark"])
    
    with tab2:
        st.subheader("Data Management")
        
        st.write("**Data Settings**")
        dm = st.session_state.data_manager
        df = dm.load_data(DATA_FILE)
        
        if df is not None:
            st.metric("Total Records", len(df))
            st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            st.divider()
            
            if st.button("Clear Cache"):
                st.cache_data.clear()
                st.success("Cache cleared!")
            
            if st.button("Reset Data"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.success("Data reset!")
                    st.rerun()
    
    with tab3:
        st.subheader("About")
        
        st.markdown("""
        ### Enterprise LMS Dashboard
        
        **Version:** 1.0.0  
        **Built with:** Streamlit  
        **Purpose:** Training Compliance Tracking
        
        #### Features
        - 📊 Real-time compliance dashboards
        - 📋 Training progress tracking
        - 📈 Advanced analytics
        - 📄 Comprehensive reporting
        - ⚙️ Customizable settings
        
        #### Key Metrics Tracked
        - Training completion rates
        - Compliance status
        - Certificate expiry
        - Employee performance
        - Department analytics
        """)

# ============= MAIN EXECUTION =============
def main():
    """Main application"""
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to selected page
    if "Dashboard" in page:
        render_dashboard()
    elif "Training Tracker" in page:
        render_training_tracker()
    elif "Analytics" in page:
        render_analytics()
    elif "Reports" in page:
        render_reports()
    elif "Settings" in page:
        render_settings()

if __name__ == "__main__":
    main()
