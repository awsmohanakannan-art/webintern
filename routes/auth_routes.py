import json
import uuid
import requests
from flask import Blueprint, request, jsonify, make_response, render_template_string
from database import query_db, execute_db
from utils.auth import generate_jwt, check_password, jwt_required
from utils.email_service import send_forgot_password_email, _dispatch_email
from config import Config
from supabase import create_client

auth_bp = Blueprint('auth_bp', __name__)

DEFAULT_SUPABASE_URL = "https://fzmdeigwxiesegvtuafk.supabase.co"
DEFAULT_SUPABASE_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6bWRlaWd3eGllc2VndnR1YWZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg0MjA2NDAsImV4cCI6MjEwMzk5NjY0MH0.aqk90jQu4yBCgc0wi9zA0cMHf5XZ31OPVc3hcED0_J8"
DEFAULT_SUPABASE_SERVICE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6bWRlaWd3eGllc2VndnR1YWZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4ODQyMDY0MCwiZXhwIjoyMTAzOTk2NjQwfQ.osKcbobbZPLz7RpO0zVgyHbIPJC2l6QDF6MBQ-W0uTA"

def get_supabase_admin():
    url = (Config.SUPABASE_URL or DEFAULT_SUPABASE_URL).strip()
    key = (Config.SUPABASE_SERVICE_ROLE_KEY or DEFAULT_SUPABASE_SERVICE).strip()
    return create_client(url, key)

def get_supabase_anon():
    url = (Config.SUPABASE_URL or DEFAULT_SUPABASE_URL).strip()
    key = (Config.SUPABASE_ANON_KEY or DEFAULT_SUPABASE_ANON).strip()
    return create_client(url, key)

@auth_bp.route('/api/auth/config', methods=['GET'])
def get_auth_config():
    """Return public Supabase configuration for frontend initialization."""
    return jsonify({
        'supabase_url': Config.SUPABASE_URL or DEFAULT_SUPABASE_URL,
        'supabase_anon_key': Config.SUPABASE_ANON_KEY or DEFAULT_SUPABASE_ANON,
        'google_client_id': Config.GOOGLE_CLIENT_ID
    }), 200

def sync_profile_to_local_db(user_id, full_name, email, phone="", phone_country_code="+91", marketing_opt_in=False):
    """Sync profile record to SQLite database for compatibility with existing routes."""
    try:
        existing = query_db("SELECT id FROM profiles WHERE id = ? OR email = ?", (user_id, email), one=True)
        if existing:
            execute_db(
                "UPDATE profiles SET full_name = ?, email = ?, phone = ?, phone_country_code = ?, marketing_opt_in = ? WHERE id = ?",
                (full_name, email, phone, phone_country_code, 1 if marketing_opt_in else 0, existing['id'])
            )
        else:
            execute_db(
                "INSERT INTO profiles (id, full_name, email, phone, phone_country_code, marketing_opt_in) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, full_name, email, phone, phone_country_code, 1 if marketing_opt_in else 0)
            )
    except Exception as e:
        print(f"[SQLite Sync Warning]: {e}")

def safe_upsert_profile(supabase_admin, profile_dict):
    """Helper to safely upsert profiles even if certain columns differ in Postgres schema."""
    try:
        supabase_admin.table('profiles').upsert(profile_dict).execute()
    except Exception as e:
        err_str = str(e)
        if 'email' in err_str and 'column' in err_str:
            fallback_dict = {k: v for k, v in profile_dict.items() if k != 'email'}
            supabase_admin.table('profiles').upsert(fallback_dict).execute()
        else:
            print(f"[Profiles Upsert Warning]: {e}")

