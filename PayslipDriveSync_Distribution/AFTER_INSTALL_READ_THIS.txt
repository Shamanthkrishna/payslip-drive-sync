# For Your Colleague - After Installation

## What You Just Installed

The setup wizard has:
- ✅ Installed the application to `C:\Program Files\PayslipDriveSync`
- ✅ Saved your Paybooks credentials securely
- ✅ Set up automatic monthly schedule (6th of month with retries)
- ✅ Created Start Menu shortcuts

## ⚠️ ONE MORE STEP - Google Drive Setup

Before the automation works, you need to connect to Google Drive (one-time only):

### Option 1: Use Shared credentials.json (Easier - Recommended)

**If your colleague provides `credentials.json` file:**

1. **Copy the file**
   - They'll send you a file named `credentials.json`
   - Save it to: `C:\Program Files\PayslipDriveSync\credentials.json`

2. **Run the setup**
   - Open Command Prompt or PowerShell
   - Run these commands:
   ```powershell
   cd "C:\Program Files\PayslipDriveSync"
   python setup.py
   ```

3. **Authenticate**
   - Browser will open automatically
   - Sign in with YOUR Google account (where you want payslips saved)
   - Click "Allow" when asked for Google Drive access
   - Close browser when it says "Authentication successful"

4. **Done!**
   - Setup creates `token.json` (your personal Google Drive access)
   - Now automatic syncs will work!

### Option 2: Create Your Own Google Cloud Project (For Privacy)

**If you want your own isolated setup:**

1. **Create Google Cloud Project** (~5 minutes)
   - Go to: https://console.cloud.google.com/
   - Click "New Project"
   - Name it: "Payslip Sync"
   - Click "Create"

2. **Enable Google Drive API**
   - Search for "Google Drive API"
   - Click "Enable"

3. **Create OAuth Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth Client ID"
   
   **If prompted to configure consent screen:**
   - Choose "External"
   - App name: "Payslip Sync"
   - Your email for support
   - Add scope: `.../auth/drive.file`
   - Add your email as test user
   - Save
   
   **Create OAuth client:**
   - Application type: "Desktop app"
   - Name: "Payslip Sync"
   - Click "Create"
   - Download JSON file

4. **Save credentials**
   - Rename downloaded file to `credentials.json`
   - Copy to: `C:\Program Files\PayslipDriveSync\credentials.json`

5. **Run setup** (same as Option 1 step 2-4 above)

## Test It Works

After completing Google Drive setup:

### Manual Test Run

1. **Run manually first** (to verify everything works):
   - Start Menu → "Payslip Drive Sync (Show Log)"
   - Watch it run (should download and upload payslips)
   - Check your Google Drive → Should see "Pay Slips" folder

2. **Check the results**:
   - Google Drive: `Pay Slips/2025/January/January_2025_PaySlip.pdf` (etc.)
   - Logs: `C:\Program Files\PayslipDriveSync\logs\payslip_20260122.log`

### Verify Automatic Schedule

1. **Open Task Scheduler**:
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Find the task**:
   - Look for "PayslipDriveSync_Monthly"
   - Check triggers: Should show multiple triggers for 6th-12th

3. **Test it** (optional):
   - Right-click the task → "Run"
   - Check logs to confirm it ran

## What Happens Next

### Automatic Monthly Sync

**Every month on the 6th:**
- Runs at 9:00 AM (completely silent, no windows)
- If PC is off or you're not logged in:
  - Retries at 11 AM, 1 PM, 3 PM on the 6th
  - Retries daily at 9 AM for next 6 days (7th-12th)
- Downloads new month's payslip
- Uploads to your Google Drive
- Logs everything to file

**You do nothing!** Just keep PC on occasionally and logged in.

### Manual Runs Anytime

Start Menu → "Payslip Drive Sync (Background)" - Silent mode  
Start Menu → "Payslip Drive Sync (Show Log)" - See what it's doing

## Troubleshooting

### "credentials.json not found"
- Make sure file is in: `C:\Program Files\PayslipDriveSync\credentials.json`
- File must be named exactly `credentials.json` (no extra .txt or anything)

### "token.json not found" 
- You haven't completed Google Drive setup yet
- Run: `python setup.py` from installation folder

### Browser doesn't open during setup
- Manually open: http://localhost:8080/ (if local server starts)
- Or check if default browser is set correctly

### No payslips appear in Drive
- Check logs: `C:\Program Files\PayslipDriveSync\logs\`
- Verify Paybooks credentials are correct
- Try manual run with visible log to see errors

### Task doesn't run automatically
- Check Task Scheduler - is task enabled?
- Check "Last Run Result" (should be 0x0 for success)
- Make sure PC is on and you're logged in at scheduled time

## Need Help?

**Check logs first:**
```
C:\Program Files\PayslipDriveSync\logs\payslip_YYYYMMDD.log
```

**Common log locations:**
- Application logs: Installation folder `\logs\`
- Task Scheduler history: Task Scheduler → View → Show Task History

**Contact:** [Your contact info - Teams, Email, etc.]

---

## Quick Summary

1. ✅ Installed? Yes (you just did this)
2. ⏳ Google Drive setup? **← DO THIS NOW** (5 minutes)
3. ✅ Test manual run? Verify it works
4. ✅ Done! Automatic forever

**Next action:** Get `credentials.json` and run `python setup.py` 🚀
