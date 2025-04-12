import streamlit as st
from src.pages.auth.login import show_login
from src.pages.dashboard import show_dashboard
from src.pages.intake_form import show_intake_form
from src.pages.session_manager import show_sessions

# Configure Streamlit
st.set_page_config(
    page_title="NextPhase Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if 'is_authenticated' not in st.session_state:
    st.session_state['is_authenticated'] = False

if not st.session_state['is_authenticated']:
    show_login()
else:
    # Navigation
    st.sidebar.title("NextPhase Insights")
    
    # User info in sidebar
    if 'user' in st.session_state:
        user = st.session_state['user']
        st.sidebar.markdown(f"**{user['company_name']}**")
        st.sidebar.markdown(f"*{user['full_name']}*")
    
    # Navigation menu
    pages = {
        "Dashboard": show_dashboard,
        "Client Intake": show_intake_form,
        "Session Manager": show_sessions
    }
    
    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
    
    # Logout button
    if st.sidebar.button("Sign Out"):
        st.session_state['is_authenticated'] = False
        st.session_state['user'] = None
        st.rerun()
    
    # Show selected page
    pages[selected_page]()