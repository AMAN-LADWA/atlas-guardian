"""
Vector DB placeholder. Implement Pinecone, Supabase, or other provider here.
This minimal interface is used by the agent to upsert/query reports and notes.
"""
from typing import List, Dict, Any, Optional


class VectorDB:
    def __init__(self, provider: str = "mock", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        # TODO: initialize Pinecone or Supabase client when integrating
        self._store = []  # local in-memory store for scaffold

    def upsert(self, namespace: str, items: List[Dict[str, Any]]):
        """Upsert items into the vector DB namespace. Items should be dicts.

        For scaffold we append to an in-memory list. Replace with embeddings+upsert.
        """
        for it in items:
            entry = {"namespace": namespace, "item": it}
            self._store.append(entry)
        return True

    def query(self, namespace: str, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Return mock results. Replace with a real similarity search."""
        # TODO: Implement real query using provider SDK
        return [s for s in self._store if s["namespace"] == namespace][:top_k]
