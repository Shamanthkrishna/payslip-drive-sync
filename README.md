# Payslip Drive Sync

Automated monthly pay slip downloader from Paybooks portal with Google Drive integration and email notifications.

**🎯 For Employees**: Want to get started quickly? See **[QUICKSTART.md](QUICKSTART.md)** for a 15-minute setup guide!

---

## 📋 Features

- ✅ Automated login to Paybooks portal
- ✅ Downloads previous month's pay slip
- ✅ Organizes files in Google Drive: `Pay Slips/YYYY/Month_Name/`
- ✅ Prevents duplicate uploads
- ✅ Email notifications (success/error/skip)
- ✅ Comprehensive logging
- ✅ Scheduled monthly execution via Windows Task Scheduler
- ✅ **Reusable for any employee** - Just update credentials!

## 👥 For Other Employees

This tool is designed to be easily used by anyone in the organization:

1. **Clone this repository** to your computer
2. **Update `.env` file** with YOUR credentials (Login ID, Password, Domain)
3. **Setup YOUR Google Drive** (follow setup guide)
4. **Configure YOUR email** for notifications
5. **Run and schedule** - Done!

**Your credentials are private** - Never commit the `.env` file!

## 🏗️ Project Structure

```
payslip-drive-sync/
├── main.py                  # Main orchestrator
├── paybooks_scraper.py      # Selenium automation for Paybooks
├── drive_uploader.py        # Google Drive API integration
├── email_notifier.py        # Email notification handler
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── POV.md                  # Project requirements
├── README.md               # This file
├── downloads/              # Temporary download folder (auto-created)
└── logs/                   # Execution logs (auto-created)
```

## 🚀 Quick Start (For Employees)

