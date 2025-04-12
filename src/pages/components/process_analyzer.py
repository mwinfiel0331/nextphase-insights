import streamlit as st
from ...utils.ai_analyzer import ProcessAnalyzer
from ...config import Config
import uuid

def show_process_analysis(client_data=None):
    """Display AI-powered process analysis
    
    Args:
        client_data (dict, optional): Client-specific data. Defaults to None.
    """
    st.subheader("🤖 AI Process Analysis")
    
    # Create unique form key using UUID
    form_key = f"process_analysis_form_{uuid.uuid4().hex}"
    
    with st.form(key=form_key):
        # Form inputs
        process_name = st.text_input(
            "Process Name",
            value="Invoice Processing"
        )
        
        steps_text = st.text_area(
            "Current Process Steps (one per line)",
            value="Manual data entry\nEmail approvals\nPayment processing"
        )
        current_steps = [s.strip() for s in steps_text.split('\n') if s.strip()]
        
        industry = st.selectbox(
            "Industry",
            options=Config.INDUSTRIES
        )
        
        analyze_button = st.form_submit_button("Analyze Process")
        
        if analyze_button:
            try:
                with st.spinner("Analyzing process..."):
                    analyzer = ProcessAnalyzer()
                    recommendations = analyzer.get_process_recommendations(
                        process_name=process_name,
                        current_steps=current_steps,
                        industry=industry
                    )
                    
                    st.success("Analysis complete!")
                    st.json(recommendations)
                    
                    # Use client data if available, otherwise defaults
                    process_details = {
                        'name': process_name,
                        'description': f"Steps: {', '.join(current_steps)}",
                        'tools': client_data.get('tools', Config.DEFAULT_TOOLS) if client_data else Config.DEFAULT_TOOLS,
                        'frequency': client_data.get('frequency', Config.DEFAULT_FREQUENCY) if client_data else Config.DEFAULT_FREQUENCY
                    }
                    
                    score = analyzer.score_automation_potential(process_details)
                    st.metric("Automation Potential", f"{score:.0f}%")
                    
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")