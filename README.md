# Web Intern — Virtual Internship Platform

**Web Intern** is a full-stack virtual internship platform enabling students to browse internships by sector, apply instantly, receive official offer letters via email, complete weekly project deliverables, receive admin evaluations, and earn verified certificates of completion.

## 🚀 Features

- **Frontend**: Pure Vanilla HTML5, CSS3, and JavaScript SPA router (no React, Node.js, or Vite). Custom Blue/White design system (`#0B3D91`, `#082B66`, `#2E7DFF`, `#EAF1FB`), dynamic hero collage, 2x2 stats grid, marquee ticker, auto-scrolling testimonials, and full mobile hamburger nav panel.
- **Backend**: Python Flask REST API with modular blueprint architecture.
- **Database**: Flexible dual-mode storage using SQLite locally and Supabase PostgreSQL in production.
- **Authentication**: Custom JWT access tokens + bcrypt admin hashing + 6-digit email OTP codes via Resend.
- **Automated PDF Generation**: ReportLab PDF generator for official Offer Letters and Completion Certificates.
- **Payments**: Razorpay integration for optional verified & printed certificate upgrades (order creation + server-side HMAC signature verification).

## 🛠️ Setup & Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/awsmohanakannan-art/webintern.git
   cd webintern
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your web browser.

## 🔑 Admin Credentials

- **Email**: `admin@webintern.com`
- **Password**: `admin123`
