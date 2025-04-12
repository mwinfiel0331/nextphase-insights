import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from db_service import get_all_clients, get_client_data, update_client_data

def calculate_optimization_score(client_data):
    """Calculate an optimization score based on client data"""
    score = 0
    if client_data.get('manual_processes'):
        score += max(0, 100 - (client_data['manual_processes'] * 10))
    if client_data.get('current_tools'):
        score += len(client_data['current_tools']) * 5
    return min(100, score)

def show_dashboard():
    st.title("NextPhase Insights Dashboard")
    
    # Load clients
    try:
        clients = get_all_clients()
        if not clients:
            st.warning("No client data available. Please add clients through the intake form.")
            return
    except Exception as e:
        st.error(f"Error loading client data: {str(e)}")
        return

    # Dashboard Layout
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Client Selection
        client_names = [client['company_name'] for client in clients]
        selected_client = st.selectbox(
            "Select Client",
            client_names,
            key="client_selector"
        )
        
        # Get selected client data
        client_data = next((client for client in clients 
                          if client['company_name'] == selected_client), None)
        
        if client_data:
            st.info(f"Last Updated: {client_data.get('updated_at', 'Not available')}")
            
            # Quick Actions
            st.subheader("Quick Actions")
            if st.button("Generate Report"):
                st.download_button(
                    "Download Report",
                    data=f"Report for {selected_client}",  # Replace with actual report generation
                    file_name=f"{selected_client}_report.pdf",
                    mime="application/pdf"
                )
    
    with col1:
        if client_data:
            # Key Metrics
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            with metrics_col1:
                optimization_score = calculate_optimization_score(client_data)
                st.metric(
                    "Optimization Score",
                    f"{optimization_score}%",
                    delta="↑ 5%" if optimization_score > 50 else "↓ 5%"
                )
            with metrics_col2:
                st.metric(
                    "Manual Processes",
                    client_data.get('manual_processes', 0),
                    delta="-2 from last month"
                )
            with metrics_col3:
                st.metric(
                    "Tools Integrated",
                    len(client_data.get('current_tools', [])),
                    delta="↑ 1"
                )

            # Process Analysis
            st.subheader("Process Analysis")
            if client_data.get('pain_points'):
                pain_points = [p.strip() for p in client_data['pain_points'].split('\n') if p.strip()]
                impact_levels = ['High', 'Medium', 'Low']
                
                for idx, point in enumerate(pain_points):
                    with st.expander(f"Pain Point {idx + 1}: {point}"):
                        impact = st.selectbox(
                            "Impact Level",
                            impact_levels,
                            key=f"impact_{idx}"
                        )
                        notes = st.text_area(
                            "Notes",
                            key=f"notes_{idx}"
                        )
                        if st.button("Update", key=f"update_{idx}"):
                            # Update logic here
                            st.success("Updated successfully!")

            # Tools Analysis
            if client_data.get('current_tools'):
                st.subheader("Technology Stack Analysis")
                fig = px.pie(
                    names=client_data['current_tools'],
                    values=[1] * len(client_data['current_tools']),
                    title="Current Tools Distribution"
                )
                fig.update_traces(textposition='inside', textinfo='label+percent')
                st.plotly_chart(fig, use_container_width=True)

            # Goals Tracking
            if client_data.get('goals'):
                st.subheader("Optimization Goals")
                goals = [g.strip() for g in client_data['goals'].split('\n') if g.strip()]
                for idx, goal in enumerate(goals):
                    progress = st.slider(
                        goal,
                        0, 100,
                        key=f"goal_progress_{idx}"
                    )
                    st.progress(progress / 100)

if __name__ == "__main__":
    show_dashboard()