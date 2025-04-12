import pytest
from datetime import datetime

def test_firebase_connection(firebase_client):
    """Test Firebase connection and basic operations"""
    test_doc = {
        'test_id': f'test_{datetime.now().timestamp()}',
        'timestamp': datetime.now()
    }
    
    # Write test document
    ref = firebase_client.collection('test').document('test_doc')
    ref.set(test_doc)
    
    # Read test document
    doc = ref.get()
    assert doc.exists
    assert doc.to_dict()['test_id'] == test_doc['test_id']
    
    # Clean up
    ref.delete()