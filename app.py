import streamlit as st
from src.pages.admindashboard import show_admin_dashboard
from src.pages.clientdashboard import show_client_dashboard
from src.pages.intake_form import show_intake_form
from src.services.user_service import UserService
from src.utils.constants import UserType
import logging

logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'show_intake' not in st.session_state:
        st.session_state.show_intake = False
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    if 'current_intake' not in st.session_state:
        st.session_state.current_intake = None

def main():
    st.set_page_config(page_title="NextPhase Insights", page_icon="🚀", layout="wide")
    init_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        # Route based on user role and current view
        if st.session_state.show_intake:
            show_intake_form(st.session_state.user_data)
        elif st.session_state.show_analysis:
            show_analysis(st.session_state.current_intake)
        else:
            # Route to appropriate dashboard based on user_type
            if st.session_state.user_data.get('user_type') == UserType.ADMIN.value:
                show_admin_dashboard(st.session_state.user_data)
            else:
                show_client_dashboard(st.session_state.user_data)

def show_auth_page():
    """Show login/signup page"""
    st.title("Welcome to NextPhase Insights")
    
    user_service = UserService()
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                try:
                    user_data = user_service.sign_in_user(email, password)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.rerun()
                except Exception as e:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("signup_form"):
            company_name = st.text_input("Company Name*")
            full_name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            password = st.text_input("Password*", type="password")
            
            if st.form_submit_button("Sign Up"):
                try:
                    user_data = user_service.create_user(
                        email=email,
                        password=password,
                        user_data={
                            'company_name': company_name,
                            'full_name': full_name
                        }
                    )
                    st.success("Account created! Please log in.")
                except Exception as e:
                    st.error(f"Failed to create account: {str(e)}")

if __name__ == "__main__":
    main()