import sqlite3
import uuid
import re
import os
import bcrypt
from config import Config

SECTORS_DATA = [
    {
        "name": "Engineering & Technology",
        "slug": "engineering-technology",
        "icon": "cpu",
        "description": "Software, hardware, robotics, embedded systems, and civil/mechanical engineering virtual tracks.",
        "internships": [
            "Software Development Internship",
            "Full Stack Web Development Internship",
            "Artificial Intelligence and Machine Learning Internship",
            "Data Science and Analytics Internship",
            "Cybersecurity and Ethical Hacking Internship",
            "Cloud Computing and DevOps Internship",
            "Embedded Systems Engineering Internship",
            "Internet of Things (IoT) Internship",
            "VLSI and Semiconductor Design Internship",
            "Robotics and Automation Engineering Internship",
            "Electrical Engineering Internship",
            "Electronics and Communication Engineering Internship",
            "Mechanical Engineering Design Internship",
            "Civil and Structural Engineering Internship",
            "Automobile and Automotive Engineering Internship",
            "Aerospace Engineering Internship",
            "Mechatronics Engineering Internship",
            "Renewable Energy Engineering Internship",
            "Electric Vehicle Technology Internship",
            "Industrial Automation and PLC/SCADA Internship"
        ]
    },
    {
        "name": "Management & Commerce",
        "slug": "management-commerce",
        "icon": "briefcase",
        "description": "Business administration, marketing, HR, finance, sales, and operations management programs.",
        "internships": [
            "Business Management Internship",
            "Marketing Management Internship",
            "Digital Marketing Internship",
            "Sales and Business Development Internship",
            "Human Resources Management Internship",
            "Financial Management Internship",
            "Accounting and Auditing Internship",
            "Investment Banking Internship",
            "Business Analytics Internship",
            "Operations Management Internship",
            "Supply Chain Management Internship",
            "Logistics Management Internship",
            "Product Management Internship",
            "Project Management Internship",
            "E-Commerce Management Internship",
            "Entrepreneurship and Startup Management Internship",
            "Market Research Internship",
            "Management Consulting Internship",
            "FinTech Internship",
            "Retail Management Internship"
        ]
    },
    {
        "name": "Science",
        "slug": "science",
        "icon": "activity",
        "description": "Physics, chemistry, biotechnology, forensic, mathematics, and material science research tracks.",
        "internships": [
            "Physics Research Internship",
            "Chemistry Research Internship",
            "Mathematics Research Internship",
            "Statistics Internship",
            "Biotechnology Internship",
            "Microbiology Internship",
            "Biochemistry Internship",
            "Zoology Research Internship",
            "Botany Research Internship",
            "Environmental Science Internship",
            "Geology Internship",
            "Marine Science Internship",
            "Food Science and Technology Internship",
            "Forensic Science Internship",
            "Bioinformatics Internship",
            "Nanotechnology Research Internship",
            "Materials Science Internship",
            "Computational Science Internship",
            "Data Science Internship",
            "Scientific Research Internship"
        ]
    },
    {
        "name": "Medical & Healthcare",
        "slug": "medical-healthcare",
        "icon": "heart",
        "description": "Clinical research, public health, pharmacy, hospital administration, and healthcare technology.",
        "internships": [
            "Clinical Research Internship",
            "Medical Research Internship",
            "Public Health Internship",
            "Hospital Administration Internship",
            "Healthcare Management Internship",
            "Epidemiology Research Internship",
            "Community Health Internship",
            "Pharmaceutical Research Internship",
            "Drug Discovery Research Internship",
            "Clinical Pharmacy Internship",
            "Pharmacovigilance Internship",
            "Pharmaceutical Quality Assurance Internship",
            "Pharmaceutical Quality Control Internship",
            "Medical Laboratory Technology Internship",
            "Medical Imaging and Radiology Internship",
            "Physiotherapy Internship",
            "Occupational Therapy Internship",
            "Optometry Internship",
            "Nutrition and Dietetics Internship",
            "Healthcare Technology Internship"
        ]
    },
    {
        "name": "Agriculture",
        "slug": "agriculture",
        "icon": "sun",
        "description": "Agronomy, soil science, AgriTech, precision farming, and food technology virtual modules.",
        "internships": [
            "Agricultural Engineering Internship",
            "Agricultural Science Internship",
            "Agronomy Internship",
            "Horticulture Internship",
            "Soil Science Internship",
            "Plant Biotechnology Internship",
            "Agricultural Economics Internship",
            "Agricultural Marketing Internship",
            "Food Technology Internship",
            "Dairy Technology Internship",
            "Fisheries Science Internship",
            "Animal Science Internship",
            "Veterinary Science Internship",
            "Precision Agriculture Internship",
            "AgriTech Internship",
            "Smart Farming Technology Internship",
            "Agricultural Drone Technology Internship",
            "Agricultural IoT Internship",
            "Farm Management Internship",
            "Rural Development Internship"
        ]
    },
    {
        "name": "Arts & Humanities",
        "slug": "arts-humanities",
        "icon": "book-open",
        "description": "Literature, history, journalism, content writing, psychology, and social research internships.",
        "internships": [
            "English Literature Internship",
            "Tamil Language and Literature Internship",
            "Hindi Language and Literature Internship",
            "History Research Internship",
            "Economics Research Internship",
            "Political Science Internship",
            "Sociology Research Internship",
            "Psychology Internship",
            "Geography Research Internship",
            "Philosophy Research Internship",
            "Journalism Internship",
            "Mass Communication Internship",
            "Public Administration Internship",
            "International Relations Internship",
            "Content Writing Internship",
            "Copywriting Internship",
            "Editing and Proofreading Internship",
            "Translation Internship",
            "Policy Research Internship",
            "Social Research Internship"
        ]
    },
    {
        "name": "Law",
        "slug": "law",
        "icon": "shield",
        "description": "Corporate law, IP rights, criminal law, legal research, drafting, and compliance modules.",
        "internships": [
            "Corporate Law Internship",
            "Criminal Law Internship",
            "Civil Law Internship",
            "Intellectual Property Rights Law Internship",
            "Cyber Law Internship",
            "Constitutional Law Internship",
            "Labour and Employment Law Internship",
            "Tax Law Internship",
            "Banking and Finance Law Internship",
            "Environmental Law Internship",
            "International Law Internship",
            "Human Rights Law Internship",
            "Legal Research Internship",
            "Legal Drafting Internship",
            "Litigation Internship",
            "Corporate Compliance Internship",
            "Legal Technology Internship",
            "Contract Law Internship",
            "Family Law Internship",
            "Alternative Dispute Resolution Internship"
        ]
    },
    {
        "name": "Architecture & Design",
        "slug": "architecture-design",
        "icon": "layout",
        "description": "UI/UX design, interior design, urban planning, BIM, graphic design, and 3D modeling.",
        "internships": [
            "Architecture Internship",
            "Interior Design Internship",
            "Urban Planning Internship",
            "Landscape Architecture Internship",
            "Sustainable Architecture Internship",
            "Building Information Modelling (BIM) Internship",
            "Architectural Visualization Internship",
            "Graphic Design Internship",
            "User Interface (UI) Design Internship",
            "User Experience (UX) Design Internship",
            "Product Design Internship",
            "Fashion Design Internship",
            "Textile Design Internship",
            "Industrial Design Internship",
            "Animation Design Internship",
            "Visual Effects (VFX) Internship",
            "3D Design and Modelling Internship",
            "Motion Graphics Design Internship",
            "Game Design Internship",
            "Creative Design Internship"
        ]
    },
    {
        "name": "Hotel Management & Tourism",
        "slug": "hotel-management-tourism",
        "icon": "compass",
        "description": "Hospitality operations, culinary arts, travel management, front office, and event production.",
        "internships": [
            "Hotel Management Internship",
            "Hospitality Management Internship",
            "Food Production Internship",
            "Food and Beverage Service Internship",
            "Front Office Management Internship",
            "Housekeeping Management Internship",
            "Event Management Internship",
            "Travel Management Internship",
            "Tourism Management Internship",
            "Aviation Hospitality Internship",
            "Cruise Hospitality Internship",
            "Restaurant Management Internship",
            "Culinary Arts Internship",
            "Bakery and Confectionery Internship",
            "Hotel Operations Internship",
            "Resort Management Internship",
            "Travel Agency Operations Internship",
            "Tour Operations Internship",
            "Hospitality Marketing Internship",
            "Hospitality Sales Internship"
        ]
    },
    {
        "name": "Education",
        "slug": "education",
        "icon": "award",
        "description": "EdTech, instructional design, curriculum development, special education, and e-learning.",
        "internships": [
            "School Teaching Internship",
            "Educational Technology Internship",
            "Curriculum Development Internship",
            "Instructional Design Internship",
            "E-Learning Development Internship",
            "Special Education Internship",
            "Educational Research Internship",
            "Academic Content Development Internship",
            "Academic Counselling Internship",
            "EdTech Internship",
            "Online Teaching Internship",
            "Classroom Management Internship",
            "Teacher Training Internship",
            "Educational Administration Internship",
            "Child Education Internship",
            "Early Childhood Education Internship",
            "Educational Psychology Internship",
            "Assessment and Evaluation Internship",
            "Digital Education Internship",
            "Learning and Development Internship"
        ]
    },
    {
        "name": "Media & Communication",
        "slug": "media-communication",
        "icon": "tv",
        "description": "Journalism, video editing, social media management, brand communication, and podcasting.",
        "internships": [
            "Journalism Internship",
            "Mass Communication Internship",
            "Digital Media Internship",
            "Social Media Management Internship",
            "Content Creation Internship",
            "Video Editing Internship",
            "Photography Internship",
            "Videography Internship",
            "Film Production Internship",
            "Script Writing Internship",
            "Copywriting Internship",
            "Advertising Internship",
            "Public Relations Internship",
            "Brand Communication Internship",
            "Podcast Production Internship",
            "Animation Internship",
            "Visual Effects Internship",
            "News Media Internship",
            "Digital Marketing Communications Internship",
            "Media Production Internship"
        ]
    },
    {
        "name": "Fashion & Textile",
        "slug": "fashion-textile",
        "icon": "tag",
        "description": "Apparel production, fashion merchandising, styling, garment technology, and sustainable fashion.",
        "internships": [
            "Fashion Design Internship",
            "Textile Design Internship",
            "Apparel Production Internship",
            "Fashion Merchandising Internship",
            "Fashion Marketing Internship",
            "Fashion Photography Internship",
            "Fashion Styling Internship",
            "Garment Technology Internship",
            "Textile Engineering Internship",
            "Textile Manufacturing Internship",
            "Fashion Retail Internship",
            "Fashion Product Development Internship",
            "Fashion Brand Management Internship",
            "Fashion Communication Internship",
            "Apparel Quality Control Internship",
            "Apparel Quality Assurance Internship",
            "Fashion Entrepreneurship Internship",
            "Textile Research Internship",
            "Sustainable Fashion Internship",
            "Fashion E-Commerce Internship"
        ]
    },
    {
        "name": "Aviation",
        "slug": "aviation",
        "icon": "send",
        "description": "Airport management, flight operations, ground handling, aircraft maintenance, and logistics.",
        "internships": [
            "Airport Management Internship",
            "Aviation Management Internship",
            "Airline Operations Internship",
            "Ground Operations Internship",
            "Aviation Safety Internship",
            "Aircraft Maintenance Internship",
            "Aerospace Engineering Internship",
            "Aviation Hospitality Internship",
            "Air Cargo Management Internship",
            "Aviation Marketing Internship",
            "Flight Operations Internship",
            "Airport Security Internship",
            "Aviation Customer Service Internship",
            "Airline Revenue Management Internship",
            "Aviation Logistics Internship",
            "Aircraft Design Internship",
            "Aviation Engineering Internship",
            "Airport Operations Internship",
            "Aviation Administration Internship",
            "Aviation Business Development Internship"
        ]
    },
    {
        "name": "Marine & Ocean",
        "slug": "marine-ocean",
        "icon": "anchor",
        "description": "Naval architecture, marine engineering, shipping management, oceanography, and port operations.",
        "internships": [
            "Marine Engineering Internship",
            "Naval Architecture Internship",
            "Ocean Engineering Internship",
            "Marine Biology Internship",
            "Oceanography Internship",
            "Fisheries Science Internship",
            "Port Management Internship",
            "Shipping Management Internship",
            "Maritime Operations Internship",
            "Marine Environmental Science Internship",
            "Offshore Engineering Internship",
            "Ship Design Internship",
            "Shipbuilding Internship",
            "Marine Surveying Internship",
            "Maritime Logistics Internship",
            "Marine Safety Internship",
            "Marine Technology Internship",
            "Coastal Engineering Internship",
            "Ocean Research Internship",
            "Maritime Business Management Internship"
        ]
    },
    {
        "name": "Environmental & Sustainability",
        "slug": "environmental-sustainability",
        "icon": "globe",
        "description": "Climate change research, renewable energy, ESG auditing, waste management, and green tech.",
        "internships": [
            "Environmental Science Internship",
            "Environmental Engineering Internship",
            "Climate Change Research Internship",
            "Renewable Energy Internship",
            "Sustainability Management Internship",
            "Environmental, Social and Governance (ESG) Internship",
            "Waste Management Internship",
            "Water Resource Management Internship",
            "Carbon Management Internship",
            "Environmental Consultancy Internship",
            "Sustainable Development Internship",
            "Green Technology Internship",
            "Environmental Impact Assessment Internship",
            "Biodiversity Conservation Internship",
            "Wildlife Conservation Internship",
            "Air Pollution Monitoring Internship",
            "Water Quality Management Internship",
            "Solid Waste Management Internship",
            "Sustainable Agriculture Internship",
            "Climate Technology Internship"
        ]
    },
    {
        "name": "Finance & Banking",
        "slug": "finance-banking",
        "icon": "dollar-sign",
        "description": "Investment banking, equity research, financial modeling, wealth management, risk, and GST.",
        "internships": [
            "Banking Internship",
            "Investment Banking Internship",
            "Equity Research Internship",
            "Financial Analysis Internship",
            "Wealth Management Internship",
            "Portfolio Management Internship",
            "FinTech Internship",
            "Risk Management Internship",
            "Credit Analysis Internship",
            "Insurance Internship",
            "Stock Market Research Internship",
            "Accounting Internship",
            "Auditing Internship",
            "Taxation Internship",
            "Goods and Services Tax (GST) Internship",
            "Corporate Finance Internship",
            "Treasury Management Internship",
            "Financial Planning Internship",
            "Investment Management Internship",
            "Financial Modelling Internship"
        ]
    },
    {
        "name": "Government & Public Sector",
        "slug": "government-public-sector",
        "icon": "landmark",
        "description": "Public policy, rural development, e-governance, smart city planning, and public finance.",
        "internships": [
            "Government Administration Internship",
            "Public Policy Internship",
            "Policy Research Internship",
            "Public Administration Internship",
            "Rural Development Internship",
            "Urban Development Internship",
            "Public Relations Internship",
            "Government Data Analysis Internship",
            "Legal Research Internship",
            "Economic Research Internship",
            "Social Welfare Internship",
            "Environmental Policy Internship",
            "Smart City Development Internship",
            "Digital Governance Internship",
            "Government Information Technology Internship",
            "Public Finance Internship",
            "Government Project Management Internship",
            "E-Governance Internship",
            "Public Sector Research Internship",
            "Government Consulting Internship"
        ]
    },
    {
        "name": "Research & Academia",
        "slug": "research-academia",
        "icon": "feather",
        "description": "R&D assistantships, patent research, lab analysis, literature reviews, and computational research.",
        "internships": [
            "Research Assistant Internship",
            "Scientific Research Internship",
            "Laboratory Research Internship",
            "Data Research Internship",
            "Academic Research Internship",
            "Computational Research Internship",
            "Literature Review Research Internship",
            "Research Publication Internship",
            "Patent Research Internship",
            "Research and Development (R&D) Internship",
            "Innovation Research Internship",
            "Technology Research Internship",
            "Social Science Research Internship",
            "Market Research Internship",
            "Biomedical Research Internship",
            "Engineering Research Internship",
            "Environmental Research Internship",
            "Materials Research Internship",
            "Artificial Intelligence Research Internship",
            "Interdisciplinary Research Internship"
        ]
    },
    {
        "name": "Startup & Entrepreneurship",
        "slug": "startup-entrepreneurship",
        "icon": "zap",
        "description": "Founder's office, growth marketing, venture capital, product strategy, and startup operations.",
        "internships": [
            "Startup Management Internship",
            "Founder’s Office Internship",
            "Business Development Internship",
            "Startup Marketing Internship",
            "Startup Sales Internship",
            "Startup Operations Internship",
            "Product Development Internship",
            "Growth Marketing Internship",
            "Startup Finance Internship",
            "Startup Technology Internship",
            "Venture Capital Internship",
            "Market Research Internship",
            "Entrepreneurship Internship",
            "Innovation Management Internship",
            "Startup Strategy Internship",
            "Customer Success Internship",
            "Product Marketing Internship",
            "Startup Investment Research Internship",
            "Business Strategy Internship",
            "Startup Ecosystem Internship"
        ]
    },
    {
        "name": "Emerging Technologies",
        "slug": "emerging-technologies",
        "icon": "cpu",
        "description": "Generative AI, LLM engineering, prompt engineering, AR/VR, Web3, and quantum computing.",
        "internships": [
            "Generative Artificial Intelligence Internship",
            "AI Agent Development Internship",
            "Large Language Model (LLM) Engineering Internship",
            "Prompt Engineering Internship",
            "Machine Learning Internship",
            "Computer Vision Internship",
            "Robotics and Autonomous Systems Internship",
            "Drone Technology Internship",
            "Electric Vehicle Technology Internship",
            "Battery Technology Internship",
            "Semiconductor Technology Internship",
            "Quantum Computing Internship",
            "Blockchain Technology Internship",
            "Web3 Development Internship",
            "Internet of Things (IoT) Internship",
            "Digital Twin Technology Internship",
            "Augmented and Virtual Reality (AR/VR) Internship",
            "Edge Computing Internship",
            "Advanced Cybersecurity Internship",
            "5G and 6G Communication Technology Internship"
        ]
    }
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def seed_all_database():
    db_path = Config.SQLITE_DB_PATH
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Re-create schema
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    conn.commit()

    # Clear previous seed data
    cursor.execute("DELETE FROM internship_tasks")
    cursor.execute("DELETE FROM internships")
    cursor.execute("DELETE FROM sectors")
    cursor.execute("DELETE FROM site_stats")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM testimonials")

    # Admin Seed
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        admin_id = str(uuid.uuid4())
        hashed_pwd = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            "INSERT INTO admins (id, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
            (admin_id, "admin@webintern.com", hashed_pwd, "Platform Administrator")
        )

    # Track used slugs to prevent collisions
    used_slugs = set()

    total_internships = 0
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

            # Weekly tasks for this internship
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
            total_internships += 1

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

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(SECTORS_DATA)} Sectors and {total_internships} Internships into Database!")

if __name__ == "__main__":
    seed_all_database()
