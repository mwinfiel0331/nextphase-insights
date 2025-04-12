import firebase_admin
from firebase_admin import auth, firestore
import logging
from datetime import datetime
from typing import Optional, Dict
from ..utils.constants import UserType

logger = logging.getLogger(__name__)

class UserService:
    """Service for managing user authentication and data"""

    def __init__(self):
        """Initialize Firestore client"""
        self.db = firestore.client()
        self.collection = 'users'

    def create_user(self, email: str, password: str, user_data: dict) -> Dict:
        """Create a new user account with Firebase Auth and Firestore profile
        
        Args:
            email (str): User's email address
            password (str): User's password
            user_data (dict): Additional user information
            
        Returns:
            Dict: Created user profile data
            
        Raises:
            Exception: If user creation fails
        """
        try:
            # Create Firebase Auth user
            user = auth.create_user(
                email=email,
                password=password,
                display_name=user_data.get('full_name')
            )
            
            # Generate client_id from company name
            client_id = user_data.get('company_name', '').lower().replace(' ', '_')
            
            # Create user profile with type
            user_profile = {
                'uid': user.uid,
                'email': email,
                'company_name': user_data.get('company_name'),
                'full_name': user_data.get('full_name'),
                'user_type': UserType.CLIENT.value,  # Default to CLIENT
                'client_id': client_id,
                'created_at': datetime.now(),
                'last_login': datetime.now()
            }
            
            # Save to Firestore
            self.db.collection(self.collection).document(user.uid).set(user_profile)
            logger.info(f"Created new user: {email}")
            
            return user_profile
            
        except Exception as e:
            logger.error(f"Error creating user {email}: {str(e)}")
            raise

    def sign_in_user(self, email: str, password: str) -> Optional[Dict]:
        """Sign in existing user and update last login
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Optional[Dict]: User profile data if successful, None if not found
            
        Raises:
            Exception: If sign in fails
        """
        try:
            # Get Firebase user
            user = auth.get_user_by_email(email)
            
            # Get and update profile
            profile_ref = self.db.collection(self.collection).document(user.uid)
            profile = profile_ref.get()
            
            if profile.exists:
                # Update last login
                profile_ref.update({
                    'last_login': datetime.now()
                })
                
                user_data = profile.to_dict()
                logger.info(f"User signed in: {email}")
                return user_data
                
            logger.error(f"No profile found for user: {email}")
            return None
            
        except Exception as e:
            logger.error(f"Error signing in user {email}: {str(e)}")
            raise

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile by ID
        
        Args:
            user_id (str): User's UID
            
        Returns:
            Optional[Dict]: User profile data if found
        """
        try:
            doc = self.db.collection(self.collection).document(user_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            return None

    def update_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Update user profile data
        
        Args:
            user_id (str): User's UID
            profile_data (Dict): Updated profile information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            profile_data['updated_at'] = datetime.now()
            self.db.collection(self.collection).document(user_id).update(profile_data)
            logger.info(f"Updated profile for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return False

    def set_user_type(self, user_id: str, user_type: UserType) -> bool:
        """Update user type (admin only)
        
        Args:
            user_id (str): User's UID
            user_type (UserType): New user type
            
        Returns:
            bool: True if successful, False otherwise
        """
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