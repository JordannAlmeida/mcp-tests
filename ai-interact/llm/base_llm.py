from abc import ABC, abstractmethod
from io import BytesIO

class BaseLLM(ABC):
    @abstractmethod
    def initialize_model(self):
        """Initializes and returns the LLM model."""
        pass

    @abstractmethod
    def generate_response(self, prompt: str, files: list[dict[str, BytesIO]] = None) -> str:
        """Generates a response from the LLM model. Optionally accepts files as BytesIO."""
        pass