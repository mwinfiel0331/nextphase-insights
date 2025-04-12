import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore_admin_v1
from google.oauth2 import service_account
from pathlib import Path
import logging
import sys
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase Admin SDK and Admin client credentials"""
    try:
        if firebase_admin._apps:
            return True

        root_dir = Path(__file__).parent.parent
        cred_files = list(root_dir.glob('*firebase-adminsdk*.json'))
        
        if not cred_files:
            logger.error("Firebase credentials not found")
            return False
            
        cred_path = str(cred_files[0].absolute())
        logger.info(f"Using credentials from: {cred_path}")

        # Set environment variable for application default credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

        # Initialize Firebase Admin
        cred = credentials.Certificate(cred_path)
        app = firebase_admin.initialize_app(cred)

        # Create credentials for Admin SDK
        admin_credentials = service_account.Credentials.from_service_account_file(
            cred_path,
            scopes=[
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/datastore'
            ]
        )

        return admin_credentials

    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        return False

def create_index(collection_name: str, fields: list, credentials_info):
    """Create a Firestore index
    
    Args:
        collection_name (str): Name of the collection
        fields (list): List of tuples (field_name, direction)
                      direction should be 'ASCENDING' or 'DESCENDING'
        credentials_info: Service account credentials for Admin client
    """
    try:
        # Get project ID from credentials
        db = firestore.client()
        project_id = db._credentials.project_id
        
        # Create Admin client with explicit credentials
        admin_client = firestore_admin_v1.FirestoreAdminClient(
            credentials=credentials_info
        )
        
        # Prepare parent path
        parent = f"projects/{project_id}/databases/(default)/collectionGroups/{collection_name}"
        
        # Create field configs
        field_configs = []
        for field_name, direction in fields:
            field_configs.append(
                firestore_admin_v1.Index.IndexField(
                    field_path=field_name,
                    order=firestore_admin_v1.Index.IndexField.Order[direction]
                )
            )
        
        # Create index
        index = firestore_admin_v1.Index(
            query_scope=firestore_admin_v1.Index.QueryScope.COLLECTION,
            fields=field_configs
        )
        
        # Submit index creation request
        operation = admin_client.create_index(
            parent=parent,
            index=index
        )
        
        logger.info(f"Creating index for {collection_name}...")
        result = operation.result()  # Wait for completion
        logger.info(f"Index created successfully: {result.name}")
        return True

    except Exception as e:
        logger.error(f"Error creating index: {str(e)}")
        return False

if __name__ == "__main__":
    # Initialize with credentials
    credentials_info = initialize_firebase()
    if not credentials_info:
        logger.error("Failed to initialize Firebase")
        sys.exit(1)

    # Common indexes for intakes collection
    indexes = [
        ('user_id', 'ASCENDING'),
        ('created_at', 'DESCENDING')
    ]
    create_index('intakes', indexes, credentials_info)

    # For admin dashboard
    status_index = [
        ('status', 'ASCENDING'),
        ('created_at', 'DESCENDING')
    ]
    create_index('intakes', status_index, credentials_info)