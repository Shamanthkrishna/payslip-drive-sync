# How to Use the Payslip Automation Tool

## Fully Automatic - No Manual Steps Required! 🎉

This tool automatically downloads your payslips from Paybooks and uploads them to Google Drive with **ZERO manual intervention**.

## Quick Start

### First-Time Setup (One-time only)
```bash
python setup.py
```
Follow the prompts to:
- Enter your Paybooks credentials (stored securely in `.env`)
- Authenticate with Google Drive (opens browser once)

### Monthly Sync (Run whenever you want)
```bash
python sync_payslips.py
```

That's it! The tool will:
1. **Automatically extract** the Paybooks token (no manual copy-paste!)
2. **Scan your Google Drive** for existing payslips
3. **Download only missing payslips** from Paybooks
4. **Upload new payslips** to Google Drive in organized folders:
   ```
   Pay Slips/
   ├── 2024/
   │   ├── December/
   │   │   └── December_2024_PaySlip.pdf
   │   └── November/
   │       └── November_2024_PaySlip.pdf
   └── 2025/
       ├── January/
       ├── February/
       └── ...
   ```

## Features

✅ **100% Automatic** - No manual token extraction, no manual steps
✅ **Smart Sync** - Scans Drive and downloads only missing payslips
✅ **Fast** - API-based downloads (~1 second per payslip)
✅ **Organized** - Creates proper folder structure in Google Drive
✅ **Safe** - Never duplicates files, skips existing payslips
✅ **Daily Logs** - All runs on same day append to single log file

## Scheduling

### Windows Task Scheduler (Run Monthly)
```powershell
# Create scheduled task to run on the 5th of every month
schtasks /create /tn "Payslip Sync" /tr "python 'd:\Shamanth_Krishna\Work\Personal\Pay Slips\sync_payslips.py'" /sc monthly /d 5 /st 09:00
```

### Manual Run Anytime
```bash
python sync_payslips.py
```

## What Happens Behind the Scenes

1. **Token Extraction** (Automatic)
   - Opens Paybooks in headless Chrome
   - Logs in with your credentials
   - Extracts authentication token from browser session
   - Saves token for 24 hours (reused on subsequent runs)

2. **Smart Download**
   - Scans your Google Drive folders
   - Identifies missing months
   - Downloads only what's needed via fast API

3. **Organized Upload**
   - Creates year/month folder structure
   - Uploads with proper naming (Month_YYYY_PaySlip.pdf)
   - Skips files that already exist

## Troubleshooting

### Token Expired
If you see "Token expired", the tool will automatically extract a fresh token. No action needed!

### Google Drive Authentication
If Drive authentication expires, run:
```bash
python setup.py
```
And re-authenticate when browser opens.

### View Logs
Daily logs are stored in `logs/payslip_YYYYMMDD.log`
```bash
# View today's log
Get-Content logs/payslip_20260121.log -Tail 50
```

## Files You Can Ignore

- `.paybooks_token` - Auto-generated token (24-hour validity)
- `logs/` - Daily log files
- `token.json` - Google Drive authentication
- `.env` - Your credentials (keep secret!)

## Project Structure

```
Pay Slips/
├── sync_payslips.py       # Main script - run this!
├── setup.py               # One-time setup
├── src/                   # Core modules
│   ├── paybooks_api.py   # Automatic token extraction + API
│   ├── drive_uploader.py # Google Drive integration
│   ├── email_notifier.py # Email notifications
│   └── config.py          # Configuration loader
├── docs/                  # Documentation
└── logs/                  # Daily log files
```

## Support

For issues or questions, check the logs first:
```bash
Get-Content logs/payslip_$(Get-Date -Format yyyyMMdd).log
```

Enjoy your fully automated payslip downloads! 🚀
