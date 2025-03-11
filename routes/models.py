from flask import Blueprint, jsonify
from providers import get_all_providers, get_provider, providers

models_bp = Blueprint("models", __name__)

@models_bp.route("/providers", methods=["GET"])
def list_providers():
    """List all configured providers."""
    return jsonify({
        "providers": get_all_providers()
    })

@models_bp.route("/models", methods=["GET"])
def list_all_models():
    """List all available models from all providers."""
    result = {}

    for provider_name in get_all_providers():
        provider = get_provider(provider_name)
        result[provider_name] = provider.available_models

    return jsonify(result)

@models_bp.route("/models/<provider>", methods=["GET"])
def list_provider_models(provider):
    """List models for a specific provider."""
    try:
        provider_instance = get_provider(provider)
        return jsonify({
            "provider": provider,
            "models": provider_instance.available_models
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
