# GitHub & Vercel Integration Setup

## Objective
Push your Web Intern project to GitHub with proper security, then auto-deploy to Vercel.

## Part 1: Push to GitHub

### If creating a NEW repository:

1. **Create repository on GitHub**
   - Go to https://github.com/new
   - Repository name: `webintern` (or your preferred name)
   - Description: "Web Intern Platform - Online internship & certificate management"
   - Visibility: Private (recommended) or Public
   - Click "Create repository"

2. **Initialize Git locally**
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

3. **Connect to remote and push**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/webintern.git
   git branch -M main
   git add .
   git commit -m "Initial commit: Web Intern Platform with Vercel deployment setup"
   git push -u origin main
   ```

### If updating existing repository:

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Stage all changes**
   ```bash
   git add .
   ```

3. **Review changes**
   ```bash
   git status
   ```

4. **Commit**
   ```bash
   git commit -m "Fix: Remove hardcoded credentials and add Vercel deployment configuration"
   ```

5. **Push to GitHub**
   ```bash
   git push origin main
   ```

## Part 2: Connect to Vercel

### Option A: Use Vercel Dashboard (Recommended)

1. **Go to Vercel**
   - Visit https://vercel.com/dashboard
   - Sign in (or create free account)

2. **Import Project**
   - Click "Add New" → "Project"
   - Select "Import Git Repository"
   - Choose your GitHub account
   - Search and select `webintern` repository
   - Click "Import"

3. **Configure Environment Variables**
   - You'll see "Environment Variables" section
   - Add each variable with its value:
   
   ```
   JWT_SECRET = your_jwt_secret_here
   SUPABASE_URL = https://your-project.supabase.co
   SUPABASE_ANON_KEY = your_anon_key
   SUPABASE_SERVICE_ROLE_KEY = your_service_role_key
   GOOGLE_CLIENT_ID = xxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET = your_secret
   RESEND_API_KEY = re_xxxxxxxxxx
   RAZORPAY_KEY_ID = rzp_live_xxxxx
   RAZORPAY_KEY_SECRET = your_secret
   RAZORPAY_WEBHOOK_SECRET = your_webhook_secret
   GOOGLE_SHEETS_WEBHOOK_URL = https://script.google.com/macros/s/xxxxx/exec
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for build to complete
   - You'll get a URL like: `https://webintern-xxxx.vercel.app`

### Option B: Use Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Link project**
   ```bash
   vercel link
   ```
   - Select "Create new project" or choose existing
   - Follow prompts

4. **Add environment variables**
   ```bash
   vercel env add JWT_SECRET
   vercel env add SUPABASE_URL
   # ... repeat for all variables
   ```

5. **Deploy**
   ```bash
   vercel --prod
   ```

## Part 3: Post-Deployment Configuration

### Update Google OAuth Redirect URI

1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Click your OAuth 2.0 Client ID
4. Add to "Authorized redirect URIs":
   ```
   https://your-vercel-domain.vercel.app/api/auth/google/callback
   https://your-custom-domain.com/api/auth/google/callback (if you have custom domain)
   ```
5. Save

### Configure Razorpay Webhook

1. Go to Razorpay Dashboard
2. Settings → Webhooks
3. Add new webhook:
   - URL: `https://your-vercel-domain.vercel.app/api/payment/webhook`
   - Events: Select payment-related events
   - Active: Checked
4. Save and copy webhook ID
5. Update `RAZORPAY_WEBHOOK_SECRET` in Vercel env vars if needed

### Update Frontend API Endpoint

In your frontend code (React/Vue/etc), update API URLs:

```javascript
// From
const API = "http://localhost:5000/api";

// To
const API = "https://your-vercel-domain.vercel.app/api";

// Or use environment variable
const API = process.env.REACT_APP_API_URL || "/api";
```

### Test Deployment

1. Visit: `https://your-vercel-domain.vercel.app`
2. Try signing up
3. Try Google OAuth login
4. Check Vercel logs if any errors

## Part 4: GitHub Actions (Optional - Auto-deploy)

Vercel automatically deploys when you push to GitHub. To add extra validation:

Create `.github/workflows/test.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: python -m py_compile app.py config.py wsgi.py
```

## Troubleshooting Deployment

### Build Failed
1. Check Vercel Deployments → Build Logs
2. Common issues:
   - Missing dependencies → Update requirements.txt
   - Python version → Update in vercel.json
   - Missing env vars → Add to Vercel dashboard

### Environment Variables Not Loading
1. Verify all env vars are added in Vercel dashboard
2. Redeploy after adding vars
3. Check app logs with: `vercel logs`

### Cannot Sign Up / Google OAuth Failed
1. Check Google Cloud Console - verify redirect URI
2. Test with: `curl https://your-domain.vercel.app/api/auth/status`
3. Check Vercel logs for error details

### Database Connection Errors
1. Verify SUPABASE_URL format (should be https://xxxx.supabase.co)
2. Test Supabase connection from Supabase dashboard
3. Ensure service role key has database access

## Monitoring & Logs

### View Vercel Logs
```bash
vercel logs --tail
```

### View Deployment History
```bash
vercel list
```

### Rollback to Previous Version
```bash
vercel rollback
```

## Custom Domain (Optional)

1. In Vercel dashboard → Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed
4. Update Google OAuth redirect URI
5. Update Razorpay webhook URL

## Success Indicators

✅ Deployment complete when:
- URL shows green checkmark in Vercel dashboard
- You can visit your domain
- Signup form appears
- Google OAuth button works
- No error in browser console

## Next Steps

1. Share your deployed URL with team
2. Test all features thoroughly
3. Set up production database backups
4. Monitor analytics in Vercel dashboard
5. Keep dependencies updated regularly

---

**Need Help?**
- Check Vercel docs: https://vercel.com/docs
- Check Flask docs: https://flask.palletsprojects.com
- Review DEPLOYMENT_GUIDE.md in this repo
