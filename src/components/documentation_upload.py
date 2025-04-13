
import streamlit as st
import logging

def show_documentation():
    st.subheader("Process Documentation")
    
    # Process flow diagrams
    flow_diagrams = st.file_uploader(
        "Process Flow Diagrams",
        type=['png', 'jpg', 'pdf'],
        accept_multiple_files=True,
        help="Upload any existing process flow diagrams"
    )
    
    # Current process documentation
    process_docs = st.file_uploader(
        "Current Process Documentation",
        type=['pdf', 'docx', 'xlsx'],
        accept_multiple_files=True,
        help="Upload any existing process documentation"
    )
    
    # Data samples
    data_samples = st.file_uploader(
        "Sample Data Files",
        type=['csv', 'xlsx', 'json'],
        accept_multiple_files=True,
        help="Upload sample data files (optional)"
    )
