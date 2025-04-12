import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def env_setup():
    """Load environment variables for tests"""
    load_dotenv()
    return os.environ

@pytest.fixture(scope="session")
def firebase_client():
    """Initialize Firebase client for tests"""
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    
    return firestore.client()