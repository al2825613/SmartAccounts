
from playwright.sync_api import sync_playwright
import time
from utils import wait_for_verification_code, log_account

def register_facebook(email, password="Test12345!"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://www.facebook.com/r.php")
            time.sleep(2)

            page.fill("input[name='firstname']", "John")
            page.fill("input[name='lastname']", "Doe")
            page.fill("input[name='reg_email__']", email)
            page.fill("input[name='reg_passwd__']", password)

            page.select_option("select[name='birthday_day']", '1')
            page.select_option("select[name='birthday_month']", '1')
            page.select_option("select[name='birthday_year']", '2000')
            page.click("input[name='sex'][value='2']")
            page.click("button[name='websubmit']")

            code = wait_for_verification_code(email)
            if not code:
                return False, "لم يتم استلام كود التفعيل."

            log_account("facebook", email, password)
            return True, {"email": email, "password": password}

        except Exception as e:
            return False, str(e)
        finally:
            browser.close()
