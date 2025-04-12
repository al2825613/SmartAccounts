
from playwright.sync_api import sync_playwright
import time
import random
from utils import wait_for_verification_code, log_account

def register_instagram(email, password="Test12345!"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://www.instagram.com/accounts/emailsignup/")
            time.sleep(3)

            page.fill("input[name='emailOrPhone']", email)
            page.fill("input[name='fullName']", "Test User")
            username = "user" + str(random.randint(1000,9999))
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)

            page.click("button[type='submit']")
            time.sleep(15)

            code = wait_for_verification_code(email)
            if not code:
                return False, "لم يتم استلام كود التفعيل."

            log_account("instagram", email, password, username)
            return True, {"email": email, "password": password, "username": username}

        except Exception as e:
            return False, str(e)
        finally:
            browser.close()
          
