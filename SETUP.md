# Web Intern Platform - Local Setup Guide

## Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git
- A modern web browser

## Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd webintern
```

## Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows
```

Edit `.env` and fill in all required values:

### Required Credentials

#### Supabase Setup
1. Go to https://supabase.com
2. Create a new project or use existing one
3. Get credentials from:
   - Project Settings → API
   - Copy: `Project URL` → SUPABASE_URL
   - Copy: `anon public` key → SUPABASE_ANON_KEY
   - Copy: `service_role` secret → SUPABASE_SERVICE_ROLE_KEY

#### Google OAuth Setup
1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable OAuth 2.0:
   - OAuth consent screen → Create
   - Credentials → Create → OAuth 2.0 Client ID (Web application)
   - Add localhost:5000 to authorized redirect URIs:
     - `http://localhost:5000/api/auth/google/callback`
   - Copy: Client ID → GOOGLE_CLIENT_ID
   - Copy: Client Secret → GOOGLE_CLIENT_SECRET

#### Razorpay Setup (for payments)
1. Go to https://dashboard.razorpay.com
2. Settings → API Keys
3. For testing use test keys (start with `rzp_test_`)
4. Copy: Key ID → RAZORPAY_KEY_ID
5. Copy: Key Secret → RAZORPAY_KEY_SECRET
6. Create webhook secret → RAZORPAY_WEBHOOK_SECRET

#### Resend Email Setup
1. Go to https://resend.com
2. Create account and verify domain
3. API Keys → Copy your key → RESEND_API_KEY

#### Google Sheets Integration
1. Create a Google Apps Script project
2. Deploy as web app
3. Copy deployment URL → GOOGLE_SHEETS_WEBHOOK_URL

#### JWT Secret
Generate a secure random string:
```bash
# macOS/Linux
openssl rand -hex 32

# Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```
Copy result to JWT_SECRET in `.env`

## Step 5: Create Required Directories
```bash
mkdir -p storage/assignments
mkdir -p storage/generated/offers
mkdir -p storage/generated/certificates
```

## Step 6: Run the Application
```bash
python app.py
```

App will start at: **http://localhost:5000**

## Testing the Setup

### Test Backend Endpoints
```bash
# Test API is running
curl http://localhost:5000/api/auth/status

# Test signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

### Test Frontend
Open http://localhost:5000 in your browser

### Test Google OAuth (if configured)
Click "Sign in with Google" button

### Test Payments (Razorpay)
Use Razorpay test card: `4111 1111 1111 1111` (any future date)

## Troubleshooting

### Module not found errors
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
```bash
# macOS/Linux - Kill process on port 5000
lsof -ti:5000 | xargs kill

# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Environment variables not loading
- Verify `.env` file exists in root directory
- Restart the Flask app after editing `.env`
- Don't commit `.env` to git (already in .gitignore)

### Database connection failed
- Verify SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
- Check internet connection
- Test Supabase connection from dashboard

### Google OAuth not working
- Verify redirect URI includes `http://localhost:5000/api/auth/google/callback`
- Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- Confirm OAuth consent screen is published

### Emails not sending
- Verify RESEND_API_KEY is correct
- Check email domain is verified in Resend
- Look at application logs for error messages

## Development Workflow

1. Make changes to code
2. Flask will auto-reload (if debug mode enabled)
3. Test in browser
4. Commit and push to GitHub
5. Vercel will auto-deploy

## Debugging
To see detailed logs:
```bash
export FLASK_DEBUG=1
python app.py
```

## Next Steps
- Read DEPLOYMENT_GUIDE.md for Vercel deployment
- Check README.md for feature documentation
- Review code comments for implementation details
