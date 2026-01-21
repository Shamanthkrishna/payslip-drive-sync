import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    DOWNLOAD_FOLDER = BASE_DIR / os.getenv('DOWNLOAD_FOLDER', 'downloads')
    LOG_FOLDER = BASE_DIR / 'logs'
    
    # Paybooks settings
    PAYBOOKS_URL = os.getenv('PAYBOOKS_URL', 'https://ess.paybooks.in/')
    PAYBOOKS_LOGIN_ID = os.getenv('PAYBOOKS_LOGIN_ID')
    PAYBOOKS_PASSWORD = os.getenv('PAYBOOKS_PASSWORD')
    PAYBOOKS_DOMAIN = os.getenv('PAYBOOKS_DOMAIN')
    
    # Google Drive settings
    GOOGLE_DRIVE_ROOT_FOLDER = os.getenv('GOOGLE_DRIVE_ROOT_FOLDER', 'Pay Slips')
    CREDENTIALS_FILE = BASE_DIR / 'credentials.json'
    TOKEN_FILE = BASE_DIR / 'token.json'
    
    # Email notification settings
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Selenium settings
    HEADLESS_MODE = True  # Run browser in background
    DOWNLOAD_TIMEOUT = 60  # seconds to wait for download
    PAGE_LOAD_TIMEOUT = 30  # seconds to wait for page load
    
    @classmethod
    def create_folders(cls):
        """Create necessary folders if they don't exist"""
        cls.DOWNLOAD_FOLDER.mkdir(exist_ok=True)
        cls.LOG_FOLDER.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            ('PAYBOOKS_LOGIN_ID', cls.PAYBOOKS_LOGIN_ID),
            ('PAYBOOKS_PASSWORD', cls.PAYBOOKS_PASSWORD),
            ('PAYBOOKS_DOMAIN', cls.PAYBOOKS_DOMAIN),
        ]
        
        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True
