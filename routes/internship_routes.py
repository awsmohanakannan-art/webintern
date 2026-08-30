from flask import Blueprint, request, jsonify
from database import query_db

internship_bp = Blueprint('internship_bp', __name__)

@internship_bp.route('/api/internships', methods=['GET'])
def get_internships():
    sector_slug = request.args.get('sector')
    search_query = request.args.get('search')
    featured_only = request.args.get('featured')
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    count_sql = """
        SELECT COUNT(*) as total
        FROM internships i
        JOIN sectors s ON i.sector_id = s.id
        WHERE 1=1
    """
    sql = """
        SELECT i.*, s.name as sector_name, s.slug as sector_slug
        FROM internships i
        JOIN sectors s ON i.sector_id = s.id
        WHERE 1=1
    """
    where_clause = ""
    params = []

    if sector_slug:
        where_clause += " AND (s.slug = ? OR s.name LIKE ? OR i.slug LIKE ?)"
        sector_term = f"%{sector_slug.replace('-', ' ')}%"
        params.extend([sector_slug, sector_term, f"%{sector_slug}%"])

    if featured_only and featured_only.lower() in ['true', '1']:
        where_clause += " AND i.is_featured = 1"

    if search_query:
        where_clause += " AND (i.title LIKE ? OR i.short_description LIKE ? OR s.name LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term])

    count_res = query_db(count_sql + where_clause, params, one=True)
    total_count = count_res['total'] if count_res else 0

    sql += where_clause + " ORDER BY i.created_at DESC"

    if page and per_page and per_page > 0:
        offset = (page - 1) * per_page
        sql += " LIMIT ? OFFSET ?"
        params.extend([per_page, offset])

    internships = query_db(sql, params)
    
    total_pages = (total_count + per_page - 1) // per_page if (per_page and per_page > 0) else 1
    current_page = page if page else 1

    return jsonify({
        'internships': internships,
        'total': total_count,
        'page': current_page,
        'per_page': per_page or total_count,
        'total_pages': total_pages
    }), 200

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
