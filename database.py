import sqlite3
import uuid
import json
import os
import bcrypt
from config import Config
from seed_all_database import SECTORS_DATA, slugify

def get_db_connection():
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if sectors table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sectors'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            if os.path.exists(schema_path):
                with open(schema_path, "r", encoding="utf-8") as f:
                    cursor.executescript(f.read())
            conn.commit()

        # Always check if data is seeded (sectors table is empty), and seed if needed
        cursor.execute("SELECT COUNT(*) FROM sectors")
        sector_count = cursor.fetchone()[0]
        
        if sector_count == 0:
            seed_data(cursor)
            conn.commit()

        conn.close()
    except Exception as e:
        print(f"Warning: Database init skipped or failed gracefully: {e}")

def seed_data(cursor):
    # Admin Seed
    admin_id = str(uuid.uuid4())
    hashed_pwd = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "INSERT INTO admins (id, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
        (admin_id, "admin@webintern.com", hashed_pwd, "Platform Administrator")
    )

    used_slugs = set()

    for sec_data in SECTORS_DATA:
        sec_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO sectors (id, name, slug, icon_url, description) VALUES (?, ?, ?, ?, ?)",
            (sec_id, sec_data["name"], sec_data["slug"], sec_data["icon"], sec_data["description"])
        )

        for idx, title in enumerate(sec_data["internships"]):
            int_id = str(uuid.uuid4())
            base_slug = slugify(title)
            
            if base_slug in used_slugs:
                int_slug = f"{sec_data['slug']}-{base_slug}"
            else:
                int_slug = base_slug

            used_slugs.add(int_slug)

            short_desc = f"Gain hands-on practical project exposure in {title} through a 4-week structured virtual program."
            full_desc = f"This 4-week Virtual Internship program in {title} provides immersive industry training in {sec_data['name']}. You will complete weekly tasks, receive constructive evaluator feedback, and build a portfolio."
            is_featured = 1 if idx < 2 else 0

            cursor.execute(
                "INSERT INTO internships (id, sector_id, title, slug, short_description, full_description, duration_weeks, mode, cover_image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (int_id, sec_id, title, int_slug, short_desc, full_desc, 4, 'Virtual', f"{int_slug}-cover.jpg", is_featured)
            )

            tasks = [
                (1, f"Week 1: Fundamentals & Research in {title.replace(' Internship', '')}", "Analyze industry standards and submit preliminary research report.", "Research Report PDF / Documentation Link"),
                (2, f"Week 2: Practical Module Execution", "Execute core project tasks and build initial deliverables.", "Project Deliverable Files / Code Repository"),
                (3, f"Week 3: Advanced Optimization & Testing", "Refine project execution, fix issues, and implement evaluator feedback.", "Updated Deliverable & Testing Logs"),
                (4, f"Week 4: Final Capstone Submission", "Finalize project documentation and prepare capstone submission for certification.", "Final Capstone Portfolio PDF & Video Demo")
            ]

            for week, task_title, obj, deliv in tasks:
                cursor.execute(
                    "INSERT INTO internship_tasks (id, internship_id, week_number, title, objective, deliverables, key_steps, evaluation_criteria) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (str(uuid.uuid4()), int_id, week, task_title, obj, deliv, "1. Read task brief.\n2. Complete module steps.\n3. Upload deliverable link.", "Quality of deliverable, adherence to timeline, technical completeness.")
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

    # Product Seed
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
