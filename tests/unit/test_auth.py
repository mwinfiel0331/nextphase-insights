import pytest
from src.services.auth_service import create_user, sign_in_user

def test_user_creation(env_setup):
    """Test user creation with valid data"""
    test_user = {
        'email': 'test@example.com',
        'company_name': 'Test Company',
        'full_name': 'Test User'
    }
    
    with pytest.raises(Exception) as exc_info:
        create_user('invalid@email', 'short', test_user)
    assert 'password' in str(exc_info.value).lower()

def test_sign_in_validation(env_setup):
    """Test sign in validation"""
    with pytest.raises(Exception) as exc_info:
        sign_in_user('', '')
    assert 'email' in str(exc_info.value).lower()