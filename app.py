import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from config import Config
from database import init_db

# Import blueprints
from routes.auth_routes import auth_bp
from routes.sector_routes import sector_bp
from routes.internship_routes import internship_bp
from routes.application_routes import application_bp
from routes.submission_routes import submission_bp
from routes.certificate_routes import certificate_bp
from routes.payment_routes import payment_bp
from routes.admin_routes import admin_bp
from routes.public_routes import public_bp
from routes.document_routes import document_bp

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Initialize Database Schema & Seed Data
    with app.app_context():
        init_db()

    # Register API blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(sector_bp)
    app.register_blueprint(internship_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(certificate_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(document_bp)

    # Static file serving routes
    @app.route('/templates/<path:path>')
    def serve_templates(path):
        templates_dir = Config.TEMPLATE_DIR
        target = os.path.join(templates_dir, path)
        if os.path.exists(target) and not os.path.isdir(target):
            return send_from_directory(templates_dir, path)
        return jsonify({'error': 'Template file not found'}), 404

    @app.route('/public/<path:path>')
    def serve_public(path):
        public_dir = Config.PUBLIC_DIR
        target = os.path.join(public_dir, path)
        if os.path.exists(target) and not os.path.isdir(target):
            return send_from_directory(public_dir, path)
        return jsonify({'error': 'Public file not found'}), 404

    @app.route('/api/templates', methods=['GET'])
    def get_template_config():
        templates = {}
        for key, info in Config.DOCUMENT_TEMPLATES.items():
            exists = os.path.exists(info['path'])
            templates[key] = {
                'filename': info['filename'],
                'url': info['url'],
                'path': info['path'],
                'exists': exists
            }
        return jsonify({
            'status': 'success',
            'templates': templates
        }), 200

    @app.route('/')
    def serve_index():
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        if os.path.exists(os.path.join(static_dir, 'index.html')):
            return send_from_directory(static_dir, 'index.html')
        return jsonify({'message': 'Web Intern API is running'}), 200

    @app.route('/<path:path>')
    def serve_static(path):
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        target = os.path.join(static_dir, path)
        if os.path.exists(target) and not os.path.isdir(target):
            return send_from_directory(static_dir, path)
        if os.path.exists(os.path.join(static_dir, 'index.html')):
            return send_from_directory(static_dir, 'index.html')
        return jsonify({'message': 'Web Intern API is running', 'requested_path': path}), 200

    @app.errorhandler(404)
    def not_found(e):
        req_path = request.path if request else ''
        if req_path.startswith('/api/') or req_path.startswith('/internships') or req_path.startswith('/sectors'):
            return jsonify({'error': f"API endpoint '{req_path}' not found"}), 404
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        if os.path.exists(os.path.join(static_dir, 'index.html')):
            return send_from_directory(static_dir, 'index.html')
        return jsonify({'error': 'Page not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
