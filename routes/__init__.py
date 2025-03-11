from flask import Flask
from .generate import generate_bp
from .models import models_bp

def register_routes(app: Flask) -> None:
    """Register all routes with the Flask application."""
    app.register_blueprint(generate_bp)
    app.register_blueprint(models_bp)
