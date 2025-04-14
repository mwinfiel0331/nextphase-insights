from firebase_admin import firestore
from datetime import datetime
import uuid
import logging
from ..models.client_process import ClientProcess
from typing import List, Optional

logger = logging.getLogger(__name__)

class ClientProcessService:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = self.db.collection('client-processes')

    def create_process(self, process_data: dict) -> ClientProcess:
        """Create a new client process"""
        try:
            # Generate ID and convert to string
            process_id = str(uuid.uuid4())
            
            # Create process data with proper types
            process_dict = {
                
                'process_id': process_id,
                'client_id': str(process_data.get('client_id')),  # Convert UUID to string
                'process_name': process_data.get('process_name'),
                'process_description': process_data.get('process_description'),
                'process_goal': process_data.get('process_goal'),
                'process_start': process_data.get('process_start'),
                'process_end': process_data.get('process_end'),
                'automation_needs': process_data.get('automation_needs'),
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }
            
            # Save to Firestore
            self.collection.document(process_id).set(process_dict)
            logger.info(f"Created client process: {process_id}")
            
            return ClientProcess(**process_dict)
        
        except Exception as e:
            logger.error(f"Error creating client process: {e}")
            raise

    def get_process(self, process_id: str) -> Optional[ClientProcess]:
        """Get process by ID"""
        try:
            doc = self.collection.document(process_id).get()
            if doc.exists:
                return ClientProcess(**doc.to_dict())
            return None
        
        except Exception as e:
            logger.error(f"Error getting process {process_id}: {e}")
            raise

    def update_process(self, process_id: str, updates: dict) -> ClientProcess:
        """Update process fields"""
        try:
            updates['updated_at'] = datetime.now()
            self.collection.document(process_id).update(updates)
            return self.get_process(process_id)
        
        except Exception as e:
            logger.error(f"Error updating process {process_id}: {e}")
            raise

    def get_client_processes(self, client_id: str) -> List[ClientProcess]:
        """Get all processes for a client"""
        try:
            docs = self.collection.where('client_id', '==', client_id).stream()
            return [ClientProcess(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting processes for client {client_id}: {e}")
            raise

    def delete_process(self, process_id: str) -> bool:
        """Delete process and associated steps"""
        try:
            # Start a batch write
            batch = self.db.batch()
            
            # Delete the process
            process_ref = self.collection.document(process_id)
            batch.delete(process_ref)
            
            # Delete associated steps
            steps_collection = self.db.collection('client-process-steps')
            steps = steps_collection.where('process_id', '==', process_id).stream()
            for step in steps:
                batch.delete(step.reference)
            
            # Commit the batch
            batch.commit()
            logger.info(f"Deleted process {process_id} and its steps")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting process {process_id}: {e}")
            raise