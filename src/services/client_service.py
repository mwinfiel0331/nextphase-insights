from firebase_admin import firestore
from datetime import datetime
import uuid
import logging
from ..models.client import Client
from typing import List, Optional

logger = logging.getLogger(__name__)

class ClientService:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = self.db.collection('clients')

    def create_client(self, client_data: dict) -> Client:
        """Create a new client"""
        try:
  
            company_name = client_data.get('company_name')
            if not company_name:
                raise ValueError("Company name is required")
            client_id = str(uuid.uuid4())
            industry = client_data.get('industry')
            company_size = client_data.get('company_size')
            contact_name = client_data.get('contact_name')
            contact_email = client_data.get('contact_email')
            contact_role = client_data.get('contact_role')
        
            client_data['created_at'] = datetime.now()
            client_data['updated_at'] = datetime.now()
            
            self.collection.document(client_id).set(client_data)
            logger.info(f"Created client: {client_id}")
            
            return Client(**client_data)
        
        except Exception as e:
            logger.error(f"Error creating client: {e}")
            raise

    def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID"""
        try:
            doc = self.collection.document(client_id).get()
            if doc.exists:
                return Client(**doc.to_dict())
            return None
        
        except Exception as e:
            logger.error(f"Error getting client {client_id}: {e}")
            raise

    def update_client(self, client_id: str, updates: dict) -> Client:
        """Update client fields"""
        try:
            updates['updated_at'] = datetime.now()
            self.collection.document(client_id).update(updates)
            return self.get_client(client_id)
        
        except Exception as e:
            logger.error(f"Error updating client {client_id}: {e}")
            raise

    def delete_client(self, client_id: str) -> bool:
        """Delete client by ID"""
        try:
            self.collection.document(client_id).delete()
            logger.info(f"Deleted client: {client_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {e}")
            raise

    def get_clients_by_industry(self, industry: str) -> List[Client]:
        """Get all clients in specific industry"""
        try:
            docs = self.collection.where('industry', '==', industry).stream()
            return [Client(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting clients in industry {industry}: {e}")
            raise

    def get_clients_by_size(self, company_size: str) -> List[Client]:
        """Get all clients of specific size"""
        try:
            docs = self.collection.where('company_size', '==', company_size).stream()
            return [Client(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting clients of size {company_size}: {e}")
            raise