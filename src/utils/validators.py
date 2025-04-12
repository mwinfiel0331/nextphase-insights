import re
from datetime import datetime
from typing import Dict, Any, Optional

class ValidationError(Exception):
    pass

def validate_client_data(data: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Validates client intake data before saving to Firestore
    
    Args:
        data (dict): Client data to validate
    Returns:
        Optional[Dict[str, str]]: Dictionary of validation errors, if any
    """
    errors = {}

    # Required fields
    required_fields = ['company_name', 'industry', 'company_size', 'contact_email']
    for field in required_fields:
        if not data.get(field):
            errors[field] = f"{field} is required"

    # Email validation
    if data.get('contact_email'):
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, data['contact_email']):
            errors['contact_email'] = "Invalid email format"

    # Industry validation
    valid_industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Other']
    if data.get('industry') and data['industry'] not in valid_industries:
        errors['industry'] = "Invalid industry selection"

    # Company size validation
    valid_sizes = ['1-10', '11-50', '51-200', '201-500', '500+']
    if data.get('company_size') and data['company_size'] not in valid_sizes:
        errors['company_size'] = "Invalid company size"

    return errors if errors else None