### Prerequisites
- Windows PC with Python 3.8+ installed ([Download Python](https://www.python.org/downloads/))
- Google Chrome browser installed
- Active Paybooks account
- Personal Gmail account (for Google Drive)

### Step 1: Clone Repository

```powershell
# Clone to your preferred location
git clone https://github.com/Shamanthkrishna/payslip-drive-sync.git
cd payslip-drive-sync

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

2. Edit `.env` with your credentials:
```env
# Paybooks Credentials (replace with YOUR credentials)
PAYBOOKS_LOGIN_ID=your_employee_id
PAYBOOKS_PASSWORD=your_paybooks_password
PAYBOOKS_DOMAIN=your_company_domain
PAYBOOKS_URL=https://ess.paybooks.in/

# Google Drive Settings
GOOGLE_DRIVE_ROOT_FOLDER=Pay Slips

# Email Notification Settings (use YOUR Gmail)
EMAIL_SENDER=your_personal_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECIPIENT=your_work_email@company.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Download Settings
DOWNLOAD_FOLDER=downloads

# Logging
LOG_LEVEL=INFO
```

### Step 3: Setup Google Drive API

#### 3.1 Enable Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to **APIs & Services** → **Library**
4. Search for "Google Drive API" and click **Enable**

#### 3.2 Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure **OAuth consent screen**:
   - User Type: **External**
   - App name: `Payslip Drive Sync`
   - User support email: Your email
   - Developer contact: Your email
   - Add scope: `../auth/drive.file`
   - Add test user: Your Google account email
4. Return to **Create OAuth client ID**:
   - Application type: **Desktop app**
   - Name: `Payslip Automation`
5. Click **Create** and **Download JSON**
6. Save the downloaded file as `credentials.json` in the project root

#### 3.3 First-Time Authentication

Run the script once to authenticate:

```powershell
python main.py
```

- A browser window will open
- Sign in with your Google account
- Grant permissions to access Google Drive
- A `token.json` file will be created (used for future runs)

### Step 4: Setup Email Notifications (Gmail)

#### 4.1 Enable 2-Step Verification
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**

#### 4.2 Create App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select app: **Mail**
3. Select device: **Windows Computer**
4. Click **Generate**
5. Copy the 16-character password
6. Add to `.env` as `EMAIL_PASSWORD`

### Step 5: Test the Setup

```powershell
# Test email configuration
python email_notifier.py

# Test full automation
python main.py
```

## 📅 Schedule Monthly Execution

### Using Windows Task Scheduler

#### Method 1: PowerShell Script (Recommended)

1. Create a batch file `run_payslip_automation.bat` in the project folder:

```batch
@echo off
cd /d "%~dp0"
python main.py >> logs\scheduler.log 2>&1
```

*Note: `%~dp0` automatically uses the batch file's directory*

2. Create the scheduled task:

```powershell
# Open Task Scheduler GUI
taskschd.msc

# Or use PowerShell to create task (update the path to YOUR project location):
$projectPath = "C:\path\to\your\payslip-drive-sync"  # UPDATE THIS
$action = New-ScheduledTaskAction -Execute "$projectPath\run_payslip_automation.bat"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00AM -WeeksInterval 4
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U

Register-ScheduledTask -TaskName "Payslip Drive Sync" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Monthly pay slip download and upload automation"
```

#### Method 2: Manual Task Scheduler Setup

1. Open **Task Scheduler** (`taskschd.msc`)
2. Click **Create Basic Task**
3. Name: `Payslip Drive Sync`
4. Trigger: **Monthly** → Select day (e.g., 5th) → Select months: **All**
5. Action: **Start a program**
   - Program: Full path to batch file (e.g., `C:\Users\YourName\payslip-drive-sync\run_payslip_automation.bat`)
   - Leave Arguments empty
   - Leave Start in empty (batch file handles it)
6. Finish and test by right-clicking → **Run**

## 🧪 Testing & Troubleshooting

### Test Individual Components

```powershell
# Test Paybooks scraper
python paybooks_scraper.py

# Test Google Drive uploader
python drive_uploader.py

# Test email notifications
python email_notifier.py

# Test full workflow
python main.py
```

### Common Issues

#### Issue: Selenium WebDriver not found
**Solution**: The script auto-downloads ChromeDriver. Ensure Chrome browser is installed.

#### Issue: Google Drive authentication fails
**Solution**: 
1. Delete `token.json`
2. Run `python main.py` again
3. Complete OAuth flow in browser

#### Issue: Email not sending
**Solution**: 
1. Verify Gmail App Password is correct (16 characters, no spaces)
2. Check 2-Step Verification is enabled
3. Test with `python email_notifier.py`

#### Issue: Paybooks button not found
**Solution**: 
1. Run with `HEADLESS_MODE = False` in `config.py` to see browser
2. Update button selectors in [paybooks_scraper.py](paybooks_scraper.py) based on actual page structure

### Logs

Check logs for detailed execution information:
```powershell
# View latest log
Get-Content logs\payslip_automation_*.log -Tail 50

# View all logs
Get-ChildItem logs\
```

## 🔒 Security Best Practices

⚠️ **IMPORTANT FOR ALL USERS**:

1. **NEVER share your `.env` file** - Contains YOUR personal credentials
2. **NEVER commit `.env` to Git** - Already in `.gitignore`, but double-check
3. **Use YOUR OWN Google account** - Don't share Google Drive credentials
4. **Keep `credentials.json` and `token.json` private** - These are YOUR authentication files
5. **Use Gmail App Passwords** - Never use your actual Gmail password
6. **Each employee must do their own setup** - This tool is for individual use
7. **Regularly rotate credentials** - Update passwords periodically
8. **Restricted API scope** - Only uses `drive.file` (not full drive access)

**Your credentials = Your privacy. Keep them safe!**

## 🛠️ Customization

### Change Folder Structure

Edit [drive_uploader.py](drive_uploader.py#L75-L90):
```python
def get_folder_structure(self, previous_month_date):
    # Example: Pay Slips/YYYY-MM/
    year_month = previous_month_date.strftime('%Y-%m')
    folder_id = self.find_or_create_folder(year_month, root_folder_id)
    return folder_id
```

### Change Schedule

Modify Task Scheduler trigger or use different intervals (weekly, daily during 1st week, etc.)

### Add More Portals

Create additional scraper classes following the pattern in [paybooks_scraper.py](paybooks_scraper.py)

## 📊 Execution Flow

```
┌─────────────────────────────────────────┐
│  Windows Task Scheduler Triggers       │
│  (Monthly on specified date/time)      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  main.py - Orchestrator                 │
│  • Validates config                     │
│  • Sets up logging                      │
│  • Handles errors                       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  paybooks_scraper.py                    │
│  • Login to Paybooks                    │
│  • Navigate to payslip page             │
│  • Download PDF to local folder         │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  drive_uploader.py                      │
│  • Authenticate with Google Drive       │
│  • Create folder structure              │
│  • Check for duplicates                 │
│  • Upload file                          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  email_notifier.py                      │
│  • Send success/error notification      │
└─────────────────────────────────────────┘
```

## 📝 License

Personal use only.

## 🤝 Support

For issues or questions, check the logs in `logs/` folder or review the error email notifications.

---

**Repository**: [github.com/Shamanthkrishna/payslip-drive-sync](https://github.com/Shamanthkrishna/payslip-drive-sync)  
**Quick Start**: [QUICKSTART.md](QUICKSTART.md) | **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)  
**Description**: Python automation tool for downloading pay slips from web portals and syncing to Google Drive with scheduled execution
