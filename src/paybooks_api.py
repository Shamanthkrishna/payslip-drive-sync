"""
Paybooks API Client - Fast API-based payslip downloader

This uses the discovered Paybooks API instead of Selenium web scraping.
Much faster and can download historical payslips easily.
"""

import os
import base64
import json
import logging
import time
from pathlib import Path
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from .config import Config

logger = logging.getLogger(__name__)


class PaybooksAPI:
    """Handles Paybooks API authentication and payslip downloads"""
    
    def __init__(self):
        self.login_token = None
        self.session = requests.Session()
        self.api_url = "https://apislip.paybooks.in/Payslip/PayslipDownload"
        self.download_folder = Config.DOWNLOAD_FOLDER
        self.token_file = Config.BASE_DIR / '.paybooks_token'
    
    def load_cached_token(self):
        """Load previously saved login token"""
        try:
            if self.token_file.exists():
                token_data = json.loads(self.token_file.read_text())
                # Check if token is not too old (24 hours)
                saved_time = datetime.fromisoformat(token_data['timestamp'])
                age_hours = (datetime.now() - saved_time).total_seconds() / 3600
                
                if age_hours < 24:
                    self.login_token = token_data['token']
                    logger.info(f"Loaded cached token (age: {age_hours:.1f} hours)")
                    return True
                else:
                    logger.info("Cached token expired")
        except Exception as e:
            logger.warning(f"Could not load cached token: {e}")
        
        return False
    
    def save_token(self, token):
        """Save login token for future use"""
        try:
            token_data = {
                'token': token,
                'timestamp': datetime.now().isoformat()
            }
            self.token_file.write_text(json.dumps(token_data, indent=2))
            logger.info("Login token saved")
        except Exception as e:
            logger.warning(f"Could not save token: {e}")
    
    def get_login_token_via_browser(self):
        """Use Selenium to login and extract the LoginToken automatically"""
        logger.info("Logging in to extract API token...")
        
        driver = None
        try:
            # Setup Chrome in headless mode for automatic extraction
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Enable performance logging to capture network requests
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # Navigate and login
            logger.info(f"Navigating to {Config.PAYBOOKS_URL}")
            driver.get(Config.PAYBOOKS_URL)
            
            wait = WebDriverWait(driver, 20)
            time.sleep(2)
            
            # Fill login form - try multiple field name variations
            try:
                login_field = wait.until(
                    EC.presence_of_element_located((By.ID, "txtUserName"))
                )
            except:
                try:
                    login_field = driver.find_element(By.XPATH, "//input[@placeholder='User ID' or @placeholder='Login ID']")
                except:
                    login_field = driver.find_element(By.XPATH, "//input[@type='text']")
            
            login_field.clear()
            login_field.send_keys(Config.PAYBOOKS_LOGIN_ID)
            
            password_field = driver.find_element(By.ID, "txtPassword")
            password_field.clear()
            password_field.send_keys(Config.PAYBOOKS_PASSWORD)
            
            # Try different domain field IDs
            try:
                domain_field = driver.find_element(By.ID, "txtDomainId")
            except:
                try:
                    domain_field = driver.find_element(By.ID, "txtDomain")
                except:
                    domain_field = driver.find_element(By.XPATH, "//input[@placeholder='Domain' or @placeholder='Company']")
            
            domain_field.clear()
            domain_field.send_keys(Config.PAYBOOKS_DOMAIN)
            
            # Try different login button selectors
            try:
                login_button = driver.find_element(By.ID, "btnLogin")
            except:
                try:
                    login_button = driver.find_element(By.XPATH, "//button[contains(@ng-click, 'userLogin')]")
                except:
                    login_button = driver.find_element(By.XPATH, "//button[@type='submit' or text()='Login' or text()='Sign In']")
            
            login_button.click()
            
            # Wait for login
            time.sleep(5)
            
            logger.info("Login successful, extracting token...")
            
            # Method 1: Check sessionStorage.userInfo for tokenKey (PRIMARY METHOD)
            try:
                user_info = driver.execute_script("return sessionStorage.getItem('userInfo');")
                if user_info:
                    import json
                    user_data = json.loads(user_info)
                    token = user_data.get('tokenKey')
                    if token:
                        logger.info("[SUCCESS] Extracted token from sessionStorage.userInfo.tokenKey")
                        return token
            except Exception as e:
                logger.debug(f"sessionStorage.userInfo failed: {e}")
            
            # Method 2: Check localStorage first
            try:
                token = driver.execute_script("return localStorage.getItem('LoginToken');")
                if token:
                    logger.info("[SUCCESS] Extracted token from localStorage")
                    return token
            except Exception as e:
                logger.debug(f"localStorage failed: {e}")
            
            # Method 2: Check sessionStorage
            try:
                token = driver.execute_script("return sessionStorage.getItem('LoginToken');")
                if token:
                    logger.info("Extracted token from sessionStorage")
                    return token
            except Exception as e:
                logger.debug(f"sessionStorage failed: {e}")
            
            # Method 3: Try to get from Angular scope (Paybooks uses AngularJS)
            try:
                script = """
                var token = null;
                try {
                    // Try to get from angular scope
                    var scope = angular.element(document.body).scope();
                    if (scope && scope.LoginToken) {
                        token = scope.LoginToken;
                    } else if (scope && scope.$root && scope.$root.LoginToken) {
                        token = scope.$root.LoginToken;
                    }
                    
                    // Try localStorage with all keys
                    if (!token) {
                        for (var i = 0; i < localStorage.length; i++) {
                            var key = localStorage.key(i);
                            if (key && key.toLowerCase().includes('token')) {
                                token = localStorage.getItem(key);
                                if (token && token.length > 20) break;
                            }
                        }
                    }
                    
                    // Try sessionStorage with all keys
                    if (!token) {
                        for (var i = 0; i < sessionStorage.length; i++) {
                            var key = sessionStorage.key(i);
                            if (key && key.toLowerCase().includes('token')) {
                                token = sessionStorage.getItem(key);
                                if (token && token.length > 20) break;
                            }
                        }
                    }
                } catch(e) {}
                return token;
                """
                token = driver.execute_script(script)
                if token:
                    logger.info("Extracted token from Angular scope")
                    return token
            except Exception as e:
                logger.debug(f"Angular scope failed: {e}")
            
            # Method 4: Navigate to payslip page and check again
            try:
                logger.info("Navigating to payslip page...")
                driver.get("https://apps.paybooks.in/#!/payslip")
                time.sleep(3)
                
                token = driver.execute_script("return localStorage.getItem('LoginToken') || sessionStorage.getItem('LoginToken');")
                if token:
                    logger.info("Extracted token after navigation")
                    return token
            except Exception as e:
                logger.debug(f"Navigation attempt failed: {e}")
            
            # Method 5: Check all cookies
            try:
                cookies = driver.get_cookies()
                for cookie in cookies:
                    if 'token' in cookie['name'].lower() and len(cookie['value']) > 20:
                        logger.info(f"Extracted token from cookie: {cookie['name']}")
                        return cookie['value']
            except Exception as e:
                logger.debug(f"Cookie check failed: {e}")
            
            # If all methods fail
            logger.error("Could not automatically extract token")
            raise Exception("Failed to extract LoginToken automatically")
            
        finally:
            if driver:
                driver.quit()
    
    def authenticate(self):
        """Authenticate and get login token"""
        # Try loading cached token first
        if self.load_cached_token():
            return True
        
        # Get new token via browser login
        token = self.get_login_token_via_browser()
        if token:
            self.login_token = token
            self.save_token(token)
            return True
        
        return False
    
    def download_payslip(self, month_date):
        """
        Download payslip for a specific month using API
        
        Args:
            month_date: datetime object for the target month
        
        Returns:
            Path to downloaded file or None
        """
        try:
            # Format month as "01-MM-YYYY"
            payslip_month = month_date.strftime('01-%m-%Y')
            month_name = month_date.strftime('%B %Y')
            
            logger.info(f"Downloading payslip for {month_name} via API...")
            
            # Prepare payload
            payload_data = {
                "PayslipMonth": payslip_month,
                "IsMailRequest": False,
                "LoginToken": self.login_token,
                "IsSendMail": False  # Don't send email
            }
            
            # Encode payload as base64
            payload_json = json.dumps(payload_data)
            payload_b64 = base64.b64encode(payload_json.encode()).decode()
            
            logger.info(f"API request for month: {payslip_month}")
            
            # Make API request
            response = self.session.post(
                self.api_url,
                data={'requestData': payload_b64},
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Response is JSON with base64-encoded PDF
                try:
                    response_data = response.json()
                    response_payload = base64.b64decode(response_data['responseData']).decode('utf-8')
                    payload_json = json.loads(response_payload)
                    
                    if payload_json.get('isSuccess'):
                        # PDF is base64-encoded in fileContentBase64
                        pdf_b64 = payload_json.get('fileContentBase64')
                        if pdf_b64:
                            # Decode the PDF content
                            pdf_content = base64.b64decode(pdf_b64)
                            
                            # Save PDF
                            filename = f"payslip_{month_date.strftime('%m%y')}.pdf"
                            filepath = self.download_folder / filename
                            
                            filepath.write_bytes(pdf_content)
                            logger.info(f"Payslip downloaded successfully: {filename}")
                            return filepath
                        else:
                            logger.error("No PDF content in response")
                            return None
                    else:
                        error_msg = payload_json.get('errorMessage', 'Unknown error')
                        logger.error(f"API returned error: {error_msg}")
                        return None
                        
                except Exception as e:
                    logger.error(f"Failed to parse API response: {e}")
                    return None
            else:
                logger.error(f"API request failed: {response.status_code}")
                logger.error(f"Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to download payslip via API: {e}")
            return None
    
    def download_latest_payslip(self):
        """Download the most recent month's payslip"""
        from dateutil.relativedelta import relativedelta
        
        # Ensure authenticated
        if not self.login_token:
            if not self.authenticate():
                raise Exception("Authentication failed")
        
        # Get previous month
        previous_month = datetime.now() - relativedelta(months=1)
        
        # Download using API
        return self.download_payslip(previous_month)
    
    def download_multiple_months(self, num_months=12, skip_existing=None):
        """
        Download payslips for multiple months
        
        Args:
            num_months: Number of months to download (going backwards from current)
            skip_existing: Set of month_dates to skip (already in Drive)
        
        Returns:
            List of (month_date, filepath) tuples
        """
        from dateutil.relativedelta import relativedelta
        
        # Ensure authenticated
        if not self.login_token:
            if not self.authenticate():
                raise Exception("Authentication failed")
        
        results = []
        current = datetime.now()
        
        for i in range(1, num_months + 1):
            month_date = current - relativedelta(months=i)
            
            # Skip if already exists in Drive
            if skip_existing and month_date in skip_existing:
                logger.info(f"Skipping {month_date.strftime('%B %Y')} - already in Drive")
                continue
            
            filepath = self.download_payslip(month_date)
            
            if filepath:
                results.append((month_date, filepath))
            
            # Small delay between requests
            time.sleep(1)
        
        return results


if __name__ == "__main__":
    # Test the API client
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        Config.validate()
        Config.create_folders()
        
        api = PaybooksAPI()
        file = api.download_latest_payslip()
        
        if file:
            print(f"\n✅ Success! Downloaded: {file}")
        else:
            print(f"\n❌ Download failed - check logs")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
