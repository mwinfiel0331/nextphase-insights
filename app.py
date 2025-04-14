import streamlit as st
from firebase_admin import firestore
from src.config.firebase_config import initialize_firebase
from src.pages.admindashboard import show_admin_dashboard
from src.pages.clientdashboard import show_client_dashboard
from src.pages.intake_form import show_intake_form
from src.services.client_intake_service import ClientIntakeService  # Fix import name
from src.services.user_service import UserService
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "show_intake_form" not in st.session_state:
        st.session_state.show_intake_form = False


def init_styling():
    """Initialize app styling"""
    st.markdown("""
        <style>
        .header-container {
            display: flex;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .logo-img {
            width: 200px;
            margin-right: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        # Initialize Firebase first
        if 'db' not in st.session_state:
            st.session_state.db = initialize_firebase()
            
        # Configure Streamlit
        st.set_page_config(
            page_title="NextPhase Insights",
            page_icon="🚀",
            layout="wide"
        )
        
        init_session_state()
        init_styling()        
    except Exception as e:
        st.error(f"Application initialization error: {e}")
        logger.error(f"Application initialization error: {str(e)}")


    
    # Display logo in header
    logo_path = "src/assets/nextphase-insights-logo.png"
    header_col1, header_col2 = st.columns([1, 4])
    
    with header_col1:
        try:
            st.image(logo_path, width=200)
        except Exception as e:
            logger.error(f"Failed to load logo: {str(e)}")
            st.write("NextPhase Insights")
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
        
    
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        user_data = st.session_state.user_data  
        app_role = st.session_state.user_data.get('app_role')
        
        # Check if we should show intake form
        if st.session_state.get('show_intake_form', False):
            show_intake_form(user_data)
        else:
            if app_role == 'admin':
                show_admin_dashboard(user_data)
            elif app_role == 'client':
                show_client_dashboard(user_data)
            else:
                st.error("Unauthorized access. Please contact support.")


def show_auth_page():
    """Handle user authentication"""
    st.title("Welcome to NextPhase Insights")
    
    # Initialize Firebase and get db instance
    db = firestore.client()
    user_service = UserService(db)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        # Show password reset form if requested
        if st.session_state.get('show_reset', False):
            show_password_reset()
        else:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    submitted = st.form_submit_button("Login", use_container_width=False)
                with col2:
                    if st.form_submit_button("Forgot Password?", type="secondary", use_container_width=True):
                        logger.debug("Password reset requested")
                        st.session_state.show_reset = True
                        st.rerun()
                
                if submitted:
                    logger.debug(f"Login attempt for email: {email}")
                
                    if not email or not password:
                        st.error("Please enter both email and password")
                        return
                        
                    success, user_data = user_service.authenticate(email, password)
                    
                    if success:
                        logger.info(f"User logged in successfully: {email}")
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.session_state.app_role = user_data.get('app_role')
                        st.rerun()
                    else:
                        logger.warning(f"Login failed for email: {email}")
                        st.error("Invalid email or password")

    with tab2:
        with st.form("signup_form"):
            company_name = st.text_input("Company Name*")
            full_name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            password = st.text_input("Password*", type="password")
            
            if st.form_submit_button("Sign Up"):
                try:
                    # Validate required fields
                    if not all([company_name, full_name, email, password]):
                        st.error("All fields are required")
                        return

                    # Create user data dictionary
                    user_data = {
                        'company_name': company_name,
                        'full_name': full_name,
                        'email': email,
                        'password': password,  
                        'app_role': 'client',
                        'created_at': firestore.SERVER_TIMESTAMP,
                        'updated_at': firestore.SERVER_TIMESTAMP
                    }
                    
                    # Pass only user_data to create_user
                    created_user = user_service.create_user(user_data)
                    
                    if created_user:
                        st.success("Account created! Please log in.")
                        logger.info(f"New user account created: {email}")
                        # Clear form
                        st.session_state.clear()
                    else:
                        st.error("Failed to create account. Please try again.")
                        
                except Exception as e:
                    logger.error(f"Account creation error: {str(e)}")
                    st.error("Failed to create account. Please try again.")

def show_password_reset():
    """Handle password reset requests"""
    st.subheader("Reset Password")
    
    with st.form("reset_form"):
        email = st.text_input("Enter your email address")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.form_submit_button("Send Reset Link", use_container_width=False):
                if email:
                    user_service = UserService()
                    if user_service.send_password_reset(email):
                        st.success("If an account exists with this email, you will receive a password reset link shortly.")
                        time.sleep(2)
                        st.session_state.show_reset = False
                        st.rerun()
                    else:
                        st.error("Unable to process reset request. Please verify your email address.")
                else:
                    st.error("Please enter your email address")
    
    # Navigation buttons outside the form
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Login", use_container_width=False):
            st.session_state.show_reset = False
            st.rerun()
            
    

    # Additional help text
    st.markdown("---")
    st.caption("Need help? Contact support@nextphaseinsights.com")

if __name__ == "__main__":
    main()