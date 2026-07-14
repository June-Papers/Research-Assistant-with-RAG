from config import LLM_PROVIDER
from rag.llm.base import LLMProvider
from rag.llm.gemini_provider import GeminiProvider
from rag.llm.openai_provider import OpenAIProvider


def get_llm() -> LLMProvider:
    """Return an LLM provider based on the configured provider name."""
    provider_name = (LLM_PROVIDER or "openai").lower()
    if provider_name == "openai":
        return OpenAIProvider()
    if provider_name == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
