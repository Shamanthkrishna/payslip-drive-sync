#!/usr/bin/env python3
"""
Smart Payslip Sync - Production Version

Automatically syncs all payslips from Paybooks to Google Drive.
- First run: Downloads ALL available payslips
- Subsequent runs: Downloads only missing payslips
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.config import Config
from src.paybooks_api import PaybooksAPI
from src.drive_uploader import DriveUploader


def setup_logging():
    """Configure logging - one log file per day"""
    Config.create_folders()
    
    log_file = Config.LOG_FOLDER / f"payslip_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def get_existing_payslips_from_drive(uploader):
    """
    Get list of months that already have payslips in Google Drive
    
    Returns:
        Set of datetime objects representing months with existing payslips
    """
    existing_months = set()
    
    try:
        # Get the root Pay Slips folder
        root_folder_id = uploader.get_folder_id("Pay Slips", uploader.drive_service.files(), None)
        if not root_folder_id:
            return existing_months
        
        # Get all year folders
        query = f"'{root_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = uploader.drive_service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        year_folders = results.get('files', [])
        
        for year_folder in year_folders:
            year = year_folder['name']
            if not year.isdigit():
                continue
            
            # Get all month folders in this year
            query = f"'{year_folder['id']}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = uploader.drive_service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            month_folders = results.get('files', [])
            
            for month_folder in month_folders:
                month_name = month_folder['name']
                
                # Check if this folder has any PDF files
                query = f"'{month_folder['id']}' in parents and mimeType='application/pdf' and trashed=false"
                results = uploader.drive_service.files().list(
                    q=query,
                    fields="files(id, name)"
                ).execute()
                
                if results.get('files', []):
                    # Parse month and year to datetime
                    try:
                        month_date = datetime.strptime(f"{month_name} {year}", "%B %Y")
                        existing_months.add(month_date)
                    except:
                        pass
        
        return existing_months
        
    except Exception as e:
        logging.error(f"Failed to get existing payslips from Drive: {e}")
        return existing_months


def sync_all_payslips(max_months=24):
    """
    Sync all payslips from Paybooks to Google Drive
    
    Args:
        max_months: Maximum number of months to go back (default 24 = 2 years)
    """
    logger = setup_logging()
    
    try:
        Config.validate()
        
        logger.info("="*70)
        logger.info("SMART PAYSLIP SYNC - PRODUCTION VERSION")
        logger.info("="*70)
        
        # Initialize components
        api_client = PaybooksAPI()
        uploader = DriveUploader()
        
        # Check existing payslips in Drive
        logger.info("Checking existing payslips in Google Drive...")
        existing_months = get_existing_payslips_from_drive(uploader)
        
        if existing_months:
            logger.info(f"Found {len(existing_months)} payslips already in Drive")
            logger.info("Months with existing payslips:")
            for month in sorted(existing_months):
                logger.info(f"  - {month.strftime('%B %Y')}")
        else:
            logger.info("No existing payslips found - will download all available")
        
        # Download missing payslips
        logger.info("-"*70)
        logger.info(f"Downloading missing payslips (checking last {max_months} months)...")
        logger.info("-"*70)
        
        results = api_client.download_multiple_months(max_months, skip_existing=existing_months)
        
        if not results:
            logger.info("All payslips are up to date!")
            print("\n\u2705 All payslips are up to date!")
            return
        
        logger.info(f"\nSuccessfully downloaded {len(results)} new payslips")
        
        # Upload each to Google Drive
        uploaded_count = 0
        skipped_count = 0
        
        logger.info("-"*70)
        logger.info("Uploading to Google Drive...")
        logger.info("-"*70)
        
        for month_date, filepath in results:
            month_name = month_date.strftime('%B %Y')
            
            logger.info(f"Uploading {month_name}...")
            
            upload_result = uploader.upload_file(filepath, month_date)
            
            if upload_result:
                logger.info(f"  [OK] {month_name} uploaded successfully")
                uploaded_count += 1
            else:
                logger.info(f"  - {month_name} already exists - skipped")
                skipped_count += 1
        
        # Summary
        logger.info("="*70)
        logger.info("SYNC COMPLETED")
        logger.info(f"Downloaded: {len(results)} payslips")
        logger.info(f"Uploaded: {uploaded_count} new files")
        logger.info(f"Skipped: {skipped_count} (already in Drive)")
        logger.info("="*70)
        
        print(f"\n[SUCCESS] Sync complete!")
        print(f"   Downloaded: {len(results)} payslips")
        print(f"   Uploaded: {uploaded_count} new files")
        print(f"   Skipped: {skipped_count} (duplicates)")
        
    except Exception as e:
        logging.error(f"Sync failed: {e}")
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Smart Payslip Sync - Automatically sync payslips to Google Drive"
    )
    parser.add_argument(
        '--max-months',
        type=int,
        default=24,
        help='Maximum months to check (default: 24)'
    )
    
    args = parser.parse_args()
    
    sync_all_payslips(args.max_months)
