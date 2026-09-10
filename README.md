# Web Intern Platform

A complete online internship and certificate management system with payment integration, built with Flask, Supabase, and modern web technologies.

## Features

✅ **User Authentication**
- Email/Password signup and login
- Google OAuth 2.0 integration
- JWT-based session management
- Password reset functionality

✅ **Internship Management**
- Browse available internships by sector
- Apply for internships
- Track application status
- Submit work assignments

✅ **Certificate System**
- Generate digital certificates
- Track certificate status
- Send certificates via email
- Download certificate PDFs

✅ **Payment Integration**
- Razorpay payment gateway
- Secure payment processing
- Invoice generation
- Payment history tracking

✅ **Email Notifications**
- Signup confirmation
- Application updates
- Certificate delivery
- Payment receipts

✅ **Admin Dashboard**
- User management
- Payment management
- Certificate tracking
- System analytics

## Tech Stack

**Backend:**
- Flask (Python web framework)
- Supabase (Database & Auth)
- JWT (Session management)
- SQLite (Local fallback)

**Integrations:**
- Google OAuth 2.0
- Razorpay (Payments)
- Resend (Email)
- Google Sheets (Data sync)

**Deployment:**
- Vercel (Serverless hosting)
- GitHub (Version control)

## Quick Start

### Local Development

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd webintern
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run locally:**
   ```bash
   python app.py
   ```
   Visit: http://localhost:5000

See **SETUP.md** for detailed credential setup instructions.

### Deploy to Vercel

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Import to Vercel:**
   - Visit https://vercel.com/dashboard
   - Click "Add New Project"
   - Select your GitHub repository
   - Add environment variables (see SETUP.md)
   - Click "Deploy"

See **GITHUB_SETUP.md** for detailed deployment steps.

## Environment Variables

Required for deployment:

```
JWT_SECRET                    # JWT signing secret
SUPABASE_URL                 # Supabase project URL
SUPABASE_ANON_KEY           # Supabase anonymous key
SUPABASE_SERVICE_ROLE_KEY   # Supabase service role key
GOOGLE_CLIENT_ID            # Google OAuth client ID
GOOGLE_CLIENT_SECRET        # Google OAuth client secret
RESEND_API_KEY              # Resend email API key
RAZORPAY_KEY_ID             # Razorpay API key ID
RAZORPAY_KEY_SECRET         # Razorpay API key secret
RAZORPAY_WEBHOOK_SECRET     # Razorpay webhook secret
GOOGLE_SHEETS_WEBHOOK_URL   # Google Apps Script webhook URL
```

See **.env.example** for template.

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/google/callback` - Google OAuth callback
- `POST /api/auth/forgot-password` - Request password reset
- `GET /api/auth/me` - Get current user

### Payments
- `POST /api/payment/create-order` - Create payment order
- `POST /api/payment/verify` - Verify payment
- `POST /api/payment/webhook` - Payment webhook

### Certificates
- `GET /api/certificates` - List user certificates
- `POST /api/certificates/generate` - Generate certificate
- `GET /api/certificates/:id` - Get certificate details

### Admin
- `GET /api/admin/users` - List all users
- `GET /api/admin/payments` - List all payments
- `GET /api/admin/certificates` - List all certificates

See **QUICK_REFERENCE.md** for complete API list.

## Project Structure

```
webintern/
├── app.py                 # Main Flask application
├── config.py              # Configuration (environment-based)
├── wsgi.py                # Vercel WSGI entry point
├── database.py            # Database initialization
├── vercel.json            # Vercel deployment config
│
├── routes/
│   ├── auth_routes.py        # Authentication endpoints
│   ├── payment_routes.py      # Payment endpoints
│   ├── certificate_routes.py  # Certificate endpoints
│   ├── admin_routes.py        # Admin endpoints
│   └── ...
│
├── static/                # Frontend files
│   ├── index.html
│   ├── css/
│   └── js/
│
├── public/
│   └── templates/        # Document templates
│
├── storage/              # Generated certificates & offers
│
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore patterns
│
└── docs/
    ├── SETUP.md                    # Local setup guide
    ├── DEPLOYMENT_GUIDE.md         # Deployment instructions
    ├── GITHUB_SETUP.md            # GitHub & Vercel guide
    ├── DEPLOYMENT_CHECKLIST.md    # Pre/post deployment checks
    ├── QUICK_REFERENCE.md         # Commands & URLs
    └── CHANGES_MADE.md            # Summary of changes
```

## Documentation

- **[SETUP.md](SETUP.md)** - Local development setup
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - How to deploy
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - Git & Vercel integration
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Deployment checklist
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands & quick links
- **[CHANGES_MADE.md](CHANGES_MADE.md)** - Recent changes summary

## Security

✅ **Best Practices Implemented:**
- No hardcoded credentials in code
- Environment variables for all secrets
- JWT-based authentication
- Password hashing with bcrypt
- HTTPS enforced (Vercel default)
- CORS properly configured
- SQL injection prevention
- Secure session management

❌ **Never:**
- Commit `.env` files
- Share API keys
- Use test credentials in production
- Expose error details to users

## Troubleshooting

### App won't start locally
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+

# Verify .env exists
ls -la .env
```

### Port 5000 in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows (find PID then taskkill)
```

### Deployment fails
1. Check Vercel build logs
2. Verify all env variables are set
3. Test locally first
4. See **DEPLOYMENT_GUIDE.md** troubleshooting section

### Features not working
1. Clear browser cache
2. Check browser console for errors
3. Verify API credentials
4. Review Vercel function logs
5. See **DEPLOYMENT_CHECKLIST.md** verification steps

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test locally
3. Commit: `git commit -am 'Add feature'`
4. Push: `git push origin feature/my-feature`
5. Create pull request

## Support & Feedback

- Check documentation in `/docs` folder
- Review error messages carefully
- Check Vercel/Supabase dashboards
- Test each feature individually

## License

[Your License Here]

## Next Steps

1. **First time?** Start with [SETUP.md](SETUP.md)
2. **Ready to deploy?** Follow [GITHUB_SETUP.md](GITHUB_SETUP.md)
3. **Deploying?** Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
4. **Quick help?** Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Status**: ✅ Ready for Deployment

**Last Updated**: September 2026

**Questions?** Refer to the documentation above or check the error logs.
