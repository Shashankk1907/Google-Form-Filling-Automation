import logging
# ==================== CONFIGURATION ====================
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Personal Information - UPDATE THESE WITH YOUR DETAILS
FORM_DATA = {
    "full_name": "SHASHANK RATNAKAR SONAWANE",
    "contact_number": "8104479816",
    "email": "shashanksonawane7@gmail.com",
    "address": "Samarth Residency, 3rd Floor, Warje, Pune.",
    "pin_code": "411058",
    "dob": "18/03/2004",
    "gender": "Male",
}

# Email Configuration - UPDATE WITH YOUR GMAIL CREDENTIALS
EMAIL_CONFIG = {
    "sender_email": "shashanksonawane7@gmail.com",  # Your Gmail address
    "sender_password": "olcd nsav kiwa tvqy",  # 16-character App Password
    "recipient_email": "1spydy1@gmail.com",
    "cc_email": "1spydy1@gmail.com",
    "subject": f"Python (Selenium) Assignment - {FORM_DATA['full_name']}"
}

# Google Form URL - UPDATE WITH ACTUAL FORM URL
GOOGLE_FORM_URL = "https://forms.gle/YsHZm5pBDzmUb58V7"

# GitHub Repository URL - UPDATE AFTER CREATING REPO
GITHUB_REPO_URL = "https://github.com/Shashankk1907"
GITHUB_PROJECTS_URL=["https://github.com/Shashankk1907/StartScope","https://github.com/Shashankk1907/n8n-Instagram-x-Ai"]
SCREENSHOTS_FOLDER = '/Users/shashank/Formfiller/screenshots'
RESUME_PATH='/Users/shashank/Formfiller/resume.pdf'