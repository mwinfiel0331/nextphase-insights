import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore_admin_v1
from google.oauth2 import service_account
import logging
import json
import os

from scripts.init.db_config import COLLECTIONS_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase Admin SDK and return credentials"""
    try:
        if firebase_admin._apps:
            return True

        cred_files = list(root_dir.glob('*firebase-adminsdk*.json'))
        
        if not cred_files:
            logger.error("Firebase credentials not found")
            return None
            
        cred_path = str(cred_files[0].absolute())
        logger.info(f"Using credentials from: {cred_path}")

        # Set environment variable for application default credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

        # Initialize Firebase Admin
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

        return cred

    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        return None

def create_collection_indexes(client, collection_name, indexes):
    """Create indexes for a collection using Admin SDK"""
    try:
        # Get project ID from client credentials
        project_id = client._credentials.project_id
        if not project_id:
            logger.error("Could not determine project ID from credentials")
            return False

        # Initialize Admin client
        admin_client = firestore_admin_v1.FirestoreAdminClient()
        parent = f"projects/{project_id}/databases/(default)/collectionGroups/{collection_name}"
        
        for index_config in indexes:
            field_configs = []
            for field_path, order in index_config['fields']:
                field_configs.append(
                    firestore_admin_v1.Index.IndexField(
                        field_path=field_path,
                        order=firestore_admin_v1.Index.IndexField.Order[order]
                    )
                )
            
            try:
                logger.info(f"Creating index for {collection_name} with fields: {[f[0] for f in index_config['fields']]}")
                index = firestore_admin_v1.Index(
                    query_scope=firestore_admin_v1.Index.QueryScope.COLLECTION,
                    fields=field_configs
                )
                
                operation = admin_client.create_index(
                    parent=parent,
                    index=index
                )
                result = operation.result()  # Wait for completion
                logger.info(f"Created index {result.name}")
                
            except Exception as e:
                logger.error(f"Failed to create index: {str(e)}")
                continue
                
        return True
            
    except Exception as e:
        logger.error(f"Error creating indexes for {collection_name}: {str(e)}")
        return False

def initialize_indexes():
    """Initialize all collection indexes from config"""
    try:
        # Initialize Firebase first
        if not initialize_firebase():
            return False

        # Get Firestore client
        db = firestore.client()
        
        # Create indexes for all collections
        for collection_name, config in COLLECTIONS_CONFIG.items():
            if 'indexes' in config:
                logger.info(f"Creating indexes for collection: {collection_name}")
                if not create_collection_indexes(db, collection_name, config['indexes']):
                    return False
        
        logger.info("All indexes created successfully")
        return True

    except Exception as e:
        logger.error(f"Index initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_indexes()