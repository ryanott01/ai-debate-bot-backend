from typing import List, Dict, Any
import google.generativeai as genai
from .base import BaseProvider

class GoogleProvider(BaseProvider):
    """Provider for Google Generative AI API."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self._models = [
            {"id": "gemini-pro", "name": "Gemini Pro"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro"}
        ]

    @property
    def name(self) -> str:
        return "google"

    @property
    def available_models(self) -> List[Dict[str, str]]:
        return self._models

    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        model_instance = genai.GenerativeModel(model_name=model)

        # Convert the messages format from OpenAI to Google format
        google_messages = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            google_messages.append({"role": role, "parts": [{"text": msg["content"]}]})

        chat = model_instance.start_chat(history=google_messages)
        response = chat.send_message(messages[-1]["content"])

        return {
            "provider": self.name,
            "model": model,
            "response": response.text
        }
