# Web Intern Platform - Deployment Guide

## Overview
This is a Flask-based application with integrations for:
- Supabase (Database & Authentication)
- Google OAuth 2.0
- Razorpay (Payments)
- Resend (Email)
- Google Sheets Integration

## Critical Fix
All hardcoded credentials have been removed from `config.py`. The application now REQUIRES environment variables to be set on your deployment platform.

## Deployment to Vercel

### Prerequisites
1. GitHub account with this repository
2. Vercel account (vercel.com)
3. All API credentials ready:
   - Supabase: URL, Anon Key, Service Role Key
   - Google OAuth: Client ID, Client Secret
   - Razorpay: Key ID, Key Secret, Webhook Secret
   - Resend: API Key
   - Google Sheets: Webhook URL

### Step-by-Step Deployment

#### 1. Create Vercel Project
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from your local directory
vercel
```

Or use Vercel Dashboard:
1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Select your GitHub repository
4. Import the project

#### 2. Set Environment Variables
In Vercel Dashboard → Project Settings → Environment Variables, add all these:

```
JWT_SECRET=your_jwt_secret_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
RESEND_API_KEY=re_xxxxxxxxxx
RAZORPAY_KEY_ID=rzp_live_xxxx
RAZORPAY_KEY_SECRET=your_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/your_script_id/exec
```

#### 3. Deploy
```bash
vercel --prod
```

Or trigger deployment automatically from GitHub:
- Push to `main` branch → Automatic deployment

### Troubleshooting

**Error: "Missing environment variable"**
- Go to Vercel Dashboard
- Check Project Settings → Environment Variables
- Ensure ALL required variables are set
- Redeploy with `vercel --prod`

**Error: "Cannot POST /api/auth/signup"**
- This usually means the backend isn't running
- Check Vercel Deployments → Recent deployment logs
- Look for startup errors

**Google OAuth not working**
- Verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are correct
- In Google Cloud Console, add your Vercel URL to "Authorized redirect URIs"
- Format: `https://your-domain.vercel.app/api/auth/google/callback`

**Razorpay payments failing**
- Verify RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
- Check if using live keys (start with `rzp_live_`) or test keys
- Ensure Webhook URL is registered in Razorpay Dashboard

**Database connection issues**
- Verify SUPABASE_URL is correct (should be https://xxxx.supabase.co)
- Test Supabase connection from dashboard
- Check if IP is whitelisted (if applicable)

## Local Development

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from .env.example
cp .env.example .env

# Update .env with your local credentials
```

### Running Locally
```bash
python app.py
```
App runs on http://localhost:5000

## Frontend Integration

Ensure your frontend (React/Vue/etc) is configured to use:
- **Development**: `http://localhost:5000/api`
- **Production**: `https://your-domain.vercel.app/api`

## Security Checklist

- [ ] All credentials in `.env` (NOT in code)
- [ ] `.env` added to `.gitignore`
- [ ] No sensitive data in commits (use `git-secrets`)
- [ ] HTTPS enabled (Vercel provides by default)
- [ ] CORS properly configured for your frontend domain
- [ ] Razorpay webhook secret secured
- [ ] Database backups enabled (Supabase)
- [ ] Google OAuth redirect URIs updated

## Support
If deployment issues persist:
1. Check Vercel Deployments logs
2. Review this guide's troubleshooting section
3. Verify all env variables are set
4. Test API endpoints with Postman
