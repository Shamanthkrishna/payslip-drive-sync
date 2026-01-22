# Payslip Drive Sync - Installation Guide

## Quick Install

1. **Run PayslipDriveSyncSetup.exe**
   - Double-click the executable
   - Windows may show a security warning - click "More info" then "Run anyway"

2. **Follow the setup wizard**
   - Choose installation location (default: C:\Program Files\PayslipDriveSync)
   - Enter your Paybooks credentials
   - Authenticate with Google Drive (browser will open)
   - Setup will automatically schedule monthly runs

3. **Done!**
   - The tool will run automatically on the 6th of every month
   - You can also run it manually anytime from Start Menu

## What Gets Installed

- Payslip sync application
- All required dependencies (Chrome driver, Python libraries)
- Scheduled task (runs 6th of every month at 9 AM)
- Start Menu shortcut

## Manual Run

After installation, you can run the sync anytime:
- Start Menu -> "Payslip Drive Sync"
- Or go to installation folder and run sync_payslips.exe

## Uninstall

Run the uninstaller from the installation folder or Add/Remove Programs.

## Support

For issues, check the logs in: %APPDATA%\PayslipDriveSync\logs\
