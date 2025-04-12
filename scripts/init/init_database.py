import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
import logging
from .firebase_init import initialize_firebase
from ...utils.constants import UserType

logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database collections and documents"""
    try:
        logger.info("Starting database initialization...")
        
        # Initialize Firebase first
        if not initialize_firebase():
            logger.error("Failed to initialize Firebase")
            return
            
        logger.info("Firebase initialized successfully")
        db = firestore.client()
        
        # Define collection indexes
        indexes = {
            'users': [
                {'fieldPath': 'user_type', 'mode': 'ASCENDING'},
                {'fieldPath': 'created_at', 'mode': 'DESCENDING'}
            ],
            'intakes': [
                {'fieldPath': 'user_id', 'mode': 'ASCENDING'},
                {'fieldPath': 'created_at', 'mode': 'DESCENDING'},
                {'fieldPath': 'status', 'mode': 'ASCENDING'}
            ]
        }
        
        # Create indexes
        for collection_name, collection_indexes in indexes.items():
            collection_ref = db.collection(collection_name)
            for index in collection_indexes:
                collection_ref.create_index([
                    firestore.FieldPath(index['fieldPath'])
                ], mode=index['mode'])
                logger.info(f"Created index for {collection_name}: {index['fieldPath']}")
        
        # Initialize collections
        collections = {
            'config': {
                'industries': {
                    'list': [
                        "Accounting & Financial Services",
                        "Agriculture & Farming",
                        "Automotive",
                        "Construction & Real Estate",
                        "Consulting & Professional Services",
                        "Education & Training",
                        "Energy & Utilities",
                        "Entertainment & Media",
                        "Food & Beverage",
                        "Government & Public Sector",
                        "Healthcare & Medical",
                        "Hospitality & Tourism",
                        "Information Technology",
                        "Insurance",
                        "Legal Services",
                        "Manufacturing",
                        "Marketing & Advertising",
                        "Non-Profit & NGO",
                        "Pharmaceutical & Biotechnology",
                        "Retail & E-commerce",
                        "Software & Technology",
                        "Telecommunications",
                        "Transportation & Logistics",
                        "Other"
                    ],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            },
            'users': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores user profiles and authentication data'
                }
            },
            'intakes': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores process intake forms'
                }
            },
            'sessions': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores optimization sessions'
                }
            }
        }
        
        # Create collections and documents
        for collection_name, documents in collections.items():
            logger.info(f"Initializing {collection_name}...")
            for doc_id, data in documents.items():
                db.collection(collection_name).document(doc_id).set(data)
                logger.info(f"Created {collection_name}/{doc_id}")

        # Create default admin if specified
        admin_email = os.getenv('ADMIN_EMAIL')
        if admin_email:
            create_default_admin(db, admin_email)
            
        # Create test data in development
        if os.getenv('FLASK_ENV') == 'development':
            create_test_data(db)
                
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

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