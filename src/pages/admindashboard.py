import streamlit as st
from datetime import datetime
from firebase_admin import firestore
from src.services import user_service
from src.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

def load_dashboard_metrics() -> dict:
    """Load metrics for admin dashboard"""
    try:
        db = firestore.client()
        metrics = {}

        # Get all users
        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        
        # Calculate user metrics
        metrics['total_users'] = len(users)
        metrics['active_users'] = sum(1 for user in users if user.get('is_active', True))
        metrics['admin_users'] = sum(1 for user in users if user.get('app_role') =='admin')
        
        # Get all intakes
        intakes_ref = db.collection('client_intakes')
        intakes = [doc.to_dict() for doc in intakes_ref.stream()]
        
        # Calculate intake metrics
        metrics['total_intakes'] = len(intakes)
        metrics['pending_intakes'] = sum(1 for intake in intakes if intake.get('workflow_status') == 'SUBMITTED')
        metrics['completed_intakes'] = sum(1 for intake in intakes if intake.get('workflow_status') == 'COMPLETED')

        logger.info(f"Loaded dashboard metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error loading dashboard metrics: {str(e)}")
        return {
            'total_users': 0,
            'active_users': 0,
            'admin_users': 0,
            'total_intakes': 0,
            'pending_intakes': 0,
            'completed_intakes': 0
        }

def show_admin_dashboard(user_data: dict):
    """Admin dashboard for managing users and viewing all intakes"""
    st.title("🔐 Admin Dashboard")
    st.write("Welcome to the admin dashboard. Here you can manage users and view all intakes.")
             
    # Admin sidebar
    with st.sidebar:
        st.write(f"**Admin:** {user_data['full_name']}")
        st.write(f"**Access Level:** {user_data['app_role']}")
        if st.button("🚪 Logout", use_container_width=False):
            st.session_state.clear()
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 Users", "📝 Intakes"])
    
    # Overview Tab
    with tab1:
        col1, col2, col3 = st.columns(3)
        try:
            metrics = load_dashboard_metrics()
            
            with col1:
                st.metric("Total Users", metrics['total_users'])
                st.metric("Active Users", metrics['active_users'])
            with col2:
                st.metric("Total Intakes", metrics['total_intakes'])
                st.metric("Pending Review", metrics['pending_intakes'])
            with col3:
                st.metric("Admin Users", metrics['admin_users'])
                st.metric("Completed Intakes", metrics['completed_intakes'])
                
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            st.error("Failed to load dashboard metrics")
    
    # Users Tab
    with tab2:
        st.subheader("User Management")
        try:
            users = user_service.list_users()
            if not users:
                st.info("No users found")
                return
                
            for user in users:
                # Skip own admin account
                if user.get('email') == user_data['email']:
                    continue
                
                # Use document ID or fallback to email as key
                user_key = user.get('uid', user.get('email', 'unknown'))
                    
                with st.expander(f"👤 {user.get('company_name', 'N/A')} - {user.get('full_name', 'N/A')}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {user.get('email', 'N/A')}")
                        st.write(f"**Created:** {user['created_at'].strftime('%Y-%m-%d')}")
                        st.write(f"**Type:** {user.get('app_role', 'client')}")
                        st.write(f"**Status:** {'🟢 Active' if user.get('is_active', True) else '🔴 Inactive'}")
                    with col2:
                        if st.button("View Intakes", key=f"view_{user_key}"):
                            st.session_state.selected_user = user_key
                            st.rerun()
                        if st.button("Toggle Status", key=f"toggle_{user_key}"):
                            new_status = not user.get('is_active', True)
                            user_service.update_user_profile(user_key, {'is_active': new_status})
                            st.rerun()
        except Exception as e:
            logger.error(f"Error loading users: {str(e)}")
            st.error("Failed to load users")
            st.exception(e)  # Show detailed error in debug mode
    
    # Intakes Tab
    with tab3:
        st.subheader("All Process Intakes")
        try:
            intakes = intake_service.get_all_intakes()
            if not intakes:
                st.info("No intake forms submitted yet")
                return

            for intake in intakes:
                # Create display title with fallbacks
                company = intake.get('company_name', 'Unknown Company')
                created = intake.get('created_at', datetime.now()).strftime('%Y-%m-%d')
                
                with st.expander(f"📝 {company} - {created}"):
                    st.write(f"**Status:** {intake.get('status', 'Unknown').title()}")
                    st.write(f"**Industry:** {intake.get('industry', 'N/A')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Contact:** {intake.get('contact_name', 'N/A')}")
                        st.write(f"**Email:** {intake.get('contact_email', 'N/A')}")
                    
                    with col2:
                        if st.button("Review", key=f"review_{intake['id']}"):
                            st.session_state.current_intake = intake
                            st.session_state.show_analysis = True
                            st.rerun()
        except Exception as e:
            logger.error(f"Error loading intakes: {e}")
            st.error("Failed to load intakes")