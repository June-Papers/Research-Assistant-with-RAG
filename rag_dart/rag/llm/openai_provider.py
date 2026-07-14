from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from rag.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI-backed LLM provider."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = model or OPENAI_MODEL

    def generate(self, prompt: str) -> str:
        """Generate a response using the OpenAI Responses API."""
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text
