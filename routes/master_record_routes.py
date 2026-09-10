import os
import uuid
from flask import Blueprint, request, jsonify, Response, send_file
from database import query_db, execute_db
from utils.auth import admin_required, jwt_required
from utils.master_record_service import (
    save_master_record,
    get_master_record,
    get_offer_letter_mapping,
    get_certificate_mapping,
    get_organization_settings,
    update_organization_settings,
    save_document_snapshot,
    validate_master_record
)
from utils.pdf_generator import generate_offer_letter_pdf, generate_certificate_pdf
from config import Config

master_record_bp = Blueprint('master_record_bp', __name__)

@master_record_bp.route('/api/admin/master-records', methods=['GET'])
@admin_required
def list_master_records():
    records = query_db("SELECT * FROM master_internships ORDER BY created_at DESC")
    return jsonify({'master_records': records}), 200

@master_record_bp.route('/api/admin/master-records', methods=['POST'])
@admin_required
def create_master_record():
    data = request.get_json() or {}
    record, errors = save_master_record(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'validation_errors': errors}), 400
    
    return jsonify({
        'message': 'Master Internship Record created successfully!',
        'master_record': record
    }), 201

@master_record_bp.route('/api/admin/master-records/<record_id>', methods=['GET'])
@admin_required
def get_master_record_detail(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404
    return jsonify({'master_record': rec}), 200

@master_record_bp.route('/api/admin/master-records/<record_id>', methods=['PUT'])
@admin_required
def update_master_record_detail(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    data = request.get_json() or {}
    updated_rec, errors = save_master_record(data, record_id=rec['id'])
    if errors:
        return jsonify({'error': 'Validation failed', 'validation_errors': errors}), 400

    return jsonify({
        'message': 'Master Internship Record updated successfully!',
        'master_record': updated_rec
    }), 200

@master_record_bp.route('/api/admin/master-records/<record_id>', methods=['DELETE'])
@admin_required
def delete_master_record_detail(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    execute_db("DELETE FROM master_internships WHERE id = ?", (rec['id'],))
    return jsonify({'message': 'Master Internship Record deleted successfully.'}), 200

@master_record_bp.route('/api/admin/master-records/<record_id>/preview-offer', methods=['GET'])
@admin_required
def preview_offer_letter(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    errors = validate_master_record(rec)
    if errors:
        return jsonify({'error': 'Cannot preview Offer Letter. Missing required master fields.', 'validation_errors': errors}), 400

    mapping = get_offer_letter_mapping(rec)
    return jsonify({
        'status': 'READY',
        'document_type': 'OFFER_LETTER',
        'mapping': mapping,
        'summary': {
            'student_full_name': mapping['student_full_name'],
            'internship_position': mapping['internship_position'],
            'internship_start_date': mapping['internship_start_date'],
            'internship_end_date': mapping['internship_end_date'],
            'internship_duration': mapping['internship_duration'],
            'offer_id': mapping['offer_id'],
            'issue_date': mapping['offer_letter_issue_date']
        }
    }), 200

@master_record_bp.route('/api/admin/master-records/<record_id>/preview-certificate', methods=['GET'])
@admin_required
def preview_certificate(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    errors = validate_master_record(rec)
    if errors:
        return jsonify({'error': 'Cannot preview Certificate. Missing required master fields.', 'validation_errors': errors}), 400

    mapping = get_certificate_mapping(rec)
    return jsonify({
        'status': 'READY',
        'document_type': 'CERTIFICATE',
        'mapping': mapping,
        'summary': {
            'student_full_name': mapping['student_full_name'],
            'college_name': mapping['college_name'],
            'university_name': mapping['university_name'],
            'internship_position': mapping['internship_position'],
            'start_date': mapping['internship_start_date'],
            'end_date': mapping['internship_end_date'],
            'project_title': mapping['project_title'],
            'mentor_name': mapping['mentor_name'],
            'certificate_id': mapping['certificate_id'],
            'issue_date': mapping['certificate_issue_date']
        }
    }), 200

@master_record_bp.route('/api/admin/master-records/<record_id>/generate-offer', methods=['POST'])
@admin_required
def generate_offer_from_master(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    errors = validate_master_record(rec)
    if errors:
        return jsonify({'error': 'Document generation blocked due to missing required fields.', 'validation_errors': errors}), 400

    mapping = get_offer_letter_mapping(rec)
    pdf_bytes = generate_offer_letter_pdf(
        student_name=mapping['student_full_name'],
        internship_title=mapping['internship_position'],
        date_str=mapping['offer_letter_issue_date'],
        save_id=rec['id'],
        company_name=mapping['organization_name'],
        start_date=mapping['internship_start_date'],
        end_date=mapping['internship_end_date'],
        duration=mapping['internship_duration'],
        skills_tools=", ".join(mapping['learning_outcomes']),
        tasks_projects="; ".join(mapping['key_responsibilities'][:2]),
        offer_id=mapping['offer_id']
    )

    out_file = os.path.join(Config.GENERATED_OFFERS_DIR, f"offer_{rec['id']}.pdf")
    snapshot_id = save_document_snapshot(rec['id'], 'OFFER_LETTER', mapping['offer_id'], mapping, out_file)

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'inline; filename="Offer_Letter_{mapping["offer_id"]}.pdf"',
            'X-Snapshot-ID': snapshot_id
        }
    )

@master_record_bp.route('/api/admin/master-records/<record_id>/generate-certificate', methods=['POST'])
@admin_required
def generate_certificate_from_master(record_id):
    rec = get_master_record(record_id)
    if not rec:
        return jsonify({'error': 'Master Internship Record not found.'}), 404

    errors = validate_master_record(rec)
    if errors:
        return jsonify({'error': 'Document generation blocked due to missing required fields.', 'validation_errors': errors}), 400

    mapping = get_certificate_mapping(rec)
    pdf_bytes = generate_certificate_pdf(
        student_name=mapping['student_full_name'],
        internship_title=mapping['internship_position'],
        date_str=mapping['certificate_issue_date'],
        cert_id=mapping['certificate_id'],
        college_name=mapping['college_name'],
        guide_name=mapping['mentor_name'],
        project_name=mapping['project_title'],
        start_date=mapping['internship_start_date'],
        end_date=mapping['internship_end_date'],
        company_name=mapping['organization_name']
    )

    clean_cert = str(mapping['certificate_id']).replace('/', '_')
    out_file = os.path.join(Config.GENERATED_CERTIFICATES_DIR, f"certificate_{clean_cert}.pdf")
    snapshot_id = save_document_snapshot(rec['id'], 'CERTIFICATE', mapping['certificate_id'], mapping, out_file)

    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'inline; filename="Certificate_{clean_cert}.pdf"',
            'X-Snapshot-ID': snapshot_id
        }
    )

@master_record_bp.route('/api/admin/organization-settings', methods=['GET'])
@admin_required
def get_org_settings():
    settings = get_organization_settings()
    return jsonify({'organization_settings': settings}), 200

@master_record_bp.route('/api/admin/organization-settings', methods=['POST'])
@admin_required
def update_org_settings():
    data = request.get_json() or {}
    settings = update_organization_settings(data)
    return jsonify({
        'message': 'Global Organization Settings updated successfully!',
        'organization_settings': settings
    }), 200
