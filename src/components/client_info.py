import streamlit as st
import logging

logger = logging.getLogger(__name__)

def show_client_info(user_data: dict):
    st.subheader("Company Information")
    
    # Initialize form data in session state if not exists
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    col1, col2 = st.columns(2)
    
    # Company Information Column
    with col1:
        company_name = st.text_input(
            "Company Name*", 
            value=user_data.get("company_name", ""),
            help="Legal name of the company"
        )
        industry = st.selectbox(
            "Industry*",
            options=[
                "Technology",
                "Healthcare",
                "Finance",
                "Manufacturing",
                "Retail",
                "Education",
                "Professional Services",
                "Other"
            ],
            index=0
        )
        company_size = st.select_slider(
            "Company Size*",
            options=["1-10", "11-50", "51-200", "201-500", "500+"],
            value="11-50"
        )

    # Contact Information Column
    with col2:
        contact_name = st.text_input(
            "Primary Contact Name*",
            value=user_data.get("contact_name", ""),
            help="Name of the main point of contact"
        )
        contact_email = st.text_input(
            "Contact Email*",
            value=user_data.get("contact_email", ""),
            help="Business email address"
        )
        contact_role = st.text_input(
            "Role/Position*",
            value=user_data.get("contact_role", ""),
            help="Job title or role in the company"
        )

    # Store all collected data in session state
    st.session_state.form_data.update({
        'company_name': company_name,
        'industry': industry,
        'company_size': company_size,
        'contact_name': contact_name,
        'contact_email': contact_email,
        'contact_role': contact_role
    })
    
    logger.debug(f"Updated form data in session state: {st.session_state.form_data}")
