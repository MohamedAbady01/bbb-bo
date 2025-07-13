# BBB.org Signup Automation with Playwright and Gradio

This project automates the registration process on [BBB.org](https://www.bbb.org/account/register) using Playwright, Gradio, and Google Sheets + Google Drive integrations. It supports full signup, email verification, and two-factor authentication (2FA) steps interactively.

## ✅ Features

- Fully automates BBB.org account registration.
- Pulls business data dynamically from Google Sheets.
- Downloads business logos/images from Google Drive.
- Handles:
  - First name, last name, email, password, zip
  - Email verification code input
  - Second (2FA) verification step
- Interactive UI using Gradio for verification inputs.
- Logs status and results to Google Sheets.

---

## 📦 Requirements

- Python 3.8+
- Playwright
- Gradio
- Google Sheets API (via `logic/bbbsheets.py`)
- Google Drive API (via `logic/drive.py`)
- Chrome browser dependencies (installable with `playwright install-deps`)

---

## 🔧 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/bbb-signup-bot.git
   cd bbb-signup-bot
