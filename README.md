# Payslip Drive Sync

Automatically download payslips from Paybooks and upload to Google Drive with zero manual intervention.

## Quick Start

```bash
# 1. First-time setup (one command)
python setup.py

# 2. Sync payslips (run monthly or anytime)
python sync_payslips.py
```

That's it! The tool will:
- **First run**: Download ALL missing payslips from your employment start date
- **Subsequent runs**: Check your Drive and download only missing months
- **Auto-upload**: Organize in Drive as `Pay Slips/YYYY/MonthName/payslip_MMYY.pdf`
- **Local backup**: Keep copies in `local_payslips/` folder

## Features

✅ **Zero Manual Steps**: Automatic token extraction from browser  
✅ **Smart Sync**: Scans Drive, downloads only missing payslips  
✅ **Bulk Initial Download**: Gets all historical payslips on first run  
✅ **Fast API**: 10x faster than web scraping (~1 sec per payslip)  
✅ **Auto-Organization**: Year/Month folder structure on Drive  
✅ **Duplicate Prevention**: Never downloads the same payslip twice  
✅ **Token Caching**: Authentication token valid for 24 hours  

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser
- Paybooks account
- Google account

### Setup

Run the automated setup script:

```bash
python setup.py
```

This will:
1. Check Python version
2. Install required dependencies
3. Collect your Paybooks credentials
4. Guide you through Google Drive setup
5. Create necessary folders

## Usage

### Monthly Sync (Recommended)

```bash
python sync_payslips.py
```

This checks your Drive and downloads only missing payslips.

### Manual Configuration (Advanced)

If you prefer manual setup, create `.env` file:

```env
PAYBOOKS_USERNAME=your_username
PAYBOOKS_PASSWORD=your_password
PAYBOOKS_DOMAIN_ID=your_company_domain
```

## Team Deployment

Each employee sets up independently:

1. **Create Google Cloud Project** (one-time, ~5 minutes)
   - Follow the detailed guide below
   - Creates your own `credentials.json`
   - No sharing needed - avoids API quota issues

2. **Run Setup Script**:
   ```bash
   python setup.py
   ```
   - Enters their own Paybooks username/password
   - Authenticates with their own Google account
   - Gets their own `token.json` for Drive access

3. **Run Sync**:
   ```bash
   python sync_payslips.py
   ```

### Setting Up Your Google Cloud Project (Step-by-Step)

Each employee creates their own project to avoid quota limits:

#### Step 1: Create Google Cloud Project (2 minutes)

1. **Go to Google Cloud Console**: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. **Sign in** with your personal Google account (the one you want to use for Drive)
3. **Click** the project dropdown at the top (next to "Google Cloud")
4. **Click** "NEW PROJECT" button (top right of dialog)
5. **Enter details**:
   - Project name: `Payslip Sync` (or any name you prefer)
   - Organization: Leave as "No organization" (unless you have one)
   - Location: Leave as default
6. **Click** "CREATE"
7. **Wait** ~30 seconds for project creation
8. **Select** your new project from the dropdown

#### Step 2: Enable Google Drive API (1 minute)

1. **In the search bar** at top, type: `Google Drive API`
2. **Click** on "Google Drive API" from results
3. **Click** the blue "ENABLE" button
4. **Wait** for confirmation (should be instant)

#### Step 3: Create OAuth Credentials (2 minutes)

1. **Click** "CREATE CREDENTIALS" button (top right)
2. **Or** go to: "APIs & Services" → "Credentials" (left menu)
3. **Click** "+ CREATE CREDENTIALS" → "OAuth client ID"
4. **If prompted** "Configure Consent Screen":
   - Click "CONFIGURE CONSENT SCREEN"
   - Select **External** (unless you have a workspace)
   - Click "CREATE"
   - Fill in:
     - App name: `Payslip Sync`
     - User support email: Your email
     - Developer contact: Your email
   - Click "SAVE AND CONTINUE"
   - **Scopes**: Click "ADD OR REMOVE SCOPES"
     - Search for `drive.file`
     - Check `.../auth/drive.file` ("See, edit, create, and delete only the files created with this app")
     - Click "UPDATE" → "SAVE AND CONTINUE"
   - **Test users**: Click "+ ADD USERS"
     - Add your email address
     - Click "ADD" → "SAVE AND CONTINUE"
   - **Summary**: Click "BACK TO DASHBOARD"

