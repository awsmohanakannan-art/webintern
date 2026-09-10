# Pre-Deployment Checklist

## Security & Credentials ✓

- [ ] All hardcoded credentials removed from `config.py` ✅ (Already done)
- [ ] `.env` file is in `.gitignore` ✅ (Already updated)
- [ ] `.env.example` shows template values (no real secrets)
- [ ] No secrets will be committed to GitHub
- [ ] All API keys are in `.env` (local) or Vercel env vars (production)

## Code Quality

- [ ] No Python syntax errors
  ```bash
  python -m py_compile app.py config.py wsgi.py
  ```
- [ ] Flask imports work correctly
  ```bash
  python -c "from app import create_app; print('OK')"
  ```
- [ ] All routes are registered
  ```bash
  python -c "from app import app; print(len(app.url_map._rules))"
  ```

## Dependencies

- [ ] `requirements.txt` is up to date
- [ ] All production packages included:
  - flask, gunicorn, wsgi ✅
  - supabase, razorpay, resend ✅
- [ ] Test locally: `pip install -r requirements.txt`

## Configuration Files

- [ ] ✅ `vercel.json` created with proper Python 3.11 runtime
- [ ] ✅ `wsgi.py` created as entry point
- [ ] ✅ `config.py` updated to require env vars (no defaults)
- [ ] ✅ `.gitignore` updated with `.env`

## Environment Variables - Collect These Now

Before deployment, gather:

```
[ ] JWT_SECRET (32+ random characters)
[ ] SUPABASE_URL (https://xxxx.supabase.co)
[ ] SUPABASE_ANON_KEY (long jwt token)
[ ] SUPABASE_SERVICE_ROLE_KEY (long jwt token)
[ ] GOOGLE_CLIENT_ID (xxx.apps.googleusercontent.com)
[ ] GOOGLE_CLIENT_SECRET (secret key)
[ ] RESEND_API_KEY (re_xxxxxxxxxx)
[ ] RAZORPAY_KEY_ID (rzp_live_xxxxx)
[ ] RAZORPAY_KEY_SECRET (secret key)
[ ] RAZORPAY_WEBHOOK_SECRET (secret key)
[ ] GOOGLE_SHEETS_WEBHOOK_URL (https://script.google.com/macros/s/xxxxx/exec)
```

## GitHub Preparation

- [ ] Git configured:
  ```bash
  git config user.name "Your Name"
  git config user.email "your@email.com"
  ```
- [ ] All changes staged:
  ```bash
  git add .
  git status  # Review what will be committed
  ```
- [ ] Ready to commit:
  ```bash
  git commit -m "Fix: Remove hardcoded credentials and add Vercel deployment setup"
  ```

## Vercel Setup

### Create Vercel Account
- [ ] Account created at vercel.com
- [ ] GitHub account linked to Vercel

### Import Repository
- [ ] Repository imported to Vercel dashboard
- [ ] Project created and configured

### Environment Variables Added
- [ ] All 11 env vars added to Vercel dashboard
- [ ] No env var left blank
- [ ] Double-checked for typos

### Deployment
- [ ] Initial deployment triggered
- [ ] Build succeeded (green checkmark)
- [ ] URL assigned: `https://webintern-xxxxx.vercel.app`

## Post-Deployment Verification

### Backend API Tests
```bash
# Test API is running
curl https://your-vercel-domain.vercel.app/api/auth/status

# Test signup endpoint
curl -X POST https://your-vercel-domain.vercel.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!", "full_name": "Test"}'
```

- [ ] API is responding
- [ ] No 500 errors
- [ ] Check Vercel logs for warnings

### Frontend Tests
- [ ] [ ] Visit `https://your-vercel-domain.vercel.app`
- [ ] [ ] Page loads (no 404)
- [ ] [ ] No JavaScript errors in browser console
- [ ] [ ] Signup form appears
- [ ] [ ] All buttons clickable

### Google OAuth
- [ ] [ ] "Sign in with Google" button visible
- [ ] [ ] Redirect URI added to Google Cloud Console:
  ```
  https://your-vercel-domain.vercel.app/api/auth/google/callback
  ```
- [ ] [ ] Test login flow

### Razorpay Payments
- [ ] [ ] "Buy Certificate" button visible
- [ ] [ ] Razorpay modal opens
- [ ] [ ] Test card details accepted:
  - Card: 4111 1111 1111 1111
  - Expiry: Any future date
  - CVV: Any 3 digits
- [ ] [ ] Webhook URL registered in Razorpay:
  ```
  https://your-vercel-domain.vercel.app/api/payment/webhook
  ```
- [ ] [ ] Payment webhook configured with secret

### Email Tests
- [ ] [ ] Signup email received
- [ ] [ ] Verification email received
- [ ] [ ] Email comes from configured domain

### Database
- [ ] [ ] Test user created in Supabase
- [ ] [ ] Data persists after page reload
- [ ] [ ] No connection errors in logs

## Final Checks

- [ ] No hardcoded credentials in git history
  ```bash
  git log --all -p | grep -i "password\|secret\|key\|token"
  ```
- [ ] `.env` file not committed
  ```bash
  git ls-files | grep ".env"  # Should be empty
  ```
- [ ] All features working end-to-end
- [ ] No console errors in browser
- [ ] No errors in Vercel deployment logs

## Troubleshooting

If deployment fails, check:

1. **Build Errors**
   - View Vercel Deployments → Build Logs
   - Check Python version compatibility
   - Verify requirements.txt is complete

2. **Runtime Errors**
   - Check Vercel Function Logs
   - Look for missing environment variables
   - Verify database connectivity

3. **Feature Not Working**
   - Clear browser cache
   - Check browser console for errors
   - Verify API endpoints returning data
   - Check third-party service credentials

## Production Readiness

When all checks pass:

- [ ] Deployment is stable (24+ hours)
- [ ] No errors in logs
- [ ] All features tested
- [ ] Team aware of deployment
- [ ] Monitoring/alerts configured (optional)
- [ ] Backup plan documented

## Celebration 🎉

✅ Your Web Intern Platform is now live!

Share your deployment:
- Frontend: `https://your-vercel-domain.vercel.app`
- API: `https://your-vercel-domain.vercel.app/api`

---

**Questions?** Refer to:
- DEPLOYMENT_GUIDE.md - Detailed deployment steps
- SETUP.md - Local development setup
- GITHUB_SETUP.md - GitHub & Vercel integration
