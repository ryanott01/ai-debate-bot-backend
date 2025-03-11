from typing import List, Dict, Any
import google.generativeai as genai
from .base import BaseProvider

class GoogleProvider(BaseProvider):
    """Provider for Google Generative AI API."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self._models = [
            # Gemini 2.0 models (newest)
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash - Powerful multi-modal (1M context)"},
            {"id": "gemini-2.0-flash-lite", "name": "Gemini 2.0 Flash-Lite - Cost effective"},

            # Gemini 1.5 models
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash - Fast multi-modal (1M context)"},
            {"id": "gemini-1.5-flash-8b", "name": "Gemini 1.5 Flash-8B - Smallest model (1M context)"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro - Highest intelligence (2M context)"},

            # Legacy models (for backward compatibility)
            {"id": "gemini-pro", "name": "Gemini Pro (Legacy)"}
        ]

    @property
    def name(self) -> str:
        return "google"

    @property
    def available_models(self) -> List[Dict[str, str]]:
        return self._models

    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        # Configure generation parameters
        generation_config = {
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.95),
            "top_k": kwargs.get("top_k", 40),
            "max_output_tokens": kwargs.get("max_tokens", 1024),  # map max_tokens to max_output_tokens
        }

        # Initialize the model with proper configuration
        model_instance = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config
        )

        # Convert the messages format from OpenAI to Google format
        google_messages = []
        for msg in messages:
            # Map roles: "system" and "assistant" -> "model", "user" -> "user"
            role = "model" if msg["role"] in ["assistant", "system"] else "user"
            google_messages.append({"role": role, "parts": [{"text": msg["content"]}]})

        try:
            # Start chat session and send the message
            chat = model_instance.start_chat(history=google_messages[:-1] if google_messages else [])
            response = chat.send_message(messages[-1]["content"])

            # Extract usage metrics if available
            usage = {}
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                meta = response.usage_metadata
                if hasattr(meta, 'prompt_token_count'):
                    usage["input_tokens"] = meta.prompt_token_count
                if hasattr(meta, 'candidates_token_count'):
                    usage["output_tokens"] = meta.candidates_token_count
                if hasattr(meta, 'total_token_count'):
                    usage["total_tokens"] = meta.total_token_count

            return {
                "provider": self.name,
                "model": model,
                "response": response.text,
                "usage": usage if usage else None
            }

        except Exception as e:
            # Provide more detailed error information
            error_msg = str(e)
            if "is not supported" in error_msg:
                error_msg += " (Note: Some models might be available only in the paid tier)"

            return {
                "provider": self.name,
                "model": model,
                "error": error_msg,
                "response": f"Error generating response: {error_msg}"
            }
