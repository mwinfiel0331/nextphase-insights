import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Firebase with more detailed error handling
try:
    if not firebase_admin._apps:
        service_account_files = [f for f in os.listdir('.') if f.endswith('.json') and 'firebase-adminsdk' in f]
        if service_account_files:
            cred = credentials.Certificate(service_account_files[0])
            logger.info("Using service account credentials")
            
            firebase_admin.initialize_app(cred)
            logger.info("Successfully initialized Firebase")
    
    # Initialize Firestore client
    db = firestore.client()
    
except ValueError as ve:
    logger.error(f"Firebase initialization error: {str(ve)}")
    raise ve
except Exception as e:
    logger.error(f"Unexpected error during Firebase initialization: {str(e)}")
    raise e

def save_client_data(intake_data):
    """
    Save client intake data to Firestore
    
    Args:
        intake_data (dict): Dictionary containing client intake form data
    Returns:
        str: Document ID of the created record
    """
    try:
        # Add company_id field using lowercase company name with no spaces
        company_id = intake_data['company_name'].lower().replace(' ', '_')
        intake_data['company_id'] = company_id
        
        # Add metadata
        intake_data['created_at'] = datetime.datetime.now()
        intake_data['updated_at'] = datetime.datetime.now()
        intake_data['status'] = 'new'
        
        # Save to Firestore
        doc_ref = db.collection('clients').document(company_id)
        doc_ref.set(intake_data)
        
        return company_id
        
    except Exception as e:
        logger.error(f"Error saving client data: {str(e)}")
        raise e

def get_client_data(company_id):
    """
    Retrieve client data from Firestore
    
    Args:
        company_id (str): Company identifier
    Returns:
        dict: Client data
    """
    try:
        doc_ref = db.collection('clients').document(company_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        logger.error(f"Error retrieving client data: {str(e)}")
        raise e

def get_client_by_id(client_id):
    """
    Retrieve a specific client by ID
    
    Args:
        client_id (str): The client's unique identifier
        
    Returns:
        dict: Client data or None if not found
    """
    try:
        if not client_id:
            return None
            
        client_doc = db.collection('clients').document(client_id).get()
        
        if client_doc.exists:
            return client_doc.to_dict()
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving client {client_id}: {str(e)}")
        return None

def get_all_clients():
    """
    Retrieve all clients
    
    Returns:
        list: List of client dictionaries
    """
    try:
        clients = db.collection('clients').stream()
        return [doc.to_dict() for doc in clients]
    except Exception as e:
        logger.error(f"Error retrieving all clients: {str(e)}")
        raise e

def update_client_data(company_id, update_data):
    """
    Update existing client data
    
    Args:
        company_id (str): Company identifier
        update_data (dict): Data to update
    """
    try:
        update_data['updated_at'] = datetime.datetime.now()
        doc_ref = db.collection('clients').document(company_id)
        doc_ref.update(update_data)
    except Exception as e:
        logger.error(f"Error updating client data: {str(e)}")
        raise e

def save_session_data(session_data):
    """
    Save session data to Firestore
    
    Args:
        session_data (dict): Dictionary containing session data
    Returns:
        str: Document ID of the created record
    """
    try:
        doc_ref = db.collection('sessions').document()
        session_data['created_at'] = datetime.datetime.now()
        doc_ref.set(session_data)
        return doc_ref.id
    except Exception as e:
        logger.error(f"Error saving session data: {str(e)}")
        raise e

def get_client_sessions(client_id):
    """
    Retrieve all sessions for a specific client
    
    Args:
        client_id (str): Client identifier
    Returns:
        list: List of session dictionaries
    """
    try:
        sessions = db.collection('sessions').where('client_id', '==', client_id).stream()
        return [doc.to_dict() for doc in sessions]
    except Exception as e:
        logger.error(f"Error retrieving client sessions: {str(e)}")
        raise e

# Add a test function to verify connection
def test_firebase_connection():
    try:
        # Test write
        test_ref = db.collection('_test').document('connection_test')
        test_ref.set({'timestamp': datetime.datetime.now(), 'status': 'testing'})
        logger.info("Successfully wrote to Firestore")
        return True
    except Exception as e:
        logger.error(f"Firebase connection test failed: {str(e)}")
        return False

# Test the connection when module is run directly
if __name__ == "__main__":
    test_firebase_connection()