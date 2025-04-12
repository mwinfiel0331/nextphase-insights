import streamlit as st
from ...utils.ai_analyzer import ProcessAnalyzer

def show_process_analysis(client_data: dict = None):
    """Display AI-powered process analysis"""
    if client_data is None:
        client_data = {}
        
    st.subheader("🤖 AI Process Analysis")
    
    analyzer = ProcessAnalyzer()
    
    with st.form("process_analysis_form"):
        process_name = st.text_input("Process Name", "Invoice Processing")
        
        steps_text = st.text_area(
            "Current Process Steps (one per line)",
            "Manual data entry\nEmail approvals\nPayment processing"
        )
        current_steps = [step.strip() for step in steps_text.split("\n") if step.strip()]
        
        industry = st.selectbox(
            "Industry",
            ["Finance", "Healthcare", "Technology", "Manufacturing", "Retail"]
        )
        
        submitted = st.form_submit_button("Analyze Process")
        
        if submitted:
            with st.spinner("Analyzing process..."):
                try:
                    result = analyzer.get_process_recommendations(
                        process_name=process_name,
                        current_steps=current_steps,
                        industry=industry
                    )
                    
                    st.json(result['recommendations'])
                    
                    process_details = {
                        'name': process_name,
                        'description': f"Process steps: {', '.join(current_steps)}",
                        'tools': client_data.get('tool_selections', []),
                        'frequency': client_data.get('process_frequency', 'Daily')
                    }
                    
                    score = analyzer.score_automation_potential(process_details)
                    st.metric("Automation Potential", f"{score:.0f}%")
                    
                except Exception as e:
                    st.error(f"Error analyzing process: {str(e)}")