import streamlit as st
import plotly.express as px
from ..services.db_service import get_all_clients

def show_dashboard():
    st.title("Process Optimization Dashboard")
    
    # Load client data
    clients = get_all_clients()
    
    # Dashboard Layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Clients",
            len(clients),
            "Active"
        )
    
    with col2:
        total_processes = sum(client.get('manual_processes', 0) for client in clients)
        st.metric(
            "Processes to Optimize",
            total_processes,
            "Identified"
        )
    
    with col3:
        avg_score = sum(calculate_optimization_score(client) for client in clients) / len(clients) if clients else 0
        st.metric(
            "Avg. Optimization Score",
            f"{avg_score:.1f}%",
            "Overall"
        )
    
    # Industry Distribution
    if clients:
        industry_counts = {}
        for client in clients:
            industry = client.get('industry', 'Other')
            industry_counts[industry] = industry_counts.get(industry, 0) + 1
        
        fig = px.pie(
            values=list(industry_counts.values()),
            names=list(industry_counts.keys()),
            title="Client Industry Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

def calculate_optimization_score(client):
    """Calculate an optimization score based on client data"""
    score = 0
    if client.get('manual_processes'):
        score += max(0, 100 - (client['manual_processes'] * 10))
    if client.get('current_tools'):
        score += len(client['current_tools']) * 5
    return min(100, score)