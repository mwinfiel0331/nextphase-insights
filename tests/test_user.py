import pytest
from datetime import datetime
from src.models.user import User
from src.services.user_service import UserService

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        'email': 'test.user@example.com',
        'full_name': 'Test User',
        'company_name': 'Test Company',
        'app_role': 'client',
        'is_active': True,
        'password': 'securepass123'  # Only used for creation
    }

@pytest.fixture
def user_service(db):
    """Initialize user service with test database"""
    return UserService(db)

def test_create_user(user_service, test_user_data):
    """Test creating a new user"""
    result = user_service.create_user(test_user_data)
    
    assert result is not None
    assert isinstance(result, dict)
    assert result['email'] == test_user_data['email']
    assert result['app_role'] == 'client'
    assert result['is_active'] is True
    assert 'user_id' in result
    assert 'password' not in result  # Password should not be returned

def test_create_user_missing_fields(user_service):
    """Test creating user with missing required fields"""
    incomplete_data = {'email': 'test@example.com'}
    
    with pytest.raises(ValueError):
        user_service.create_user(incomplete_data)

def test_get_user_by_email(user_service, test_user_data):
    """Test retrieving user by email"""
    created = user_service.create_user(test_user_data)
    result = user_service.get_user_by_email(test_user_data['email'])
    
    assert result is not None
    assert result['email'] == test_user_data['email']
    assert result['user_id'] == created['user_id']

def test_authenticate_user(user_service, test_user_data):
    """Test user authentication"""
    user_service.create_user(test_user_data)
    
    # Test valid credentials
    success, user = user_service.authenticate(
        test_user_data['email'],
        test_user_data['password']
    )
    assert success is True
    assert user is not None
    assert user['email'] == test_user_data['email']
    
    # Test invalid password
    success, user = user_service.authenticate(
        test_user_data['email'],
        'wrongpassword'
    )
    assert success is False
    assert user is None

def test_update_user(user_service, test_user_data):
    """Test updating user details"""
    created = user_service.create_user(test_user_data)
    
    updates = {
        'full_name': 'Updated Name',
        'company_name': 'New Company'
    }
    
    updated = user_service.update_user(created['user_id'], updates)
    assert updated is True
    
    result = user_service.get_user_by_id(created['user_id'])
    assert result['full_name'] == 'Updated Name'
    assert result['company_name'] == 'New Company'

def test_deactivate_user(user_service, test_user_data):
    """Test deactivating a user"""
    created = user_service.create_user(test_user_data)
    
    deactivated = user_service.update_user(
        created['user_id'],
        {'is_active': False}
    )
    assert deactivated is True
    
    result = user_service.get_user_by_id(created['user_id'])
    assert result['is_active'] is False

def test_list_active_users(user_service, test_user_data):
    """Test listing all active users"""
    user_service.create_user(test_user_data)
    
    results = user_service.list_users(active_only=True)
    
    assert len(results) > 0
    for user in results:
        assert user['is_active'] is True