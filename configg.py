import logging

# -------------------------------------------------------------------
# Logging Setup
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Personal Information (Fill locally, keep secret on GitHub)
# -------------------------------------------------------------------
FORM_DATA = {
    "full_name": "YOUR_FULL_NAME",
    "contact_number": "YOUR_CONTACT_NUMBER",
    "email": "YOUR_EMAIL_ADDRESS",
    "address": "YOUR_HOME_ADDRESS",
    "pin_code": "YOUR_PINCODE",
    "dob": "DD/MM/YYYY",
    "gender": "Male/Female/Other",
}


# -------------------------------------------------------------------
# Email Configuration (⚠ Use environment variables for security)
# -------------------------------------------------------------------
EMAIL_CONFIG = {
    "sender_email":"your_email@gmail.com",
    "sender_password": "your 16 char password",
    "recipient_email": "receiver@example.com",
    "cc_email": "receiver@example.com",
    "subject": f"Python (Selenium) Assignment - {FORM_DATA['full_name']}",
}


# -------------------------------------------------------------------
# Links & Paths
# -------------------------------------------------------------------
GOOGLE_FORM_URL = "https://forms.gle/YOUR_FORM_ID"

# GitHub Links
GITHUB_REPO_URL = "https://github.com/YOUR_USERNAME/Project"
GITHUB_PROJECTS_URL = [
    "https://github.com/YOUR_USERNAME/Project1",
    "https://github.com/YOUR_USERNAME/Project2",
]
# Local paths
SCREENSHOTS_FOLDER = "./screenshots"
RESUME_PATH = "./resume.pdf"
