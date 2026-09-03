import io
import os
import qrcode
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from config import Config

# --- Text Fitting Helpers (Section 8 Requirements) ---

def calculate_font_size(text, base_size=26, min_size=14):
    """Dynamically calculate font size to prevent overlapping fixed template elements."""
    if not text:
        return base_size
    length = len(str(text))
    if length > 35:
        return max(min_size, base_size - int((length - 35) * 0.35))
    return base_size

def wrap_text(text, max_chars_per_line=60):
    """Safely wrap long text into multiline strings."""
    if not text:
        return ""
    words = str(text).split(" ")
    lines = []
    current_line = []
    current_length = 0
    for w in words:
        if current_length + len(w) + 1 > max_chars_per_line:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_length = len(w)
        else:
            current_line.append(w)
            current_length += len(w) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return "<br/>".join(lines)

def fit_text(text, max_width=500, default_font_size=12):
    """Fit text within container bounds preventing clipping/overflow."""
    font_size = calculate_font_size(text, base_size=default_font_size)
    wrapped = wrap_text(text, max_chars_per_line=max(30, int(max_width / 8)))
    return wrapped, font_size

# --- Template Drawing Callbacks ---

def draw_offer_background(canvas_obj, doc):
    template_path = Config.OFFER_LETTER_TEMPLATE_PATH
    if os.path.exists(template_path):
        canvas_obj.saveState()
        canvas_obj.drawImage(template_path, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1])
        canvas_obj.restoreState()

def draw_certificate_background_with_qr(canvas_obj, doc, verify_url=None):
    template_path = Config.CERTIFICATE_TEMPLATE_PATH
    if os.path.exists(template_path):
        canvas_obj.saveState()
        canvas_obj.drawImage(template_path, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1])
        
        # Optional QR Code placement (Section 30)
        if verify_url:
            try:
                qr = qrcode.QRCode(box_size=3, border=1)
                qr.add_data(verify_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                # Draw QR code in bottom-right corner safely
                canvas_obj.drawImage(ImageReader(img_buffer), doc.pagesize[0] - 85, 35, width=55, height=55)
            except Exception as e:
                print(f"[QR Draw Warning]: {e}")
                
        canvas_obj.restoreState()

# --- PDF Generation Functions ---

def generate_offer_letter_pdf(
    student_name,
    internship_title,
    date_str,
    save_id=None,
    company_name="Web Intern Platform",
    start_date=None,
    end_date=None,
    duration="4 Weeks",
    location="Virtual / Remote",
    skills_tools=None,
    tasks_projects=None,
    offer_id=None
):
    """Generate Offer Letter PDF with exact template background and dynamic data overlay."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0B3D91'),
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.HexColor('#2E7DFF'),
        alignment=0
    )
    
    heading_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#082B66'),
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=12
    )

    story = []

    # Header section
    story.append(Paragraph(f"{company_name.lower().replace(' platform', '')}", title_style))
    story.append(Paragraph("VIRTUAL INTERNSHIP OFFER LETTER", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0B3D91'), spaceAfter=20))

    # Metadata & Recipient
    eff_offer_id = offer_id or f"WI-OFFER-{save_id[:8].upper() if save_id else '2026-1001'}"
    eff_start = start_date or date_str
    eff_end = end_date or "4 Weeks from Start Date"

    fitted_name, name_size = fit_text(student_name, max_width=450, default_font_size=11)

    story.append(Paragraph(f"<b>Offer ID:</b> {eff_offer_id}", body_style))
    story.append(Paragraph(f"<b>Issue Date:</b> {date_str}", body_style))
    story.append(Paragraph(f"<b>To Candidate:</b> {fitted_name}", body_style))
    story.append(Paragraph(f"<b>Location/Mode:</b> {location}", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"<b>Subject: Official Offer Letter for {internship_title}</b>", heading_style))
    
    p1 = f"Dear <b>{fitted_name}</b>,<br/><br/>We are pleased to extend this official Offer of Internship for the <b>{internship_title}</b> position at <b>{company_name}</b>. This appointment is awarded in recognition of your academic performance and drive for technical excellence."
    story.append(Paragraph(p1, body_style))

    skills_str = f"<br/>• <b>Skills & Tools Covered:</b> {skills_tools}" if skills_tools else ""
    projects_str = f"<br/>• <b>Tasks & Capstone:</b> {tasks_projects}" if tasks_projects else ""

    p2 = f"<b>Internship Program Overview:</b><br/>" \
         f"• <b>Role / Specialization:</b> {internship_title}<br/>" \
         f"• <b>Start Date:</b> {eff_start}<br/>" \
         f"• <b>End Date:</b> {eff_end}<br/>" \
         f"• <b>Duration:</b> {duration}<br/>" \
         f"• <b>Format:</b> 100% Virtual / Remote Project Execution" \
         f"{skills_str}{projects_str}"
    story.append(Paragraph(p2, body_style))

    p3 = "During this internship, you will submit weekly project deliverables via your WebIntern student dashboard, receive evaluator feedback, and adhere to platform code of conduct."
    story.append(Paragraph(p3, body_style))

    story.append(Spacer(1, 20))

    # Signatures
    sig_data = [
        [
            Paragraph(f"<b>{company_name} Operations</b><br/>Authorized Verification Board", body_style),
            Paragraph(f"<b>Accepted & Acknowledged:</b><br/>{student_name}<br/>Candidate Signature", body_style)
        ]
    ]
    t = Table(sig_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)

    doc.build(story, onFirstPage=draw_offer_background, onLaterPages=draw_offer_background)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    if save_id:
        try:
            os.makedirs(Config.GENERATED_OFFERS_DIR, exist_ok=True)
            out_file = os.path.join(Config.GENERATED_OFFERS_DIR, f"offer_{save_id}.pdf")
            with open(out_file, 'wb') as f:
                f.write(pdf_bytes)
        except Exception as e:
            print(f"Warning: Failed to save offer PDF to storage: {e}")

    return pdf_bytes

def generate_certificate_pdf(
    student_name,
    internship_title,
    date_str,
    cert_id,
    is_verified=False,
    college_name=None,
    guide_name=None,
    project_name=None,
    duration="4 Weeks",
    start_date=None,
    end_date=None,
    company_name="Web Intern Platform",
    verification_url=None
):
    """Generate Certificate PDF with exact template background, QR code, and dynamic overlay."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()

    cert_title_style = ParagraphStyle(
        'CertTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=32,
        textColor=colors.HexColor('#0B3D91'),
        alignment=1
    )

    cert_sub_style = ParagraphStyle(
        'CertSub',
        fontName='Helvetica',
        fontSize=13,
        textColor=colors.HexColor('#2E7DFF'),
        alignment=1,
        spaceAfter=12
    )

    name_font_size = calculate_font_size(student_name, base_size=26, min_size=18)

    name_style = ParagraphStyle(
        'CandidateName',
        fontName='Helvetica-Bold',
        fontSize=name_font_size,
        leading=name_font_size + 4,
        textColor=colors.HexColor('#082B66'),
        alignment=1,
        spaceAfter=8
    )

    desc_style = ParagraphStyle(
        'CertDesc',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#4B5563'),
        alignment=1
    )

    badge_text = "OFFICIAL VERIFIED CERTIFICATE OF COMPLETION" if is_verified else "CERTIFICATE OF COMPLETION"
    eff_verify_url = verification_url or f"https://webintern.in/verify/{cert_id}"

    story = []
    story.append(Spacer(1, 15))
    story.append(Paragraph(company_name, cert_title_style))
    story.append(Paragraph(badge_text.upper(), cert_sub_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#2E7DFF'), spaceAfter=15))

    story.append(Paragraph("THIS IS PROUDLY PRESENTED TO", ParagraphStyle('Sub', fontName='Helvetica', fontSize=10, alignment=1, textColor=colors.HexColor('#6B7280'))))
    story.append(Spacer(1, 6))
    
    college_str = f" ({college_name})" if college_name else ""
    story.append(Paragraph(f"{student_name}{college_str}", name_style))
    story.append(Spacer(1, 6))

    proj_str = f" Project: <b>{project_name}</b>." if project_name else ""
    guide_str = f" Supervised by <b>{guide_name}</b>." if guide_name else ""
    dates_str = f" Program period: {start_date} to {end_date}." if (start_date and end_date) else ""

    desc = f"for successfully completing the intensive {duration} virtual internship in <b>{internship_title}</b> at <b>{company_name}</b>, demonstrating outstanding dedication, task execution, and technical excellence.{proj_str}{guide_str}{dates_str}"
    story.append(Paragraph(desc, desc_style))

    story.append(Spacer(1, 20))

    meta_data = [
        [
            Paragraph(f"<b>Issue Date:</b> {date_str}", ParagraphStyle('M1', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#4B5563'))),
            Paragraph(f"<b>Certificate ID:</b> {cert_id}", ParagraphStyle('M2', fontName='Helvetica-Bold', fontSize=9, alignment=1, textColor=colors.HexColor('#0B3D91'))),
            Paragraph(f"<b>Verification:</b> <a href='{eff_verify_url}' color='#2E7DFF'>Verify Online</a>", ParagraphStyle('M3', fontName='Helvetica', fontSize=9, alignment=2, textColor=colors.HexColor('#10B981')))
        ]
    ]
    t = Table(meta_data, colWidths=[240, 240, 240])
    story.append(t)

    def _on_page(canvas_obj, document):
        draw_certificate_background_with_qr(canvas_obj, document, verify_url=eff_verify_url)

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    if cert_id:
        try:
            os.makedirs(Config.GENERATED_CERTIFICATES_DIR, exist_ok=True)
            clean_cert_id = str(cert_id).replace('/', '_')
            out_file = os.path.join(Config.GENERATED_CERTIFICATES_DIR, f"certificate_{clean_cert_id}.pdf")
            with open(out_file, 'wb') as f:
                f.write(pdf_bytes)
        except Exception as e:
            print(f"Warning: Failed to save certificate PDF to storage: {e}")

    return pdf_bytes
