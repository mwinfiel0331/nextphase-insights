import streamlit as st
from ...services.auth_service import create_user, sign_in_user
from ...services.db_service import get_industries

def show_login():
    """Display login/registration interface"""
    st.title("NextPhase Insights")
    st.markdown("### Process Optimization Platform")
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_registration_form()

def show_login_form():
    """Display the login form"""
    with st.form("login_form"):
        st.subheader("Welcome Back")
        
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password")
                return
                
            try:
                user = sign_in_user(email, password)
                if user:
                    # Set session state
                    st.session_state['user'] = user
                    st.session_state['is_authenticated'] = True
                    st.session_state['client_id'] = user.get('client_id')
                    st.session_state['is_admin'] = user.get('is_admin', False)
                    
                    st.success("Successfully signed in!")
                    st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

def show_registration_form():
    """Display the registration form"""
    # Get industries from database
    industries = get_industries()
    
    with st.form("registration_form"):
        st.subheader("Create Your Account")
        
        # Company Information
        st.markdown("#### Company Information")
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name*")
            industry = st.selectbox(
                "Industry*",
                options=industries if industries else ["Other"],
                help="Select the primary industry of your business"
            )
        
        with col2:
            company_size = st.select_slider(
                "Company Size*",
                options=["1-10", "11-50", "51-200", "201-500", "500+"]
            )
            website = st.text_input("Company Website")
        
        # Contact Information
        st.markdown("#### Contact Information")
        col3, col4 = st.columns(2)
        
        with col3:
            full_name = st.text_input("Full Name*")
            email = st.text_input("Business Email*")
        
        with col4:
            role = st.text_input("Job Title*")
            phone = st.text_input("Phone Number")
        
        # Account Security
        st.markdown("#### Account Security")
        password = st.text_input("Password*", type="password")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        # Terms and Conditions
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if not all([company_name, full_name, email, password, role, industry]):
                st.error("Please fill in all required fields")
                return
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return
                
            if not agree:
                st.error("Please agree to the Terms of Service")
                return
                
            try:
                user_data = {
                    'company_name': company_name,
                    'industry': industry,
                    'company_size': company_size,
                    'website': website,
                    'full_name': full_name,
                    'email': email,
                    'role': role,
                    'phone': phone
                }
                
                user = create_user(email, password, user_data)
                if user:
                    st.success("Account created successfully! Please sign in.")
                    st.balloons()
                    
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")