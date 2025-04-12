import streamlit as st
from ..services.intake_service import IntakeService
from .intake_form import show_intake_form
import logging

logger = logging.getLogger(__name__)

def show_client_dashboard(user_data: dict):
    """Display client dashboard with intake history"""
    # Initialize page state if not exists
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
        
    st.title(f"Welcome, {user_data.get('full_name', 'Client')}")
    
    intake_service = IntakeService()
    
    # Check for existing intake
    existing_intake = intake_service.get_client_intake(user_data['email'])
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if existing_intake:
            st.info("You have an existing intake form")
            if st.button("👁️ View Intake Form", use_container_width=True):
                st.session_state.current_intake = existing_intake
                st.session_state.show_readonly = True
                st.rerun()
        else:
            if st.button("➕ Create New Intake Form", use_container_width=True, key="create_intake"):
                logger.info("Navigating to intake form")
                st.session_state.page = "intake_form"
                st.session_state.show_readonly = False
                st.rerun()
                logger.debug(f"Session state after button click: {st.session_state}")
    
    # Show intake details if viewing
    if st.session_state.get('show_readonly'):
        show_readonly_intake(st.session_state.current_intake)

def show_readonly_intake(intake_data: dict):
    """Display read-only view of intake form"""
    st.subheader("Your Process Intake Form")
    
    with st.expander("Company Information", expanded=True):
        st.write(f"**Company Name:** {intake_data.get('company_name', 'N/A')}")
        st.write(f"**Industry:** {intake_data.get('industry', 'N/A')}")
        st.write(f"**Process Name:** {intake_data.get('process_name', 'N/A')}")
    
    with st.expander("Process Details", expanded=True):
        st.write(f"**Current Challenges:** {intake_data.get('current_challenges', 'N/A')}")
        st.write(f"**Desired Outcomes:** {intake_data.get('desired_outcomes', 'N/A')}")
        
    with st.expander("Status Information", expanded=True):
        st.write(f"**Status:** {intake_data.get('status', 'N/A').title()}")
        st.write(f"**Submitted:** {intake_data.get('created_at').strftime('%Y-%m-%d %H:%M')}")
    
    if st.button("← Back to Dashboard"):
        st.session_state.show_readonly = False
        st.rerun()