from typing import List, Dict, Any
import anthropic
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    """Provider for Anthropic API."""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self._models = [
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
            {"id": "claude-3.5-sonnet-20240620", "name": "Claude 3.5 Sonnet"}
        ]

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def available_models(self) -> List[Dict[str, str]]:
        return self._models

    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        # Convert the messages format from OpenAI to Anthropic format
        anthropic_messages = []
        for msg in messages:
            role = "assistant" if msg["role"] == "assistant" else "user"
            anthropic_messages.append({"role": role, "content": msg["content"]})

        response = self.client.messages.create(
            model=model,
            messages=anthropic_messages,
            max_tokens=kwargs.get("max_tokens", 1024)
        )

        return {
            "provider": self.name,
            "model": model,
            "response": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
