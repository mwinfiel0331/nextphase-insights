
import streamlit as st
from typing import Optional, List
import logging
def client_intake():
    st.subheader("Business Assessment")
    
    # Business Overview
    st.markdown("### Business Overview")
    business_description = st.text_area(
        "Business Description*",
        placeholder="Briefly describe your business and its primary operations",
        help="Provide a high-level overview of your business activities"
    )
    
    # Challenges and Goals
    st.markdown("### Challenges and Goals")
    current_challenges = st.text_area(
        "Current Workflow Challenges*",
        placeholder="What are the main challenges you're facing with your current workflows?"
    )
    
    primary_pain_point = st.text_area(
        "Primary Pain Point*",
        placeholder="Describe your biggest pain point in more detail"
    )
    
    optimization_goals = st.text_area(
        "Optimization Goals*",
        placeholder="""What specific outcomes are you looking to achieve through process optimization? 
        For example:
        - Reduce processing time by X%
        - Automate specific manual tasks
        - Improve accuracy and reduce errors
        - Better visibility into process bottlenecks
        - Integration between existing systems
        """,
        help="Define clear, measurable goals you'd like to achieve through our collaboration"
    )

