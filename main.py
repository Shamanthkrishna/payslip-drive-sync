#!/usr/bin/env python3
"""
Pay Slip Automation - Main Script (API-Based)

Automates downloading pay slips from Paybooks portal and uploading to Google Drive.
Uses fast API calls instead of Selenium web scraping.
Designed to run monthly via Windows Task Scheduler.
"""

import os
import sys
import logging
import traceback
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.config import Config
from src.paybooks_api import PaybooksAPI
from src.drive_uploader import DriveUploader
from src.email_notifier import EmailNotifier


def setup_logging():
    """Configure logging to both file and console"""
    Config.create_folders()
    
    # Create log filename with date
    log_file = Config.LOG_FOLDER / f"payslip_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Setup handlers
    handlers = [
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=handlers
    )
    
    logger = logging.getLogger(__name__)
    logger.info("="*70)
    logger.info("PAY SLIP AUTOMATION STARTED")
    logger.info("="*70)
    logger.info(f"Log file: {log_file}")
    
    return logger


def get_previous_month():
    """Get the previous month's date"""
    return datetime.now() - relativedelta(months=1)


def cleanup_download(file_path, previous_month):
    """Rename and keep the downloaded file in local storage"""
    try:
        if file_path and Path(file_path).exists():
            # Create archive folder
            archive_folder = Config.BASE_DIR / 'payslips_archive'
            archive_folder.mkdir(exist_ok=True)
            
            # Create filename: payslip_MMYY (e.g., payslip_1225 for Dec 2025)
            month_year = previous_month.strftime('%m%y')
            new_filename = f"payslip_{month_year}.pdf"
            new_path = archive_folder / new_filename
            
            # Move and rename file
            import shutil
            shutil.move(str(file_path), str(new_path))
            logging.getLogger(__name__).info(f"Payslip archived to: {new_path}")
            return new_path
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to archive file: {e}")


def main():
    """Main execution flow"""
    logger = setup_logging()
    notifier = EmailNotifier()
    downloaded_file = None
    
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        Config.validate()
        logger.info("Configuration valid")
        
        # Get target month
        previous_month = get_previous_month()
        month_year = previous_month.strftime('%B %Y')
        logger.info(f"Target month: {month_year}")
        
        # Step 1: Download from Paybooks
        logger.info("-"*70)
        logger.info("STEP 1: Downloading pay slip from Paybooks API")
        logger.info("-"*70)
        
        api_client = PaybooksAPI()
        downloaded_file = api_client.download_latest_payslip()
        
        if not downloaded_file or not downloaded_file.exists():
            raise Exception("Pay slip download failed - file not found")
        
        logger.info(f"Download successful: {downloaded_file}")
        
        # Step 2: Upload to Google Drive
        logger.info("-"*70)
        logger.info("STEP 2: Uploading to Google Drive")
        logger.info("-"*70)
        
        uploader = DriveUploader()
        upload_result = uploader.upload_file(downloaded_file, previous_month)
        
        if upload_result:
            logger.info("Upload successful!")
            
            # Send success notification
            file_name = previous_month.strftime('%B_%Y_PaySlip.pdf')
            notifier.notify_success(month_year, file_name)
            
            logger.info("="*70)
            logger.info("PAY SLIP AUTOMATION COMPLETED SUCCESSFULLY")
            logger.info("="*70)
            
        else:
            logger.warning("File already exists in Google Drive - skipping upload")
            
            file_name = previous_month.strftime('%B_%Y_PaySlip.pdf')
            notifier.notify_already_exists(month_year, file_name)
            
            logger.info("="*70)
            logger.info("PAY SLIP AUTOMATION COMPLETED - FILE ALREADY EXISTS")
            logger.info("="*70)
        
        return 0  # Success
        
    except Exception as e:
        # Log error with full traceback
        error_msg = f"{str(e)}\n\nFull traceback:\n{traceback.format_exc()}"
        logger.error("="*70)
        logger.error("PAY SLIP AUTOMATION FAILED")
        logger.error("="*70)
        logger.error(error_msg)
        
        # Send error notification
        try:
            month_year = get_previous_month().strftime('%B %Y')
            notifier.notify_error(error_msg, month_year)
        except Exception as notify_error:
            logger.error(f"Failed to send error notification: {notify_error}")
        
        return 1  # Failure
        
    finally:
        # Archive downloaded file locally
        if downloaded_file:
            cleanup_download(downloaded_file, previous_month)
        
        logger.info("Script execution finished")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
