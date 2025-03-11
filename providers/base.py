from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    """Base class for all AI providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the provider name."""
        pass

    @property
    @abstractmethod
    def available_models(self) -> List[Dict[str, str]]:
        """Get a list of available models for this provider."""
        pass

    @abstractmethod
    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model.

        Args:
            model: The specific model to use
            messages: List of message objects with role and content
            **kwargs: Additional parameters specific to the provider

        Returns:
            Dictionary with the generated response
        """
        pass
