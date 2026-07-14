from typing import List

from openai import OpenAI

from config import OPENAI_API_KEY


class EmbeddingClient:
    """Create embeddings using OpenAI."""

    def __init__(self, api_key: str, model: str = "text-embedding-3-large") -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts."""
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]
