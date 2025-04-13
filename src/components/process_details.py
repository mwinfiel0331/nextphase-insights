import streamlit as st
from ..models.process_section import Process, ProcessStep
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def show_process_details_section(existing_processes: Optional[List[Process]] = None) -> None:
    """Display the process details section with help text and form"""
    
    # Initialize step count in session state if not exists
    if 'step_count' not in st.session_state:
        st.session_state.step_count = 1

    st.markdown("""
        ### Process Documentation
        In this section, we'll document each business process you'd like to optimize. 
        Please document one process at a time, breaking down all the steps involved.
        
        **Example Process: Invoice Processing**
        1. Receive invoice via email
        2. Extract invoice data (dates, amounts, vendor info)
        3. Match invoice to purchase order
        4. Validate line items and amounts
        5. Route for department approval
        6. Obtain finance director sign-off if over $5000
        7. Enter into accounting system
        8. Schedule payment based on terms
        9. Process payment via banking system
        10. Update vendor records
        11. File documentation for audit
        
        Think about similar end-to-end processes in your organization that could benefit from automation.
        """)
    
    # Initialize processes list in session state if not exists
    if 'processes' not in st.session_state:
        st.session_state.processes = existing_processes or []

    # Show the form for entering process details
    with st.form("process_details_form"):
        st.subheader("Process Documentation")
        
        # Basic Process Information
        process_name = st.text_input(
            "Name of Process*",
            placeholder="What are you naming this process? (e.g., Employee Onboarding, Expense Approval)",
            help="Enter a clear, recognizable name for this process"
        )
        
        process_goal = st.text_area(
            "Goal of Process*",
            placeholder="What does this process accomplish? What is its business value?",
            help="Describe the main objective this process serves"
        )
        
        process_start = st.text_area(
            "Process Start Point*",
            placeholder="What triggers this process to begin? (e.g., new hire acceptance, expense report submission)",
            help="Describe what initiates this process"
        )
        
        process_end = st.text_area(
            "Process End Point*",
            placeholder="How do you know when this process is complete? What's the final output?",
            help="Define the completion point of this process"
        )
        
        automation_needs = st.text_area(
            "Automation Needs*",
            placeholder="Which parts of this process are manual and time-consuming?",
            help="Identify tasks that could benefit from automation"
        )
        
        # Process steps section
        st.markdown("### Process Steps")
        steps = []
        
        # Show existing steps
        for i in range(st.session_state.step_count):
            # Get step description from session state if it exists
            step_desc = st.session_state.get(f"step_{i}_desc", "")
            step_title = f"Step {i+1}: {step_desc[:50]}..." if step_desc else f"Step {i+1}"
            
            with st.expander(step_title, expanded=i==0):
                # Add delete button in the top right
                col1, col2 = st.columns([5, 1])
                with col2:
                    # Use unique key for each delete button
                    delete_label = f"🗑️ Step {i+1}"
                    if st.form_submit_button(delete_label, type="secondary"):
                        # Remove step data from session state
                        for key in [f"step_{i}_desc", f"step_{i}_perf", f"step_{i}_tools", 
                                  f"step_{i}_dur", f"step_{i}_pain", f"step_{i}_appr", f"step_{i}_img"]:
                            if key in st.session_state:
                                del st.session_state[key]
                        # Decrease step count
                        st.session_state.step_count -= 1
                        # Reorder remaining steps
                        for j in range(i, st.session_state.step_count):
                            for field in ["desc", "perf", "tools", "dur", "pain", "appr", "img"]:
                                next_key = f"step_{j+1}_{field}"
                                current_key = f"step_{j}_{field}"
                                if next_key in st.session_state:
                                    st.session_state[current_key] = st.session_state[next_key]
                                    del st.session_state[next_key]
                        st.rerun()
                
                # Existing step input fields
                step = {
                    'description': st.text_area(
                        "Step Description*",
                        placeholder="List what happens in this step. Be specific about the actions taken.",
                        key=f"step_{i}_desc"
                    ),
                    'performer': st.text_input(
                        "Step Performer*",
                        placeholder="Who is responsible for completing this step?",
                        key=f"step_{i}_perf"
                    ),
                    'current_tools': st.multiselect(
                        "Tools Used",
                        ["Email", "Excel", "Word", "SharePoint", "Custom Software", "Other"],
                        placeholder="Select all tools used in this step",
                        key=f"step_{i}_tools"
                    ),
                    'desired_tools': st.multiselect(
                        "Desired Tools",
                        ["Email", "Excel", "Word", "SharePoint", "Custom Software", "Other"],
                        placeholder="Select all tools desired in this step",
                        key=f"step_{i}_desired_tools"
                    ),
                    'duration': st.text_input(
                        "Step Duration*",
                        placeholder="How long does this step typically take?",
                        key=f"step_{i}_dur"
                    ),
                    'pain_points': st.text_area(
                        "Step Pain Points",
                        placeholder="What challenges exist with this step?",
                        key=f"step_{i}_pain"
                    ),
                    'approvals': st.text_area(
                        "Step Approvals",
                        placeholder="Are any approvals needed?",
                        key=f"step_{i}_appr"
                    ),
                    'screenshot': st.file_uploader(
                        "Step Screenshot",
                        help="Upload a screenshot (optional)",
                        key=f"step_{i}_img"
                    )
                }
                if step['description']:
                    steps.append(ProcessStep(i+1, **step))
        
        # Form actions
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            add_step = st.form_submit_button("+ Add Step", type="secondary", use_container_width=True)
            if add_step:
                st.session_state.step_count += 1
                st.rerun()
        
        with col3:
            submit_button = st.form_submit_button("Save Process", type="primary", use_container_width=True)
        
        # Handle form submission
        if submit_button and process_name and steps:
            try:
                new_process = Process(
                    process_name=process_name,
                    process_goal=process_goal,
                    process_start=process_start,
                    process_end=process_end,
                    automation_needs=automation_needs,
                    steps=steps
                )
                st.session_state.processes.append(new_process)
                st.success("Process saved successfully!")
                # Reset step count for next process
                st.session_state.step_count = 1
                st.rerun()
            except Exception as e:
                logger.error(f"Error saving process: {str(e)}")
                st.error("Failed to save process. Please try again.")