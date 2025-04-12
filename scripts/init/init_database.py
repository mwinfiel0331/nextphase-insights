import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
from .firebase_init import initialize_firebase  # Changed import to use relative path

def initialize_database():
    """Initialize database collections and documents"""
    try:
        print("Starting database initialization...")
        
        # Initialize Firebase first
        if not initialize_firebase():
            print("❌ Failed to initialize Firebase")
            return
            
        print("✅ Firebase initialized successfully")
        db = firestore.client()
        
        # Initialize collections
        collections = {
            'config': {
                'industries': {
                    'list': [
                        "Accounting & Financial Services",
                        "Agriculture & Farming",
                        "Automotive",
                        "Construction & Real Estate",
                        "Consulting & Professional Services",
                        "Education & Training",
                        "Energy & Utilities",
                        "Entertainment & Media",
                        "Food & Beverage",
                        "Government & Public Sector",
                        "Healthcare & Medical",
                        "Hospitality & Tourism",
                        "Information Technology",
                        "Insurance",
                        "Legal Services",
                        "Manufacturing",
                        "Marketing & Advertising",
                        "Non-Profit & NGO",
                        "Pharmaceutical & Biotechnology",
                        "Retail & E-commerce",
                        "Software & Technology",
                        "Telecommunications",
                        "Transportation & Logistics",
                        "Other"
                    ],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
            },
            'clients': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores client information'
                }
            },
            'users': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores user profiles'
                }
            },
            'sessions': {
                '_metadata': {
                    'collection_created': datetime.now(),
                    'description': 'Stores optimization sessions'
                }
            }
        }
        
        # Create collections and documents
        for collection_name, documents in collections.items():
            print(f"\nInitializing {collection_name}...")
            for doc_id, data in documents.items():
                db.collection(collection_name).document(doc_id).set(data)
                print(f"✅ Created {collection_name}/{doc_id}")
                
        print("\n✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"\n❌ Database initialization error: {str(e)}")

if __name__ == "__main__":
    initialize_database()