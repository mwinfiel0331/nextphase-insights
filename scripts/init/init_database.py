import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore_admin_v1
from google.cloud.firestore_admin_v1 import types
from datetime import datetime
import os
import json
import logging

# Local imports
from .firebase_init import initialize_firebase
from .db_config import COLLECTIONS_CONFIG
from src.utils.constants import UserType  # Changed to absolute import

logger = logging.getLogger(__name__)

def create_collection_indexes(client, collection_name, indexes):
    """Create indexes for a collection using Admin SDK"""
    try:
        # Get project ID from client credentials
        project_id = client._credentials.project_id
        if not project_id:
            logger.error("Could not determine project ID from credentials")
            return False

        # Initialize Admin client with explicit credentials
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

def create_document(collection_ref, doc_id, data):
    """Create a single document in a collection"""
    try:
        doc_ref = collection_ref.document(doc_id)
        # Check if document exists
        if not doc_ref.get().exists:
            doc_ref.set(data)
            logger.info(f"Created document '{doc_id}'")
        else:
            logger.debug(f"Document '{doc_id}' already exists")
        return True
    except Exception as e:
        logger.error(f"Error creating document '{doc_id}': {str(e)}")
        return False

def initialize_database():
    """Initialize database collections and documents"""
    try:
        logger.info("Starting database initialization...")
        
        # Initialize Firebase first
        if not initialize_firebase():
            logger.error("Failed to initialize Firebase")
            return
            
        logger.info("Firebase initialized successfully")
        
        # Get Firestore client
        db = firestore.client()
        
        # Create collections and their documents
        for collection_name, config in COLLECTIONS_CONFIG.items():
            logger.info(f"Initializing '{collection_name}' collection...")
            collection_ref = db.collection(collection_name)

            # Create metadata document
            if 'metadata' in config:
                metadata = {
                    **config['metadata'],
                    'collection_created': datetime.now()
                }
                create_document(
                    collection_ref, 
                    '_metadata', 
                    metadata
                )

            # Create predefined documents
            if 'documents' in config:
                for doc_id, doc_data in config['documents'].items():
                    create_document(
                        collection_ref,
                        doc_id,
                        doc_data
                    )

            # Create indexes
            if 'indexes' in config:
                create_collection_indexes(db, collection_name, config['indexes'])
        
        # Create default admin if specified
        admin_email = os.getenv('ADMIN_EMAIL')
        if admin_email:
            create_default_admin(db, admin_email)
            
        # Create test data in development
        if os.getenv('FLASK_ENV') == 'development':
            create_test_data(db)
                
        logger.info("Database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        return False

def create_default_admin(db: firestore.Client, admin_email: str):
    """Create default admin user if not exists"""
    admin_query = db.collection('users').where('email', '==', admin_email).limit(1)
    
    if not list(admin_query.stream()):
        admin_data = {
            'email': admin_email,
            'full_name': 'System Administrator',
            'company_name': 'NextPhase Insights',
            'user_type': UserType.ADMIN.value,
            'created_at': datetime.now(),
            'last_login': datetime.now(),
            'is_system_admin': True
        }
        
        db.collection('users').document().set(admin_data)
        logger.info(f"Created system admin user: {admin_email}")

def create_test_data(db: firestore.Client):
    """Create test data for development environment"""
    if not db.collection('users').limit(1).get():
        test_user = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'company_name': 'Test Company',
            'user_type': UserType.CLIENT.value,
            'created_at': datetime.now(),
            'last_login': datetime.now()
        }
        
        db.collection('users').document().set(test_user)
        logger.info("Created test user data")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    initialize_database()