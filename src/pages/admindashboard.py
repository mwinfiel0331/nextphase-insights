import streamlit as st
from ..services.intake_service import IntakeService
from ..services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

def show_admin_dashboard(user_data: dict):
    """Admin dashboard for managing users and viewing all intakes"""
    st.title("🔐 Admin Dashboard")
    
    # Initialize services
    intake_service = IntakeService()
    user_service = UserService()
    
    # Admin sidebar
    with st.sidebar:
        st.write(f"**Admin:** {user_data['full_name']}")
        st.write(f"**Access Level:** Administrator")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 Users", "📝 Intakes"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        try:
            users = user_service.list_users()
            intakes = intake_service.get_all_intakes()
            
            with col1:
                st.metric("Total Users", len(users))
            with col2:
                st.metric("Total Intakes", len(intakes))
            with col3:
                active = sum(1 for i in intakes if i['status'] == 'active')
                st.metric("Active Processes", active)
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            st.error("Failed to load dashboard metrics")
    
    with tab2:
        st.subheader("User Management")
        for user in users:
            if not user.get('is_admin'):  # Skip other admins
                with st.expander(f"👤 {user['company_name']} - {user['full_name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {user['email']}")
                        st.write(f"**Created:** {user['created_at'].strftime('%Y-%m-%d')}")
                    with col2:
                        if st.button("View Intakes", key=f"view_{user['uid']}"):
                            st.session_state.selected_user = user['uid']
                            st.rerun()
    
    with tab3:
        st.subheader("All Process Intakes")
        for intake in intakes:
            with st.expander(f"📝 {intake['company_name']} - {intake['created_at'].strftime('%Y-%m-%d')}"):
                st.write(f"**Status:** {intake['status'].title()}")
                st.write(f"**Industry:** {intake['industry']}")
                if st.button("Review", key=f"review_{intake['id']}"):
                    st.session_state.current_intake = intake
                    st.session_state.show_analysis = True
                    st.rerun()