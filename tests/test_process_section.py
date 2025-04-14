import pytest
from datetime import datetime
from firebase_admin import firestore
from src.models.process_section import ProcessSection
from src.services.process_section_service import ProcessSectionService

@pytest.fixture
def test_section_data():
    """Sample process section data for testing"""
    return {
        'process_id': 'test-process-123',
        'section_name': 'Document Processing',
        'section_description': 'Handle incoming documents and validation',
        'section_order': 1,
        'expected_duration': '2 hours',
        'dependencies': [],
        'owner': 'test@example.com',
        'status': 'not_started',
        'created_at': firestore.SERVER_TIMESTAMP,
        'updated_at': firestore.SERVER_TIMESTAMP
    }

@pytest.fixture
def section_service(db):
    """Initialize section service with test database"""
    return ProcessSectionService(db)

def test_create_section(section_service, test_section_data):
    """Test creating a new process section"""
    result = section_service.create_section(test_section_data)
    
    assert result is not None
    assert isinstance(result, ProcessSection)
    assert result.section_name == test_section_data['section_name']
    assert result.process_id == test_section_data['process_id']
    assert result.section_id is not None

def test_get_sections_by_process(section_service, test_section_data):
    """Test retrieving sections for a process"""
    created = section_service.create_section(test_section_data)
    
    results = section_service.get_process_sections(test_section_data['process_id'])
    
    assert len(results) > 0
    assert isinstance(results[0], ProcessSection)
    assert results[0].process_id == test_section_data['process_id']
    assert results[0].section_id == created.section_id

def test_update_section_status(section_service, test_section_data):
    """Test updating section status"""
    created = section_service.create_section(test_section_data)
    
    updated = section_service.update_section(
        created.section_id,
        {'status': 'in_progress'}
    )
    
    assert updated is True
    result = section_service.get_section(created.section_id)
    assert result.status == 'in_progress'

def test_reorder_sections(section_service, test_section_data):
    """Test reordering process sections"""
    # Create two sections
    section1 = test_section_data.copy()
    section2 = test_section_data.copy()
    section2['section_order'] = 2
    
    created1 = section_service.create_section(section1)
    created2 = section_service.create_section(section2)
    
    # Reorder them
    new_order = [
        {'section_id': created1.section_id, 'section_order': 2},
        {'section_id': created2.section_id, 'section_order': 1}
    ]
    
    success = section_service.reorder_sections(new_order)
    assert success is True
    
    # Verify new order
    sections = section_service.get_process_sections(test_section_data['process_id'])
    assert sections[0].section_id == created2.section_id
    assert sections[0].section_order == 1
    assert sections[1].section_id == created1.section_id
    assert sections[1].section_order == 2

def test_delete_section(section_service, test_section_data):
    """Test deleting a process section"""
    created = section_service.create_section(test_section_data)
    
    deleted = section_service.delete_section(created.section_id)
    assert deleted is True
    
    result = section_service.get_section(created.section_id)
    assert result is None