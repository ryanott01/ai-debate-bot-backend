from typing import List, Dict, Any
import openai
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    """Provider for OpenAI API."""

    def __init__(self, api_key: str):
        # Initialize OpenAI client without proxies to avoid compatibility issues
        self.client = openai.OpenAI(
            api_key=api_key
        )
        self._models = [
            # GPT-4 models
            {"id": "gpt-4o", "name": "GPT-4o - Latest flagship model"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo - Strong performance"},
            {"id": "gpt-4-vision-preview", "name": "GPT-4 Vision - Image capabilities"},
            {"id": "gpt-4", "name": "GPT-4 - Older stable model"},

            # GPT-3.5 models
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo - Fast and cost-effective"}
        ]

    @property
    def name(self) -> str:
        return "openai"

    @property
    def available_models(self) -> List[Dict[str, str]]:
        return self._models

    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        return {
            "provider": self.name,
            "model": model,
            "response": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
