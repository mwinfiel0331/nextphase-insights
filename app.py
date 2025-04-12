import streamlit as st
from intake_form import show_intake_form
from dashboard import show_dashboard

# Configure the Streamlit page
st.set_page_config(
    page_title="NextPhase Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("NextPhase Insights")
page = st.sidebar.radio("Navigation", ["Dashboard", "Client Intake"])

# Route to appropriate page
if page == "Dashboard":
    show_dashboard()
elif page == "Client Intake":
    show_intake_form()