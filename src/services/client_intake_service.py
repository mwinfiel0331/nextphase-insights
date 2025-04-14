from firebase_admin import firestore
from datetime import datetime
import uuid
import logging
from ..utils.types import ClientIntake
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

class ClientIntakeService:
    def __init__(self, db: firestore.Client):
        """Initialize service with Firestore client"""
        self.db = db
        self.collection = self.db.collection('client-intakes')


    def create_intake(self, intake_dict: dict) -> Optional[ClientIntake]:
        """Create a new client intake"""
        try:
            # Create new clean dictionary for Firestore
            intake_data = {
                'intake_id': str(uuid.uuid4()),
                'client_id': str(intake_dict['client_id']) if intake_dict.get('client_id') else None,
                'client_email': intake_dict.get('client_email'),
                'business_description': intake_dict.get('business_description'),
                'current_challenges': intake_dict.get('current_challenges'),
                'primary_pain_point': intake_dict.get('primary_pain_point'),
                'optimization_goals': intake_dict.get('optimization_goals'),
                'workflow_status': intake_dict.get('workflow_status', 'draft'),
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }

            # Save to Firestore using clean data
            doc_ref = self.collection.document(intake_data['intake_id'])
            doc_ref.set(intake_data)
            
            logger.info(f"Created intake form: {intake_data['intake_id']}")
            return ClientIntake(**intake_data)

        except Exception as e:
            logger.error(f"Error creating intake: {e}")
            raise

    def get_intake(self, intake_id: str) -> Optional[ClientIntake]:
        """Get intake by ID"""
        try:
            doc = self.collection.document(intake_id).get()
            if doc.exists:
                return ClientIntake(**doc.to_dict())
            return None
        
        except Exception as e:
            logger.error(f"Error getting intake {intake_id}: {e}")
            raise

    def update_intake(self, intake_id: str, updates: dict) -> ClientIntake:
        """Update intake fields"""
        try:
            updates['updated_at'] = datetime.now()
            self.collection.document(intake_id).update(updates)
            return self.get_intake(intake_id)
        
        except Exception as e:
            logger.error(f"Error updating intake {intake_id}: {e}")
            raise

    def get_client_intakes(self, client_id: str) -> List[ClientIntake]:
        """Get all intakes for a client"""
        try:
            docs = self.collection.where('client_id', '==', client_id).stream()
            return [ClientIntake(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting intakes for client {client_id}: {e}")
            raise

    def get_intakes_by_status(self, status: str) -> List[ClientIntake]:
        """Get all intakes with specific status"""
        try:
            docs = self.collection.where('workflow_status', '==', status).stream()
            return [ClientIntake(**doc.to_dict()) for doc in docs]
        
        except Exception as e:
            logger.error(f"Error getting intakes with status {status}: {e}")
            raise

    def get_client_intake(self, email: str) -> Optional[Dict]:
        """Get latest intake form for client"""
        try:
            docs = (self.collection
                   .where('client_email', '==', email)
                   .order_by('created_at', direction=firestore.Query.DESCENDING)
                   .limit(1)
                   .stream())
            
            for doc in docs:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error getting intake for {email}: {e}")
            return None

    def get_client_intakes(self, email: str) -> list[Dict]:
        """Get all intake forms for a client by email"""
        try:
            docs = (self.collection
                   .where('client_email', '==', email)
                   .order_by('created_at', direction=firestore.Query.DESCENDING)
                   .stream())
            
            return [doc.to_dict() for doc in docs]

        except Exception as e:
            logger.error(f"Error retrieving intakes for client {email}: {e}")
            return []