import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import click
from firebase_admin import firestore
import logging
from init.firebase_init import initialize_firebase
from src.utils.constants import UserType
from datetime import datetime

logger = logging.getLogger(__name__)

@click.command()
@click.option('--email', prompt='Admin email', help='Email address for admin account')
@click.option('--full_name', prompt='Full name', help='Admin\'s full name')
@click.option('--company', prompt='Company name', default='NextPhase Insights', help='Company name')
@click.password_option(help='Admin password')
def create_admin(email: str, full_name: str, company: str, password: str):
    """Create a new admin user in Firebase"""
    try:
        # Initialize Firebase
        if not initialize_firebase():
            logger.error("Failed to initialize Firebase")
            return

        db = firestore.client()

        # Check if user already exists
        existing_user = db.collection('users').where('email', '==', email).limit(1).get()
        if list(existing_user):
            logger.error(f"User with email {email} already exists")
            return

        # Create admin data
        admin_data = {
            'email': email,
            'full_name': full_name,
            'company_name': company,
            'user_type': UserType.ADMIN.value,
            'created_at': datetime.now(),
            'last_login': datetime.now(),
            'is_system_admin': True
        }

        # Save to Firestore
        db.collection('users').document().set(admin_data)
        logger.info(f"Successfully created admin user: {email}")
        click.echo(f"Admin user created: {email}")

    except Exception as e:
        logger.error(f"Failed to create admin: {str(e)}")
        click.echo(f"Error creating admin: {str(e)}", err=True)

if __name__ == '__main__':
    create_admin()