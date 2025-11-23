"""
Exercise 3c: Hybrid Search for RAG (Optional Advanced)
Learn about combining keyword and semantic search.

This exercise combines both approaches with weighted scoring:
- 70% semantic similarity (meaning-based)
- 30% keyword overlap (exact matches)
"""

from src.chatbot.rag import RAGChatbot
from src.chatbot.model_loader import load_model
from llama_cpp import Llama
import math


class HybridRAGChatbot(RAGChatbot):
    """RAG chatbot using weighted hybrid search."""
    
    def retrieve_context(self, query: str) -> str:
        """
        Retrieve context using hybrid search:
        - 70% weight: semantic similarity (embedding-based)
        - 30% weight: keyword overlap (term matching)
        """
        if not self.vector_store.documents:
            return "No documents available."
        
        # Get semantic scores (if available)
        semantic_scores = {}
        if self.embedding_model:
            query_embedding = self.embedding_model.embed(query)
            for i, doc in enumerate(self.vector_store.documents):
                doc_embedding = self.vector_store.embeddings[i]
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                semantic_scores[i] = similarity
        
        # Get keyword scores
        query_words = set(query.lower().split())
        keyword_scores = {}
        for i, doc in enumerate(self.vector_store.documents):
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            keyword_scores[i] = overlap / (len(query_words) + len(doc_words)) if query_words else 0
        
        # Combine scores (hybrid weighting)
        hybrid_scores = {}
        for i in range(len(self.vector_store.documents)):
            semantic = semantic_scores.get(i, 0) if semantic_scores else 0
            keyword = keyword_scores.get(i, 0)
            # 70% semantic + 30% keyword
            hybrid_scores[i] = (0.7 * semantic) + (0.3 * keyword)
        
        # Get top-k documents by hybrid score
        top_indices = sorted(
            hybrid_scores.keys(),
            key=lambda i: hybrid_scores[i],
            reverse=True
        )[:self.retrieve_top_k]
        
        # Build context with scores
        context_parts = []
        for idx in top_indices:
            score = hybrid_scores[idx]
            semantic = semantic_scores.get(idx, 0) if semantic_scores else 0
            keyword = keyword_scores.get(idx, 0)
            doc_name = self.vector_store.documents[idx][:30] + "..."
            
            context_parts.append(
                f"[{doc_name}]\n"
                f"Hybrid: {score:.2f} (semantic: {semantic:.2f}, keyword: {keyword:.2f})\n"
                f"{self.vector_store.documents[idx][:200]}..."
            )
        
        return "\n---\n".join(context_parts)
    
    @staticmethod
    def _cosine_similarity(vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2:
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0


def main():
    """
    Create and run a RAG chatbot with hybrid search.
    
    This demonstrates:
    - Loading both text and embedding models
    - Combining keyword and semantic retrieval
    - Weighted scoring (70% semantic + 30% keyword)
    """
    
    # Load text generation model
    model = load_model("./models/tinyllama.gguf")
    
    # TODO: Load embedding model for hybrid search
    # Without it, hybrid search falls back to keyword-only
    try:
        embedding_model = Llama(
            model_path="./models/all-MiniLM-L6-v2-f16.gguf",
            embed=True,
            n_threads=4,
            verbose=False
        )
    except Exception as e:
        print(f"Warning: Embedding model not available, using keyword-only: {e}")
        embedding_model = None
    
    # TODO: Try different weights by modifying the hybrid formula
    # Current: 70% semantic + 30% keyword
    # Try: 80/20, 60/40, or 50/50. Which works best?
    top_k = 3
    
    # Create RAG chatbot with hybrid search
    chatbot = HybridRAGChatbot(
        model=model,
        system_prompt="You are a helpful assistant. Use retrieved documents to answer questions accurately.",
        max_tokens=256,
        retrieve_top_k=top_k,
        embedding_model=embedding_model,
        retrieval_mode="hybrid"
    )
    
    # Load documents
    try:
        chatbot.load_documents("./data")
        print(f"Loaded {len(chatbot.vector_store.documents)} documents (hybrid search, top_k={top_k})")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    print("Type 'exit' to quit\n")
    chatbot.chat()


if __name__ == "__main__":
    main()
