# Quick Reference - Commands & URLs

## Local Development

### Start Application
```bash
source venv/bin/activate  # macOS/Linux
python app.py
```

App runs at: http://localhost:5000

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
python -m pytest tests/
```

### Generate JWT Secret
```bash
# macOS/Linux
openssl rand -hex 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

## Git Commands

### Initial Setup
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Push to GitHub
```bash
git add .
git status
git commit -m "Your message"
git push origin main
```

### Check for Secrets
```bash
git log --all -p | grep -i "password\|secret\|key"
```

## Vercel Deployment

### Deploy with CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

### View Logs
```bash
vercel logs --tail
```

### Rollback
```bash
vercel rollback
```

### View Deployments
```bash
vercel list
```

## API Endpoints

### Authentication
```
POST   /api/auth/signup              - Create new user
POST   /api/auth/login               - Login user
GET    /api/auth/google/callback     - Google OAuth callback
POST   /api/auth/forgot-password     - Request password reset
POST   /api/auth/reset-password      - Reset password
GET    /api/auth/me                  - Get current user
```

### Payments
```
POST   /api/payment/create-order     - Create Razorpay order
POST   /api/payment/verify           - Verify payment
POST   /api/payment/webhook          - Razorpay webhook
GET    /api/payment/status/:id       - Get payment status
```

### Certificates
```
GET    /api/certificates             - Get user certificates
POST   /api/certificates/generate    - Generate certificate
GET    /api/certificates/:id         - Get certificate details
POST   /api/certificates/:id/send    - Send certificate email
```

### Admin
```
GET    /api/admin/users              - List all users
GET    /api/admin/payments           - List all payments
GET    /api/admin/certificates       - List all certificates
```

## Environment Variables Required

```
JWT_SECRET                    # 32+ character random string
SUPABASE_URL                 # https://xxxx.supabase.co
SUPABASE_ANON_KEY           # JWT token from Supabase
SUPABASE_SERVICE_ROLE_KEY   # Service role JWT token
GOOGLE_CLIENT_ID            # Google OAuth client ID
GOOGLE_CLIENT_SECRET        # Google OAuth secret
RESEND_API_KEY              # Resend email API key
RAZORPAY_KEY_ID             # Razorpay Key ID
RAZORPAY_KEY_SECRET         # Razorpay Key Secret
RAZORPAY_WEBHOOK_SECRET     # Razorpay webhook secret
GOOGLE_SHEETS_WEBHOOK_URL   # Google Apps Script URL
```

## Third-Party Service URLs

- Supabase: https://supabase.com
- Google Cloud: https://console.cloud.google.com
- Razorpay: https://dashboard.razorpay.com
- Resend: https://resend.com
- Vercel: https://vercel.com
- GitHub: https://github.com

## File Structure

```
webintern/
├── app.py                 # Main Flask application
├── config.py              # Configuration (uses env vars)
├── wsgi.py                # WSGI entry point for Vercel
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel deployment config
├── .env                   # Local env vars (NOT committed)
├── .env.example           # Template (committed)
├── .gitignore             # Git ignore patterns
├── routes/                # API route blueprints
├── static/                # Frontend files (HTML/CSS/JS)
├── public/                # Static assets
├── storage/               # Generated documents
└── database.py            # Database initialization
```

## Troubleshooting Commands

### Check Python Installation
```bash
python --version
pip --version
```

### Check Port Usage (5000)
```bash
# macOS/Linux
lsof -i :5000

# Windows CMD
netstat -ano | findstr :5000
```

### Clear Python Cache
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Test Flask App
```bash
python -c "from app import create_app; app = create_app(); print('✓ App loaded')"
```

### Test Supabase Connection
```bash
python -c "
from config import Config
from supabase import create_client
client = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)
print('✓ Connected to Supabase')
"
```

## Common Error Solutions

### Module Not Found
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
# macOS/Linux - Kill process on 5000
lsof -ti:5000 | xargs kill -9

# Windows - Kill process on 5000
taskkill /PID <PID> /F
```

### Env Variables Not Loading
1. Check `.env` exists in root
2. Restart Flask: `python app.py`
3. Verify no typos in env var names

### Database Connection Failed
1. Verify SUPABASE_URL is correct
2. Check SUPABASE_ANON_KEY
3. Test URL in browser

### Google OAuth Not Working
1. Add redirect URI to Google Cloud Console
2. Verify CLIENT_ID and CLIENT_SECRET
3. Check OAuth consent screen published

### Razorpay Payments Failing
1. Use test keys (start with rzp_test_)
2. Verify webhook secret
3. Test with card: 4111 1111 1111 1111

## Deployment Workflow

1. **Develop Locally**
   ```bash
   python app.py
   ```

2. **Test Features**
   - Signup, login, OAuth
   - Payments, certificates
   - Email notifications

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Feature: Add X functionality"
   git push origin main
   ```

4. **Verify on Vercel**
   - Check Vercel dashboard
   - Test production features
   - Monitor logs

5. **Share URL**
   - Deployment URL: `https://webintern-xxxx.vercel.app`
   - Send to team/clients

## Performance Monitoring

### View Real-time Logs
```bash
vercel logs --tail
```

### Check Build Time
- Visit Vercel dashboard → Deployments
- Look at "Build time" column

### Monitor Function Execution
- Vercel dashboard → Analytics
- Check response times, error rates

## Security Checklist

- [ ] No secrets in code
- [ ] `.env` not committed
- [ ] HTTPS enabled (Vercel default)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled (if applicable)
- [ ] Sensitive data encrypted in DB

## Support Resources

- **Flask Docs**: https://flask.palletsprojects.com
- **Supabase Docs**: https://supabase.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Razorpay Docs**: https://razorpay.com/docs
- **Resend Docs**: https://resend.com/docs

---

**Last Updated**: September 2026
