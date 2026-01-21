# Contributing to Payslip Drive Sync

Thank you for using this automation tool! This guide helps employees in the organization use and contribute to the project.

## 🎯 For Employees Using This Tool

### Getting Started
1. **Clone the repository** to your work PC
2. **Follow the [README.md](README.md)** setup instructions
3. **Configure with YOUR credentials** - Keep them private!
4. **Test before scheduling** - Run `python main.py` manually first

### Your Responsibilities
- ✅ Keep your `.env` file secure and private
- ✅ Use your personal Gmail for Google Drive (not work email)
- ✅ Test the automation before relying on it
- ✅ Check logs if something fails
- ❌ NEVER commit your `.env`, `credentials.json`, or `token.json` files
- ❌ NEVER share your Google Drive API credentials

## 🐛 Reporting Issues

If you encounter problems:

1. **Check the logs** first: `logs/payslip_automation_*.log`
2. **Verify credentials** in `.env` file
3. **Test components individually**:
   ```powershell
   python paybooks_scraper.py
   python drive_uploader.py
   python email_notifier.py
   ```
4. **Create a GitHub issue** with:
   - Error message (remove any credentials!)
   - Steps to reproduce
   - Your setup (Python version, Windows version)

## 💡 Suggesting Improvements

Have an idea to make this better? We welcome:
- Bug fixes
- Feature suggestions
- Documentation improvements
- Support for other portals
- UI/UX enhancements

### How to Contribute Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m "Add: description of your changes"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Create Pull Request** on GitHub

### Coding Guidelines
- Follow existing code style
- Add comments for complex logic
- Update README if you add features
- Test on Windows before submitting
- Remove any hardcoded credentials

## 🔒 Security Guidelines

**CRITICAL**: This tool handles sensitive credentials!

- All credentials must be in `.env` (never hardcoded)
- `.env` is in `.gitignore` - verify before committing
- Sanitize logs before sharing (remove credentials)
- Use environment variables for all sensitive data
- Never commit actual credentials in example files

## 📝 Documentation

When contributing:
- Update README.md if you add features
- Add code comments for clarity
- Document configuration changes
- Update .env.example for new variables

## 🙏 Questions?

- Check [README.md](README.md) first
- Review existing GitHub issues
- Create new issue if needed
- Contact repository maintainer

---

**Remember**: Each employee's setup is independent. Your credentials, your Google Drive, your privacy!
