@echo off
cd /d "%~dp0"
echo ========================================
echo    Payslip Drive Sync
echo ========================================
echo.
python sync_payslips.py
echo.
echo ========================================
echo    Press any key to close...
echo ========================================
pause >nul
