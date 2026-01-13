"""Flask application initialization"""
from flask import Flask
from app.config import Config

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app

