from flask import Flask, jsonify

def register_error_handlers(app: Flask) -> None:
    """Register error handlers with the Flask application."""

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500
