import streamlit as st
import plotly.express as px
import pandas as pd
from ..services.db_service import get_client_by_id
from ..utils.scoring import calculate_optimization_score
from .admin.admin_dashboard import show_admin_dashboard
from .components.process_analyzer import show_process_analysis

def show_dashboard():
    """Display main dashboard"""
    st.title("Process Optimization Dashboard")
    
    # Get client data
    client_id = st.session_state.get('client_id')
    client_data = get_client_by_id(client_id) if client_id else {}
    
    # Add AI analysis section
    show_process_analysis(client_data)
    
    if st.session_state.get('is_admin', False):
        dashboard_type = st.sidebar.radio(
            "Dashboard View",
            ["Customer Dashboard", "Admin Dashboard"]
        )
        
        if dashboard_type == "Admin Dashboard":
            show_admin_dashboard()
            return
    
    # Add AI analysis section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_process_analysis(client_data)
    
    with col2:
        # Show other metrics
        show_customer_dashboard()

def show_customer_dashboard():
    """Individual customer view"""
    st.title("Your Process Optimization Status")
    
    # Get current client's data
    client = get_client_by_id(st.session_state.get('client_id'))
    if not client:
        st.warning("Please log in to view your dashboard")
        return
    
    # Company Overview
    st.header(f"{client['company_name']} Overview")
    
    show_kpi_cards(client)
    show_tool_analysis(client)

def show_kpi_cards(client):
    """Display KPI metrics for customer"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Processes Identified",
            client.get('manual_processes', 0),
            "To Optimize"
        )
    
    with col2:
        optimization_score = calculate_optimization_score(client)
        st.metric(
            "Optimization Score",
            f"{optimization_score:.1f}%",
            "Current Progress"
        )
    
    with col3:
        hours_saved = client.get('hours_per_week', 0) * (optimization_score/100)
        st.metric(
            "Potential Hours Saved",
            f"{hours_saved:.1f}",
            "Weekly"
        )

def show_tool_analysis(client):
    """Display tool usage analysis"""
    if client.get('tool_selections'):
        st.subheader("Current Tool Usage")
        tool_data = []
        for category, tools in client['tool_selections'].items():
            if tools:
                tool_data.extend([(category, tool) for tool in tools])
        
        if tool_data:
            df = pd.DataFrame(tool_data, columns=['Category', 'Tool'])
            fig = px.treemap(
                df, 
                path=['Category', 'Tool'],
                title="Tool Distribution by Category"
            )
            st.plotly_chart(fig, use_container_width=True)