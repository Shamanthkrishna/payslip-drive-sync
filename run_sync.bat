@echo off
cd /d "%~dp0"
echo ========================================
echo    Payslip Drive Sync
echo ========================================
echo.
if exist ".venv\Scripts\python.exe" (
	".venv\Scripts\python.exe" sync_payslips.py
) else (
	python sync_payslips.py
)
echo.
echo ========================================
echo    Press any key to close...
echo ========================================
pause >nul
