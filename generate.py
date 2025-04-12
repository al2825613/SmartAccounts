
from utils import extract_email, wait_for_verification_code, log_account
from tiktok_register import register_tiktok
from insta_register import register_instagram
from facebook_register import register_facebook
from iraq import gen

def generate_bulk_accounts(platform, quantity):
    results = []
    for i in range(quantity):
        try:
            _, output = gen(EmailType=1)
            email = extract_email(output)
            if not email:
                results.append({"status": "fail", "reason": "فشل في إنشاء البريد."})
                continue

            if platform == 'tiktok':
                success, data = register_tiktok(email)
            elif platform == 'instagram':
                success, data = register_instagram(email)
            elif platform == 'facebook':
                success, data = register_facebook(email)
            else:
                results.append({"status": "fail", "reason": "منصة غير مدعومة."})
                continue

            if success:
                results.append({"status": "success", **data})
            else:
                results.append({"status": "fail", "reason": data})
        except Exception as e:
            results.append({"status": "fail", "reason": str(e)})
    return results
  
