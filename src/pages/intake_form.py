import streamlit as st
from datetime import datetime
import pandas as pd
import logging
from ..services.intake_service import IntakeService
from ..utils.validators import validate_client_data
from google.cloud import firestore

logger = logging.getLogger(__name__)

def show_intake_form(user_data: dict):
    """Display the multi-step intake form"""
    st.title("Process Optimization Intake")
    
    # Initialize session state if needed
    if 'form_section' not in st.session_state:
        st.session_state.form_section = 0
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Progress tracker
    progress_sections = ["Company Info", "Process Details", "Documentation", "Review"]
    current_section = st.session_state.form_section
    
    # Display progress bar
    progress_bar = st.progress(0)
    progress_bar.progress((current_section + 1) / len(progress_sections))
    st.caption(f"Section {current_section + 1} of {len(progress_sections)}: {progress_sections[current_section]}")

    # Initialize service
    intake_service = IntakeService()

    try:
        # Show current section
        if current_section == 0:
            show_company_info(user_data)
        elif current_section == 1:
            show_process_details()
        elif current_section == 2:
            show_documentation()
        else:
            show_review(user_data)

        # Navigation buttons
        cols = st.columns([1, 1, 1])
        
        with cols[0]:
            if current_section > 0:
                if st.button("← Previous"):
                    st.session_state.form_section -= 1
                    st.rerun()

        with cols[2]:
            if current_section < len(progress_sections) - 1:
                if st.button("Next →"):
                    st.session_state.form_section += 1
                    st.rerun()
            else:
                if st.button("Submit"):
                    submit_form(user_data['uid'])

    except Exception as e:
        logger.error(f"Error displaying intake form: {str(e)}")
        st.error("An error occurred while displaying the form. Please try again.")

def show_company_info(user_data: dict):
    st.subheader("Company Information")
    col1, col2 = st.columns(2)
    
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

def show_process_details():
    st.subheader("Process Assessment")
    
    # Business Overview
    st.markdown("### Business Overview")
    business_description = st.text_area(
        "Business Description*",
        placeholder="Briefly describe your business and its primary operations",
        help="Provide a high-level overview of your business activities"
    )
    
    # Challenges and Goals
    st.markdown("### Challenges and Goals")
    current_challenges = st.text_area(
        "Current Workflow Challenges*",
        placeholder="What are the main challenges you're facing with your current workflows?"
    )
    
    main_pain_point = st.text_area(
        "Primary Pain Point*",
        placeholder="Describe your biggest pain point in more detail"
    )
    
    partnership_goals = st.text_area(
        "Partnership Goals*",
        placeholder="What do you hope to achieve as a result of our partnership?"
    )

    # Current Tools Assessment
    st.markdown("### Current Tools & Systems")
    
    tool_categories = {
        "Communication & Messaging": [
            "Slack",
            "Microsoft Teams",
            "Discord",
            "Zoom",
            "Google Meet",
            "Other"
        ],
        "Task & Project Management": [
            "Asana",
            "Trello",
            "Jira",
            "Monday.com",
            "ClickUp",
            "Other"
        ],
        "Calendar & Scheduling": [
            "Google Calendar",
            "Outlook",
            "Calendly",
            "Other"
        ],
        "Productivity": [
            "Microsoft Office",
            "Google Workspace",
            "Notion",
            "Evernote",
            "Other"
        ],
        "CRM": [
            "Salesforce",
            "HubSpot",
            "Zoho",
            "None",
            "Other"
        ],
        "E-commerce & Payments": [
            "Shopify",
            "WooCommerce",
            "Stripe",
            "PayPal",
            "Square",
            "None",
            "Other"
        ],
        "Data & Analytics": [
            "Google Analytics",
            "Tableau",
            "Power BI",
            "None",
            "Other"
        ],
        "Social Media Management": [
            "Hootsuite",
            "Buffer",
            "Later",
            "None",
            "Other"
        ],
        "Cloud Services": [
            "AWS",
            "Google Cloud",
            "Azure",
            "Dropbox",
            "None",
            "Other"
        ],
        "Marketing & Advertising": [
            "Google Ads",
            "Meta Ads",
            "Mailchimp",
            "None",
            "Other"
        ],
        "Automation & Workflow": [
            "Zapier",
            "Make (Integromat)",
            "Power Automate",
            "None",
            "Other"
        ],
        "Customer Support": [
            "Zendesk",
            "Intercom",
            "Freshdesk",
            "None",
            "Other"
        ]
    }

    # Create columns for tool selection
    st.markdown("### Tool Assessment")
    st.caption("Select the tools and systems currently in use")
    
    tool_selections = {}
    for category, tools in tool_categories.items():
        st.markdown(f"**{category}**")
        tool_selections[category] = st.multiselect(
            f"Select {category} tools",
            options=tools,
            key=f"tools_{category.lower().replace(' ', '_')}"
        )
        
        # If "Other" is selected, show text input
        if "Other" in tool_selections[category]:
            other_tool = st.text_input(
                f"Please specify other {category} tools",
                key=f"other_{category.lower().replace(' ', '_')}"
            )
            if other_tool:
                tool_selections[category].append(other_tool)

    # Additional Details
    st.markdown("### Process Details")
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

    # Store data in session state
    st.session_state.form_data.update({
        'business_description': business_description,
        'current_challenges': current_challenges,
        'main_pain_point': main_pain_point,
        'partnership_goals': partnership_goals,
        'tool_selections': tool_selections,
        'manual_processes': manual_processes,
        'hours_per_week': hours_per_week
    })

def show_documentation():
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

def show_review(user_data: dict):
    st.subheader("Review Information")
    
    # Display summary of entered information
    if 'form_data' in st.session_state:
        data = st.session_state.form_data
        
        st.info("Company Information")
        st.write(f"**Company:** {data.get('company_name')}")
        st.write(f"**Industry:** {data.get('industry')}")
        st.write(f"**Size:** {data.get('company_size')}")

def submit_form(user_id: str):
    """Submit the form data"""
    try:
        intake_service = IntakeService()
        intake_service.save_intake_form(user_id, st.session_state.form_data)
        st.success("Form submitted successfully!")
    except Exception as e:
        logger.error(f"Error submitting form: {str(e)}")
        st.error("An error occurred while submitting the form. Please try again.")