import pytest
from datetime import datetime
from src.models.client_process_step import ClientProcessStep
from src.services.client_process_step_service import ClientProcessStepService

@pytest.fixture
def test_step_data():
    """Sample process step data for testing"""
    return {
        'process_id': 'test-process-123',
        'step_name': 'Review Document',
        'step_description': 'Initial document review and validation',
        'step_order': 1,
        'estimated_time': '30 minutes',
        'required_tools': ['Adobe Reader', 'Microsoft Word'],
        'status': 'pending',
        'assignee': 'test@example.com'
    }

@pytest.fixture
def step_service(db):
    """Initialize process step service with test database"""
    return ClientProcessStepService(db)

def test_create_process_step(step_service, test_step_data):
    """Test creating a new process step"""
    result = step_service.create_step(test_step_data)
    
    assert result is not None
    assert isinstance(result, ClientProcessStep)
    assert result.step_name == test_step_data['step_name']
    assert result.step_order == test_step_data['step_order']
    assert result.status == 'pending'
    assert result.step_id is not None

def test_create_step_missing_fields(step_service):
    """Test creating step with missing required fields"""
    incomplete_data = {'step_name': 'Test Step'}
    
    with pytest.raises(ValueError):
        step_service.create_step(incomplete_data)

def test_get_steps_by_process(step_service, test_step_data):
    """Test retrieving all steps for a process"""
    # Create test step
    created = step_service.create_step(test_step_data)
    
    # Get steps for process
    results = step_service.get_process_steps(test_step_data['process_id'])
    
    assert len(results) > 0
    assert isinstance(results[0], ClientProcessStep)
    assert results[0].process_id == test_step_data['process_id']
    assert results[0].step_id == created.step_id

def test_update_step_status(step_service, test_step_data):
    """Test updating step status"""
    # Create test step
    created = step_service.create_step(test_step_data)
    
    # Update status
    updated = step_service.update_step(
        created.step_id,
        {'status': 'completed'}
    )
    
    assert updated is True
    
    # Verify update
    result = step_service.get_step(created.step_id)
    assert result.status == 'completed'

def test_reorder_steps(step_service, test_step_data):
    """Test reordering process steps"""
    # Create multiple steps
    step1 = test_step_data.copy()
    step1['step_order'] = 1
    step2 = test_step_data.copy()
    step2['step_order'] = 2
    
    created1 = step_service.create_step(step1)
    created2 = step_service.create_step(step2)
    
    # Reorder steps
    reordered = step_service.reorder_steps([
        {'step_id': created1.step_id, 'step_order': 2},
        {'step_id': created2.step_id, 'step_order': 1}
    ])
    
    assert reordered is True
    
    # Verify new order
    steps = step_service.get_process_steps(test_step_data['process_id'])
    assert steps[0].step_id == created2.step_id
    assert steps[0].step_order == 1
    assert steps[1].step_id == created1.step_id
    assert steps[1].step_order == 2

def test_delete_step(step_service, test_step_data):
    """Test deleting a process step"""
    # Create test step
    created = step_service.create_step(test_step_data)
    
    # Delete step
    deleted = step_service.delete_step(created.step_id)
    assert deleted is True
    
    # Verify deletion
    result = step_service.get_step(created.step_id)
    assert result is None