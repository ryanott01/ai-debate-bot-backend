from flask import Flask
from routes import register_routes
from utils.error_handlers import register_error_handlers
from config import configure_app

def create_app():
    app = Flask(__name__)

    # Configure the app
    configure_app(app)

    # Register routes
    register_routes(app)

    # Register error handlers
    register_error_handlers(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=app.config.get("PORT", 4000))
