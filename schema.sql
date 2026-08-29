-- Web Intern Platform Database Schema (PostgreSQL & SQLite compatible)

CREATE TABLE IF NOT EXISTS profiles (
  id VARCHAR(36) PRIMARY KEY,
  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  phone_country_code TEXT DEFAULT '+91',
  college TEXT,
  avatar_url TEXT,
  marketing_opt_in BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
  id VARCHAR(36) PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  full_name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS otp_codes (
  id VARCHAR(36) PRIMARY KEY,
  email TEXT NOT NULL,
  code_hash TEXT NOT NULL,
  purpose TEXT NOT NULL, -- 'register' | 'login'
  expires_at TIMESTAMP NOT NULL,
  consumed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sectors (
  id VARCHAR(36) PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  icon_url TEXT,
  description TEXT
);

CREATE TABLE IF NOT EXISTS internships (
  id VARCHAR(36) PRIMARY KEY,
  sector_id VARCHAR(36) REFERENCES sectors(id),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  short_description TEXT,
  full_description TEXT,
  duration_weeks INT DEFAULT 4,
  mode TEXT DEFAULT 'Virtual',
  cover_image_url TEXT,
  is_featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS internship_tasks (
  id VARCHAR(36) PRIMARY KEY,
  internship_id VARCHAR(36) REFERENCES internships(id) ON DELETE CASCADE,
  week_number INT NOT NULL,
  title TEXT NOT NULL,
  objective TEXT,
  deliverables TEXT,
  key_steps TEXT, -- JSON string or comma-separated steps
  evaluation_criteria TEXT
);

CREATE TABLE IF NOT EXISTS applications (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) REFERENCES profiles(id) ON DELETE CASCADE,
  internship_id VARCHAR(36) REFERENCES internships(id),
  status TEXT DEFAULT 'active', -- active, completed, withdrawn
  offer_letter_sent BOOLEAN DEFAULT FALSE,
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS submissions (
  id VARCHAR(36) PRIMARY KEY,
  application_id VARCHAR(36) REFERENCES applications(id) ON DELETE CASCADE,
  week_number INT NOT NULL,
  file_url TEXT,
  status TEXT DEFAULT 'pending', -- pending, approved, revise
  feedback TEXT,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reviewed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS certificates (
  id VARCHAR(36) PRIMARY KEY,
  application_id VARCHAR(36) REFERENCES applications(id),
  certificate_url TEXT,
  is_verified_paid BOOLEAN DEFAULT FALSE,
  issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(36) PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price_inr INT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS payments (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) REFERENCES profiles(id),
  certificate_id VARCHAR(36) REFERENCES certificates(id),
  product_id VARCHAR(36) REFERENCES products(id),
  razorpay_order_id TEXT NOT NULL,
  razorpay_payment_id TEXT,
  razorpay_signature TEXT,
  amount_inr INT NOT NULL,
  status TEXT DEFAULT 'created', -- created, paid, failed, refunded
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS newsletter_subscribers (
  id VARCHAR(36) PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS testimonials (
  id VARCHAR(36) PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT,
  quote TEXT NOT NULL,
  rating INT DEFAULT 5,
  photo_url TEXT,
  source_link TEXT,
  is_published BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS site_stats (
  id VARCHAR(36) PRIMARY KEY,
  label TEXT NOT NULL,
  value TEXT NOT NULL,
  icon_name TEXT,
  sort_order INT DEFAULT 0
);
