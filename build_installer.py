"""
Build script to create standalone Windows installer for Payslip Drive Sync

This creates a single executable that colleagues can run to install everything.
"""

import os
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("=" * 70)
    print("BUILDING PAYSLIP DRIVE SYNC INSTALLER")
    print("=" * 70)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n[ERROR] PyInstaller not found. Installing...")
        subprocess.run(['pip', 'install', 'pyinstaller'], check=True)
    
    # Clean previous builds
    print("\n[1/4] Cleaning previous builds...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")
    
    # Create PyInstaller spec
    print("\n[2/4] Creating installer specification...")
    
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['installer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
        ('.env.example', '.'),
        ('README.md', '.'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'selenium',
        'google.oauth2',
        'google.auth.transport.requests',
        'googleapiclient.discovery',
        'googleapiclient.http',
        'dotenv',
        'dateutil',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PayslipDriveSyncSetup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    coerce_macros=True,
    entitlements_file=None,
    icon=None,
)
"""
    
    with open('PayslipDriveSyncSetup.spec', 'w') as f:
        f.write(spec_content)
    
    print("  Created PayslipDriveSyncSetup.spec")
    
    # Build the executable
    print("\n[3/4] Building executable (this may take 2-3 minutes)...")
    result = subprocess.run(
        ['pyinstaller', '--clean', 'PayslipDriveSyncSetup.spec'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("[ERROR] Build failed!")
        print(result.stderr)
        return False
    
    print("  Build successful!")
    
    # Create distribution folder
    print("\n[4/4] Creating distribution package...")
    dist_folder = Path('PayslipDriveSync_Distribution')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    dist_folder.mkdir()
    
    # Copy executable
    exe_name = 'PayslipDriveSyncSetup.exe'
    shutil.copy(f'dist/{exe_name}', dist_folder / exe_name)
    
    # Create README for distribution
    readme_content = """# Payslip Drive Sync - Installation Guide

## Quick Install

1. **Run PayslipDriveSyncSetup.exe**
   - Double-click the executable
   - Windows may show a security warning - click "More info" then "Run anyway"

2. **Follow the setup wizard**
   - Choose installation location (default: C:\\Program Files\\PayslipDriveSync)
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
- Start Menu → "Payslip Drive Sync"
- Or go to installation folder and run `sync_payslips.exe`

## Uninstall

Run the uninstaller from the installation folder or Add/Remove Programs.

## Support

For issues, check the logs in: `%APPDATA%\\PayslipDriveSync\\logs\\`
"""
    
    with open(dist_folder / 'README.txt', 'w') as f:
        f.write(readme_content)
    
    print(f"\n{'=' * 70}")
    print("BUILD COMPLETE!")
    print(f"{'=' * 70}")
    print(f"\nDistribution package created in: {dist_folder.absolute()}")
    print(f"\nTo distribute:")
    print(f"  1. Zip the '{dist_folder}' folder")
    print(f"  2. Send to colleagues")
    print(f"  3. They just run PayslipDriveSyncSetup.exe")
    print(f"\n{'=' * 70}\n")
    
    return True

if __name__ == '__main__':
    build_executable()
