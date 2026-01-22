# Building and Distributing Payslip Drive Sync

This guide explains how to create a single-file installer for your colleagues.

## Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

## Build the Installer

Run the build script:
```bash
python build_installer.py
```

This will create:
- `PayslipDriveSync_Distribution/` folder containing:
  - `PayslipDriveSyncSetup.exe` - The installer
  - `README.txt` - Instructions for users

**Build time**: ~2-3 minutes

## Distribute to Colleagues

1. **Zip the distribution folder**:
   ```bash
   Compress-Archive -Path PayslipDriveSync_Distribution -DestinationPath PayslipDriveSync.zip
   ```

2. **Send to colleagues** via email, shared drive, or Teams

3. **They extract and run** `PayslipDriveSyncSetup.exe`

## What the Installer Does

When colleagues run the installer, it will:

### 1. **Installation Wizard** (GUI)
   - Choose installation location (default: `C:\Program Files\PayslipDriveSync`)
   - Enter Paybooks credentials (username, password, domain)
   - All stored securely on their PC

### 2. **Google Drive Setup**
   - Opens browser for Google authentication
   - One-time authorization
   - Creates `token.json` for Drive access

### 3. **Automatic Scheduling**
   - Creates Windows Task Scheduler entry
   - Runs every 6th of the month at 9:00 AM
   - Only runs if PC is on (will run next opportunity if missed)

### 4. **Creates Shortcuts**
   - Start Menu shortcut for manual runs
   - Can run sync anytime, not just on schedule

## User Experience

**First Time**:
1. Double-click `PayslipDriveSyncSetup.exe`
2. Windows may show security warning → "More info" → "Run anyway"
3. Follow wizard (enter credentials, Google auth)
4. Click "Finish"

**Automatic Runs**:
- Every 6th of month at 9 AM (if PC is on)
- Silent background operation
- Logs saved to `%APPDATA%\PayslipDriveSync\logs\`

**Manual Run**:
- Start Menu → "Payslip Drive Sync"
- Or run from installation folder

## Important Notes

### Google Cloud Credentials

Each user needs their own `credentials.json`:
- **Option 1**: You create one project, share `credentials.json` with team
  - Pro: Easy setup for users
  - Con: Shared API quota (500 requests/day)
  
- **Option 2**: Each user creates their own Google Cloud project
  - Pro: Individual quotas, no sharing issues
  - Con: Extra setup step for users

**Recommended**: Option 1 for small teams (<10 people), Option 2 for larger teams.

If using Option 1, include `credentials.json` in the installer:
1. Add to `build_installer.py` in the `datas` section:
   ```python
   datas=[
       ('credentials.json', '.'),  # Add this line
       ('requirements.txt', '.'),
       ...
   ]
   ```

### Scheduling Details

The scheduled task:
- **Trigger**: 6th of every month at 9:00 AM
- **Condition**: Only if computer is on (won't wake PC)
- **Settings**: 
  - Run when user is logged in
  - Start even if on battery
  - Allow running on demand

Users can modify schedule via Task Scheduler:
- Open Task Scheduler (`taskschd.msc`)
- Find "PayslipDriveSync_Monthly"
- Modify triggers/settings as needed

## Troubleshooting

### "Windows protected your PC" warning

This is normal for unsigned executables. Users should:
1. Click "More info"
2. Click "Run anyway"

To avoid this, you'd need to sign the executable (requires code signing certificate, ~$300/year).

### Installation fails

Common causes:
- No admin rights: Run as administrator
- Antivirus blocking: Add to antivirus exceptions
- Python not installed: Installer bundles Python, should work standalone

### Scheduled task not running

Check Task Scheduler:
1. Open Task Scheduler
2. Find "PayslipDriveSync_Monthly"
3. Check "Last Run Result" (should be 0x0 for success)
4. Check "Last Run Time"

## Testing the Installer

Before distributing, test on a clean Windows PC:

1. Build the installer
2. Copy to test PC (without Python or dependencies)
3. Run installer
4. Verify:
   - Files copied to Program Files
   - .env created with credentials
   - Scheduled task appears in Task Scheduler
   - Start Menu shortcut created
   - Manual run works

## File Size

Expected installer size: ~50-80 MB
- Includes Python interpreter
- All dependencies (Selenium, Google libraries)
- Chrome driver

## Updates

To distribute updates:
1. Update version in `src/__init__.py`
2. Rebuild installer: `python build_installer.py`
3. Distribute new exe
4. Users run to update (overwrites old files, keeps credentials)

## Advanced: Silent Installation

For IT departments deploying to many machines:

```powershell
# Silent install with pre-configured credentials
.\PayslipDriveSyncSetup.exe /S /USERNAME="user@company.com" /PASSWORD="pass" /DOMAIN="company"
```

(Note: This requires adding command-line argument parsing to installer.py)
