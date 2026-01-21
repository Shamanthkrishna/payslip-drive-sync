"""
One-Click Setup for Payslip Sync Tool

This script sets up everything needed to run the payslip automation.
Run this ONCE when setting up for the first time.
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_step(number, text):
    """Print step number"""
    print(f"\n[{number}/5] {text}")
    print("-"*70)


def check_python():
    """Check Python version"""
    print_step(1, "Checking Python installation...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"\u274c Python 3.8+ required. You have Python {version.major}.{version.minor}")
        sys.exit(1)
    
    print(f"\u2705 Python {version.major}.{version.minor}.{version.micro} detected")


def install_dependencies():
    """Install required packages"""
    print_step(2, "Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("\u2705 All dependencies installed")
    except subprocess.CalledProcessError:
        print("\u274c Failed to install dependencies")
        sys.exit(1)


def setup_credentials():
    """Setup credentials"""
    print_step(3, "Setting up Paybooks credentials...")
    
    env_file = Path(".env")
    
    if env_file.exists():
        response = input("\n.env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("\u2713 Using existing .env file")
            return
    
    print("\nPlease enter your Paybooks credentials:")
    print("(These will be saved securely in .env file)")
    
    login_id = input("\nLogin ID (Employee ID): ").strip()
    password = input("Password: ").strip()
    domain = input("Domain (usually your company name): ").strip()
    
    env_content = f"""# Paybooks Credentials
PAYBOOKS_URL=https://apps.paybooks.in/
PAYBOOKS_LOGIN_ID={login_id}
PAYBOOKS_PASSWORD={password}
PAYBOOKS_DOMAIN={domain}

# Email Notifications (Optional - leave empty to disable)
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=

# Download Settings
DOWNLOAD_FOLDER=downloads

# Logging
LOG_LEVEL=INFO
"""
    
    env_file.write_text(env_content)
    print("\u2705 Credentials saved to .env")


def setup_google_drive():
    """Setup Google Drive"""
    print_step(4, "Setting up Google Drive...")
    
    credentials_file = Path("credentials.json")
    
    if not credentials_file.exists():
        print("\n⚠️  credentials.json NOT FOUND")
        print("\nYou need to create your own Google Cloud project:")
        print("\n📋 Step-by-Step Guide:")
        print("\n1. Go to: https://console.cloud.google.com/")
        print("2. Click project dropdown → 'NEW PROJECT'")
        print("3. Name: 'Payslip Sync' → CREATE")
        print("4. Search for 'Google Drive API' → ENABLE")
        print("5. Create credentials:")
        print("   - 'CREATE CREDENTIALS' → 'OAuth client ID'")
        print("   - Configure consent screen if prompted:")
        print("     • External → App name: 'Payslip Sync'")
        print("     • Scopes: Add '.../auth/drive.file'")
        print("     • Test users: Add your email")
        print("   - Application type: Desktop app")
        print("   - DOWNLOAD JSON → Save as 'credentials.json'")
        print("6. Place credentials.json in this folder")
        print("\n📖 Detailed guide: See README.md (Team Deployment section)")
        print("\n⚠️  Each person creates their own project to avoid quota issues.")
        print("\nPress Enter after you've placed credentials.json here...")
        input()
        
        if not credentials_file.exists():
            print("\u274c credentials.json still not found. Please add it and run setup again.")
            sys.exit(1)
    
    print("\u2705 Google Drive credentials found")
    print("\n\u26a0\ufe0f  Note: You'll authenticate with Google on first run")


def create_folders():
    """Create necessary folders"""
    print_step(5, "Creating folders...")
    
    folders = ['downloads', 'logs']
    
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
    
    print(f"\u2705 Created folders: {', '.join(folders)}")


def print_next_steps():
    """Print what to do next"""
    print_header("SETUP COMPLETE!")
    
    print("Next steps:")
    print("\n1. Run the sync tool:")
    print("   python sync_payslips.py")
    print("\n2. On first run:")
    print("   - A browser will open for Google Drive authentication")
    print("   - Click 'Allow' to grant access")
    print("   - The tool will download ALL available payslips")
    print("\n3. Schedule monthly sync (optional):")
    print("   - Windows: Use Task Scheduler")
    print("   - Run: python sync_payslips.py")
    print("   - Schedule: Monthly on 5th of each month")
    
    print("\n" + "="*70)
    print("\n\u2705 Ready to go! Run: python sync_payslips.py\n")


def main():
    """Main setup flow"""
    print_header("PAYSLIP SYNC TOOL - ONE-CLICK SETUP")
    
    print("This will set up everything needed to run payslip automation.")
    print("The setup will:")
    print("  - Check Python installation")
    print("  - Install required packages")
    print("  - Configure Paybooks credentials")
    print("  - Setup Google Drive connection")
    print("  - Create necessary folders")
    
    response = input("\nContinue? (Y/n): ").strip().lower()
    if response == 'n':
        print("Setup cancelled.")
        sys.exit(0)
    
    try:
        check_python()
        install_dependencies()
        setup_credentials()
        setup_google_drive()
        create_folders()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\u274c Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
