import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("JWT_SECRET", "webintern_default_secret_key_2026")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24

    # Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY", "")

    # Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

    # Razorpay
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_WebInternKey123")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "rzp_secret_WebInternSecret456")
    RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "rzp_webhook_secret_789")

    # DB Fallback Path
    SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "webintern.db")
