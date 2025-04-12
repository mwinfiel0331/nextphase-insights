import re
from typing import Dict, Any

def validate_client_data(data: Dict[str, Any]):
    """Validate client intake data"""
    errors = []
    
    # Required fields
    required_fields = {
        'company_name': 'Company name is required',
        'industry': 'Industry is required',
        'contact_email': 'Contact email is required'
    }
    
    for field, message in required_fields.items():
        if not data.get(field):
            errors.append(message)
    
    # Email validation
    if data.get('contact_email'):
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, data['contact_email']):
            errors.append('Invalid email format')
    
    # Tools validation
    if not data.get('current_tools'):
        errors.append('Please select at least one current tool')
    
    # Process count validation
    if data.get('manual_processes', 0) < 1:
        errors.append('Number of manual processes must be at least 1')
    
    return errors

def validate_session_data(data: Dict[str, Any]):
    """Validate session data"""
    errors = []
    
    required_fields = {
        'client_id': 'Client ID is required',
        'session_type': 'Session type is required',
        'notes': 'Session notes are required'
    }
    
    for field, message in required_fields.items():
        if not data.get(field):
            errors.append(message)
    
    if data.get('progress') is not None and not 0 <= data['progress'] <= 100:
        errors.append('Progress must be between 0 and 100')
    
    return errors