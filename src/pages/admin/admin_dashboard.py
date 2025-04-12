import streamlit as st
import plotly.express as px
import pandas as pd
from ...services.db_service import get_all_clients
from ...utils.scoring import calculate_optimization_score

def show_admin_dashboard():
    """Admin/reviewer overview dashboard"""
    st.title("Process Optimization Dashboard")
    
    # Load all client data
    clients = get_all_clients()
    
    # Summary Metrics
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
            "Total Processes",
            total_processes,
            "To Optimize"
        )
    
    with col3:
        avg_score = sum(calculate_optimization_score(client) for client in clients) / len(clients) if clients else 0
        st.metric(
            "Avg. Optimization Score",
            f"{avg_score:.1f}%",
            "Overall"
        )
    
    show_visualizations(clients)
    show_client_details(clients)

def show_visualizations(clients):
    """Display admin dashboard visualizations"""
    if clients:
        col1, col2 = st.columns(2)
        
        with col1:
            show_industry_distribution(clients)
        
        with col2:
            show_optimization_progress(clients)

def show_industry_distribution(clients):
    """Show pie chart of industry distribution"""
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

def show_optimization_progress(clients):
    """Show bar chart of optimization progress"""
    progress_data = [
        {
            'company': client['company_name'],
            'score': calculate_optimization_score(client)
        }
        for client in clients
    ]
    
    fig = px.bar(
        progress_data,
        x='company',
        y='score',
        title="Optimization Progress by Client",
        labels={'score': 'Optimization Score (%)', 'company': 'Company'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_client_details(clients):
    """Display expandable client details"""
    st.subheader("Client Details")
    for client in clients:
        with st.expander(f"{client['company_name']} - {client.get('industry', 'N/A')}"):
            st.write(f"**Contact:** {client.get('contact_name', 'N/A')}")
            st.write(f"**Main Pain Point:** {client.get('main_pain_point', 'N/A')}")
            st.write(f"**Manual Processes:** {client.get('manual_processes', 0)}")
            st.progress(calculate_optimization_score(client) / 100)