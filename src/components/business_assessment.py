
import streamlit as st
from typing import Optional, List
import logging
def show_business_assessment():
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
    
    main_pain_point = st.text_area(
        "Primary Pain Point*",
        placeholder="Describe your biggest pain point in more detail"
    )
    
    partnership_goals = st.text_area(
        "Partnership Goals*",
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

    # Current Tools Assessment
    st.markdown("### Current Tools & Systems")
    
    tool_categories = {
        "Communication & Messaging": [
            "Slack",
            "Microsoft Teams",
            "Discord",
            "Zoom",
            "Google Meet",
            "Other"
        ],
        "Task & Project Management": [
            "Asana",
            "Trello",
            "Jira",
            "Monday.com",
            "ClickUp",
            "Other"
        ],
        "Calendar & Scheduling": [
            "Google Calendar",
            "Outlook",
            "Calendly",
            "Other"
        ],
        "Productivity": [
            "Microsoft Office",
            "Google Workspace",
            "Notion",
            "Evernote",
            "Other"
        ],
        "CRM": [
            "Salesforce",
            "HubSpot",
            "Zoho",
            "None",
            "Other"
        ],
        "E-commerce & Payments": [
            "Shopify",
            "WooCommerce",
            "Stripe",
            "PayPal",
            "Square",
            "None",
            "Other"
        ],
        "Data & Analytics": [
            "Google Analytics",
            "Tableau",
            "Power BI",
            "None",
            "Other"
        ],
        "Social Media Management": [
            "Hootsuite",
            "Buffer",
            "Later",
            "None",
            "Other"
        ],
        "Cloud Services": [
            "AWS",
            "Google Cloud",
            "Azure",
            "Dropbox",
            "None",
            "Other"
        ],
        "Marketing & Advertising": [
            "Google Ads",
            "Meta Ads",
            "Mailchimp",
            "None",
            "Other"
        ],
        "Automation & Workflow": [
            "Zapier",
            "Make (Integromat)",
            "Power Automate",
            "None",
            "Other"
        ],
        "Customer Support": [
            "Zendesk",
            "Intercom",
            "Freshdesk",
            "None",
            "Other"
        ]
          

    }
  
    # Create columns for tool selection
    st.markdown("### Tool Assessment")
    st.caption("Select the tools and systems currently in use")
    
    tool_selections = {}
    for category, tools in tool_categories.items():
        st.markdown(f"**{category}**")
        tool_selections[category] = st.multiselect(
            f"Select {category} tools",
            options=tools,
            key=f"tools_{category.lower().replace(' ', '_')}"
        )
        
        # If "Other" is selected, show text input
        if "Other" in tool_selections[category]:
            other_tool = st.text_input(
                f"Please specify other {category} tools",
                key=f"other_{category.lower().replace(' ', '_')}"
            )
            if other_tool:
                tool_selections[category].append(other_tool)

