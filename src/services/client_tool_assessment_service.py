from firebase_admin import firestore
from datetime import datetime
import logging
from typing import List, Optional, Dict
from ..models.client_tool_assessment import ClientToolAssessment

logger = logging.getLogger(__name__)

class ClientToolAssessmentService:
    def __init__(self, db: firestore.Client):
        """Initialize service with Firestore client"""
        self.db = db
        self.collection = self.db.collection('client-tool-assessments')

    def create_assessment(self, assessment_data: dict) -> Optional[ClientToolAssessment]:
        """Create a new tool assessment"""
        try:
            # Validate required fields
            required_fields = ['client_id', 'client_name']
            if not all(field in assessment_data for field in required_fields):
                logger.error(f"Missing required fields: {required_fields}")
                return None

            # Generate document reference
            doc_ref = self.collection.document()
            
            # Set metadata
            assessment_data.update({
                'assessment_id': doc_ref.id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            })

            # Save to Firestore
            doc_ref.set(assessment_data)
            logger.info(f"Created tool assessment for client: {assessment_data['client_name']}")
            
            return ClientToolAssessment(**assessment_data)

        except Exception as e:
            logger.error(f"Error creating tool assessment: {str(e)}")
            return None

    def get_assessment(self, client_id: str) -> Optional[ClientToolAssessment]:
        """Get latest tool assessment for a client"""
        try:
            docs = (self.collection
                   .where('client_id', '==', client_id)
                   .order_by('created_at', direction=firestore.Query.DESCENDING)
                   .limit(1)
                   .stream())
            
            for doc in docs:
                return ClientToolAssessment(**doc.to_dict())
            return None

        except Exception as e:
            logger.error(f"Error getting tool assessment: {str(e)}")
            return None

    def update_assessment(self, assessment_id: str, updates: dict) -> bool:
        """Update an existing tool assessment"""
        try:
            updates['updated_at'] = datetime.now()
            self.collection.document(assessment_id).update(updates)
            logger.info(f"Updated tool assessment: {assessment_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating tool assessment: {str(e)}")
            return False

    def list_assessments(self, client_id: str = None) -> List[ClientToolAssessment]:
        """Get all tool assessments, optionally filtered by client"""
        try:
            query = self.collection
            if client_id:
                query = query.where('client_id', '==', client_id)
            
            docs = query.stream()
            return [ClientToolAssessment(**doc.to_dict()) for doc in docs]

        except Exception as e:
            logger.error(f"Error listing tool assessments: {str(e)}")
            return []

    def delete_assessment(self, assessment_id: str) -> bool:
        """Delete a tool assessment"""
        try:
            self.collection.document(assessment_id).delete()
            logger.info(f"Deleted tool assessment: {assessment_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting tool assessment: {str(e)}")
            return False