import streamlit as st
import sys
from pathlib import Path

# Add src to Python path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

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

# Navigation
st.sidebar.title("NextPhase Insights")
pages = {
    "Dashboard": show_dashboard,
    "Client Intake": show_intake_form,
    "Session Manager": show_sessions
}

selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
pages[selected_page]()