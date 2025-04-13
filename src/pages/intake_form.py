import streamlit as st
from datetime import datetime
import pandas as pd
import logging

from src.models.process_step import Process, ProcessStep
from ..services.intake_service import IntakeService
from ..utils.validators import validate_client_data
from google.cloud import firestore

logger = logging.getLogger(__name__)

def show_intake_form(user_data: dict):
    """Display multi-step intake form"""
    st.title("Process Optimization Intake Form")
    
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
    process_details()
    


    # Store data in session state
    st.session_state.form_data.update({
        'business_description': business_description,
        'current_challenges': current_challenges,
        'main_pain_point': main_pain_point,
        'partnership_goals': partnership_goals,
        'tool_selections': tool_selections
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


def process_details():
    """Show process details section with popup form"""
    st.markdown("""
    ### Process Documentation
    For the next section, include details related to process improvements you wish to focus on. 
    Let's separate them by process (so, you only want to include details for one process at a time for each item you enter).
    """)
    
    # Initialize processes in session state if not exists
    if 'processes' not in st.session_state:
        st.session_state.processes = []
    
    # Display existing processes summary
    if st.session_state.processes:
        st.subheader("Documented Processes")
        for i, process in enumerate(st.session_state.processes):
            with st.expander(f"Process: {process.process_name}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Primary Goal:**", process.primary_goal)
                    st.write("**Start Trigger:**", process.start_trigger)
                    st.write("**End Condition:**", process.end_condition)
                with col2:
                    st.write("**Automation Desires:**", process.automation_desires)
                    st.write("**Tools of Interest:**", process.tools_of_interest)
                
                st.markdown("#### Process Steps")
                for step in process.steps:
                    with st.expander(f"Step {step.step_number}: {step.description[:50]}..."):
                        show_step_details(step)
                
                if st.button("Edit Process", key=f"edit_{i}"):
                    st.session_state.editing_process = i
                    show_process_popup(editing=True)
    
    # Add new process button
    if len(st.session_state.processes) < 10:
        if st.button("Add New Process", type="primary"):
            show_process_popup()

def show_process_popup(editing=False):
    """Show popup for process details entry"""
    with st.form("process_details"):
        st.subheader("Process Details")
        
        process_name = st.text_input("What is the name of the process you are documenting?")
        primary_goal = st.text_area("What is the primary goal or outcome of this process?")
        start_trigger = st.text_area("When does this process start? What initiates it?")
        end_condition = st.text_area("What marks the end of this process?")
        automation_desires = st.text_area("What do you wish was automated?")
        tools_interest = st.text_area("Are there any tools that you've heard about that you would like to try out or learn more about?")
        
        st.markdown("### Process Steps")
        steps = []
        
        for i in range(10):  # Allow up to 10 steps
            with st.expander(f"Step {i+1}", expanded=i==0):
                step = ProcessStep(
                    step_number=i+1,
                    description=st.text_area("Description", key=f"desc_{i}"),
                    performer=st.text_input("Who performs this step?", key=f"perf_{i}"),
                    tools=st.multiselect("Which tools are used?", 
                                       options=["Email", "Excel", "Word", "Custom Software", "Other"],
                                       key=f"tools_{i}"),
                    duration=st.text_input("Duration (e.g., 30 mins, 2 hours)", key=f"dur_{i}"),
                    pain_points=st.text_area("Pain points", key=f"pain_{i}"),
                    approvals=st.text_area("Approvals or decision points", key=f"appr_{i}"),
                    screenshot=st.file_uploader("Upload screenshot", key=f"screen_{i}")
                )
                if step.description:  # Only add steps that have a description
                    steps.append(step)
        
        if st.form_submit_button("Save Process"):
            process = Process(
                process_name=process_name,
                primary_goal=primary_goal,
                start_trigger=start_trigger,
                end_condition=end_condition,
                automation_desires=automation_desires,
                tools_of_interest=tools_interest,
                steps=steps
            )
            
            if editing and 'editing_process' in st.session_state:
                st.session_state.processes[st.session_state.editing_process] = process
            else:
                st.session_state.processes.append(process)
            
            st.success("Process saved successfully!")
            st.rerun()

def show_step_details(step: ProcessStep):
        """Display details for a single process step"""
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Performer:**", step.performer)
            st.write("**Tools:**", ", ".join(step.tools))
            st.write("**Duration:**", step.duration)
        with col2:
            st.write("**Pain Points:**", step.pain_points)
            st.write("**Approvals:**", step.approvals)
        
        if step.screenshot:
            st.image(step.screenshot, caption="Step Screenshot")