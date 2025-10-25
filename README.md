
## Google Form Auto-Filler & Email Submission Bot

An intelligent Python automation tool that fills out and submits Google Forms using **Selenium**, then automatically emails a confirmation (with screenshot and resume attached) using **Flask-Mail**.


## 🧩 Introduction

This automation tool was designed to streamline repetitive form-filling tasks, specifically for Google Forms. It:

* Opens a target Google Form.
* Intelligently detects input fields (name, contact, email, address, etc.).
* Automatically fills in data using preconfigured values.
* Extracts and fills any verification or CAPTCHA code.
* Submits the form and captures screenshots for proof.
* Emails the submission confirmation, screenshots, and resume through Flask-Mail.

---

## ✨ Features

* 🔍 Smart question-field matching via keyword detection.
* 🤖 Auto-handling of CAPTCHA/verification code extraction.
* 📸 Automated screenshots (before/after submission).
* 📧 Secure email automation via **Flask-Mail** (TLS-enabled).
* 🧱 Modular configuration structure for easy customization.
* 🪶 Logging system for monitoring all automation steps.

---

## 🗂️ Project Structure

```
├── Form.py           # Handles Google Form automation with Selenium
├── emaill.py         # Manages email automation via Flask-Mail
├── configg.py        # Contains configuration data and credentials
├── screenshots/      # Stores screenshots captured during automation
└── resume.pdf        # Resume file to attach in email
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shashankk1907/Google-Form-Filling-Automation.git
cd Google-Form-Filling-Automation
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # (Linux/macOS)
venv\Scripts\activate      # (Windows)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
---

## 🧠 Configuration

All configuration settings are stored in **`configg.py`**.

### Example:

```python
FORM_DATA = {
    "full_name": "Your Name",
    "contact_number": "1234567890",
    "email": "youremail@gmail.com",
    "address": "Your Address",
    "pin_code": "123456",
    "dob": "DD/MM/YYYY",
    "gender": "Male"
}

EMAIL_CONFIG = {
    "sender_email": "youremail@gmail.com",
    "sender_password": "your_app_password",
    "recipient_email": "recipient@example.com",
    "cc_email": "cc@example.com",
    "subject": f"Python (Selenium) Assignment - {FORM_DATA['full_name']}"
}

GOOGLE_FORM_URL = "https://forms.gle/yourformurl"
GITHUB_REPO_URL = "https://github.com/yourusername/yourrepo"
SCREENSHOTS_FOLDER = "path/to/screenshots"
RESUME_PATH = "path/to/resume.pdf"
```

> ⚠️ **Important:** Use an **App Password** for Gmail (not your main password).
> Enable 2FA and create an App Password via your [Google Account settings](https://myaccount.google.com/security).

---

## ▶️ Usage

Run the main automation from the command line:

```bash
python Form.py
```

The script will:

1. Open the target Google Form.
2. Fill and submit the form automatically.
3. Take screenshots for verification.
4. Send an email with attachments and logs.

---

## 🔍 How It Works

### 1. **Form Automation (`Form.py`):**

* Uses **Selenium WebDriver** to open and interact with the Google Form.
* Detects question fields dynamically using `CSS` and `XPath`.
* Matches each question with the appropriate field from `FORM_DATA`.
* Handles verification codes intelligently via regex.
* Captures screenshots before and after submission.

### 2. **Email Automation (`emaill.py`):**

* Uses **Flask-Mail** to securely send emails via Gmail’s SMTP.
* Attaches:

  * Latest screenshot from `/screenshots`
  * Resume file from configured path
* Includes formatted message body with project documentation.

### 3. **Configuration (`configg.py`):**

* Central hub for all variables: form data, email settings, URLs, and paths.
* Keeps credentials separate for security and flexibility.

---

## 🧩 Dependencies

Main Python libraries used:

* `selenium`
* `flask`
* `flask-mail`
* `glob`
* `logging`
* `datetime`
* `re`
* `os`, `time`

---

## 🧰 Troubleshooting

| Issue                                           | Possible Cause              | Solution                                              |
| ----------------------------------------------- | --------------------------- | ----------------------------------------------------- |
| `selenium.common.exceptions.WebDriverException` | Missing ChromeDriver        | Install and add it to PATH                            |
| `smtplib.SMTPAuthenticationError`               | Invalid Gmail credentials   | Use a valid 16-char Gmail App Password                |
| `⚠️ No screenshot found`                        | Screenshot directory empty  | Ensure `screenshots/` folder exists and accessible    |
| `Email not sent`                                | Network or credential issue | Check internet connection and Gmail security settings |

---

## 👨‍💻 Contributors

**Author:** [Shashank Ratnakar Sonawane](mailto:shashanksonawane7@gmail.com)
**GitHub:** [Shashankk1907](https://github.com/Shashankk1907)

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---
