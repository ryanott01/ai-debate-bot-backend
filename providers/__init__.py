from typing import Dict, List
from flask import Flask
from .base import BaseProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider

# Registry to store configured providers
providers: Dict[str, BaseProvider] = {}

def register_provider(provider: BaseProvider) -> None:
    """Register a provider in the global registry."""
    providers[provider.name] = provider

def unregister_provider(name: str) -> None:
    """Remove a provider from the registry."""
    if name in providers:
        del providers[name]

def get_provider(name: str) -> BaseProvider:
    """Get a provider by name."""
    if name not in providers:
        raise ValueError(f"Provider '{name}' not configured")
    return providers[name]

def get_all_providers() -> List[str]:
    """Get a list of all registered provider names."""
    return list(providers.keys())

def register_configured_providers(app: Flask) -> None:
    """Register providers based on configured API keys."""
    # Clear existing providers
    providers.clear()

    # Register OpenAI if API key is provided
    if app.config.get("OPENAI_API_KEY"):
        try:
            register_provider(OpenAIProvider(app.config["OPENAI_API_KEY"]))
            print("✅ OpenAI provider registered successfully")
        except Exception as e:
            print(f"❌ Failed to register OpenAI provider: {str(e)}")

    # Register Anthropic if API key is provided
    if app.config.get("ANTHROPIC_API_KEY"):
        try:
            register_provider(AnthropicProvider(app.config["ANTHROPIC_API_KEY"]))
            print("✅ Anthropic provider registered successfully")
        except Exception as e:
            print(f"❌ Failed to register Anthropic provider: {str(e)}")

    # Register Google if API key is provided
    if app.config.get("GOOGLE_API_KEY"):
        try:
            register_provider(GoogleProvider(app.config["GOOGLE_API_KEY"]))
            print("✅ Google provider registered successfully")
        except Exception as e:
            print(f"❌ Failed to register Google provider: {str(e)}")
