"""
Payslip Drive Sync - Core Package

Automatically downloads payslips from Paybooks and uploads to Google Drive.
"""

__version__ = "2.0.0"
__author__ = "Shamanth Krishna"

from .paybooks_api import PaybooksAPI
from .drive_uploader import DriveUploader
from .config import Config

__all__ = ['PaybooksAPI', 'DriveUploader', 'Config']
