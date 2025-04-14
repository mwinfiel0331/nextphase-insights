import pytest
from datetime import datetime
from src.models.client_intake import ClientIntake
from src.services.client_intake_service import ClientIntakeService

@pytest.fixture
def test_intake_data():
    """Sample intake data for testing"""
    return {
        'client_email': 'test@example.com',
        'business_description': 'Test business description',
        'current_challenges': 'Test challenges',
        'primary_pain_point': 'Test pain point',
        'optimization_goals': 'Test goals',
        'workflow_status': 'draft'
    }

@pytest.fixture
def intake_service(db):
    """Initialize intake service with test database"""
    return ClientIntakeService(db)

def test_create_intake(intake_service, test_intake_data):
    """Test creating a new intake form"""
    result = intake_service.create_intake(test_intake_data)
    
    assert result is not None
    assert isinstance(result, ClientIntake)
    assert result.client_email == test_intake_data['client_email']
    assert result.workflow_status == 'draft'
    assert result.intake_id is not None

def test_create_intake_missing_fields(intake_service):
    """Test creating intake with missing required fields"""
    incomplete_data = {'client_email': 'test@example.com'}
    
    with pytest.raises(ValueError):
        intake_service.create_intake(incomplete_data)

def test_get_intake_by_client(intake_service, test_intake_data):
    """Test retrieving intake by client email"""
    # Create test intake
    created = intake_service.create_intake(test_intake_data)
    
    # Retrieve it
    result = intake_service.get_client_intake(test_intake_data['client_email'])
    
    assert result is not None
    assert result.client_email == test_intake_data['client_email']
    assert result.intake_id == created.intake_id

def test_update_intake_status(intake_service, test_intake_data):
    """Test updating intake workflow status"""
    # Create test intake
    created = intake_service.create_intake(test_intake_data)
    
    # Update status
    updated = intake_service.update_intake(
        created.intake_id,
        {'workflow_status': 'submitted'}
    )
    
    assert updated is True
    
    # Verify update
    result = intake_service.get_intake(created.intake_id)
    assert result.workflow_status == 'submitted'

def test_list_client_intakes(intake_service, test_intake_data):
    """Test listing all intakes for a client"""
    # Create multiple intakes
    intake_service.create_intake(test_intake_data)
    intake_service.create_intake(test_intake_data)
    
    # List intakes
    results = intake_service.list_intakes(test_intake_data['client_email'])
    
    assert len(results) >= 2
    for intake in results:
        assert isinstance(intake, ClientIntake)
        assert intake.client_email == test_intake_data['client_email']