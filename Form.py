"""
Google Form Automation Script with Selenium and Flask Email Integration
Complete Solution for Assignment Submission
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from flask import Flask
from flask_mail import Mail, Message
import logging
from configg import EMAIL_CONFIG, FORM_DATA, GITHUB_REPO_URL,GOOGLE_FORM_URL, logger
from emaill import send_email_with_latest_screenshot
import re
# ==================== SELENIUM FORM FILLER CLASS ====================
class SmartGoogleFormFiller:
    """Enhanced form filler with intelligent field detection"""
    
    def __init__(self, form_url, form_data):
        self.form_url = form_url
        self.form_data = form_data
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        logger.info("✓ Chrome WebDriver initialized")
        
    def extract_verification_code(self):
        """Automatically extract verification code from the form"""
        try:
            # Method 1: Look for "Type this code:" pattern
            code_patterns = [
                r"Type this code:\s*<b>(.*?)</b>",
                r"Type this code:\s*(\w+)",
                r"code:\s*<b>(.*?)</b>",
                r"code:\s*(\w+)",
                r"CAPTCHA:\s*(\w+)"
            ]
            
            page_source = self.driver.page_source
            
            for pattern in code_patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    code = match.group(1).strip()
                    logger.info(f"✓ Extracted verification code: {code}")
                    return code
            
            # Method 2: Find bold text in verification div
            try:
                code_element = self.driver.find_element(By.XPATH, 
                    "//div[contains(text(), 'Type this code') or contains(text(), 'code:')]//b")
                code = code_element.text.strip()
                if code:
                    logger.info(f"✓ Extracted verification code: {code}")
                    return code
            except:
                pass
            
            # Method 3: Look for any bold text near "code" keyword
            try:
                bold_elements = self.driver.find_elements(By.TAG_NAME, "b")
                for elem in bold_elements:
                    text = elem.text.strip()
                    parent_text = elem.find_element(By.XPATH, "./..").text.lower()
                    if "code" in parent_text and text and len(text) == 6:
                        logger.info(f"✓ Extracted verification code: {text}")
                        return text
            except:
                pass
            
            logger.warning("Could not extract verification code automatically")
            return self.form_data.get("verification_code", "")
            
        except Exception as e:
            logger.error(f"Error extracting verification code: {str(e)}")
            return self.form_data.get("verification_code", "")
    
    def fill_form(self):
        """Main method to fill the form intelligently"""
        try:
            self.setup_driver()
            logger.info(f"Navigating to: {self.form_url}")
            self.driver.get(self.form_url)
            time.sleep(3)
            # Extract verification code
            verification_code = self.extract_verification_code()
            if verification_code:
                self.form_data["verification_code"] = verification_code
            logger.info("Starting intelligent form filling...")
            questions = self.analyze_form_structure()
            self.smart_fill_all_fields(questions)
            self._smart_submit()
            time.sleep(3)
            self._save_screenshot("after_submission")
            logger.info("✓ Form completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            self._save_screenshot("error")
            return False
            
        finally:
            if self.driver:
                time.sleep(2)
                self.driver.quit()
    
    def analyze_form_structure(self):
        """Analyze form structure to identify all questions"""
        questions = []
        
        try:
            # Find all question containers
            question_divs = self.driver.find_elements(By.CSS_SELECTOR, 
                "div[jsmodel='CP1oW'], div[role='listitem']")
            
            for idx, div in enumerate(question_divs):
                try:
                    # Get question text
                    heading = div.find_element(By.CSS_SELECTOR, 
                        "div[role='heading'], .M4DNQ")
                    question_text = heading.text.strip()
                    
                    # Get input field
                    input_field = None
                    try:
                        input_field = div.find_element(By.CSS_SELECTOR, 
                            "input[type='text'], input[type='email'], input[type='tel'], textarea")
                    except:
                        # Might be radio button
                        pass
                    
                    # Check if required
                    is_required = "*" in question_text
                    
                    questions.append({
                        'index': idx,
                        'text': question_text.replace('*', '').strip(),
                        'element': div,
                        'input': input_field,
                        'required': is_required
                    })
                    
                    logger.info(f"Found question {idx + 1}: {question_text[:50]}...")
                    
                except:
                    continue
            
            logger.info(f"✓ Analyzed {len(questions)} questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error analyzing form: {str(e)}")
            return []
    
    def smart_fill_all_fields(self, questions):
        """Intelligently fill all form fields"""
        for question in questions:
            question_text = question['text'].lower()
            
            # Match question to data
            if any(keyword in question_text for keyword in ['name', 'full name']):
                self._fill_input(question, self.form_data['full_name'], "Full Name")
                
            elif any(keyword in question_text for keyword in ['contact', 'phone', 'mobile', 'number']):
                self._fill_input(question, self.form_data['contact_number'], "Contact Number")
                
            elif any(keyword in question_text for keyword in ['email', 'e-mail']):
                self._fill_input(question, self.form_data['email'], "Email")
                
            elif any(keyword in question_text for keyword in ['address', 'full address']):
                self._fill_input(question, self.form_data['address'], "Address")
                
            elif any(keyword in question_text for keyword in ['pin', 'pincode', 'pin code', 'postal', 'zip']):
                self._fill_input(question, self.form_data['pin_code'], "Pin Code")
                
            elif any(keyword in question_text for keyword in ['dob', 'date of birth', 'birth', 'birthday']):
                self._fill_input(question, self.form_data['dob'], "Date of Birth")
                
            elif any(keyword in question_text for keyword in ['gender', 'sex']):
                self._fill_input(question, self.form_data['gender'], "Gender")
                
            elif any(keyword in question_text for keyword in ['code', 'captcha', 'verify', 'verification']):
                self._fill_input(question, self.form_data['verification_code'], "Verification Code")
    
    def _fill_input(self, question, value, field_name):
        """Fill a text input field"""
        try:
            if question['input']:
                input_field = question['input']
                input_field.clear()
                time.sleep(0.3)
                input_field.send_keys(value)
                logger.info(f"✓ Filled {field_name}: {value}")
            else:

                input_field = question['element'].find_element(By.CSS_SELECTOR, 
                    "input, textarea")
                input_field.clear()
                time.sleep(0.3)
                input_field.send_keys(value)
                logger.info(f"✓ Filled {field_name}: {value}")
        except Exception as e:
            logger.warning(f"Could not fill {field_name}: {str(e)}")

    
    def _smart_submit(self):
        """Smart form submission"""
        try:
            # Method 1: Find submit button by text
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "div[role='button'], span[role='button']")
            
            for button in submit_buttons:
                if 'submit' in button.text.lower():
                    button.click()
                    logger.info("✓ Form submitted")
                    return
            
            # Method 2: Find by specific class
            try:
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, 
                    "div[role='button'].uArJ5e")
                submit_btn.click()
                logger.info("✓ Form submitted")
                return
            except:
                pass
            
            logger.warning("Could not find submit button")
            
        except Exception as e:
            logger.error(f"Error submitting: {str(e)}")
    
    def _save_screenshot(self, name):
        """Save screenshot and return its filename"""
        try:
            os.makedirs("screenshots", exist_ok=True)
            filename = f"screenshots/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            # Take screenshot using Selenium
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename  # ✅ Return the path
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None  # ✅ Return None if failed




# ==================== MAIN ====================
def main():

    # Validate config
    if "YOUR_" in GOOGLE_FORM_URL or "your." in EMAIL_CONFIG['sender_email']:
        logger.error("❌ Please update configuration first!")
        return

    logger.info("=" * 70)
    logger.info("STEP 1: Smart Form Filling")
    logger.info("=" * 70)

    filler = SmartGoogleFormFiller(GOOGLE_FORM_URL, FORM_DATA)
    form_success = filler.fill_form()

    if not form_success:
        logger.error("❌ Form filling failed")
        return


    screenshots = []
    try:
        time.sleep(3)  # Wait to ensure confirmation page is fully loaded
        after = filler._save_screenshot("after_submission")
        if after:
            screenshots.append(after)
    except Exception as e:
        logger.warning(f"Screenshot capture failed: {e}")

    # Quit driver safely
    try:
        filler.driver.quit()
    except Exception as e:
        logger.warning(f"Driver quit issue: {e}")

    time.sleep(2)

    logger.info("\n" + "=" * 70)
    logger.info("STEP 2: Email Submission")
    logger.info("=" * 70)

    email_success = send_email_with_latest_screenshot()

    if email_success:
        logger.info("\n" + "=" * 70)
        logger.info("✓ ✓ ✓  ASSIGNMENT COMPLETED!  ✓ ✓ ✓")
        logger.info("=" * 70)
    else:
        logger.error("❌ Email failed (but form was submitted)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise