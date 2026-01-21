# Quick Setup Guide for Employees

**Time needed**: ~15 minutes | **Technical level**: Beginner-friendly

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Google Chrome installed
- [ ] Paybooks account credentials ready
- [ ] Personal Gmail account for Google Drive

## 🚀 5-Step Setup

### Step 1: Download the Code (2 min)

```powershell
# Open PowerShell and run:
cd C:\Users\YourName\Documents  # or your preferred location
git clone https://github.com/Shamanthkrishna/payslip-drive-sync.git
cd payslip-drive-sync
```

**No Git installed?** [Download Git](https://git-scm.com/download/win) or download ZIP from GitHub.

### Step 2: Install Python Packages (3 min)

```powershell
# Install required packages
pip install -r requirements.txt
```

**Seeing errors?** Make sure Python is installed: `python --version`

### Step 3: Configure YOUR Credentials (3 min)

```powershell
# Create your personal config file
Copy-Item .env.example .env

# Open .env file and update with YOUR information:
notepad .env
```

**What to update in `.env`**:
- `PAYBOOKS_LOGIN_ID` → Your employee ID (e.g., 1234567)
- `PAYBOOKS_PASSWORD` → Your Paybooks password
- `PAYBOOKS_DOMAIN` → Your company domain (e.g., TISMO)
- `EMAIL_SENDER` → Your personal Gmail
- `EMAIL_RECIPIENT` → Your work email (for notifications)

**Don't update `EMAIL_PASSWORD` yet** - we'll do this in Step 4.

### Step 4: Setup Google Drive Access (5 min)

#### A. Enable Google Drive API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Payslip Automation"
3. Enable "Google Drive API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` → Save in project folder

#### B. Setup Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Create "App Password" for "Mail"
4. Copy the 16-character password
5. Add to `.env` as `EMAIL_PASSWORD`

**Detailed instructions**: See [README.md](README.md#step-3-setup-google-drive-api)

### Step 5: Test Everything (2 min)

```powershell
# Run the automation once
python main.py
```

**What happens**:
1. Browser opens (or runs hidden)
2. Logs into Paybooks
3. Downloads previous month's pay slip
4. Asks for Google Drive permission (first time only)
5. Uploads to your Google Drive
6. Sends you an email

**Success?** Check your Google Drive: `Pay Slips/YYYY/Month_Name/`

## 📅 Schedule Monthly Run

### Option A: Simple Task Scheduler (Recommended)

1. Create `run_payslip_automation.bat` in project folder:
   ```batch
   @echo off
   cd /d "%~dp0"
   python main.py >> logs\scheduler.log 2>&1
   ```

2. Press `Win + R`, type `taskschd.msc`, press Enter
3. Click "Create Basic Task"
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
