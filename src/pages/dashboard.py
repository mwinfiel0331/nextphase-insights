import streamlit as st
import plotly.express as px
import pandas as pd
from ..services.db_service import get_client_by_id
from .admin.admin_dashboard import show_admin_dashboard

def show_dashboard():
    """Main dashboard router"""
    if st.session_state.get('is_admin', False):
        dashboard_type = st.sidebar.radio(
            "Dashboard View",
            ["Customer Dashboard", "Admin Dashboard"]
        )
        
        if dashboard_type == "Admin Dashboard":
            show_admin_dashboard()
            return
    
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

def calculate_optimization_score(client):
    """Calculate an optimization score based on client data"""
    score = 0
    
    # Base score from manual processes
    if client.get('manual_processes'):
        score += max(0, 100 - (client['manual_processes'] * 10))
    
    # Tool adoption score
    if client.get('tool_selections'):
        tool_count = sum(len(tools) for tools in client['tool_selections'].values())
        score += min(50, tool_count * 5)
    
    # Progress score
    if client.get('progress', 0):
        score = (score + client['progress']) / 2
    
    return min(100, score)