import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import platform
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import OperationSystemManager
from config import Config

logger = logging.getLogger(__name__)


class PaybooksScraper:
    """Handles Paybooks portal automation for pay slip download"""
    
    def __init__(self):
        self.driver = None
        self.download_folder = Config.DOWNLOAD_FOLDER.resolve()
    
    def setup_driver(self):
        """Configure and initialize Chrome WebDriver"""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        # Headless mode (runs without opening browser window)
        if Config.HEADLESS_MODE:
            chrome_options.add_argument('--headless=new')
            logger.info("Running in headless mode")
        
        # Performance and stability options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--log-level=3')  # Suppress console errors
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Set download directory
        prefs = {
            'download.default_directory': str(self.download_folder),
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True,
            'plugins.always_open_pdf_externally': True  # Download PDFs instead of opening
        }
        chrome_options.add_experimental_option('prefs', prefs)
        
        # Initialize driver
        try:
            # Try using system ChromeDriver or let Selenium find it automatically
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logger.warning(f"Default Chrome setup failed: {e}")
            # Fallback to webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        logger.info("WebDriver setup complete")
    
    def login(self):
        """Login to Paybooks portal"""
        logger.info(f"Navigating to {Config.PAYBOOKS_URL}")
        self.driver.get(Config.PAYBOOKS_URL)
        
        try:
            # Wait for login page to load
            wait = WebDriverWait(self.driver, 15)
            time.sleep(2)  # Let page fully load
            
            # Fill in login credentials in order: Login ID, Password, Domain
            logger.info("Entering login credentials...")
            
            # Try multiple possible selectors for each field
            # Login ID field (first)
            login_selectors = [
                (By.ID, "txtUserId"),
                (By.NAME, "txtUserId"),
                (By.XPATH, "//input[@placeholder='User ID' or @placeholder='Login ID' or @type='text']"),
            ]
            
            login_field = None
            for by, selector in login_selectors:
                try:
                    login_field = wait.until(EC.presence_of_element_located((by, selector)))
                    logger.info(f"Found login field with {by}: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not login_field:
                raise Exception("Could not find login ID field")
            
            login_field.clear()
            login_field.send_keys(Config.PAYBOOKS_LOGIN_ID)
            logger.info("Login ID entered")
            
            # Password field (second)
            password_selectors = [
                (By.ID, "txtPassword"),
                (By.NAME, "txtPassword"),
                (By.XPATH, "//input[@type='password']"),
            ]
            
            password_field = None
            for by, selector in password_selectors:
                try:
                    password_field = self.driver.find_element(by, selector)
                    logger.info(f"Found password field with {by}: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                raise Exception("Could not find password field")
            
            password_field.clear()
            password_field.send_keys(Config.PAYBOOKS_PASSWORD)
            logger.info("Password entered")
            
            # Domain field (third)
            domain_selectors = [
                (By.ID, "txtDomain"),
                (By.ID, "txtDomainId"),
                (By.NAME, "txtDomain"),
                (By.XPATH, "//input[@placeholder='Domain' or @placeholder='Company']"),
            ]
            
            domain_field = None
            for by, selector in domain_selectors:
                try:
                    domain_field = self.driver.find_element(by, selector)
                    logger.info(f"Found domain field with {by}: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not domain_field:
                raise Exception("Could not find domain field")
            
            # Enter domain with retry logic
            try:
                domain_field.clear()
                time.sleep(0.5)
                domain_field.send_keys(Config.PAYBOOKS_DOMAIN)
                logger.info("Domain entered")
            except Exception as e:
                logger.error(f"Failed to enter domain: {e}")
                # Try clicking first then entering
                domain_field.click()
                time.sleep(0.5)
                domain_field.send_keys(Config.PAYBOOKS_DOMAIN)
                logger.info("Domain entered (after click)")
            
            # Click login button
            login_button_selectors = [
                (By.ID, "btnLogin"),
                (By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), 'Sign In')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]
            
            login_button = None
            for by, selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(by, selector)
                    logger.info(f"Found login button with {by}: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                raise Exception("Could not find login button")
            
            login_button.click()
            logger.info("Login credentials submitted")
            
            # Wait for successful login (adjust selector based on actual homepage)
            wait.until(EC.url_changes(Config.PAYBOOKS_URL))
            time.sleep(3)  # Additional wait for page to stabilize
            
            logger.info("Login successful")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Login failed: {str(e)}")
            self.save_screenshot("login_failure")
            raise Exception(f"Failed to login to Paybooks: {str(e)}")
    
    def download_payslip(self):
        """Navigate to pay slip and download it"""
        try:
            wait = WebDriverWait(self.driver, 15)
            
            # Click on "Previous Month Payslip" button on homepage
            logger.info("Looking for previous month payslip button...")
            
            # Try multiple possible selectors
            possible_selectors = [
                (By.XPATH, "//div[@ng-click='viewPayslip(); $event.stopPropagation()']"),
                (By.XPATH, "//div[contains(@ng-click, 'viewPayslip')]"),
                (By.XPATH, "//div[contains(text(), 'payslip')]"),
                (By.LINK_TEXT, "View Payslip"),
                (By.PARTIAL_LINK_TEXT, "Payslip"),
                (By.PARTIAL_LINK_TEXT, "Pay Slip"),
                (By.XPATH, "//a[contains(text(), 'Payslip') or contains(text(), 'Pay Slip')]"),
                (By.XPATH, "//button[contains(text(), 'Payslip') or contains(text(), 'Pay Slip')]"),
            ]
            
            payslip_button = None
            for by, selector in possible_selectors:
                try:
                    payslip_button = wait.until(EC.element_to_be_clickable((by, selector)))
                    break
                except TimeoutException:
                    continue
            
            if not payslip_button:
                raise Exception("Could not find payslip button on homepage")
            
            logger.info("Clicking on payslip button...")
            payslip_button.click()
            time.sleep(3)
            
            # Now on detailed payslip page, find download button
            logger.info("Looking for download button...")
            
            download_selectors = [
                (By.XPATH, "//a[@ng-click='fileDownloadClick()']"),
                (By.XPATH, "//a[contains(@ng-click, 'fileDownloadClick')]"),
                (By.XPATH, "//i[@class='fa fa-download']/ancestor::a"),
                (By.XPATH, "//i[contains(@class, 'fa-download')]/ancestor::a"),
                (By.LINK_TEXT, "Download"),
                (By.PARTIAL_LINK_TEXT, "Download"),
                (By.XPATH, "//a[contains(text(), 'Download')]"),
                (By.XPATH, "//button[contains(text(), 'Download')]"),
                (By.XPATH, "//i[contains(@class, 'download')]//parent::*"),
            ]
            
            download_button = None
            for by, selector in download_selectors:
                try:
                    download_button = wait.until(EC.element_to_be_clickable((by, selector)))
                    break
                except TimeoutException:
                    continue
            
            if not download_button:
                raise Exception("Could not find download button")
            
            # Get list of files before download
            files_before = set(self.download_folder.glob('*'))
            
            logger.info("Clicking download button...")
            download_button.click()
            
            # Wait for download to complete
            downloaded_file = self.wait_for_download(files_before)
            
            if downloaded_file:
                logger.info(f"Pay slip downloaded successfully: {downloaded_file.name}")
                return downloaded_file
            else:
                raise Exception("Download did not complete within timeout period")
            
        except Exception as e:
            logger.error(f"Failed to download payslip: {str(e)}")
            self.save_screenshot("download_failure")
            raise
    
    def wait_for_download(self, files_before, timeout=None):
        """Wait for new file to appear in download folder"""
        if timeout is None:
            timeout = Config.DOWNLOAD_TIMEOUT
        
        logger.info(f"Waiting for download to complete (timeout: {timeout}s)...")
        
        end_time = time.time() + timeout
        while time.time() < end_time:
            time.sleep(2)
            
            # Check for new files
            files_after = set(self.download_folder.glob('*'))
            new_files = files_after - files_before
            
            # Filter out temporary download files
            completed_files = [
                f for f in new_files 
                if f.is_file() and not f.name.endswith('.crdownload') and not f.name.endswith('.tmp')
            ]
            
            if completed_files:
                return completed_files[0]
        
        logger.warning("Download timeout reached")
        return None
    
    def save_screenshot(self, name):
        """Save screenshot for debugging"""
        try:
            screenshot_path = Config.LOG_FOLDER / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.warning(f"Could not save screenshot: {e}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            logger.info("Closing WebDriver...")
            self.driver.quit()
            self.driver = None
    
    def download_latest_payslip(self):
        """Main method to download pay slip"""
        try:
            Config.create_folders()
            self.setup_driver()
            self.login()
            payslip_file = self.download_payslip()
            return payslip_file
        finally:
            self.close()


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        Config.validate()
        scraper = PaybooksScraper()
        file = scraper.download_latest_payslip()
        print(f"Downloaded: {file}")
    except Exception as e:
        print(f"Error: {e}")
