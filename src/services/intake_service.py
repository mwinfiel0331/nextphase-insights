from firebase_admin import firestore
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class IntakeService:
    """Service for managing process intake forms"""
    
    def __init__(self):
        self.db = firestore.client()
        self.collection = 'intakes'

    def save_intake_data(self, data: Dict[str, Any]) -> str:
        """Save complete intake form data to Firestore
        
        Args:
            data (Dict[str, Any]): Form data including:
                - company_info: Company and contact details
                - process_details: Business overview and challenges
                - tool_selections: Current tools and systems in use
                - documentation: References to uploaded files
                
        Returns:
            str: Document ID of saved intake
        """
        try:
            intake_data = {
                # Company Information
                'company_name': data.get('company_name'),
                'industry': data.get('industry'),
                'company_size': data.get('company_size'),
                'contact_name': data.get('contact_name'),
                'contact_email': data.get('contact_email'),
                'contact_role': data.get('contact_role'),
                
                # Process Assessment
                'business_description': data.get('business_description'),
                'current_challenges': data.get('current_challenges'),
                'main_pain_point': data.get('main_pain_point'),
                'partnership_goals': data.get('partnership_goals'),
                'tool_selections': data.get('tool_selections', {}),
                'manual_processes': data.get('manual_processes'),
                'hours_per_week': data.get('hours_per_week'),
                
                # Metadata
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'status': 'pending_review',
                'form_section': data.get('form_section', 0)
            }
            
            doc_ref = self.db.collection(self.collection).add(intake_data)
            return doc_ref[1].id
            
        except Exception as e:
            raise Exception(f"Failed to save intake data: {str(e)}")

    def update_intake_section(self, intake_id: str, section: int, section_data: Dict[str, Any]) -> None:
        """Update a specific section of the intake form
        
        Args:
            intake_id (str): Document ID
            section (int): Form section number (0-3)
            section_data (Dict[str, Any]): Updated section data
        """
        try:
            update_data = {
                'updated_at': datetime.utcnow(),
                'form_section': section,
                **section_data
            }
            
            self.db.collection(self.collection).document(intake_id).update(update_data)
            
        except Exception as e:
            raise Exception(f"Failed to update intake section: {str(e)}")

    def get_intake_by_id(self, intake_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve complete intake data by ID
        
        Args:
            intake_id (str): Firestore document ID
            
        Returns:
            Optional[Dict[str, Any]]: Complete intake data or None if not found
        """
        try:
            doc = self.db.collection(self.collection).document(intake_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            raise Exception(f"Failed to retrieve intake data: {str(e)}")

    def list_intakes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent intake submissions
        
        Args:
            limit (int): Maximum number of intakes to return
            
        Returns:
            List[Dict[str, Any]]: List of intake documents
        """
        try:
            docs = (self.db.collection(self.collection)
                   .order_by('created_at', direction=firestore.Query.DESCENDING)
                   .limit(limit)
                   .stream())
            
            return [doc.to_dict() for doc in docs]
            
        except Exception as e:
            raise Exception(f"Failed to list intakes: {str(e)}")

    def update_documentation(self, intake_id: str, file_refs: Dict[str, List[str]]) -> None:
        """Update documentation file references
        
        Args:
            intake_id (str): Document ID
            file_refs (Dict[str, List[str]]): Dictionary of file references by type
        """
        try:
            update_data = {
                'documentation': file_refs,
                'updated_at': datetime.utcnow(),
                'status': 'documentation_added'
            }
            
            self.db.collection(self.collection).document(intake_id).update(update_data)
            
        except Exception as e:
            raise Exception(f"Failed to update documentation: {str(e)}")

    def get_user_intakes(self, user_id: str) -> list:
        """Get all intakes for a specific user"""
        try:
            # Use filter keyword argument for query
            query = (self.db.collection(self.collection)
                    .filter('user_id', '==', user_id)
                    .order_by('created_at', direction=firestore.Query.DESCENDING))
            
            intakes = []
            for doc in query.stream():
                intake_data = doc.to_dict()
                intake_data['id'] = doc.id
                intakes.append(intake_data)
            
            logger.debug(f"Retrieved {len(intakes)} intakes for user {user_id}")
            return intakes
            
        except Exception as e:
            logger.error(f"Error fetching user intakes: {str(e)}")
            return []

def save_intake_form(user_id: str, form_data: dict, status: str = 'DRAFT') -> str:
    """Save intake form data to Firestore"""
    try:
        db = firestore.client()
        
        # Prepare intake document
        intake_data = {
            # Company Info
            'company_info': {
                'company_name': form_data.get('company_name', ''),
                'industry': form_data.get('industry', ''),
                'team_size': int(form_data.get('team_size', 0)),
                'timeline': form_data.get('timeline', '')
            },
            # Process Details
            'process_details': {
                'process_name': form_data.get('process_name', ''),
                'process_description': form_data.get('process_description', ''),
                'current_challenges': form_data.get('current_challenges', ''),
                'desired_outcomes': form_data.get('desired_outcomes', '')
            },
            # Documentation
            'documentation': {
                'attachments': form_data.get('attachments', []),
                'additional_notes': form_data.get('additional_notes', '')
            },
            # System fields
            'user_id': user_id,
            'status': status,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Add submitted_at if status is SUBMITTED
        if status == 'SUBMITTED':
            intake_data['submitted_at'] = datetime.now()
        
        # Save to Firestore
        doc_ref = db.collection('intakes').document()
        doc_ref.set(intake_data)
        
        logger.info(f"Saved intake form with ID: {doc_ref.id}")
        return doc_ref.id
        
    except Exception as e:
        logger.error(f"Error saving intake form: {str(e)}")
        raise