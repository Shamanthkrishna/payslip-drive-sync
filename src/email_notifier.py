import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .config import Config

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Handles email notifications for errors and important events"""
    
    def __init__(self):
        self.sender = Config.EMAIL_SENDER
        self.password = Config.EMAIL_PASSWORD
        self.recipient = Config.EMAIL_RECIPIENT
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
    
    def send_email(self, subject, body, is_html=False):
        """Send an email notification"""
        
        # Skip if email not configured
        if not all([self.sender, self.password, self.recipient]):
            logger.warning("Email notification skipped - credentials not configured")
            return False
        
        try:
            logger.info(f"Sending email to {self.recipient}...")
            
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender
            message['To'] = self.recipient
            message['Subject'] = subject
            
            # Add body
            mime_type = 'html' if is_html else 'plain'
            message.attach(MIMEText(body, mime_type))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(message)
            
            logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def notify_success(self, month_year, file_name, drive_url=None):
        """Send success notification"""
        subject = f"[SUCCESS] Pay Slip Downloaded - {month_year}"
        
        body = f"""
Pay Slip Automation - Success

The pay slip for {month_year} has been successfully downloaded and uploaded to Google Drive.

File: {file_name}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if drive_url:
            body += f"\nView in Drive: {drive_url}"
        
        body += "\n\n---\nPayslip Drive Sync - Automated System"
        
        return self.send_email(subject, body)
    
    def notify_error(self, error_message, month_year=None):
        """Send error notification"""
        month_info = f" - {month_year}" if month_year else ""
        subject = f"[ERROR] Pay Slip Automation Failed{month_info}"
        
        body = f"""
Pay Slip Automation - Error

The automated pay slip download process has failed.

Error Details:
{error_message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check the logs for more information or run the script manually.

---
Payslip Drive Sync - Automated System
"""
        
        return self.send_email(subject, body)
    
    def notify_already_exists(self, month_year, file_name):
        """Send notification that file already exists"""
        subject = f"ℹ️ Pay Slip Already Exists - {month_year}"
        
        body = f"""
Pay Slip Automation - Skip

The pay slip for {month_year} already exists in Google Drive.

File: {file_name}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

No action was taken.

---
Payslip Drive Sync - Automated System
"""
        
        return self.send_email(subject, body)
    
    def send_test_email(self):
        """Send a test email to verify configuration"""
        subject = "Test - Pay Slip Automation"
        body = f"""
This is a test email from Pay Slip Automation system.

If you received this, your email configuration is working correctly.

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Payslip Drive Sync - Automated System
"""
        
        return self.send_email(subject, body)


if __name__ == "__main__":
    # Test the notifier
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    notifier = EmailNotifier()
    
    print("Sending test email...")
    result = notifier.send_test_email()
    
    if result:
        print("[SUCCESS] Test email sent successfully!")
    else:
        print("[ERROR] Failed to send test email. Check your configuration.")
