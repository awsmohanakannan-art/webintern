import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_offer_letter_pdf(student_name, internship_title, date_str):
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
    story.append(Paragraph("web<b>intern</b>", title_style))
    story.append(Paragraph("VIRTUAL INTERNSHIP OFFER LETTER", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0B3D91'), spaceAfter=20))

    # Date & Recipient
    story.append(Paragraph(f"<b>Date:</b> {date_str}", body_style))
    story.append(Paragraph(f"<b>To:</b> {student_name}", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Subject: Official Offer Letter for Virtual Internship</b>", heading_style))
    
    p1 = f"Dear <b>{student_name}</b>,<br/><br/>We are pleased to inform you that you have been selected for the <b>{internship_title}</b> at <b>Web Intern Platform</b>. This offer is extended in recognition of your academic drive and passion for industry-level practical skill growth."
    story.append(Paragraph(p1, body_style))

    p2 = "<b>Internship Program Overview:</b><br/>" \
         "• <b>Format:</b> 100% Virtual / Self-Paced Project Modules<br/>" \
         "• <b>Duration:</b> 4 Weeks<br/>" \
         "• <b>Evaluation:</b> Weekly Task Deliverable Reviews<br/>" \
         "• <b>Certificate:</b> Official Certificate of Completion issued upon final module approval."
    story.append(Paragraph(p2, body_style))

    p3 = "During this internship, you will be expected to adhere to professional standards, submit work deliverables on schedule via your student dashboard, and engage constructively with feedback."
    story.append(Paragraph(p3, body_style))

    story.append(Spacer(1, 25))

    # Signatures
    sig_data = [
        [
            Paragraph("<b>Web Intern Operations</b><br/>Authorized Verification Board<br/>Web Intern Platform", body_style),
            Paragraph(f"<b>Accepted & Acknowledged:</b><br/>{student_name}<br/>Candidate Signature", body_style)
        ]
    ]
    t = Table(sig_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_certificate_pdf(student_name, internship_title, date_str, cert_id, is_verified=False):
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
        fontSize=30,
        leading=34,
        textColor=colors.HexColor('#0B3D91'),
        alignment=1
    )

    cert_sub_style = ParagraphStyle(
        'CertSub',
        fontName='Helvetica',
        fontSize=14,
        textColor=colors.HexColor('#2E7DFF'),
        alignment=1,
        spaceAfter=15
    )

    name_style = ParagraphStyle(
        'CandidateName',
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#082B66'),
        alignment=1,
        spaceAfter=10
    )

    desc_style = ParagraphStyle(
        'CertDesc',
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=colors.HexColor('#4B5563'),
        alignment=1
    )

    badge_text = "OFFICIAL VERIFIED CERTIFICATE" if is_verified else "CERTIFICATE OF COMPLETION"

    story = []
    story.append(Spacer(1, 20))
    story.append(Paragraph("web<b>intern</b>", cert_title_style))
    story.append(Paragraph(badge_text.upper(), cert_sub_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor('#2E7DFF'), spaceAfter=20))

    story.append(Paragraph("THIS IS PROUDLY PRESENTED TO", ParagraphStyle('Sub', fontName='Helvetica', fontSize=11, alignment=1, textColor=colors.HexColor('#6B7280'))))
    story.append(Spacer(1, 10))
    story.append(Paragraph(student_name, name_style))
    story.append(Spacer(1, 10))

    desc = f"for successfully completing the intensive 4-week virtual internship in <b>{internship_title}</b>, demonstrating outstanding dedication, practical task execution, and technical excellence."
    story.append(Paragraph(desc, desc_style))

    story.append(Spacer(1, 30))

    meta_data = [
        [
            Paragraph(f"<b>Issue Date:</b> {date_str}", ParagraphStyle('M1', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#4B5563'))),
            Paragraph(f"<b>Certificate ID:</b> {cert_id}", ParagraphStyle('M2', fontName='Helvetica-Bold', fontSize=10, alignment=1, textColor=colors.HexColor('#0B3D91'))),
            Paragraph("<b>Verification Status:</b> " + ("✅ Verified Paid" if is_verified else "Standard Verified"), ParagraphStyle('M3', fontName='Helvetica', fontSize=10, alignment=2, textColor=colors.HexColor('#10B981')))
        ]
    ]
    t = Table(meta_data, colWidths=[240, 240, 240])
    story.append(t)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
