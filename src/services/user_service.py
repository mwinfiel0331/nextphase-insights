import firebase_admin
from firebase_admin import auth, firestore
import logging
from datetime import datetime
from typing import Optional, Dict, Tuple
from ..utils.constants import UserType
import os

logger = logging.getLogger(__name__)

class UserService:
    """Service for managing user authentication and data"""

    def __init__(self):
        """Initialize Firestore client"""
        self.db = firestore.client()
        self.collection = 'users'

    def authenticate(self, email: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate user and return profile data"""
        try:
            # Get Firebase user by exact email match
            user = auth.get_user_by_email(email)
            logger.info(f"Firebase auth successful for: {email}")
            
            # Get Firestore profile with exact email match
            query = self.db.collection(self.collection).where('email', '==', email).limit(1)
            docs = [doc for doc in query.stream()]
            
            if not docs:
                logger.error(f"No Firestore profile found for email: {email}")
                return False, None
                
            user_data = docs[0].to_dict()
            logger.info(f"Found user profile: {user_data}")
            
            # Verify emails match exactly
            if user_data.get('email') != email:
                logger.error(f"Email mismatch - Auth: {email}, Profile: {user_data.get('email')}")
                return False, None

            # Update last login
            self.update_user_profile(user.uid, {'last_login': datetime.now()})
            return True, user_data

        except Exception as e:
            logger.error(f"Authentication failed for {email}: {str(e)}")
            return False, None

    def create_user(self, email: str, password: str, user_data: dict) -> Dict:
        """Create a new user account with Firebase Auth and Firestore profile"""
        try:
            # Create Firebase Auth user
            user = auth.create_user(
                email=email,
                password=password,
                display_name=user_data.get('full_name')
            )
            
            # Generate client_id from company name
            client_id = user_data.get('company_name', '').lower().replace(' ', '_')
            
            # Create user profile
            user_profile = {
                'uid': user.uid,
                'email': email,
                'company_name': user_data.get('company_name'),
                'full_name': user_data.get('full_name'),
                'user_type': user_data.get('user_type', UserType.CLIENT.value),
                'client_id': client_id,
                'created_at': datetime.now(),
                'last_login': datetime.now(),
                'is_active': True
            }
            
            # Save to Firestore
            self.db.collection(self.collection).document(user.uid).set(user_profile)
            logger.info(f"Created new user: {email}")
            
            return user_profile
            
        except Exception as e:
            logger.error(f"Error creating user {email}: {str(e)}")
            raise

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile by ID"""
        try:
            doc = self.db.collection(self.collection).document(user_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Retrieve user profile by email"""
        try:
            query = self.db.collection(self.collection).where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}")
            return None

    def update_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Update user profile data"""
        try:
            profile_data['updated_at'] = datetime.now()
            self.db.collection(self.collection).document(user_id).update(profile_data)
            logger.info(f"Updated profile for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return False

    def set_user_type(self, user_id: str, user_type: UserType) -> bool:
        """Update user type (admin only)"""
        try:
            self.db.collection(self.collection).document(user_id).update({
                'user_type': user_type.value,
                'updated_at': datetime.now()
            })
            logger.info(f"Updated user type for {user_id} to {user_type.value}")
            return True
        except Exception as e:
            logger.error(f"Error updating user type: {str(e)}")
            return False

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account"""
        try:
            self.db.collection(self.collection).document(user_id).update({
                'is_active': False,
                'updated_at': datetime.now()
            })
            logger.info(f"Deactivated user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {str(e)}")
            return False

    def list_users(self) -> list:
        """Get all users from Firestore"""
        try:
            users = []
            users_ref = self.db.collection(self.collection)
            docs = users_ref.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                # Add document ID as uid if not present
                if 'uid' not in user_data:
                    user_data['uid'] = doc.id
                # Ensure created_at exists
                if 'created_at' not in user_data:
                    user_data['created_at'] = datetime.now()
                users.append(user_data)
                
            logger.info(f"Retrieved {len(users)} users")
            return users
            
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}")
            return []

    def send_password_reset(self, email: str) -> bool:
        """Send password reset email using Firebase Auth"""
        try:
            logger.debug(f"Attempting password reset for email: {email}")
            
            # First verify user exists
            try:
                user = auth.get_user_by_email(email)
                logger.debug(f"User found in Firebase: {user.uid}")
            except auth.UserNotFoundError:
                logger.warning(f"Password reset attempted for non-existent user: {email}")
                return False
                
            # Generate reset link with proper URL format
            auth_domain = os.getenv('FIREBASE_AUTH_DOMAIN', '')
            reset_url = f"https://{auth_domain}"
            
            logger.debug(f"Using reset URL: {reset_url}")
            
            reset_link = auth.generate_password_reset_link(
                email,
                action_code_settings=auth.ActionCodeSettings(
                    url=reset_url,
                    handle_code_in_app=True
                )
            )
            
            logger.debug(f"Reset link generated: {reset_link}")
            logger.info(f"Password reset link sent to: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error in password reset: {str(e)}", exc_info=True)
            return False