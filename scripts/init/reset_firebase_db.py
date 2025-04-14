import sys
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from datetime import datetime

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from src.services.user_service import UserService
from init_firebase_db import create_test_data, initialize_firebase

logger = logging.getLogger(__name__)

def delete_collection(db: firestore.Client, collection_name: str, batch_size: int = 100) -> int:
    """
    Delete all documents in a collection using batch operations
    
    Args:
        db: Firestore client
        collection_name: Name of collection to delete
        batch_size: Number of documents to delete in each batch
    
    Returns:
        int: Number of documents deleted
    """
    try:
        batch = db.batch()
        coll_ref = db.collection(collection_name)
        docs = coll_ref.limit(batch_size).stream()
        deleted = 0
        docs_to_delete = []

        for doc in docs:
            docs_to_delete.append(doc)
            batch.delete(doc.reference)
            deleted += 1

            # Commit batch when size limit reached
            if len(docs_to_delete) >= batch_size:
                batch.commit()
                batch = db.batch()
                docs_to_delete = []

        # Commit any remaining documents
        if docs_to_delete:
            batch.commit()

        if deleted >= batch_size:
            # Recursively delete remaining documents
            deleted += delete_collection(db, collection_name, batch_size)

        logger.info(f"Deleted {deleted} documents from {collection_name}")
        return deleted

    except Exception as e:
        logger.error(f"Error deleting collection {collection_name}: {e}")
        raise

def resetdb():
    """Reset database by deleting all documents and reinserting test data"""
    try:
        # Initialize Firebase
        db = initialize_firebase()
        start_time = datetime.now()

        # Collections to reset - order matters for deletion (child to parent)
        collections = [
            'client-process-steps',
            'client-processes',
            'client-tool-assessment',
            'client-intakes',
            'clients',
            'users'
        ]

        total_deleted = 0
        
        # Delete all documents in each collection
        for collection in collections:
            deleted = delete_collection(db, collection)
            total_deleted += deleted
            logger.info(f"Cleared collection: {collection}")

        # Reinsert test data
        #create_test_data(db)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"Successfully reset database:")
        logger.info(f"- Total documents deleted: {total_deleted}")
        logger.info(f"- Collections processed: {len(collections)}")
        logger.info(f"- Time taken: {duration:.2f} seconds")

    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    resetdb()