5. **Now create credentials**:
   - Go to "Credentials" (left menu)
   - Click "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: **Desktop app**
   - Name: `Payslip Sync Desktop`
   - Click "CREATE"

6. **Download credentials**:
   - Click "DOWNLOAD JSON" button
   - **Save as** `credentials.json` in your project folder
   - **Important**: Keep this file - you'll need it for setup

#### Step 4: Verify Setup

You should now have:
- ✅ Google Cloud Project created
- ✅ Google Drive API enabled
- ✅ OAuth consent screen configured
- ✅ `credentials.json` file downloaded

**Next**: Run `python setup.py` to complete the installation!

## How It Works

1. **Token Extraction**: 
   - Opens Chrome to Paybooks login page
   - Intercepts the API authentication token automatically
   - Caches token for 24 hours (`.paybooks_token`)

2. **Smart Sync**:
   - Scans your Google Drive folder structure
   - Identifies which months are already downloaded
   - Calculates missing months since employment start
   - Downloads only missing payslips via API

3. **Upload**:
   - Creates folder structure: `Pay Slips/YYYY/MonthName/`
   - Uploads as `payslip_MMYY.pdf`
   - Keeps local backup in `local_payslips/`

## Troubleshooting

### Chrome doesn't open / Token extraction fails

**Solution**: Make sure Chrome is installed and not currently running. Close all Chrome windows and try again.

### "Token expired" error

**Solution**: Delete `.paybooks_token` file and run again. The tool will extract a fresh token.

### "File already exists" when uploading

**Solution**: This is normal. The tool skips files that already exist on Drive. Your Drive already has that payslip.

### Google Drive authentication fails

**Solution**: 
1. Delete `token.json`
2. Run `python sync_payslips.py` again
3. Complete the Google authentication in the browser
4. Make sure `credentials.json` exists

### Missing payslips aren't downloading

**Solution**: Check the script output to see which months it detected as existing. If Drive folders are named incorrectly, the scan might not find them. Ensure folders follow the pattern: `Pay Slips/YYYY/MonthName/`

## Automation

### Windows Task Scheduler

Run automatically on the 5th of each month:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Payslip Sync"
4. Trigger: Monthly, Day 5
5. Action: Start a program
   - Program: `C:\Path\To\Python\python.exe`
   - Arguments: `sync_payslips.py`
   - Start in: `D:\Shamanth_Krishna\Work\Personal\Pay Slips`

### Linux/Mac (cron)

```bash
# Run on the 5th of each month at 9 AM
0 9 5 * * cd /path/to/payslips && /usr/bin/python3 sync_payslips.py
```

## File Structure

```
Pay Slips/
├── sync_payslips.py        # Main production script (run this)
├── setup.py                # One-time setup wizard
├── paybooks_api.py         # API client with token extraction
├── drive_uploader.py       # Google Drive integration
├── config.py               # Configuration loader
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials (not in Git)
├── credentials.json        # Google OAuth app (shared)
├── token.json              # Your Google Drive token (auto-generated)
├── .paybooks_token         # Cached Paybooks token (auto-generated)
└── local_payslips/         # Local backup folder
```

## Security

- `.env` file contains your credentials - **NEVER commit to Git**
- `token.json` is your personal Google Drive access - **NEVER share**
- `credentials.json` is your Google Cloud app ID - **KEEP PRIVATE** (each person creates their own)
- `.paybooks_token` is auto-generated and expires in 24 hours

All sensitive files are in `.gitignore` by default.

## FAQ

**Q: How many months does it download on first run?**  
A: By default, the last 24 months. You can modify `sync_payslips.py` to change this.

**Q: What if I have gaps in employment?**  
A: The tool tries to download all months but skips those that don't exist on Paybooks. No errors.

**Q: Can I run this on a server?**  
A: Yes, but you need a display/virtual display for Chrome during token extraction. After that, it's headless.

**Q: Does it send notifications?**  
A: Not by default. You can add email notifications by using the `email_notifier.py` module (configure SMTP settings).

**Q: What if Paybooks changes their API?**  
A: The tool uses the official Paybooks API endpoint. If it changes, update the URL in `paybooks_api.py`.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Run with verbose output: `python sync_payslips.py` (check terminal output)
3. Check `.paybooks_token` exists and is recent (<24 hours)
4. Verify `.env` file has correct credentials

## License

MIT License - Free for personal and commercial use.
