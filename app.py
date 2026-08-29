import os
from flask import Flask, send_from_directory, jsonify
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

    # Static file serving routes
    @app.route('/')
    def serve_index():
        return send_from_directory('static', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join('static', path)):
            return send_from_directory('static', path)
        return send_from_directory('static', 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
        return send_from_directory('static', 'index.html')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
