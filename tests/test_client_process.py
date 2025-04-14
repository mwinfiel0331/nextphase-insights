import pytest
from datetime import datetime
from src.models.client_process import ClientProcess
from src.services.client_process_service import ClientProcessService

@pytest.fixture
def test_process_data():
    """Sample process data for testing"""
    return {
        'client_id': 'test-client-123',
        'process_name': 'Invoice Processing',
        'process_description': 'End-to-end invoice processing workflow',
        'process_goal': 'Automate invoice handling',
        'process_start': datetime.now(),
        'process_end': None,
        'automation_needs': ['Document scanning', 'Data extraction'],
        'status': 'draft'
    }

@pytest.fixture
def process_service(db):
    """Initialize process service with test database"""
    return ClientProcessService(db)

def test_create_process(process_service, test_process_data):
    """Test creating a new client process"""
    result = process_service.create_process(test_process_data)
    
    assert result is not None
    assert isinstance(result, ClientProcess)
    assert result.process_name == test_process_data['process_name']
    assert result.client_id == test_process_data['client_id']
    assert result.status == 'draft'
    assert result.process_id is not None

def test_create_process_missing_fields(process_service):
    """Test creating process with missing required fields"""
    incomplete_data = {'process_name': 'Test Process'}
    
    with pytest.raises(ValueError):
        process_service.create_process(incomplete_data)

def test_get_process_by_id(process_service, test_process_data):
    """Test retrieving process by ID"""
    # Create test process
    created = process_service.create_process(test_process_data)
    
    # Retrieve it
    result = process_service.get_process(created.process_id)
    
    assert result is not None
    assert result.process_id == created.process_id
    assert result.process_name == test_process_data['process_name']

def test_get_client_processes(process_service, test_process_data):
    """Test retrieving all processes for a client"""
    # Create test process
    created = process_service.create_process(test_process_data)
    
    # Get client processes
    results = process_service.get_client_processes(test_process_data['client_id'])
    
    assert len(results) > 0
    assert isinstance(results[0], ClientProcess)
    assert results[0].client_id == test_process_data['client_id']

def test_update_process(process_service, test_process_data):
    """Test updating process details"""
    # Create test process
    created = process_service.create_process(test_process_data)
    
    # Update process
    updates = {
        'process_name': 'Updated Process Name',
        'status': 'in_progress'
    }
    
    updated = process_service.update_process(created.process_id, updates)
    assert updated is True
    
    # Verify updates
    result = process_service.get_process(created.process_id)
    assert result.process_name == 'Updated Process Name'
    assert result.status == 'in_progress'

def test_delete_process(process_service, test_process_data):
    """Test deleting a process"""
    # Create test process
    created = process_service.create_process(test_process_data)
    
    # Delete process
    deleted = process_service.delete_process(created.process_id)
    assert deleted is True
    
    # Verify deletion
    result = process_service.get_process(created.process_id)
    assert result is None

def test_process_status_transition(process_service, test_process_data):
    """Test process status transitions"""
    # Create test process
    created = process_service.create_process(test_process_data)
    
    # Test valid status transition
    updated = process_service.update_process_status(
        created.process_id, 
        'draft', 
        'in_progress'
    )
    assert updated is True
    
    # Verify status
    result = process_service.get_process(created.process_id)
    assert result.status == 'in_progress'
    
    # Test invalid status transition
    with pytest.raises(ValueError):
        process_service.update_process_status(
            created.process_id,
            'completed',
            'draft'
        )