import pytest
from datetime import datetime
from src.models.client import Client
from src.services.client_service import ClientService

@pytest.fixture
def test_client_data():
    """Sample client data for testing"""
    return {
        'user_id': 'test-user-123',
        'company_name': 'Acme Corporation',
        'industry': 'Technology',
        'company_size': '51-200',
        'contact_name': 'John Doe',
        'contact_email': 'john.doe@acme.com',
        'contact_role': 'Process Manager',
        'status': 'active'
    }

@pytest.fixture
def client_service(db):
    """Initialize client service with test database"""
    return ClientService(db)

def test_create_client(client_service, test_client_data):
    """Test creating a new client"""
    result = client_service.create_client(test_client_data)
    
    assert result is not None
    assert isinstance(result, Client)
    assert result.company_name == test_client_data['company_name']
    assert result.user_id == test_client_data['user_id']
    assert result.client_id is not None
    assert result.status == 'active'

def test_create_client_missing_fields(client_service):
    """Test creating client with missing required fields"""
    incomplete_data = {'company_name': 'Test Company'}
    
    with pytest.raises(ValueError):
        client_service.create_client(incomplete_data)

def test_get_client_by_id(client_service, test_client_data):
    """Test retrieving client by ID"""
    created = client_service.create_client(test_client_data)
    result = client_service.get_client(created.client_id)
    
    assert result is not None
    assert result.client_id == created.client_id
    assert result.company_name == test_client_data['company_name']

def test_get_client_by_user_id(client_service, test_client_data):
    """Test retrieving client by user ID"""
    client_service.create_client(test_client_data)
    result = client_service.get_client_by_user_id(test_client_data['user_id'])
    
    assert result is not None
    assert result.user_id == test_client_data['user_id']
    assert result.company_name == test_client_data['company_name']

def test_update_client(client_service, test_client_data):
    """Test updating client details"""
    created = client_service.create_client(test_client_data)
    
    updates = {
        'company_name': 'Updated Company Name',
        'company_size': '201-500'
    }
    
    updated = client_service.update_client(created.client_id, updates)
    assert updated is True
    
    result = client_service.get_client(created.client_id)
    assert result.company_name == 'Updated Company Name'
    assert result.company_size == '201-500'

def test_list_active_clients(client_service, test_client_data):
    """Test listing all active clients"""
    client_service.create_client(test_client_data)
    
    results = client_service.list_clients(status='active')
    
    assert len(results) > 0
    for client in results:
        assert isinstance(client, Client)
        assert client.status == 'active'

def test_deactivate_client(client_service, test_client_data):
    """Test deactivating a client"""
    created = client_service.create_client(test_client_data)
    
    deactivated = client_service.update_client_status(created.client_id, 'inactive')
    assert deactivated is True
    
    result = client_service.get_client(created.client_id)
    assert result.status == 'inactive'