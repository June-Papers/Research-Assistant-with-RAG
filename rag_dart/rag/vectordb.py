import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings


class VectorDB:
    """Manage a ChromaDB vector store for report chunks."""

    def __init__(self, persist_dir: str = "vector_db") -> None:
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="dart_reports")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        """Add document chunks to the vector store."""
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query(self, query: str, embeddings: List[float], where: Optional[Dict[str, Any]] = None, top_k: int = 3) -> Dict[str, Any]:
        """Query the collection using metadata filters and similarity search."""
        return self.collection.query(
            query_embeddings=[embeddings],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
