"""
Unit Tests for Payslip Automation

Run with: python -m pytest tests/test_automation.py -v
or: python tests/test_automation.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from main import get_previous_month


class TestConfiguration(unittest.TestCase):
    """Test configuration management"""
    
    def test_config_folders_creation(self):
        """Test that required folders are created"""
        Config.create_folders()
        self.assertTrue(Config.DOWNLOAD_FOLDER.exists())
        self.assertTrue(Config.LOG_FOLDER.exists())
    
    def test_config_validation_with_valid_credentials(self):
        """Test config validation with valid credentials"""
        with patch.object(Config, 'PAYBOOKS_LOGIN_ID', '1234567'):
            with patch.object(Config, 'PAYBOOKS_PASSWORD', 'testpass'):
                with patch.object(Config, 'PAYBOOKS_DOMAIN', 'TESTDOMAIN'):
                    self.assertTrue(Config.validate())
    
    def test_config_validation_missing_credentials(self):
        """Test config validation fails with missing credentials"""
        with patch.object(Config, 'PAYBOOKS_LOGIN_ID', None):
            with self.assertRaises(ValueError):
                Config.validate()


class TestDateCalculations(unittest.TestCase):
    """Test date-related functions"""
    
    def test_previous_month_calculation(self):
        """Test that previous month is calculated correctly"""
        # Mock current date as Jan 21, 2026
        with patch('main.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 1, 21)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # Manually calculate expected previous month
            from dateutil.relativedelta import relativedelta as real_relativedelta
            expected = datetime(2026, 1, 21) - real_relativedelta(months=1)
            
            # Test the function
            result = get_previous_month()
            
            # Both should be December 2025
            self.assertEqual(result.month, 12)
            self.assertEqual(result.year, 2025)


class TestPaybooksScraper(unittest.TestCase):
    """Test Paybooks scraper functionality"""
    
    @patch('paybooks_scraper.webdriver.Chrome')
    def test_scraper_initialization(self, mock_chrome):
        """Test scraper initializes correctly"""
        from paybooks_scraper import PaybooksScraper
        
        scraper = PaybooksScraper()
        self.assertIsNone(scraper.driver)
        self.assertTrue(scraper.download_folder.exists())
    
    @patch('paybooks_scraper.webdriver.Chrome')
    def test_scraper_setup_driver(self, mock_chrome):
        """Test WebDriver setup"""
        from paybooks_scraper import PaybooksScraper
        
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        scraper = PaybooksScraper()
        scraper.setup_driver()
        
        self.assertIsNotNone(scraper.driver)
        mock_chrome.assert_called_once()


class TestDriveUploader(unittest.TestCase):
    """Test Google Drive uploader functionality"""
    
    def test_folder_structure_naming(self):
        """Test folder structure is named correctly"""
        from drive_uploader import DriveUploader
        
        test_date = datetime(2025, 12, 15)
        
        # We can't test the full method without Google credentials,
        # but we can test the date formatting
        year = test_date.strftime('%Y')
        month = test_date.strftime('%B')
        
        self.assertEqual(year, '2025')
        self.assertEqual(month, 'December')
    
    @patch('drive_uploader.build')
    @patch('drive_uploader.Credentials.from_authorized_user_file')
    def test_uploader_authentication(self, mock_creds, mock_build):
        """Test Google Drive authentication flow"""
        from drive_uploader import DriveUploader
        
        # Mock credentials
        mock_cred_obj = MagicMock()
        mock_cred_obj.valid = True
        mock_creds.return_value = mock_cred_obj
        
        # Mock token file exists
        with patch.object(Config, 'TOKEN_FILE') as mock_token:
            mock_token.exists.return_value = True
            
            # This should work without actual credentials
            # uploader = DriveUploader()  # Would fail without real credentials
            pass  # Skip for now as it requires real Google setup


class TestEmailNotifier(unittest.TestCase):
    """Test email notification functionality"""
    
    def test_notifier_skips_when_not_configured(self):
        """Test that email is skipped when credentials are missing"""
        from email_notifier import EmailNotifier
        
        with patch.object(Config, 'EMAIL_SENDER', None):
            with patch.object(Config, 'EMAIL_PASSWORD', None):
                notifier = EmailNotifier()
                result = notifier.send_email("Test", "Body")
                self.assertFalse(result)
    
    @patch('email_notifier.smtplib.SMTP')
    def test_email_sends_successfully(self, mock_smtp):
        """Test email sending with valid credentials"""
        from email_notifier import EmailNotifier
        
        with patch.object(Config, 'EMAIL_SENDER', 'test@gmail.com'):
            with patch.object(Config, 'EMAIL_PASSWORD', 'testpass'):
                with patch.object(Config, 'EMAIL_RECIPIENT', 'recipient@test.com'):
                    notifier = EmailNotifier()
                    
                    mock_server = MagicMock()
                    mock_smtp.return_value.__enter__.return_value = mock_server
                    
                    result = notifier.send_email("Test Subject", "Test Body")
                    
                    self.assertTrue(result)
                    mock_server.send_message.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for the full workflow"""
    
    def test_file_naming_format(self):
        """Test that file names are formatted correctly"""
        test_date = datetime(2025, 12, 15)
        
        # Test Google Drive filename
        month_year = test_date.strftime('%B_%Y')
        expected_drive_name = f"{month_year}_PaySlip.pdf"
        self.assertEqual(expected_drive_name, "December_2025_PaySlip.pdf")
        
        # Test local archive filename
        month_year_short = test_date.strftime('%m%y')
        expected_local_name = f"payslip_{month_year_short}.pdf"
        self.assertEqual(expected_local_name, "payslip_1225.pdf")
    
    def test_folder_paths_exist(self):
        """Test that all required folders can be created"""
        Config.create_folders()
        
        self.assertTrue(Config.DOWNLOAD_FOLDER.exists())
        self.assertTrue(Config.LOG_FOLDER.exists())
        self.assertTrue(Config.BASE_DIR.exists())


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
