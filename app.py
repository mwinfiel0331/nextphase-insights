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
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "user_type" not in st.session_state:
        st.session_state.user_type = None

def main():
    """Main application entry point"""
    st.set_page_config(page_title="NextPhase Insights", page_icon="🚀", layout="wide")
    init_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        # Add debug info
        logger.info(f"User type: {st.session_state.user_type}")
        logger.info(f"User data: {st.session_state.user_data}")
        
        # Route based on user type
        if st.session_state.user_type == UserType.ADMIN.value:
            logger.info("Showing admin dashboard")
            show_admin_dashboard(st.session_state.user_data)
        else:
            logger.info("Showing client dashboard")
            show_client_dashboard(st.session_state.user_data)

def show_auth_page():
    """Handle user authentication"""
    st.title("Welcome to NextPhase Insights")
    
    user_service = UserService()
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                try:
                    success, user_data = user_service.authenticate(email, password)
                    
                    if success and user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.session_state.user_type = user_data.get('user_type')
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                        
                except Exception as e:
                    logger.error(f"Authentication error: {str(e)}")
                    st.error("Authentication failed")

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