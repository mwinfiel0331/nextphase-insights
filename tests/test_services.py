import pytest
from datetime import datetime
from src.services.user_service import UserService
from src.services.client_service import ClientService
from src.services.client_intake_service import ClientIntakeService
from src.services.client_process_service import ClientProcessService

@pytest.fixture
def services(db):
    """Initialize all services with test database"""
    return {
        'user': UserService(db),
        'client': ClientService(db),
        'intake': ClientIntakeService(db),
        'process': ClientProcessService(db)
    }

@pytest.fixture
def test_data():
    """Sample test data for service integration tests"""
    return {
        'user': {
            'email': 'test.user@example.com',
            'full_name': 'Test User',
            'company_name': 'Test Company',
            'app_role': 'client',
            'password': 'securepass123'
        },
        'client': {
            'company_name': 'Test Company',
            'industry': 'Technology',
            'company_size': '51-200'
        },
        'intake': {
            'business_description': 'Test business',
            'current_challenges': 'Test challenges',
            'optimization_goals': 'Test goals'
        },
        'process': {
            'process_name': 'Test Process',
            'process_description': 'Test process workflow',
            'process_goal': 'Improve efficiency'
        }
    }

def test_end_to_end_workflow(services, test_data):
    """Test complete user->client->intake->process workflow"""
    # 1. Create user
    user = services['user'].create_user(test_data['user'])
    assert user is not None
    assert user['email'] == test_data['user']['email']

    # 2. Create client for user
    client_data = test_data['client']
    client_data['user_id'] = user['user_id']
    client = services['client'].create_client(client_data)
    assert client is not None
    assert client.user_id == user['user_id']

    # 3. Create intake for client
    intake_data = test_data['intake']
    intake_data['client_id'] = client.client_id
    intake_data['client_email'] = user['email']
    intake = services['intake'].create_intake(intake_data)
    assert intake is not None
    assert intake.client_email == user['email']

    # 4. Create process for client
    process_data = test_data['process']
    process_data['client_id'] = client.client_id
    process = services['process'].create_process(process_data)
    assert process is not None
    assert process.client_id == client.client_id

def test_service_relationships(services, test_data):
    """Test relationships between services"""
    # Create user and client
    user = services['user'].create_user(test_data['user'])
    client_data = {**test_data['client'], 'user_id': user['user_id']}
    client = services['client'].create_client(client_data)

    # Test client service can find by user
    found_client = services['client'].get_client_by_user_id(user['user_id'])
    assert found_client is not None
    assert found_client.client_id == client.client_id

    # Test intake service links to client
    intake_data = {
        **test_data['intake'],
        'client_id': client.client_id,
        'client_email': user['email']
    }
    intake = services['intake'].create_intake(intake_data)
    found_intake = services['intake'].get_client_intake(user['email'])
    assert found_intake is not None
    assert found_intake.client_id == client.client_id

def test_service_error_handling(services):
    """Test error handling across services"""
    # Test user creation with duplicate email
    user_data = {
        'email': 'duplicate@example.com',
        'full_name': 'Test User',
        'password': 'test123'
    }
    services['user'].create_user(user_data)
    
    with pytest.raises(ValueError):
        services['user'].create_user(user_data)

    # Test client creation with invalid user
    with pytest.raises(ValueError):
        services['client'].create_client({
            'user_id': 'invalid-id',
            'company_name': 'Test Company'
        })

    # Test intake creation with invalid client
    with pytest.raises(ValueError):
        services['intake'].create_intake({
            'client_id': 'invalid-id',
            'business_description': 'Test'
        })