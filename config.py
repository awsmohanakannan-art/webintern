import os
import shutil
import tempfile
from dotenv import load_dotenv

load_dotenv()

def get_sqlite_db_path():
    root_db = os.path.join(os.path.dirname(__file__), "webintern.db")
    
    # Detect Vercel / AWS Lambda / Serverless read-only environment
    is_serverless = os.getenv("VERCEL") == "1" or os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None
    
    if is_serverless:
        tmp_db = os.path.join(tempfile.gettempdir(), "webintern.db")
        if os.path.exists(root_db):
            root_size = os.path.getsize(root_db)
            if not os.path.exists(tmp_db) or os.path.getsize(tmp_db) < root_size:
                try:
                    shutil.copy2(root_db, tmp_db)
                except Exception as e:
                    print(f"Warning: Failed to copy DB to /tmp: {e}")
                    return root_db
            return tmp_db
    
    return root_db

class Config:
    SECRET_KEY = os.getenv("JWT_SECRET", "webintern_default_secret_key_2026")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24

    # Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Google OAuth credentials (SERVER-SIDE ONLY)
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

    # Resend
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

    # Razorpay
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_WebInternKey123")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "rzp_secret_WebInternSecret456")
    RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "rzp_webhook_secret_789")

    # DB Fallback Path
    SQLITE_DB_PATH = get_sqlite_db_path()
