# Quick Start - Payslip Drive Sync

Get your payslips automatically synced to Google Drive in 4 simple steps.

## ⚡ 4-Step Setup (15 minutes)

### Step 1: Create Google Cloud Project (5 minutes)

**Important**: Each person creates their own project to avoid API quota issues.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click project dropdown → "NEW PROJECT"
3. Name: `Payslip Sync` → CREATE
4. Search for "Google Drive API" → ENABLE
5. Create credentials:
   - "CREATE CREDENTIALS" → "OAuth client ID"
   - Configure consent screen if prompted:
     - External → App name: `Payslip Sync`
     - Scopes: Add `.../auth/drive.file`
     - Test users: Add your email
   - Application type: **Desktop app**
   - DOWNLOAD JSON → Save as `credentials.json`

📖 **Need detailed steps?** See [README.md - Setting Up Google Cloud Project](README.md#setting-up-your-google-cloud-project-step-by-step)

### Step 2: Run Setup Script (5 minutes)

```bash
python setup.py
```

The script will:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Collect your Paybooks credentials
- ✅ Guide you through Google Drive authentication

### Step 3: Complete Google Drive Authentication (2 minutes)

When the browser opens:
1. Sign in with your Google account
2. Click "Allow" to grant Drive access
3. Close the browser window

### Step 4: Sync Your Payslips

```bash
python sync_payslips.py
```

**First run**: Downloads all missing payslips (last 24 months)  
**Future runs**: Downloads only new/missing months

## ✅ That's It!

Your payslips are now on Google Drive at:
```
Pay Slips/
  └── 2024/
      ├── January/
      │   └── payslip_0124.pdf
      ├── February/
      │   └── payslip_0224.pdf
      └── ...
```

Local backups are in the `local_payslips/` folder.

## 🔄 Run Monthly

### Option 1: Manual (Easiest)
Run this command on the 5th of each month:
```bash
python sync_payslips.py
```

### Option 2: Windows Task Scheduler (Automated)
1. Press `Win + R`, type `taskschd.msc`
2. Create Basic Task → Name: "Payslip Sync"
3. Trigger: Monthly, Day 5
4. Action: Start a program
   - Program: `python.exe` (full path, e.g., `C:\Python\python.exe`)
   - Arguments: `sync_payslips.py`
   - Start in: Your project folder path

### Option 3: Linux/Mac (cron)
```bash
# Run on 5th of each month at 9 AM
0 9 5 * * cd /path/to/project && python3 sync_payslips.py
```

## ❓ Troubleshooting

**Chrome doesn't open?**
- Make sure Chrome is installed
- Close all Chrome windows and try again

**"Token expired" error?**
- Delete `.paybooks_token` file
- Run `python sync_payslips.py` again

**Google Drive auth fails?**
- Delete `token.json`
- Run the sync again
- Complete the Google authentication in browser

**Missing payslips not downloading?**
- Check the console output for which months were detected
- Ensure Drive folders follow: `Pay Slips/YYYY/MonthName/`

See [README.md](README.md) for detailed documentation.

## 📁 What Each File Does

- `sync_payslips.py` - Main script (run this monthly)
- `setup.py` - First-time setup wizard
- `paybooks_api.py` - Handles Paybooks API
- `drive_uploader.py` - Uploads to Google Drive
- `.env` - Your credentials (never share!)
- `credentials.json` - Google app ID (shared with team)
- `token.json` - Your Google Drive access (auto-generated)

## 🔒 Security

Your `.env` file contains sensitive credentials - it's automatically excluded from Git. Never share it with anyone!
4. Name: `Payslip Automation`
5. Trigger: Monthly, Day 5, All months
6. Action: Start a program
7. Browse to your `run_payslip_automation.bat`
8. Finish!

### Option B: Manual Run (No Schedule)

Just run `python main.py` whenever you want to download your pay slip.

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| Login fails | Check credentials in `.env` file |
| Google Drive auth fails | Delete `token.json`, run again |
| Email not sending | Verify Gmail App Password (16 chars, no spaces) |
| Browser not found | Install Google Chrome |

**Still stuck?** Check `logs/` folder or create a GitHub issue.

## 🎉 You're Done!

Your pay slips will now automatically download to your Google Drive every month.

**Next time**: Just keep your PC on during the scheduled time. That's it!

---

**Need help?** See [README.md](README.md) for detailed documentation or [CONTRIBUTING.md](CONTRIBUTING.md) to report issues.
