import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Feature flags
    ENABLE_AUTH = os.getenv('ENABLE_AUTH', 'false').lower() == 'true'
    
    # Auth settings
    REQUIRE_LOGIN = ENABLE_AUTH  # Tie login requirement to auth setting
    
    # Default values
    DEFAULT_TOOLS = ['Email', 'Spreadsheets']
    DEFAULT_FREQUENCY = 'Daily'
    INDUSTRIES = [
        "Finance",
        "Healthcare", 
        "Technology",
        "Manufacturing",
        "Retail"
    ]