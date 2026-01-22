
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
