import streamlit as st
from ..services.intake_service import IntakeService
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def show_client_dashboard(user_data: dict):
    """Display the client dashboard"""
    st.title("My Process Intakes")
    
    try:
        # Initialize service and get intakes
        intake_service = IntakeService()
        intakes = intake_service.get_user_intakes(user_data['uid'])
        
        # Display appropriate button based on intake status
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if not intakes:
                st.info("No process intakes found. Start your first intake by clicking the button below.")
                button_text = "Start Client Intake"
            else:
                # Display intakes in a table
                df = pd.DataFrame(intakes)
                st.dataframe(
                    df[['created_at', 'status', 'process_name', 'company_name']],
                    hide_index=True,
                    column_config={
                        'created_at': st.column_config.DatetimeColumn('Submitted'),
                        'status': 'Status',
                        'process_name': 'Process',
                        'company_name': 'Company'
                    }
                )
                button_text = "Start New Intake"
        
        with col2:
            if st.button(
                button_text, 
                key="start_intake_btn", 
                type="primary",
                use_container_width=True
            ):
                logger.info("Navigating to intake form")
                if "page" not in st.session_state:
                    st.session_state.page = "intake_form"
                else:
                    st.session_state["page"] = "intake_form"
                st.session_state.form_section = 0
                st.session_state.form_data = {}
                st.rerun()
            
    except Exception as e:
        logger.error(f"Error in client dashboard: {str(e)}")
        st.error("Unable to load dashboard. Please try again later.")