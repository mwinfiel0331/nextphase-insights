import streamlit as st
from src.pages.admindashboard import show_admin_dashboard
from src.pages.clientdashboard import show_client_dashboard
from src.pages.intake_form import show_intake_form
from src.services.user_service import UserService
from src.utils.constants import UserType
import logging
import time

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
    st.set_page_config(page_title="NextPhase Insights", page_icon="🚀", layout="wide")
    init_session_state()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
        
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        # Debug log current page
        logger.debug(f"Current page: {st.session_state.page}")
        
        # Page routing
        if st.session_state.page == "intake_form":
            logger.info("Loading intake form")
            show_intake_form(st.session_state.user_data)
        elif st.session_state.page == "dashboard":
            logger.info("Loading client dashboard")
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
            
            col1, col2 = st.columns([1, 2])
            with col1:
                submitted = st.form_submit_button("Login", use_container_width=True)
            with col2:
                if st.form_submit_button("Forgot Password?", type="secondary", use_container_width=True):
                    st.session_state.show_reset = True
                    st.rerun()
    
    # Show password reset form if requested
    if st.session_state.get('show_reset', False):
        show_password_reset()

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

def show_password_reset():
    """Handle password reset requests"""
    st.subheader("Reset Password")
    
    with st.form("reset_form"):
        email = st.text_input("Enter your email address")
        submitted = st.form_submit_button("Send Reset Link")
        
        if submitted and email:
            user_service = UserService()
            if user_service.send_password_reset(email):
                st.success("If an account exists with this email, you will receive a password reset link shortly.")
                # Add delay for user to read message
                time.sleep(2)
                st.session_state.show_reset = False
                st.rerun()
            else:
                st.error("Unable to process reset request. Please verify your email address.")

if __name__ == "__main__":
    main()