import streamlit as st
from firebase_admin import firestore  # Add this import
from datetime import datetime
import pandas as pd
import logging

from src.components import client_tools_intake
from src.components.client_intake import client_intake
from src.components.client_info import show_client_info
from src.components.documentation_upload import show_documentation
from ..components.process_details import show_process_details_section


from src.models.process_section import Process, ProcessStep
from ..services.client_intake_service import ClientIntakeService

logger = logging.getLogger(__name__)

def show_intake_form(user_data: dict):
    """Display multi-step intake form"""
    st.title("Client Intake Form")
    
    # Add back button
    if st.button("← Back to Dashboard"):
        st.session_state.show_intake_form = False
        st.rerun()
    
    # Initialize form data in session state if not exists
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'company_name': user_data.get('company_name', ''),
            'contact_name': user_data.get('contact_name', ''),
            'contact_email': user_data.get('contact_email', ''),
            'contact_role': user_data.get('contact_role', ''),
            'industry': user_data.get('industry', ''),
            'company_size': user_data.get('company_size', '11-50')
        }
    
    if 'form_section' not in st.session_state:
        st.session_state.form_section = 0
    
    # Progress tracker
    progress_sections = ["Company Info", "Process Details", "Documentation", "Review"]
    current_section = st.session_state.form_section
    
    # Display progress bar
    progress_bar = st.progress(0)
    progress_bar.progress((current_section + 1) / len(progress_sections))
    st.caption(f"Section {current_section + 1} of {len(progress_sections)}: {progress_sections[current_section]}")

    # Initialize service with Firestore client
    db = firestore.client()
    intake_service = ClientIntakeService(db)  # Fix: Pass db instance

    try:
        # Show current section
        if current_section == 0:
            show_client_info(user_data)
        elif current_section == 1:
            client_intake()
        elif current_section == 2:
            client_tools_intake()
        elif current_section == 3:
            show_process_details_section() 
        elif current_section == 4:
            show_documentation()
        else:
            st.subheader("Review & Submit")
            st.markdown("### Review your information")
            #st.json(st.session_state.form_data)
            
            if st.button("Submit", type="primary", use_container_width=True):
                # Validate data before submission
                validation_errors = validate_client_data(st.session_state.form_data)
                if validation_errors:
                    st.error(f"Validation errors: {', '.join(validation_errors)}")
                else:
                    # Save data to Firestore
                    intake_id = intake_service.save_intake(
                        user_id=user_data.get('user_id', ''),
                        form_data=st.session_state.form_data,
                        status='SUBMITTED'
                    )
                    st.success(f"Intake form submitted successfully! ID: {intake_id}")
                    st.session_state.form_section = 0

        # Navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_section > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.form_section -= 1
                    st.rerun()

        with col3:
            if current_section < len(progress_sections) - 1:
                if st.button("Next →", type="primary", use_container_width=True):
                    st.session_state.form_section += 1
                    st.rerun()

    except Exception as e:
        logger.error(f"Error displaying intake form: {str(e)}")
        st.error("An error occurred while displaying the form. Please try again.")







