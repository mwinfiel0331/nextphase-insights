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
    """Run database initialization"""
    try:
        # Import here after path is set
        from .firebase_init import initialize_firebase
        from .init_database import init_collections
        from .config_data import init_config_data
        
        # Initialize Firebase
        if not initialize_firebase():
            logger.error("Firebase initialization failed")
            return False
            
        # Initialize collections and indexes
        if not init_collections():
            logger.error("Collection initialization failed")
            return False
            
        # Initialize configuration data
        if not init_config_data():
            logger.error("Config initialization failed")
            return False
            
        logger.info("Initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    main()