@auth_bp.route('/api/auth/register', methods=['POST'])
def register_user():
    """Register user with Supabase Auth and directly create activated profile."""
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    phone = data.get('phone', '').strip()
    phone_country_code = data.get('phone_country_code', '+91').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    terms_accepted = data.get('terms_accepted', False)
    marketing_opt_in = data.get('marketing_opt_in', False)

    # Validations
    if not full_name:
        return jsonify({'error': 'Full name is required.'}), 400
    if not email:
        return jsonify({'error': 'Email address is required.'}), 400
    if not password:
        return jsonify({'error': 'Password is required.'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400
    if confirm_password and password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if not terms_accepted:
        return jsonify({'error': 'You must agree to the Terms & Conditions and Privacy Policy.'}), 400

    full_mobile = f"{phone_country_code} {phone}".strip() if phone else ""

    try:
        supabase_admin = get_supabase_admin()
        
        # 1. Create user in Supabase Auth
        res = supabase_admin.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': True,
            'user_metadata': {'name': full_name}
        })

        if not res.user:
            return jsonify({'error': 'Failed to create account in Supabase Auth.'}), 400

        user_id = str(res.user.id)

        # 2. Insert into public.profiles in Supabase as completed/active
        profile_data = {
            'id': user_id,
            'name': full_name,
            'email': email,
            'mobile': full_mobile,
            'phone_verified': True,
            'auth_provider': 'email',
            'terms_accepted': True,
            'marketing_opt_in': marketing_opt_in,
            'profile_complete': True
        }
        
        safe_upsert_profile(supabase_admin, profile_data)
        sync_profile_to_local_db(user_id, full_name, email, phone, phone_country_code, marketing_opt_in)

        token = generate_jwt({
            'sub': user_id,
            'email': email,
            'name': full_name,
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Account created successfully!',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'mobile': full_mobile,
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        err_msg = str(e)
        if any(term in err_msg.lower() for term in ['already registered', 'already exists', 'duplicate', 'user with this email', 'has already been registered']):
            return jsonify({'error': 'An account with this email address already exists. Please sign in instead.'}), 400
        return jsonify({'error': f'Registration failed: {err_msg}'}), 400

@auth_bp.route('/api/auth/login', methods=['POST'])
def login_user():
    """Login user with Email and Password using Supabase Auth."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email address and password are required.'}), 400

    try:
        supabase_anon = get_supabase_anon()
        supabase_admin = get_supabase_admin()

        # Sign in via Supabase Auth
        auth_res = supabase_anon.auth.sign_in_with_password({
            'email': email,
            'password': password
        })

        if not auth_res.user:
            return jsonify({'error': 'Invalid email or password.'}), 401

        user_id = str(auth_res.user.id)

        # Retrieve profile from Supabase profiles table by ID
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        
        profile = None
        if prof_res.data and len(prof_res.data) > 0:
            profile = prof_res.data[0]
        else:
            default_profile = {
                'id': user_id,
                'name': auth_res.user.user_metadata.get('name', email.split('@')[0]),
                'email': email,
                'mobile': '',
                'phone_verified': True,
                'auth_provider': 'email',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            safe_upsert_profile(supabase_admin, default_profile)
            profile = default_profile
            sync_profile_to_local_db(user_id, profile['name'], email)

        token = generate_jwt({
            'sub': user_id,
            'email': email,
            'name': profile.get('name') or email.split('@')[0],
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Login successful.',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': profile.get('name') or email.split('@')[0],
                'mobile': profile.get('mobile', ''),
                'profile_complete': True,
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        err_msg = str(e)
        if 'invalid credentials' in err_msg.lower() or 'invalid login' in err_msg.lower() or 'invalid email' in err_msg.lower():
            return jsonify({'error': 'Invalid email or password.'}), 401
        return jsonify({'error': f'Authentication failed: {err_msg}'}), 400

def google_sub_to_uuid(user_id):
    """Convert Google numeric/string ID to a deterministic UUID compatible with Supabase Postgres schema."""
    try:
        uuid.UUID(str(user_id))
        return str(user_id)
    except Exception:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"google:{user_id}"))

def get_or_create_supabase_auth_user(supabase_admin, email, name):
    """Ensure user exists in Supabase auth.users table to satisfy profiles foreign key constraint."""
    try:
        res = supabase_admin.auth.admin.create_user({
            'email': email,
            'email_confirm': True,
            'user_metadata': {'name': name}
        })
        if res.user:
            return str(res.user.id)
    except Exception as e:
        print(f"[Supabase Auth Admin Note]: {e}")

    try:
        users_list = supabase_admin.auth.admin.list_users()
        for u in users_list:
            if u.email and u.email.lower() == email.lower():
                return str(u.id)
    except Exception as e:
        print(f"[Supabase Auth Admin List Users Warning]: {e}")

    return google_sub_to_uuid(email)

@auth_bp.route('/oauth2callback')
@auth_bp.route('/api/auth/google/callback')
def google_oauth_callback():
    """Handle Google OAuth 2.0 redirect callback."""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error or not code:
        err_msg = error or "Authorization code missing."
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Authentication Error</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #e53e3e;">Google Sign-In Failed</h2>
            <p>{err_msg}</p>
            <a href="/#/login" style="padding: 10px 20px; background: #0B3D91; color: white; border-radius: 5px; text-decoration: none;">Return to Sign In</a>
        </body>
        </html>
        """
        return render_template_string(html), 400

    try:
        token_url = "https://oauth2.googleapis.com/token"
        redirect_uri = request.base_url
        if redirect_uri.endswith('/api/auth/google/callback'):
            redirect_uri = redirect_uri.replace('/api/auth/google/callback', '/oauth2callback')
        
        token_data = {
            'code': code,
            'client_id': Config.GOOGLE_CLIENT_ID,
            'client_secret': Config.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        token_res = requests.post(token_url, data=token_data, timeout=15)
        token_json = token_res.json()
        
        access_token = token_json.get('access_token')
        if not access_token:
            raise Exception(token_json.get('error_description') or 'Failed to obtain access token from Google.')

        userinfo_res = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=15
        )
        userinfo = userinfo_res.json()
        
        raw_user_id = str(userinfo.get('id'))
        email = userinfo.get('email', '').strip().lower()
        name = userinfo.get('name', '').strip() or email.split('@')[0]

        if not raw_user_id or not email:
            raise Exception('Google profile did not return valid email address.')

        supabase_admin = get_supabase_admin()
        user_id = get_or_create_supabase_auth_user(supabase_admin, email, name)

        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_id).execute()
        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else None

        if not profile:
            profile = {
                'id': user_id,
                'name': name,
                'email': email,
                'mobile': '',
                'phone_verified': True,
                'auth_provider': 'google',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            safe_upsert_profile(supabase_admin, profile)
            sync_profile_to_local_db(user_id, name, email)

        app_token = generate_jwt({
            'sub': profile['id'],
            'email': email,
            'name': name,
            'role': 'student'
        })

        user_json = json.dumps({
            'id': profile['id'],
            'email': email,
            'full_name': name,
            'profile_complete': True,
            'auth_provider': 'google',
            'role': 'student'
        })
        token_json_str = json.dumps(app_token)

        callback_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <script>
                localStorage.setItem('access_token', {token_json_str});
                localStorage.setItem('user_profile', {user_json});
                window.location.href = '/#/dashboard';
            </script>
        </head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
            <h3 style="color: #0B3D91;">Google Authentication Successful!</h3>
            <p>Redirecting to your dashboard...</p>
        </body>
        </html>
        """
        resp = make_response(render_template_string(callback_html))
        resp.set_cookie('access_token', app_token, httponly=True, samesite='Lax', max_age=86400)
        return resp
    except Exception as e:
        err_msg = str(e)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>OAuth Callback Error</title></head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #e53e3e;">Authentication Error</h2>
            <p>{err_msg}</p>
            <a href="/#/login" style="padding: 10px 20px; background: #0B3D91; color: white; border-radius: 5px; text-decoration: none;">Return to Sign In</a>
        </body>
        </html>
        """
        return render_template_string(html), 400

@auth_bp.route('/api/auth/google-sync', methods=['POST'])
def sync_google_user():
    """Sync profile and handle provider linking for users logging in via Google OAuth."""
    data = request.get_json() or {}
    user_id = data.get('id')
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()
    credential = data.get('credential')
    access_token = data.get('access_token')

    if credential and (not email or not user_id):
        try:
            res = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}', timeout=10)
            if res.status_code == 200:
                tinfo = res.json()
                user_id = str(tinfo.get('sub'))
                email = tinfo.get('email', '').strip().lower()
                name = tinfo.get('name', name) or email.split('@')[0]
        except Exception as e:
            print(f"[Google TokenInfo Error]: {e}")

    if access_token and (not email or not user_id):
        try:
            res = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': f'Bearer {access_token}'}, timeout=10)
            if res.status_code == 200:
                uinfo = res.json()
                user_id = str(uinfo.get('id'))
                email = uinfo.get('email', '').strip().lower()
                name = uinfo.get('name', name) or email.split('@')[0]
        except Exception as e:
            print(f"[Google UserInfo Error]: {e}")

    if not email:
        return jsonify({'error': 'Email is required for Google auth sync.'}), 400

    try:
        supabase_admin = get_supabase_admin()
        user_uuid = get_or_create_supabase_auth_user(supabase_admin, email, name or email.split('@')[0])
        
        prof_res = supabase_admin.table('profiles').select('*').eq('id', user_uuid).execute()
        profile = prof_res.data[0] if (prof_res.data and len(prof_res.data) > 0) else None

        if not profile:
            new_profile = {
                'id': user_uuid,
                'name': name or email.split('@')[0],
                'email': email,
                'mobile': '',
                'phone_verified': True,
                'auth_provider': 'google',
                'terms_accepted': True,
                'marketing_opt_in': False,
                'profile_complete': True
            }
            safe_upsert_profile(supabase_admin, new_profile)
            profile = new_profile
            sync_profile_to_local_db(user_uuid, name or email.split('@')[0], email)
        else:
            if profile.get('auth_provider') == 'email':
                supabase_admin.table('profiles').update({'auth_provider': 'both'}).eq('id', user_uuid).execute()
                profile['auth_provider'] = 'both'

        token = generate_jwt({
            'sub': profile['id'],
            'email': email,
            'name': profile.get('name') or name or email.split('@')[0],
            'role': 'student'
        })

        resp = make_response(jsonify({
            'message': 'Google authentication successful.',
            'token': token,
            'user': {
                'id': profile['id'],
                'email': email,
                'full_name': profile.get('name') or name or email.split('@')[0],
                'mobile': profile.get('mobile', ''),
                'profile_complete': True,
                'auth_provider': profile.get('auth_provider', 'google'),
                'role': 'student'
            }
        }))
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
        return resp, 200

    except Exception as e:
        return jsonify({'error': f'Failed to sync Google user: {str(e)}'}), 400

@auth_bp.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Trigger password reset email flow using Resend integration."""
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email address is required.'}), 400

    try:
        reset_code = str(uuid.uuid4().hex[:8]).upper()
        reset_link = f"{request.host_url}#/reset-password?email={email}&code={reset_code}"
        
        success, res = send_forgot_password_email(email, reset_link=reset_link, reset_code=reset_code)

        if success:
            return jsonify({
                'message': f'Password reset email sent to {email} successfully via Resend.'
            }), 200
        else:
            return jsonify({'error': f'Failed to send password reset email via Resend: {res}'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to process password reset email: {str(e)}'}), 400

@auth_bp.route('/api/auth/test-email', methods=['POST'])
def test_email_endpoint():
    """Endpoint to trigger and test email sending via Resend API."""
    data = request.get_json() or {}
    to_email = data.get('to_email', 'delivered@resend.dev').strip().lower()
    subject = data.get('subject', 'Test Email from Web Intern')
    content = data.get('content', 'This is a test email sent via Resend API key integration.')

    html_content = f"""
    <div style="font-family: 'Inter', Arial, sans-serif; padding: 24px; border: 1px solid #DCE6F5; border-radius: 12px; max-width: 500px; margin: 0 auto;">
        <h2 style="color: #0B3D91; margin-top: 0;">web<span style="color: #2E7DFF;">intern</span></h2>
        <h3 style="color: #082B66;">{subject}</h3>
        <p style="color: #4B5563; line-height: 1.6;">{content}</p>
        <hr style="border: none; border-top: 1px solid #DCE6F5; margin: 20px 0;" />
        <p style="color: #9CA3AF; font-size: 12px; text-align: center;">Verified Resend Integration Test • Web Intern</p>
    </div>
    """
    
    success, result = _dispatch_email(to_email, subject, html_content)
    if success:
        return jsonify({'message': f'Email sent successfully to {to_email}', 'result': result}), 200
    else:
        return jsonify({'error': f'Email sending failed: {result}'}), 500

@auth_bp.route('/api/auth/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    admin = query_db("SELECT * FROM admins WHERE email = ?", (email,), one=True)
    if not admin or not check_password(password, admin['password_hash']):
        return jsonify({'error': 'Invalid administrator credentials.'}), 401

    token = generate_jwt({
        'sub': admin['id'],
        'email': admin['email'],
        'name': admin['full_name'],
        'role': 'admin'
    })

    resp = make_response(jsonify({
        'message': 'Admin authentication successful.',
        'token': token,
        'user': {
            'id': admin['id'],
            'email': admin['email'],
            'full_name': admin['full_name'],
            'role': 'admin'
        }
    }))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax', max_age=86400)
    return resp, 200

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required
def get_current_user():
    user_payload = request.user
    if user_payload.get('role') == 'admin':
        admin = query_db("SELECT id, email, full_name, created_at FROM admins WHERE id = ?", (user_payload['sub'],), one=True)
        if admin:
            admin['role'] = 'admin'
            return jsonify({'user': admin}), 200
    else:
        try:
            supabase_admin = get_supabase_admin()
            prof_res = supabase_admin.table('profiles').select('*').eq('id', user_payload['sub']).execute()
            if prof_res.data and len(prof_res.data) > 0:
                p = prof_res.data[0]
                return jsonify({
                    'user': {
                        'id': p['id'],
                        'full_name': p.get('name') or user_payload.get('name'),
                        'email': user_payload.get('email'),
                        'mobile': p.get('mobile'),
                        'profile_complete': True,
                        'role': 'student'
                    }
                }), 200
        except Exception:
            pass

        profile = query_db("SELECT id, full_name, email, phone, phone_country_code, college, avatar_url, created_at FROM profiles WHERE id = ?", (user_payload['sub'],), one=True)
        if profile:
            profile['role'] = 'student'
            return jsonify({'user': profile}), 200

    return jsonify({'error': 'User not found.'}), 404
