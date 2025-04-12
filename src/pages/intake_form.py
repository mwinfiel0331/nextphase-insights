import streamlit as st
import datetime
from db_service import save_client_data

def show_intake_form():
    st.title("Process Optimization Intake")
    st.markdown("### Let's understand your business needs")

    with st.form("client_intake_form"):
        # Company Information
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            industry = st.selectbox(
                "Industry",
                ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"]
            )
            company_size = st.select_slider(
                "Company Size",
                options=["1-10", "11-50", "51-200", "201-500", "500+"]
            )
        
        with col2:
            contact_name = st.text_input("Contact Name")
            contact_email = st.text_input("Email")
            contact_role = st.text_input("Role/Position")

        # Current Process Assessment
        st.markdown("### Current Process Assessment")
        current_tools = st.multiselect(
            "What tools do you currently use?",
            ["Excel", "Google Sheets", "Slack", "Teams", "Asana", "Trello", 
             "Monday.com", "Notion", "Custom Software", "Other"]
        )
        
        pain_points = st.text_area(
            "What are your main process pain points?",
            placeholder="Example: Manual data entry takes 4 hours/week..."
        )
        
        goals = st.text_area(
            "What are your key goals for process optimization?",
            placeholder="Example: Reduce manual work, improve accuracy..."
        )

        # Process Details
        st.markdown("### Process Details")
        manual_processes = st.number_input(
            "How many manual processes would you like to optimize?",
            min_value=1,
            max_value=10,
            value=3
        )
        
        urgency = st.select_slider(
            "How urgent is this optimization needed?",
            options=["Not urgent", "Within 3 months", "Within 1 month", "ASAP"]
        )

        submitted = st.form_submit_button("Submit Intake Form")
        
        if submitted:
            # Prepare data for storage
            intake_data = {
                "company_name": company_name,
                "industry": industry,
                "company_size": company_size,
                "contact_name": contact_name,
                "contact_email": contact_email,
                "contact_role": contact_role,
                "current_tools": current_tools,
                "pain_points": pain_points,
                "goals": goals,
                "manual_processes": manual_processes,
                "urgency": urgency,
                "submission_date": datetime.datetime.now().isoformat()
            }
            
            try:
                save_client_data(intake_data)
                st.success("Thank you! Your intake form has been submitted successfully.")
                st.balloons()
            except Exception as e:
                st.error(f"Error saving data: {str(e)}")

if __name__ == "__main__":
    show_intake_form()