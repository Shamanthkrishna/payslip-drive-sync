# Email Notifications Setup Guide

## ❓ Do I Need This?

**NO, it's completely OPTIONAL!** 

Email notifications are just helpful alerts sent to you when:
- ✅ Pay slip successfully downloaded and uploaded
- ❌ Something went wrong (so you can check logs)
- ℹ️ Pay slip already exists (skipped)

**Without email**: You can still check the `logs/` folder to see what happened.

## 📧 How Email Notifications Work

```
Your Gmail Account          Script           Your Work Email
(any Gmail you own)    --sends email-->   (you receive notification)
      ↑
Uses App Password
(NOT your real password)
```

## 🔧 Setup Steps (5 minutes)

### Step 1: Choose a Gmail Account

Use **any Gmail account you have access to**:
- ✅ Personal Gmail
- ✅ Secondary Gmail
- ✅ Any Gmail you control
- ❌ NOT your work email (work email receives the notification)

### Step 2: Enable 2-Step Verification

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Sign in with your chosen Gmail
3. Click **2-Step Verification**
4. Follow the prompts to enable it (usually phone verification)

### Step 3: Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Or search "App passwords" in your Google Account settings
2. You might need to verify it's you (phone code, etc.)
3. Under "Select app": Choose **Mail**
4. Under "Select device": Choose **Windows Computer**
5. Click **Generate**
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 4: Update Your `.env` File

```env
# Use the Gmail you chose
EMAIL_SENDER=your.personal.email@gmail.com

# Use the 16-character App Password (remove spaces)
EMAIL_PASSWORD=abcdefghijklmnop

# Your work email (where you want to receive notifications)
EMAIL_RECIPIENT=yourname@yourcompany.com

# Keep these as-is
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Step 5: Test It

```powershell
python email_notifier.py
```

You should receive a test email at your work address!

## 🚫 Don't Want Email Notifications?

Just leave the email fields **empty** in `.env`:

```env
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECIPIENT=
```

The script will skip email notifications and just use logs.

## ❓ FAQ

### Q: Why can't I use my regular Gmail password?
**A**: Google blocks apps from using your regular password for security. App Passwords are special codes just for apps.

### Q: Is it safe to use an App Password?
**A**: Yes! It's **safer** than your regular password because:
- It only works for this one app
- You can revoke it anytime without changing your Gmail password
- It doesn't give access to your Google Account settings

### Q: Can I use my work email as the sender?
**A**: Only if your work email is Gmail and your company allows App Passwords (usually not).

### Q: What if I don't have a Gmail account?
**A**: You have 2 options:
1. Create a free Gmail account (takes 3 minutes)
2. Skip email notifications (leave fields empty)

### Q: Can multiple people use the same Gmail for sending?
**A**: Technically yes, but **NOT recommended**. Each person should use their own Gmail for privacy.

## 🔒 Security Notes

- ✅ App Password is specific to this app only
- ✅ Can be revoked anytime from your Google Account
- ✅ Doesn't give access to your emails or account
- ✅ Only allows sending emails through Gmail's SMTP server
- ❌ Never share your App Password with others
- ❌ Don't use your actual Gmail password

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Username and password not accepted" | Use App Password, not regular password |
| "App Passwords option not available" | Enable 2-Step Verification first |
| No email received | Check spam folder, verify EMAIL_RECIPIENT is correct |
| "SMTPAuthenticationError" | Regenerate App Password, ensure no spaces when copying |

---

**Still confused?** Skip email notifications for now and just use the automation! You can always enable it later.
