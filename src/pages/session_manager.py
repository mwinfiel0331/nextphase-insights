import streamlit as st
from ..services.db_service import get_all_clients, save_session_data, get_client_sessions
import datetime

def show_sessions():
    st.title("Optimization Session Manager")
    
    # Get all clients
    clients = get_all_clients()
    
    # Client selection
    selected_client = st.selectbox(
        "Select Client",
        options=[client['company_name'] for client in clients],
        key="session_client_select"
    )
    
    if selected_client:
        client = next((c for c in clients if c['company_name'] == selected_client), None)
        
        if client:
            # Display client info
            st.subheader(f"Session for {client['company_name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"Industry: {client['industry']}")
            with col2:
                st.info(f"Company Size: {client['company_size']}")
            
            # Add tabs for form and history
            tab1, tab2 = st.tabs(["New Session", "Session History"])
            
            with tab1:
                # Session Form
                with st.form("session_form"):
                    session_type = st.selectbox(
                        "Session Type",
                        ["Initial Assessment", "Process Mapping", "Tool Integration", "Training", "Review"]
                    )
                    
                    notes = st.text_area(
                        "Session Notes",
                        placeholder="Document key findings, decisions, and next steps..."
                    )
                    
                    action_items = st.text_area(
                        "Action Items",
                        placeholder="List specific tasks and responsibilities..."
                    )
                    
                    progress = st.slider(
                        "Overall Progress",
                        0, 100, 
                        help="Estimate the overall optimization progress"
                    )
                    
                    submitted = st.form_submit_button("Save Session")
                    
                    if submitted:
                        try:
                            session_data = {
                                "client_id": client['company_id'],
                                "session_type": session_type,
                                "notes": notes,
                                "action_items": action_items,
                                "progress": progress,
                                "timestamp": datetime.datetime.now().isoformat()
                            }
                            save_session_data(session_data)
                            st.success("Session saved successfully!")
                            
                        except Exception as e:
                            st.error(f"Error saving session: {str(e)}")
            
            with tab2:
                sessions = get_client_sessions(client['company_id'])
                if sessions:
                    for session in sorted(sessions, key=lambda x: x['created_at'], reverse=True):
                        with st.expander(f"{session['session_type']} - {session['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                            st.write(f"**Notes:** {session['notes']}")
                            st.write(f"**Action Items:** {session['action_items']}")
                            st.progress(session['progress'])
                else:
                    st.info("No sessions recorded yet")