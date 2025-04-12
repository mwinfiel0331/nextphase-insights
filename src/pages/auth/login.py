import streamlit as st
from ...services.auth_service import create_user, sign_in_user

def show_login():
    """Display login/registration interface"""
    st.title("NextPhase Insights")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()

def show_login_form():
    """Display login form"""
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            try:
                user = sign_in_user(email, password)
                if user:
                    st.session_state['user'] = user
                    st.session_state['is_authenticated'] = True
                    st.session_state['client_id'] = user.get('client_id')
                    st.session_state['is_admin'] = user.get('is_admin', False)
                    st.success("Login successful!")
                    st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

def show_register_form():
    """Display registration form"""
    with st.form("register_form"):
        st.subheader("Create New Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name*")
            full_name = st.text_input("Full Name*")
        
        with col2:
            email = st.text_input("Business Email*")
            password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Confirm Password*", type="password")
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not all([company_name, full_name, email, password]):
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                try:
                    user = create_user(email, password, {
                        'company_name': company_name,
                        'full_name': full_name,
                        'email': email
                    })
                    if user:
                        st.success("Registration successful! Please log in.")
                        st.session_state['show_login'] = True
                        st.rerun()
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")