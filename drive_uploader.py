import os
import logging
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from config import Config

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class DriveUploader:
    """Handles Google Drive file upload and folder management"""
    
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive API"""
        logger.info("Authenticating with Google Drive...")
        
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if Config.TOKEN_FILE.exists():
            logger.info("Loading existing credentials...")
            creds = Credentials.from_authorized_user_file(str(Config.TOKEN_FILE), SCOPES)
        
        # If credentials are invalid or don't exist, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                if not Config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Google Drive credentials file not found: {Config.CREDENTIALS_FILE}\n"
                        "Please follow the setup instructions in README.md"
                    )
                
                logger.info("Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(Config.CREDENTIALS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            Config.TOKEN_FILE.write_text(creds.to_json())
            logger.info("Credentials saved")
        
        self.service = build('drive', 'v3', credentials=creds)
        logger.info("Google Drive authentication successful")
    
    def find_or_create_folder(self, folder_name, parent_id=None):
        """Find existing folder or create new one"""
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                logger.info(f"Found existing folder: {folder_name}")
                return folders[0]['id']
            
            # Create new folder
            logger.info(f"Creating folder: {folder_name}")
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            logger.info(f"Folder created: {folder_name} (ID: {folder['id']})")
            return folder['id']
            
        except HttpError as e:
            logger.error(f"Error finding/creating folder: {e}")
            raise
    
    def get_folder_structure(self, previous_month_date):
        """
        Create folder structure: Pay Slips/YYYY/Month_Name/
        Returns the folder ID of the target folder
        """
        year = previous_month_date.strftime('%Y')
        month_name = previous_month_date.strftime('%B')  # Full month name (e.g., "December")
        
        logger.info(f"Setting up folder structure for {month_name} {year}")
        
        # Create/find root folder
        root_folder_id = None
        if Config.GOOGLE_DRIVE_ROOT_FOLDER:
            root_folder_id = self.find_or_create_folder(Config.GOOGLE_DRIVE_ROOT_FOLDER)
        
        # Create/find year folder
        year_folder_id = self.find_or_create_folder(year, root_folder_id)
        
        # Create/find month folder
        month_folder_id = self.find_or_create_folder(month_name, year_folder_id)
        
        return month_folder_id
    
    def file_exists(self, file_name, folder_id):
        """Check if file already exists in the folder"""
        try:
            query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                logger.info(f"File already exists: {file_name}")
                return True
            
            return False
            
        except HttpError as e:
            logger.error(f"Error checking file existence: {e}")
            return False
    
    def upload_file(self, local_file_path, previous_month_date):
        """
        Upload file to Google Drive with proper folder structure
        Returns True if successful, False if file already exists or error
        """
        try:
            local_file = Path(local_file_path)
            
            if not local_file.exists():
                raise FileNotFoundError(f"File not found: {local_file_path}")
            
            # Get target folder
            folder_id = self.get_folder_structure(previous_month_date)
            
            # Create filename with month and year
            month_year = previous_month_date.strftime('%B_%Y')
            new_filename = f"{month_year}_PaySlip.pdf"
            
            # Check if file already exists
            if self.file_exists(new_filename, folder_id):
                logger.warning(f"File already exists in Google Drive: {new_filename}")
                return False
            
            # Upload file
            logger.info(f"Uploading {new_filename} to Google Drive...")
            
            file_metadata = {
                'name': new_filename,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(
                str(local_file),
                mimetype='application/pdf',
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            logger.info(f"Upload successful: {file.get('name')}")
            logger.info(f"File ID: {file.get('id')}")
            logger.info(f"View link: {file.get('webViewLink')}")
            
            return True
            
        except HttpError as e:
            logger.error(f"Google Drive upload failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Upload error: {e}")
            raise
    
    def get_file_url(self, file_name, folder_id):
        """Get the web view link for an uploaded file"""
        try:
            query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
            
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(webViewLink)'
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                return files[0].get('webViewLink')
            
            return None
            
        except HttpError as e:
            logger.error(f"Error getting file URL: {e}")
            return None


if __name__ == "__main__":
    # Test the uploader
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        uploader = DriveUploader()
        
        # Test with previous month
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        previous_month = datetime.now() - relativedelta(months=1)
        print(f"Testing folder structure for: {previous_month.strftime('%B %Y')}")
        
        folder_id = uploader.get_folder_structure(previous_month)
        print(f"Target folder ID: {folder_id}")
        
    except Exception as e:
        print(f"Error: {e}")
