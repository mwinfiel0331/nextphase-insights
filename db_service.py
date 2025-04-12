import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import os

# Initialize Firebase Admin
try:
    # Use service account key
    cred = credentials.Certificate("service-account-key.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # Skip if already initialized
    pass

db = firestore.client()

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
        intake_data['created_at'] = datetime.now()
        intake_data['updated_at'] = datetime.now()
        intake_data['status'] = 'new'
        
        # Save to Firestore
        doc_ref = db.collection('clients').document(company_id)
        doc_ref.set(intake_data)
        
        return company_id
        
    except Exception as e:
        print(f"Error saving client data: {str(e)}")
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
        print(f"Error retrieving client data: {str(e)}")
        raise e

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
        print(f"Error retrieving all clients: {str(e)}")
        raise e

def update_client_data(company_id, update_data):
    """
    Update existing client data
    
    Args:
        company_id (str): Company identifier
        update_data (dict): Data to update
    """
    try:
        update_data['updated_at'] = datetime.now()
        doc_ref = db.collection('clients').document(company_id)
        doc_ref.update(update_data)
    except Exception as e:
        print(f"Error updating client data: {str(e)}")
        raise e