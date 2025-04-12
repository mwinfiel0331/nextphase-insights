import streamlit as st
from ..services.intake_service import IntakeService
import logging

logger = logging.getLogger(__name__)

def show_client_dashboard(user_data: dict):
    """Client dashboard for managing their process intakes"""
    st.title(f"Welcome, {user_data['full_name']}")
    
    intake_service = IntakeService()
    
    # Client sidebar
    with st.sidebar:
        st.write(f"**Company:** {user_data['company_name']}")
        st.write(f"**Email:** {user_data['email']}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Process Intakes")
        try:
            intakes = intake_service.get_user_intakes(user_data['uid'])
            
            if not intakes:
                st.info("No intake forms yet. Create your first one!")
            else:
                for intake in intakes:
                    with st.expander(
                        f"📝 {intake['company_name']} - {intake['created_at'].strftime('%Y-%m-%d')}",
                        expanded=False
                    ):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Status:** {intake['status'].title()}")
                            st.write(f"**Industry:** {intake['industry']}")
                        with col_b:
                            if st.button("View Analysis", key=f"analyze_{intake['id']}"):
                                st.session_state.current_intake = intake
                                st.session_state.show_analysis = True
                                st.rerun()
        
        except Exception as e:
            logger.error(f"Error loading intakes: {e}")
            st.error("Failed to load your intakes")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("➕ New Process Intake", use_container_width=True):
            st.session_state.show_intake = True
            st.session_state.current_intake = None
            st.rerun()
        
        st.divider()
        st.subheader("Process Status")
        if intakes:
            completed = sum(1 for i in intakes if i['status'] == 'completed')
            st.progress(completed / len(intakes), "Completion Rate")
            st.metric("Total Processes", len(intakes))