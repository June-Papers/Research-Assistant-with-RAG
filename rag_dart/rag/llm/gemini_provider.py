from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL
from rag.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Gemini-backed LLM provider."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.client = genai.Client(api_key=api_key or GEMINI_API_KEY)
        self.model = model or GEMINI_MODEL

    def generate(self, prompt: str) -> str:
        """Generate a response using the Gemini API."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return getattr(response, "text", str(response))
