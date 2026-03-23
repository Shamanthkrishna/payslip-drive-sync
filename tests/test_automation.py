"""
Unit tests for current Payslip Sync architecture.

Run with:
    python -m unittest tests.test_automation -v
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from src.config import Config
from src.paybooks_api import PaybooksAPI


class TestConfiguration(unittest.TestCase):
    def test_create_folders(self):
        Config.create_folders()
        self.assertTrue(Config.DOWNLOAD_FOLDER.exists())
        self.assertTrue(Config.LOG_FOLDER.exists())

    def test_validate_success(self):
        with patch.object(Config, 'PAYBOOKS_LOGIN_ID', 'user1'), \
             patch.object(Config, 'PAYBOOKS_PASSWORD', 'password1'), \
             patch.object(Config, 'PAYBOOKS_DOMAIN', 'example'):
            self.assertTrue(Config.validate())

    def test_validate_missing_values(self):
        with patch.object(Config, 'PAYBOOKS_LOGIN_ID', None), \
             patch.object(Config, 'PAYBOOKS_PASSWORD', 'password1'), \
             patch.object(Config, 'PAYBOOKS_DOMAIN', 'example'):
            with self.assertRaises(ValueError):
                Config.validate()


class TestFormatting(unittest.TestCase):
    def test_expected_drive_filename_format(self):
        month_date = datetime(2026, 2, 1)
        month_year = month_date.strftime('%B_%Y')
        self.assertEqual(f"{month_year}_PaySlip.pdf", "February_2026_PaySlip.pdf")

    def test_expected_local_filename_format(self):
        month_date = datetime(2026, 2, 1)
        self.assertEqual(f"payslip_{month_date.strftime('%m%y')}.pdf", "payslip_0226.pdf")


class TestPaybooksApiBasics(unittest.TestCase):
    def test_download_folder_exists_on_init(self):
        api = PaybooksAPI()
        self.assertTrue(api.download_folder.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
