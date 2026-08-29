from flask import Blueprint, jsonify
from database import query_db

sector_bp = Blueprint('sector_bp', __name__)

@sector_bp.route('/api/sectors', methods=['GET'])
def get_sectors():
    sectors = query_db("SELECT * FROM sectors ORDER BY name ASC")
    for sec in sectors:
        count_res = query_db("SELECT COUNT(*) as count FROM internships WHERE sector_id = ?", (sec['id'],), one=True)
        sec['internships_count'] = count_res['count'] if count_res else 0
    return jsonify({'sectors': sectors}), 200

@sector_bp.route('/api/sectors/<slug>', methods=['GET'])
def get_sector_by_slug(slug):
    sector = query_db("SELECT * FROM sectors WHERE slug = ?", (slug,), one=True)
    if not sector:
        return jsonify({'error': 'Sector not found.'}), 404
        
    internships = query_db("SELECT * FROM internships WHERE sector_id = ? ORDER BY created_at DESC", (sector['id'],))
    for item in internships:
        item['sector_name'] = sector['name']
        item['sector_slug'] = sector['slug']
        
    sector['internships'] = internships
    return jsonify({'sector': sector}), 200
