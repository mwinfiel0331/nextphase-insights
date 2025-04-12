from firebase_admin import firestore
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

TOOL_CATEGORIES = {
    "Communication & Messaging": [
        "Slack", "Microsoft Teams", "Discord", "Zoom", "Google Meet", "Other"
    ],
    "Task & Project Management": [
        "Asana", "Trello", "Jira", "Monday.com", "ClickUp", "Other"
    ],
    "Calendar & Scheduling": [
        "Google Calendar", "Outlook", "Calendly", "Other"
    ],
    "Document Management": [
        "Google Drive", "SharePoint", "Dropbox", "OneDrive", "Other"
    ]
}

def init_config_data():
    """Initialize configuration data"""
    try:
        db = firestore.client()
        config_ref = db.collection('config').document('tool_categories')
        config_ref.set({
            'categories': TOOL_CATEGORIES,
            'updated_at': datetime.now()
        })
        logger.info("Configuration data initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Config initialization failed: {str(e)}")
        return False