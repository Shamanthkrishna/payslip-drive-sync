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
    Get list of months that already have payslips in Google Drive.
    Supports both the new flat structure (Pay Slips/YYYY/MonthName_YYYY_PaySlip.pdf)
    and the legacy structure (Pay Slips/YYYY/MonthName/MonthName_YYYY_PaySlip.pdf).

    Returns:
        Set of datetime objects (normalized to 1st of month) representing months with existing payslips
    """
    existing_months = set()
    
    try:
        service = uploader.service

        # Find root folder by configured name.
        root_query = (
            f"name='{Config.GOOGLE_DRIVE_ROOT_FOLDER}' and "
            "mimeType='application/vnd.google-apps.folder' and trashed=false"
        )
        root_results = service.files().list(q=root_query, fields="files(id, name)").execute()
        root_folders = root_results.get('files', [])
        if not root_folders:
            return existing_months

        root_folder_id = root_folders[0]['id']

        # Get all year folders.
        year_query = f"'{root_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        year_results = service.files().list(q=year_query, fields="files(id, name)").execute()

        for year_folder in year_results.get('files', []):
            year = year_folder['name']
            if not year.isdigit():
                continue

            # --- New flat structure: PDFs directly in year folder ---
            pdf_query = (
                f"'{year_folder['id']}' in parents and "
                "mimeType='application/pdf' and trashed=false"
            )
            pdf_results = service.files().list(q=pdf_query, fields="files(id, name)").execute()
            for pdf_file in pdf_results.get('files', []):
                filename = pdf_file['name']  # e.g. "January_2026_PaySlip.pdf"
                try:
                    month_date = datetime.strptime(
                        filename.replace('_PaySlip.pdf', ''), "%B_%Y"
                    )
                    existing_months.add(month_date)
                except ValueError:
                    logging.debug(f"Skipping non-standard file: {filename}")

            # --- Legacy structure: month subfolders inside year folder ---
            month_query = (
                f"'{year_folder['id']}' in parents and "
                "mimeType='application/vnd.google-apps.folder' and trashed=false"
            )
            month_results = service.files().list(q=month_query, fields="files(id, name)").execute()
            for month_folder in month_results.get('files', []):
                month_name = month_folder['name']
                pdf_in_month_query = (
                    f"'{month_folder['id']}' in parents and "
                    "mimeType='application/pdf' and trashed=false"
                )
                pdf_in_month = service.files().list(
                    q=pdf_in_month_query, fields="files(id)"
                ).execute()
                if pdf_in_month.get('files', []):
                    try:
                        month_date = datetime.strptime(f"{month_name} {year}", "%B %Y")
                        existing_months.add(month_date)
                    except ValueError:
                        logging.debug(f"Skipping non-standard month folder: {month_name} {year}")

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
            return True
        
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
            
            # Skip the existence check: these months were already confirmed absent
            # by get_existing_payslips_from_drive(), avoiding a redundant Drive API call.
            upload_result = uploader.upload_file(filepath, month_date, check_exists=False)
            
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
        return True
        
    except Exception as e:
        logging.error(f"Sync failed: {e}")
        print(f"\n[ERROR] {e}")
        return False


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
    
    success = sync_all_payslips(args.max_months)
    if not success:
        sys.exit(1)
