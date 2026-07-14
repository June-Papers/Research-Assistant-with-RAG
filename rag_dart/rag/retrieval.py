from typing import Any, Dict, List, Optional

from rag.embedding import EmbeddingClient
from rag.vectordb import VectorDB


class Retriever:
    """Retrieve relevant chunks from the vector store using metadata filters."""

    def __init__(self, vector_db: VectorDB, embedding_client: EmbeddingClient) -> None:
        self.vector_db = vector_db
        self.embedding_client = embedding_client

    def retrieve(self, query: str, metadata_filter: Optional[Dict[str, Any]] = None, top_k: int = 3) -> Dict[str, Any]:
        """Retrieve top-k chunks for the query and filter by metadata."""
        embeddings = self.embedding_client.embed_texts([query])[0]
        return self.vector_db.query(query=query, embeddings=embeddings, where=metadata_filter, top_k=top_k)
