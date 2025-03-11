import os
from dotenv import load_dotenv
from providers import register_configured_providers

# Load environment variables from .env file
load_dotenv()

def configure_app(app):
    """Configure the Flask application."""
    # Set Flask configuration
    app.config["JSON_SORT_KEYS"] = False

    # Provider API keys
    app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
    app.config["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY", "")
    app.config["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "")

    # Optional: Configure custom port
    app.config["PORT"] = int(os.environ.get("PORT", 4000))

    # Register providers based on configured API keys
    register_configured_providers(app)
