from flask import Blueprint, request, jsonify
from database import query_db

internship_bp = Blueprint('internship_bp', __name__)

@internship_bp.route('/api/internships', methods=['GET'])
def get_internships():
    sector_slug = request.args.get('sector')
    search_query = request.args.get('search')
    featured_only = request.args.get('featured')

    sql = """
        SELECT i.*, s.name as sector_name, s.slug as sector_slug
        FROM internships i
        JOIN sectors s ON i.sector_id = s.id
        WHERE 1=1
    """
    params = []

    if sector_slug:
        sql += " AND s.slug = ?"
        params.append(sector_slug)

    if featured_only and featured_only.lower() in ['true', '1']:
        sql += " AND i.is_featured = 1"

    if search_query:
        sql += " AND (i.title LIKE ? OR i.short_description LIKE ? OR s.name LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term])

    sql += " ORDER BY i.created_at DESC"

    internships = query_db(sql, params)
    return jsonify({'internships': internships}), 200

@internship_bp.route('/api/internships/<slug>', methods=['GET'])
def get_internship_detail(slug):
    internship = query_db("""
        SELECT i.*, s.name as sector_name, s.slug as sector_slug
        FROM internships i
        JOIN sectors s ON i.sector_id = s.id
        WHERE i.slug = ?
    """, (slug,), one=True)

    if not internship:
        return jsonify({'error': 'Internship program not found.'}), 404

    tasks = query_db("""
        SELECT * FROM internship_tasks
        WHERE internship_id = ?
        ORDER BY week_number ASC
    """, (internship['id'],))

    related = query_db("""
        SELECT i.*, s.name as sector_name, s.slug as sector_slug
        FROM internships i
        JOIN sectors s ON i.sector_id = s.id
        WHERE i.sector_id = ? AND i.id != ?
        LIMIT 3
    """, (internship['sector_id'], internship['id']))

    internship['tasks'] = tasks
    internship['related'] = related
    return jsonify({'internship': internship}), 200
