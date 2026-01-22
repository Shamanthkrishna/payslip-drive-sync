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
- Runs **every 6th of the month at 9:00 AM**
- Only if your PC is on and you're logged in
- Completely automatic - no action needed
- Downloads payslips → Uploads to Google Drive

**If Your PC Was Off:**
- Task Scheduler will try next time you log in
- Or you can run manually (see below)

### Manual Sync Anytime

You can also run the sync manually:

**Method 1: Start Menu**
- Click Start
- Search "Payslip Drive Sync"
- Click the shortcut

**Method 2: Installation Folder**
- Go to `C:\Program Files\PayslipDriveSync`
- Double-click `sync_payslips.py`

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
**A:** The task will run the next time you log in, or you can run manually anytime.

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
