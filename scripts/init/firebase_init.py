import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json
import os
import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    try:
        # Check if already initialized
        if firebase_admin._apps:
            logger.debug("Firebase already initialized")
            return True

        # Find credentials file
        root_dir = Path(__file__).parent.parent.parent
        cred_files = list(root_dir.glob('*firebase-adminsdk*.json'))
        
        if not cred_files:
            logger.error("Firebase credentials not found in project root")
            logger.error("Please download from Firebase Console > Project Settings > Service Accounts")
            return False
            
        cred_path = cred_files[0]
        logger.info(f"Using credentials file: {cred_path.name}")

        # Set environment variable for Admin SDK
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_path.absolute())

        # Initialize Firebase with credentials
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
        
        # Verify initialization
        db = firestore.client()
        logger.info("Firebase successfully initialized")
        return True

    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        return False