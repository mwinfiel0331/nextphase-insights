import pytest
import streamlit as st
from src.pages.intake_form import show_intake_form, show_client_info
from src.services.intake_service import IntakeService
from unittest.mock import Mock, patch

@pytest.fixture
def mock_session_state():
    """Mock Streamlit session state"""
    with patch('streamlit.session_state', create=True) as mock_state:
        mock_state.form_section = 0
        mock_state.form_data = {}
        mock_state.page = "intake_form"
        yield mock_state

@pytest.fixture
def mock_user_data():
    """Sample user data for testing"""
    return {
        'uid': 'test123',
        'company_name': 'Test Company',
        'contact_name': 'John Doe',
        'contact_email': 'john@testcompany.com',
        'contact_role': 'Process Manager'
    }

@pytest.fixture
def mock_intake_service():
    """Mock IntakeService"""
    with patch('src.services.intake_service.IntakeService') as mock_service:
        instance = mock_service.return_value
        instance.save_intake.return_value = 'test_intake_id'
        yield instance

def test_company_info_section(mock_session_state, mock_user_data):
    """Test company information section of the form"""
    with patch('streamlit.text_input') as mock_text_input, \
         patch('streamlit.selectbox') as mock_select, \
         patch('streamlit.select_slider') as mock_slider:
        
        # Set up mock returns
        mock_text_input.return_value = 'Test Company'
        mock_select.return_value = 'Technology'
        mock_slider.return_value = '11-50'
        
        # Show company info section
        show_client_info(mock_user_data)
        
        # Verify form fields were displayed
        mock_text_input.assert_any_call(
            "Company Name*",
            value="Test Company",
            help="Legal name of the company"
        )
        
        mock_select.assert_called_with(
            "Industry*",
            options=[
                "Technology",
                "Healthcare",
                "Finance",
                "Manufacturing",
                "Retail",
                "Education",
                "Professional Services",
                "Other"
            ],
            index=0
        )

def test_form_submission(mock_session_state, mock_user_data, mock_intake_service):
    """Test form submission process"""
    with patch('streamlit.button') as mock_button:
        mock_button.return_value = True
        
        # Prepare form data
        mock_session_state.form_data = {
            'company_name': 'Test Company',
            'industry': 'Technology',
            'team_size': 50,
            'process_name': 'Test Process',
            'process_description': 'Test Description',
            'current_challenges': 'Test Challenges',
            'desired_outcomes': 'Test Outcomes'
        }
        
        # Submit form
        submit_form(mock_user_data['uid'])
        
        # Verify intake service was called
        mock_intake_service.save_intake_form.assert_called_once_with(
            mock_user_data['uid'],
            mock_session_state.form_data
        )

def test_form_navigation(mock_session_state, mock_user_data):
    """Test form navigation between sections"""
    with patch('streamlit.button') as mock_button:
        mock_button.return_value = True
        
        # Initial section should be 0
        assert mock_session_state.form_section == 0
        
        # Click next
        show_intake_form(mock_user_data)
        assert mock_session_state.form_section == 1
        
        # Move to last section
        mock_session_state.form_section = 3
        show_intake_form(mock_user_data)
        
        # Verify submit button is shown in last section
        mock_button.assert_any_call("Submit", type="primary")

@pytest.mark.parametrize("invalid_data", [
    {'company_name': ''},  # Empty company name
    {'industry': 'Invalid'},  # Invalid industry
    {'team_size': -1},  # Invalid team size
])
def test_form_validation(mock_session_state, mock_user_data, invalid_data):
    """Test form validation with invalid data"""
    with patch('src.utils.validators.validate_client_data') as mock_validate:
        mock_validate.return_value = False
        
        mock_session_state.form_data = invalid_data
        with pytest.raises(ValueError):
            submit_form(mock_user_data['uid'])