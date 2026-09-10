import random
import hashlib
import datetime
from database import query_db, execute_db

def generate_otp_code():
    """Generates a 6-digit numeric OTP code."""
    return f"{random.randint(100000, 999999)}"

def hash_otp(code):
    """Generates SHA-256 hash of the OTP code for database storage."""
    return hashlib.sha256(code.encode('utf-8')).hexdigest()

def create_and_store_otp(email, purpose='login', valid_minutes=10):
    code = generate_otp_code()
    code_hash = hash_otp(code)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=valid_minutes)
    
    # Invalidate previous unconsumed OTPs for this email/purpose
    execute_db(
        "UPDATE otp_codes SET consumed = 1 WHERE email = ? AND purpose = ? AND consumed = 0",
        (email, purpose)
    )
    
    import uuid
    otp_id = str(uuid.uuid4())
    execute_db(
        "INSERT INTO otp_codes (id, email, code_hash, purpose, expires_at, consumed) VALUES (?, ?, ?, ?, ?, 0)",
        (otp_id, email, code_hash, purpose, expires_at.strftime('%Y-%m-%d %H:%M:%S'))
    )
    
    return code

def verify_otp_code(email, code, purpose='login'):
    code_hash = hash_otp(code)
    
    otp = query_db(
        "SELECT * FROM otp_codes WHERE email = ? AND purpose = ? AND code_hash = ? AND consumed = 0 ORDER BY created_at DESC LIMIT 1",
        (email, purpose, code_hash),
        one=True
    )
    
    if not otp:
        return False, "Invalid verification code"
        
    expires_at = datetime.datetime.strptime(otp['expires_at'], '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.utcnow() > expires_at:
        return False, "Verification code has expired. Please request a new one."
        
    # Mark OTP as consumed
    execute_db("UPDATE otp_codes SET consumed = 1 WHERE id = ?", (otp['id'],))
    return True, "Verification successful"
