from typing import List, Tuple
import logging

_logger = logging.getLogger(__name__)


class SimpleRetriever:
    """A minimal retriever: uses sentence-transformers if available, otherwise falls
    back to naive keyword matching over provided documents.
    """

    def __init__(self, docs: List[Tuple[str, str]]):
        # docs: list of (id, text)
        self.docs = docs
        self._embedder = None
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            self._embedder = SentenceTransformer('all-MiniLM-L6-v2')
            texts = [t for (_id, t) in docs]
            self._embeddings = self._embedder.encode(texts, convert_to_numpy=True)
            _logger.info("SentenceTransformer embedder loaded for RAG")
        except Exception:
            self._embedder = None
            self._embeddings = None
            _logger.warning("sentence-transformers unavailable; falling back to keyword matching")

    def retrieve(self, query: str, k: int = 3) -> List[Tuple[str, str]]:
        if self._embedder is not None:
            import numpy as np
            q_emb = self._embedder.encode([query], convert_to_numpy=True)[0]
            sims = (self._embeddings @ q_emb) / (
                (np.linalg.norm(self._embeddings, axis=1) * (np.linalg.norm(q_emb) + 1e-12))
            )
            idxs = list(reversed(sims.argsort()))[:k]
            return [self.docs[i] for i in idxs]
        # naive keyword match
        query_terms = set(query.lower().split())
        scored = []
        for _id, text in self.docs:
            words = set(text.lower().split())
            score = len(query_terms & words)
            scored.append((_id, text, score))
        scored.sort(key=lambda x: x[2], reverse=True)
        return [(i, t) for (i, t, s) in scored[:k]]


class RAG:
    def __init__(self, retriever: SimpleRetriever):
        self.retriever = retriever

    def augment(self, prompt: str, query: str, k: int = 3) -> str:
        docs = self.retriever.retrieve(query, k=k)
        context = "\n\n--- Retrieved Context ---\n"
        for doc_id, text in docs:
            context += f"[{doc_id}] {text}\n"
        return prompt + context