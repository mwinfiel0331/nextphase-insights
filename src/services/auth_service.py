import firebase_admin
from firebase_admin import auth, firestore
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
db = firestore.client()

def create_user(email: str, password: str, user_data: dict) -> dict:
    """
    Create a new user account with Firebase Auth and Firestore profile
    
    Args:
        email (str): User's email address
        password (str): User's password
        user_data (dict): Additional user information
        
    Returns:
        dict: Created user profile data
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
        
        # Create user profile in Firestore
        user_profile = {
            'uid': user.uid,
            'email': email,
            'company_name': user_data.get('company_name'),
            'full_name': user_data.get('full_name'),
            'is_admin': False,
            'client_id': client_id,
            'created_at': datetime.now(),
            'last_login': datetime.now()
        }
        
        # Save profile to Firestore
        db.collection('users').document(user.uid).set(user_profile)
        logger.info(f"Created new user: {email}")
        
        return user_profile
        
    except Exception as e:
        logger.error(f"Error creating user {email}: {str(e)}")
        raise e

def sign_in_user(email: str, password: str) -> dict:
    """
    Sign in existing user and update last login
    
    Args:
        email (str): User's email address
        password (str): User's password
        
    Returns:
        dict: User profile data
    """
    try:
        # Get Firebase user
        user = auth.get_user_by_email(email)
        
        # Get and update user profile
        profile_ref = db.collection('users').document(user.uid)
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
        raise e