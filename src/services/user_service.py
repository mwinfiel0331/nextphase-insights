from firebase_admin import firestore
from datetime import datetime
import logging
from typing import List, Optional, Dict
from enum import Enum
import uuid

from src.models.user import User
logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: firestore.Client):
        """Initialize service with Firestore client"""
        self.db = db
        self.collection = self.db.collection('users')
    
    def create_user(self, user_data: dict) -> Optional[Dict]:
        """Create a new user"""
        try:
            # Validate required fields
            required_fields = ['email', 'company_name', 'full_name']
            if not all(field in user_data for field in required_fields):
                logger.error(f"Missing required fields: {required_fields}")
                return None

            # Generate document reference
            doc_ref = self.collection.document()
            
            # Set metadata
            user_data.update({
                'user_id': doc_ref.id,
                'app_role': user_data.get('app_role', 'client'),
                'is_active': True,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            })

            # Save to Firestore
            doc_ref.set(user_data)
            logger.info(f"Created user: {user_data['email']} with ID: {user_data['user_id']}")
            return user_data

        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            users = self.collection.where('email', '==', email).limit(1).stream()
            for user in users:
                return user.to_dict()
            return None

        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None

    def list_users(self) -> List[Dict]:
        """Get all users"""
        try:
            return [doc.to_dict() for doc in self.collection.stream()]
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}")
            return []

    def update_user_profile(self, user_id: str, updates: dict) -> bool:
        """Update user profile fields"""
        try:
            updates['updated_at'] = datetime.now()
            self.collection.document(user_id).update(updates)
            logger.info(f"Updated user profile: {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            return False

    def set_app_role(self, user_id: str, role: str) -> bool:
        """Update user's application role"""
        try:
            if role not in ['admin', 'client']:
                logger.error(f"Invalid role type: {role}")
                return False

            return self.update_user_profile(user_id, {'app_role': role})

        except Exception as e:
            logger.error(f"Error setting user role: {str(e)}")
            return False

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account"""
        try:
            return self.update_user_profile(user_id, {'is_active': False})
        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            return False

    def authenticate(self, email: str, password: str) -> tuple[bool, Optional[Dict]]:
        """Authenticate user and return profile"""
        try:
            user = self.get_user_by_email(email)
            if not user:
                logger.warning(f"User not found: {email}")
                return False, None

            if not user.get('is_active', True):
                logger.warning(f"Inactive user attempted login: {email}")
                return False, None

            # Update last login timestamp
            self.update_user_profile(user['user_id'], {'last_login': datetime.now()})
            return True, user

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False, None