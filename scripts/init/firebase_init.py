import firebase_admin
from firebase_admin import credentials
import os
import json
from pathlib import Path

def initialize_firebase():
    """Initialize Firebase with required configurations"""
    try:
        if not firebase_admin._apps:
            # Get project root directory
            root_dir = Path(__file__).parent.parent.parent
            
            # Look for service account key
            cred_files = list(root_dir.glob('*firebase-adminsdk*.json'))
            if not cred_files:
                raise ValueError("Firebase credentials not found")
            
            # Load service account
            with open(cred_files[0], 'r') as f:
                service_account = json.load(f)
            
            # Initialize Firebase with auth config
            cred = credentials.Certificate(service_account)
            firebase_admin.initialize_app(cred, {
                'projectId': service_account['project_id'],
                'databaseURL': f"https://{service_account['project_id']}.firebaseio.com",
                'storageBucket': f"{service_account['project_id']}.appspot.com",
            })
            return True
            
    except Exception as e:
        print(f"❌ Firebase initialization error: {str(e)}")
        return False