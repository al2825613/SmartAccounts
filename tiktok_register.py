
from playwright.sync_api import sync_playwright
import time
from utils import wait_for_verification_code, log_account

def register_tiktok(email, password="Test12345!"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://www.tiktok.com/signup/phone-or-email/email")
            time.sleep(2)

            page.select_option('select[aria-label="Month"]', '1')
            page.select_option('select[aria-label="Day"]', '1')
            page.select_option('select[aria-label="Year"]', '2000')

            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.click('button:has-text("Next")')

            code = wait_for_verification_code(email)
            if not code:
                return False, "لم يتم استلام كود التفعيل."

            page.fill('input[name="code"]', code)
            page.click('button:has-text("Next")')

            time.sleep(5)
            log_account('tiktok', email, password)
            return True, {"email": email, "password": password}

        except Exception as e:
            return False, str(e)
        finally:
            browser.close()
