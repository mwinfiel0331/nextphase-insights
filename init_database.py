import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import sys
import os

def initialize_database_structure():
    print("\n=== Initializing Database Structure ===\n")
    
    try:
        # Look for service account key file
        service_account_files = [f for f in os.listdir('.') if f.endswith('.json') and 'firebase-adminsdk' in f]
        
        if not service_account_files:
            print("❌ No Firebase service account key file found!")
            print("Please ensure your service account key is in the current directory.")
            return False
            
        key_path = service_account_files[0]
        print(f"Found service account key: {key_path}")
        
        # Initialize Firebase if not already initialized
        print("Loading Firebase credentials...")
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            print("✓ Firebase initialized")
        else:
            print("✓ Firebase already initialized")
        
        db = firestore.client()
        print("✓ Connected to Firestore")
        
        # Define collections and their initial documents
        collections = {
            'clients': {
                'metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores client information and process assessments'
                }
            },
            'sessions': {
                'metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Tracks optimization sessions and progress'
                }
            },
            'tools': {
                'metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Common tools and integrations catalog'
                }
            }
        }
        
        # Create collections and their metadata documents
        print("\nCreating collections:")
        print("--------------------")
        for collection_name, initial_data in collections.items():
            try:
                db.collection(collection_name).document('_metadata').set(initial_data)
                print(f"✓ Created collection: {collection_name}")
            except Exception as collection_error:
                print(f"❌ Error creating collection {collection_name}: {str(collection_error)}")
                return False
            
        print("\n✅ Database structure initialized successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}\n")
        return False

if __name__ == "__main__":
    initialize_database_structure()