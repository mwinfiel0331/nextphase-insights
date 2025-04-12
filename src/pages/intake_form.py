import streamlit as st
import datetime
from ..services.db_service import save_client_data
from ..utils.validators import validate_client_data

def show_intake_form():
    st.title("Process Optimization Intake")
    
    with st.form("client_intake_form"):
        company_name = st.text_input("Company Name")
        industry = st.selectbox(
            "Industry",
            ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"]
        )
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                data = {
                    "company_name": company_name,
                    "industry": industry,
                    "created_at": datetime.datetime.now()
                }
                save_client_data(data)
                st.success("Form submitted successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")