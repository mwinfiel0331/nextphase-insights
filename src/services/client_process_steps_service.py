from firebase_admin import firestore
from datetime import datetime
import uuid
import logging
from ..models.client_process_step import ClientProcessStep
from typing import List, Optional

logger = logging.getLogger(__name__)

class ClientProcessStepsService:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = self.db.collection('client-process-steps')

    def create_step(self, process_id: str, step_data: dict) -> ClientProcessStep:
        """Create a new process step"""
        try:
            step_id = str(uuid.uuid4())
            step_data['step_id'] = step_id
            step_data['process_id'] = process_id
            step_data['created_at'] = datetime.now()
            step_data['updated_at'] = datetime.now()
            
            # Create and validate step model
            step = ClientProcessStep(**step_data)
            
            # Save to Firestore
            self.collection.document(step_id).set(step.to_dict())
            logger.info(f"Created process step: {step_id} for process: {process_id}")
            
            return step
        
        except ValueError as ve:
            logger.error(f"Validation error creating step: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error creating process step: {e}")
            raise

    def get_step(self, step_id: str) -> Optional[ClientProcessStep]:
        """Get step by ID"""
        try:
            doc = self.collection.document(step_id).get()
            if doc.exists:
                return ClientProcessStep(**doc.to_dict())
            return None
        
        except Exception as e:
            logger.error(f"Error getting step {step_id}: {e}")
            raise

    def update_step(self, step_id: str, updates: dict) -> ClientProcessStep:
        """Update step fields"""
        try:
            self.collection.document(step_id).update(updates)
            return self.get_step(step_id)
        
        except Exception as e:
            logger.error(f"Error updating step {step_id}: {e}")
            raise

    def get_process_steps(self, process_id: str) -> List[ClientProcessStep]:
        """Get all steps for a process ordered by step number"""
        try:
            docs = (self.collection
                   .where('process_id', '==', process_id)
                   .order_by('step_number')
                   .stream())
            return [ClientProcessStep(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting steps for process {process_id}: {e}")
            raise

    def delete_step(self, step_id: str) -> bool:
        """Delete a step and reorder remaining steps"""
        try:
            step = self.get_step(step_id)
            if not step:
                return False

            batch = self.db.batch()
            
            # Delete the step
            batch.delete(self.collection.document(step_id))
            
            # Reorder remaining steps
            remaining_steps = (self.collection
                             .where('process_id', '==', step.process_id)
                             .where('step_number', '>', step.step_number)
                             .stream())
            
            for doc in remaining_steps:
                ref = self.collection.document(doc.id)
                batch.update(ref, {'step_number': doc.get('step_number') - 1})
            
            batch.commit()
            logger.info(f"Deleted step {step_id} and reordered remaining steps")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting step {step_id}: {e}")
            raise