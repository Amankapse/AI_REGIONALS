# app.py - NO auto-threads
from flask import Flask
from flask_session import Session
from routes.main import main_bp
from routes.inspection import inspection_bp
from routes.dashboard import dashboard_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(inspection_bp, url_prefix="/inspection")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    
    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 Flask + Vision + Voice AI running on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
