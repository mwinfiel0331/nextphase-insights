import sys
from pathlib import Path
import logging

# Add scripts directory to Python path
current_dir = Path(__file__).parent
scripts_dir = current_dir.parent
sys.path.insert(0, str(current_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run initialization scripts"""
    try:
        # Import here after path is set
        from .firebase_init import initialize_firebase
        from .init_database import initialize_database
        
        # Initialize Firebase
        if not initialize_firebase():
            logger.error("Firebase initialization failed")
            return False
            
        # Initialize database structure
        initialize_database()
        logger.info("Initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    main()