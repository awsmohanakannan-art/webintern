import sqlite3
import uuid
import json
import os
import bcrypt
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    conn.commit()

    # Check if seed data exists
    cursor.execute("SELECT COUNT(*) FROM sectors")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()

    conn.close()

def seed_data(cursor):
    # Admin Seed
    admin_id = str(uuid.uuid4())
    hashed_pwd = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "INSERT INTO admins (id, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
        (admin_id, "admin@webintern.com", hashed_pwd, "Platform Administrator")
    )

    # Sectors Seed
    sectors = [
        ("Full Stack Development", "full-stack-development", "code", "Build modern web apps using HTML, CSS, JavaScript, Python, and cloud tools."),
        ("Data Science & AI", "data-science-ai", "cpu", "Analyze datasets, build machine learning models, and derive actionable business insights."),
        ("UI/UX & Product Design", "ui-ux-design", "layout", "Design intuitive interfaces, create interactive wireframes, and run usability tests."),
        ("Digital Marketing & SEO", "digital-marketing", "trending-up", "Drive brand growth, execute performance campaigns, and master social media strategy.")
    ]
    
    sector_ids = {}
    for name, slug, icon, desc in sectors:
        s_id = str(uuid.uuid4())
        sector_ids[slug] = s_id
        cursor.execute(
            "INSERT INTO sectors (id, name, slug, icon_url, description) VALUES (?, ?, ?, ?, ?)",
            (s_id, name, slug, icon, desc)
        )

    # Internships Seed
    internships = [
        (
            sector_ids["full-stack-development"],
            "Full Stack Web Developer Internship",
            "full-stack-web-developer",
            "Master frontend development, Python backend APIs, database management, and cloud deployment in a hands-on 4-week virtual simulation.",
            "This 4-week Virtual Internship guides you through real-world web application development. You will design responsive user interfaces using HTML5/CSS3/JavaScript, build scalable backend REST APIs with Python Flask, integrate Supabase PostgreSQL databases, and deploy your production web app to cloud hosting platforms.",
            4, "Virtual", "web-dev-cover.jpg", True
        ),
        (
            sector_ids["data-science-ai"],
            "Data Analytics & Machine Learning Virtual Internship",
            "data-analytics-machine-learning",
            "Work with real-world datasets, build predictive algorithms, and create executive analytics dashboards using Python and pandas.",
            "Dive deep into data analysis, exploratory data visualization, statistical hypothesis testing, and machine learning models. Over 4 weeks, you will clean raw industry datasets, engineer predictive features, build automated visualization dashboards, and report findings.",
            4, "Virtual", "data-science-cover.jpg", True
        ),
        (
            sector_ids["ui-ux-design"],
            "UI/UX Product Design Internship",
            "ui-ux-product-design",
            "Design user journeys, create high-fidelity UI prototypes, establish color/typography systems, and perform user research.",
            "Transform business concepts into high-converting, accessible user interfaces. You will create user personas, wireframe mobile and desktop layouts, establish component design systems, and prototype interactive app flows.",
            4, "Virtual", "ui-ux-cover.jpg", True
        ),
        (
            sector_ids["digital-marketing"],
            "Performance Marketing & SEO Internship",
            "performance-marketing-seo",
            "Learn digital advertising strategies, content marketing pipelines, Google SEO optimization, and social media analytics.",
            "Gain practical exposure to growth hacking, search engine optimization, pay-per-click ad campaign management, and digital marketing analytics. Craft copy, analyze conversion metrics, and optimize campaigns.",
            4, "Virtual", "marketing-cover.jpg", True
        )
    ]

    internship_ids = {}
    for sec_id, title, slug, short_desc, full_desc, duration, mode, cover, featured in internships:
        i_id = str(uuid.uuid4())
        internship_ids[slug] = i_id
        cursor.execute(
            "INSERT INTO internships (id, sector_id, title, slug, short_description, full_description, duration_weeks, mode, cover_image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (i_id, sec_id, title, slug, short_desc, full_desc, duration, mode, cover, featured)
        )

    # Weekly Tasks for Full Stack Internship
    fs_tasks = [
        (1, "Week 1: Responsive UI & Component Design", "Design and develop a responsive landing page following modern UI guidelines.", "Submit a ZIP file containing index.html, main.css, and assets with full mobile responsiveness.", "1. Create HTML structure.\n2. Apply CSS variables & flexbox/grid layout.\n3. Add mobile navigation and smooth animations.\n4. Test cross-browser compatibility.", "Code formatting, responsive breakpoint alignment, color hierarchy compliance."),
        (2, "Week 2: Backend REST API Construction", "Build a Python Flask REST API with JSON responses and database CRUD operations.", "Upload Python API code files (app.py, routes, schema) along with API test documentation.", "1. Define Flask application blueprints.\n2. Connect to database storage.\n3. Implement authentication & data endpoints.\n4. Handle error states cleanly.", "Clean API routing, proper HTTP status codes, error handling."),
        (3, "Week 3: Database & Auth Integration", "Integrate user authentication via JWT & email OTP codes with database persistence.", "Submit backend auth module and video demo or screenshot proof of registration/login flow.", "1. Implement OTP generation logic.\n2. Hash credentials securely.\n3. Issue signed JWT tokens.\n4. Add protected route middleware.", "Security of JWT tokens, password/OTP hashing integrity, session management."),
        (4, "Week 4: Final Platform Deployment & Capstone", "Deploy the full-stack web application to production and submit project documentation.", "Live application deployment URL, source code repository link, and final project report PDF.", "1. Configure environment variables.\n2. Perform end-to-end integration testing.\n3. Deploy frontend and backend.\n4. Write complete README and documentation.", "System functionality, live deployment stability, code documentation quality.")
    ]

    for week, title, obj, deliv, steps, criteria in fs_tasks:
        cursor.execute(
            "INSERT INTO internship_tasks (id, internship_id, week_number, title, objective, deliverables, key_steps, evaluation_criteria) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), internship_ids["full-stack-web-developer"], week, title, obj, deliv, steps, criteria)
        )

    # Site Stats Seed (Section 4A 2x2 Grid)
    stats = [
        ("Happy Users", "1 Lakh+", "users", 1),
        ("Job-Role Match Rate", "97%", "target", 2),
        ("Skill Improvement", "98%", "trending-up", 3),
        ("Verified Program", "Web Intern", "shield-check", 4)
    ]
    for label, val, icon, order in stats:
        cursor.execute(
            "INSERT INTO site_stats (id, label, value, icon_name, sort_order) VALUES (?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), label, val, icon, order)
        )

    # Products Seed (Certificate Upgrade)
    cursor.execute(
        "INSERT INTO products (id, name, description, price_inr, is_active) VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), "Verified & Printed Certificate Upgrade", "Get an official tamper-proof QR-verified digital certificate with optional high-quality physical hardcopy delivery to your doorstep.", 499, True)
    )

    # Testimonials Seed
    testimonials = [
        ("Ananya Sharma", "Full Stack Intern", "Web Intern gave me hands-on practical project experience! Receiving my offer letter immediately and working through weekly tasks prepared me directly for software developer interviews.", 5, "avatar1.jpg"),
        ("Rahul Verma", "Data Analytics Intern", "The weekly task evaluations and detailed admin feedback were invaluable. I earned a verified certificate that I proudly showcased on my LinkedIn profile!", 5, "avatar2.jpg"),
        ("Priya Nair", "UI/UX Design Intern", "Building real portfolio projects with real feedback completely transformed my confidence as a product designer. Highly recommended for students!", 5, "avatar3.jpg")
    ]
    for name, role, quote, rating, photo in testimonials:
        cursor.execute(
            "INSERT INTO testimonials (id, name, role, quote, rating, photo_url, is_published) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), name, role, quote, rating, photo, True)
        )

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (dict(rv[0]) if rv else None) if one else [dict(r) for r in rv]

def execute_db(query, args=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id
