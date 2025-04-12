import streamlit as st
import datetime
import pandas as pd
from ..services.db_service import save_client_data
from ..utils.validators import validate_client_data

def show_intake_form():
    st.title("Process Optimization Intake")
    
    # Progress tracker
    progress_sections = ["Company Info", "Process Details", "Documentation", "Review"]
    current_section = st.session_state.get('form_section', 0)
    
    # Display progress bar
    progress_bar = st.progress(0)
    progress_bar.progress((current_section + 1) / len(progress_sections))
    st.caption(f"Section {current_section + 1} of {len(progress_sections)}: {progress_sections[current_section]}")

    with st.form("client_intake_form"):
        if current_section == 0:
            show_company_info()
        elif current_section == 1:
            show_process_details()
        elif current_section == 2:
            show_documentation_upload()
        else:
            show_review()

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if current_section > 0:
                if st.form_submit_button("Previous"):
                    st.session_state.form_section = current_section - 1
                    st.rerun()

        with col2:
            if current_section < len(progress_sections) - 1:
                next_button = st.form_submit_button("Next")
                if next_button:
                    if validate_section(current_section):
                        st.session_state.form_section = current_section + 1
                        st.rerun()
            else:
                if st.form_submit_button("Submit"):
                    submit_form()

def show_company_info():
    st.subheader("Company Information")
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Company Name*", 
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
            ]
        )
        company_size = st.select_slider(
            "Company Size*",
            options=["1-10", "11-50", "51-200", "201-500", "500+"],
            value="11-50"
        )

    with col2:
        contact_name = st.text_input(
            "Primary Contact Name*",
            help="Name of the main point of contact"
        )
        contact_email = st.text_input(
            "Contact Email*",
            help="Business email address"
        )
        contact_role = st.text_input(
            "Role/Position*",
            help="Job title or role in the company"
        )

def show_process_details():
    st.subheader("Process Assessment")
    
    current_tools = st.multiselect(
        "Current Tools & Software*",
        options=[
            "Microsoft Excel",
            "Google Sheets",
            "Slack",
            "Microsoft Teams",
            "Asana",
            "Trello",
            "Jira",
            "Monday.com",
            "Notion",
            "Custom Software",
            "Other"
        ],
        help="Select all tools currently used in your processes"
    )

    col1, col2 = st.columns(2)
    with col1:
        manual_processes = st.number_input(
            "Number of Manual Processes*",
            min_value=1,
            max_value=20,
            value=3,
            help="How many processes need optimization?"
        )
    
    with col2:
        hours_per_week = st.number_input(
            "Hours Spent on Manual Tasks*",
            min_value=1,
            max_value=168,
            value=10,
            help="Estimated hours per week spent on manual tasks"
        )

def show_documentation_upload():
    st.subheader("Process Documentation")
    
    # Process flow diagrams
    flow_diagrams = st.file_uploader(
        "Process Flow Diagrams",
        type=['png', 'jpg', 'pdf'],
        accept_multiple_files=True,
        help="Upload any existing process flow diagrams"
    )
    
    # Current process documentation
    process_docs = st.file_uploader(
        "Current Process Documentation",
        type=['pdf', 'docx', 'xlsx'],
        accept_multiple_files=True,
        help="Upload any existing process documentation"
    )
    
    # Data samples
    data_samples = st.file_uploader(
        "Sample Data Files",
        type=['csv', 'xlsx', 'json'],
        accept_multiple_files=True,
        help="Upload sample data files (optional)"
    )

def show_review():
    st.subheader("Review Information")
    
    # Display summary of entered information
    if 'form_data' in st.session_state:
        data = st.session_state.form_data
        
        st.info("Company Information")
        st.write(f"**Company:** {data.get('company_name')}")
        st.write(f"**Industry:** {data.get('industry')}")
        st.write(f"**Size:** {data.get('company_size')}")