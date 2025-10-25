import time
import os
import glob
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
from configg import EMAIL_CONFIG, FORM_DATA, GITHUB_REPO_URL,SCREENSHOTS_FOLDER,RESUME_PATH,GITHUB_PROJECTS_URL, logger


# ==================== FLASK APP SETUP ====================
app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=EMAIL_CONFIG['sender_email'],
    MAIL_PASSWORD=EMAIL_CONFIG['sender_password']
)
mail = Mail(app)


def get_latest_screenshot(folder_path):
    """
    Get the most recently saved screenshot from the folder.
    
    Args:
        folder_path: Path to screenshots folder
        
    Returns:
        str: Path to latest screenshot or None if not found
    """
    try:
        # Support common image formats
        patterns = ['*.png', '*.jpg', '*.jpeg', '*.gif']
        files = []
        
        for pattern in patterns:
            files.extend(glob.glob(os.path.join(folder_path, pattern)))
        
        if not files:
            logger.warning(f"⚠️ No screenshots found in {folder_path}")
            return None
        
        # Get the most recent file by modification time
        latest_file = max(files, key=os.path.getmtime)
        return latest_file
        
    except Exception as e:
        logger.error(f"❌ Error finding latest screenshot: {e}")
        return None


def create_email_body():
    """Create formatted email body"""
    return f"""Dear Hiring Team,

I hope you’re doing well. Please find my assignment submission below as requested.
1. Screenshot of the form filled via code(attached)
2. Source code (GitHub repository link)
    {GITHUB_REPO_URL}
3. My updated resume(attached)
4. Links to my past projects/work samples
    {GITHUB_PROJECTS_URL}
5. Brief documentation of my approach
    Objective:
    This project automates the process of filling and submitting a Google Form using Python Selenium and then emails the submission proof (screenshot + resume) automatically through a Flask-Mail setup.
    
    Overview:
    The solution consists of three main files:

    1. `form.py` – Handles the complete Google Form automation using Selenium.
        * Launches the Chrome WebDriver and navigates to the target Google Form.
        * Intelligently identifies and fills each form field (name, email, contact, DOB, etc.) based on keywords.
        * Extracts verification/captcha codes automatically using regex or text-based matching.
        * Takes screenshots before/after submission for proof and logging.
        * Submits the form smartly by detecting the correct submit button.

    2. `email.py` – Manages the email automation using Flask-Mail.
        * Configures SMTP with TLS for secure email sending.
        * Composes a formatted email body containing personal and form details.
        * Attaches the latest screenshot and resume automatically from the configured directories.
        * Logs all steps (success/warning/error) using Python’s `logging` module.

    3. `config.py` – Stores all configuration and sensitive details.
        * Includes form data (`FORM_DATA`), sender/receiver email credentials (`EMAIL_CONFIG`), and the form/repo URLs.
        * Keeps credentials separate from logic for better security and modularity.


    Execution Flow:

    1. The script initializes and validates configurations.
    2. The `SmartGoogleFormFiller` class fills and submits the Google Form automatically.
    3. A screenshot of the submission confirmation page is saved locally.
    4. The `send_email_with_latest_screenshot()` function sends an email with:
        * The latest screenshot attached.
        * Resume file attached.
        * Form details and GitHub link in the email body.
    5. Logs confirm each step and ensure visibility into success or failure.

I confirm that I’m available to work full-time (10 am – 7 pm) for the next 3–6 months.

Please let me know if you need any additional information or clarification.

Best regards,
{FORM_DATA['full_name']}
{FORM_DATA['email']}
{FORM_DATA['contact_number']}

---
Submitted: {datetime.now().strftime("%d %B %Y, %I:%M %p")}
"""

def attach_file_to_message(msg, file_path):
    """
    Attach a file to email message.
    
    Args:
        msg: Flask-Mail Message object
        file_path: Path to file to attach
        
    Returns:
        bool: True if attachment successful, False otherwise
    """
    try:
        abs_path = os.path.abspath(file_path)
        
        if not os.path.exists(abs_path):
            logger.warning(f"⚠️ File not found: {abs_path}")
            return False
        
        # Determine content type based on extension
        ext = os.path.splitext(abs_path)[1].lower()
        content_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain'
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        
        with open(abs_path, 'rb') as f:
            msg.attach(
                filename=os.path.basename(abs_path),
                content_type=content_type,
                data=f.read()
            )
        
        logger.info(f"✓ Attached file: {os.path.basename(abs_path)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to attach file {file_path}: {e}")
        return False


def send_email_with_latest_screenshot():
    """
    Send submission email with the latest screenshot and resume attached.
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        with app.app_context():
            # Create message
            msg = Message(
                subject=EMAIL_CONFIG['subject'],
                sender=EMAIL_CONFIG['sender_email'],
                recipients=[EMAIL_CONFIG['recipient_email']],
                cc=[EMAIL_CONFIG['cc_email']],
                body=create_email_body()
            )
            
            # Get and attach latest screenshot
            latest_screenshot = get_latest_screenshot(SCREENSHOTS_FOLDER)
            
            if latest_screenshot:
                attach_file_to_message(msg, latest_screenshot)
            else:
                logger.warning("⚠️ No screenshot attached - none found in folder")
            
            # Attach resume
            if os.path.exists(RESUME_PATH):
                attach_file_to_message(msg, RESUME_PATH)
            else:
                logger.warning(f"⚠️ Resume not found at: {RESUME_PATH}")
            
            # Send email
            mail.send(msg)
            logger.info("✅ Email sent successfully!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Email sending failed: {e}", exc_info=True)
        return False
