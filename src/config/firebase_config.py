import firebase_admin
from firebase_admin import credentials, firestore
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            # Get project root path
            project_root = Path(__file__).parent.parent.parent
            
            # Load credentials file
            cred_path = project_root / 'nextphase-insights-firebase-adminsdk.json'
            cred = credentials.Certificate(str(cred_path))
            
            # Initialize Firebase
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully")
        
        return firestore.client()
    except Exception as e:
        logger.error(f"Firebase initialization error: {e}")
        raise