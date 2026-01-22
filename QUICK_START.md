# Quick Distribution Guide

## For You (The Developer)

### Step 1: Build the Installer (One-time)

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the standalone installer
python build_installer.py
```

**Time**: 2-3 minutes  
**Output**: `PayslipDriveSync_Distribution/PayslipDriveSyncSetup.exe` (50-80 MB)

### Step 2: Package for Distribution

```bash
# Zip the distribution folder
Compress-Archive -Path PayslipDriveSync_Distribution -DestinationPath PayslipDriveSync.zip
```

### Step 3: Send to Colleagues

Send `PayslipDriveSync.zip` via:
- Email attachment
- Teams/Slack
- Shared network drive
- Cloud storage (Google Drive, OneDrive)

---

## For Your Colleagues (The Users)

### Installation Steps (First Time Only)

1. **Extract the ZIP file**
   - Right-click → Extract All

2. **Run the Installer**
   - Double-click `PayslipDriveSyncSetup.exe`
   - If Windows shows security warning:
     - Click "More info"
     - Click "Run anyway"

3. **Follow the Setup Wizard**
   
   **Screen 1: Installation Location**
   - Default: `C:\Program Files\PayslipDriveSync`
   - Can change if needed
   - Click "Next"
   
   **Screen 2: Paybooks Credentials**
   - Enter username/email
   - Enter password
   - Enter company domain (e.g., "tismo")
   - Click "Next"
   
   **Screen 3: Installation Progress**
   - Wait 30-60 seconds
   - Installing files, setting up automation
   
   **Screen 4: Google Drive Setup**
   - Browser will open automatically
   - Sign in to your Google account
   - Click "Allow" to grant Drive access
   
   **Screen 5: Complete!**
   - Click "Finish"

### What Happens Next

**Automatic Monthly Sync:**
- **Primary**: Runs every **6th of the month at 9:00 AM**
- **Retry Logic**: If PC is off or you're not logged in:
  - Retries at 11 AM, 1 PM, and 3 PM on the 6th
  - Retries daily at 9 AM for the next 7 days (7th-12th)
  - Completely automatic recovery
- **Next Month**: Automatically resumes on the 6th regardless of previous failures
- **Silent Operation**: Runs completely in background (no windows, no console)

**Smart Retry Examples:**
- PC off on 6th at 9 AM? → Tries at 11 AM, 1 PM, 3 PM
- Not logged in all day on 6th? → Tries 7th at 9 AM, 8th at 9 AM, etc.
- On vacation 6th-10th? → Tries 11th at 9 AM, or 12th at 9 AM
- All retries fail? → No problem! Next month it tries again on the 6th

**Background Operation:**
- No console windows pop up
- No interruption to your work
- Check logs anytime to see what happened

### Manual Sync Anytime

You can also run the sync manually:

**Method 1: Background Mode (Recommended)**
- Click Start
- Search "Payslip Drive Sync (Background)"
- Click the shortcut
- Runs silently, check logs for results

**Method 2: Visible Console (Troubleshooting)**
- Click Start
- Search "Payslip Drive Sync (Show Log)"
- Click the shortcut
- Shows console output for debugging

### Check Logs

View sync history and any errors:
- Open: `C:\Program Files\PayslipDriveSync\logs\`
- Files named: `payslip_YYYYMMDD.log`

### Update Scheduled Time

If you want to change when it runs:

1. Open Task Scheduler (search in Start Menu)
2. Find "PayslipDriveSync_Monthly"
3. Right-click → Properties
4. Triggers tab → Edit
5. Change day/time as needed

---

## Common Questions

### Q: Does it need to run every month?
**A:** Yes, new payslips are available monthly. The tool runs on the 6th to ensure the new month's payslip is available.

### Q: What if I forget to turn on my PC on the 6th?
**A:** No problem! The system has smart retry logic:
- Tries 4 times on the 6th (9 AM, 11 AM, 1 PM, 3 PM)
- Tries daily for next 6 days (7th-12th at 9 AM)
- Next month it automatically tries again on the 6th
- You never "miss" a month permanently

### Q: What if I'm on vacation for the whole week?
**A:** The tool will try every day while you're gone. When you return and log in, it will run on the next scheduled time. Or you can run it manually anytime. Next month it resumes normal schedule.

### Q: Will I see any windows or popups during automatic runs?
**A:** No! Runs completely in background using `pythonw` (windowless Python). Silent operation, no interruptions.

### Q: Where are my payslips saved?
**A:** Google Drive, in folder: `Pay Slips/YYYY/Month/`

### Q: Is my password safe?
**A:** Yes, stored in encrypted `.env` file on your PC only. Never transmitted anywhere except directly to Paybooks.

### Q: Can I run it more than once a month?
**A:** Yes! Run manually anytime. It's smart - won't download duplicates.

### Q: How do I uninstall?
**A:** 
1. Delete folder: `C:\Program Files\PayslipDriveSync`
2. Delete scheduled task: Open Task Scheduler → Delete "PayslipDriveSync_Monthly"
3. Delete Start Menu shortcut

---

## Support

**For installation issues:**
- Check logs in installation folder
- Make sure Chrome browser is installed
- Try running as Administrator

**For sync errors:**
- Check log files
- Verify Paybooks credentials are correct
- Verify Google Drive has space
- Re-run Google Drive authentication: `python setup.py`

**Contact:** [Your Contact Info]
