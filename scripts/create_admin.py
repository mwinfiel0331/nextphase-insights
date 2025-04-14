import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import click
from firebase_admin import auth, firestore, exceptions
from init.firebase_init import initialize_firebase
from datetime import datetime

@click.command()
@click.option('--email', prompt='Admin email', help='Email address for admin account')
@click.option('--full_name', prompt='Full name', help='Admin\'s full name')
@click.option('--company', prompt='Company name', default='NextPhase Insights', help='Company name')
@click.password_option(help='Admin password')
@click.option('--debug', is_flag=True, help='Enable debug logging')
def create_admin(email: str, full_name: str, company: str, password: str, debug: bool):
    """Create a new admin user in Firebase"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        logger.info("Initializing Firebase...")
        if not initialize_firebase():
            logger.error("Firebase initialization failed")
            sys.exit(1)

        # Check if user already exists
        try:
            existing_user = auth.get_user_by_email(email)
            logger.error(f"User with email {email} already exists")
            if click.confirm("Would you like to update this user to admin?"):
                db = firestore.client()
                admin_data = {
                    'user_id': existing_user.user_id,
                    'email': email,
                    'full_name': full_name,
                    'company_name': company,
                    'app_role': 'admin',
                    'updated_at': firestore.SERVER_TIMESTAMP,
                    'is_system_admin': True
                }
                db.collection('users').document(existing_user.user_id).set(admin_data, merge=True)
                click.echo(f"✅ Updated user to admin: {email}")
            return
        except auth.UserNotFoundError:
            pass  # User doesn't exist, continue with creation

        logger.info("Creating user in Firebase Auth...")
        user = auth.create_user(
            email=email,
            password=password,
            display_name=full_name
        )

        logger.info(f"Created auth user with user_id: {user.user_id}")
        
        admin_data = {
            'user_id': user.user_id,
            'email': email,
            'full_name': full_name,
            'company_name': company,
            'app_role': 'admin',
            'created_at': firestore.SERVER_TIMESTAMP,
            'last_login': datetime.now(),
            'is_system_admin': True
        }

        logger.info("Saving admin data to Firestore...")
        db = firestore.client()
        db.collection('users').document(user.user_id).set(admin_data)
        
        click.echo(f"✅ Successfully created admin user: {email}")

    except Exception as e:
        logger.error(f"Error creating admin: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    create_admin()