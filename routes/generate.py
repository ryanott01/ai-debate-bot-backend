
from flask import Blueprint, request, jsonify
from providers import get_provider
from utils.validation import validate_generate_request

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate", methods=["POST"])
def generate():
    """Generate a response from an AI model."""
    # Validate request
    data = request.json
    errors = validate_generate_request(data)
    if errors:
        return jsonify({"errors": errors}), 400

    provider_name = data["provider"]
    model = data["model"]
    messages = data["messages"]

    # Optional parameters
    options = data.get("options", {})

    try:
        # Get the provider and generate response
        provider = get_provider(provider_name)
        response = provider.generate(model=model, messages=messages, **options)
        return jsonify(response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to generate response: {str(e)}"}), 500
