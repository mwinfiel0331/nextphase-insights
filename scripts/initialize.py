import os
import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from scripts.init.init_database import initialize_database

def main():
    """Initialize the NextPhase Insights database"""
    print("\n=== NextPhase Insights Database Initialization ===\n")
    
    # Check for Firebase credentials
    cred_files = list(root_dir.glob('*firebase-adminsdk*.json'))
    if not cred_files:
        print("❌ Error: Firebase credentials not found!")
        print("Please place your service account key in the project root.")
        return
        
    print(f"Found credentials: {cred_files[0].name}")
    initialize_database()

if __name__ == "__main__":
    main()