"""
Exercise 3c: Hybrid Search for RAG (SOLUTION - Optional Advanced)

This is the reference implementation showing:
- Combining keyword and semantic search
- Weighted scoring: 70% semantic + 30% keyword
"""

from src.chatbot.rag import RAGChatbot
from src.chatbot.model_loader import load_model
from llama_cpp import Llama
import math


class HybridRAGChatbot(RAGChatbot):
    """RAG chatbot using weighted hybrid search (70% semantic + 30% keyword)."""
    
    def retrieve_context(self, query: str) -> str:
        """
        Retrieve context using hybrid search:
        - 70% weight: semantic similarity (embedding-based)
        - 30% weight: keyword overlap (term matching)
        
        This combines the best of both approaches:
        - Semantic search handles synonyms and paraphrasing
        - Keyword search catches exact matches
        """
        if not self.vector_store.documents:
            return "No documents available."
        
        # Step 1: Get semantic scores (if embedding model available)
        semantic_scores = {}
        if self.embedding_model:
            query_embedding = self.embedding_model.embed(query)
            for i, doc in enumerate(self.vector_store.documents):
                doc_embedding = self.vector_store.embeddings[i]
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                semantic_scores[i] = similarity
        
        # Step 2: Get keyword scores (term overlap)
        query_words = set(query.lower().split())
        keyword_scores = {}
        for i, doc in enumerate(self.vector_store.documents):
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            # Normalize by total words to get a score between 0 and 1
            keyword_scores[i] = overlap / (len(query_words) + len(doc_words)) if query_words else 0
        
        # Step 3: Combine scores with weights (70% semantic + 30% keyword)
        hybrid_scores = {}
        for i in range(len(self.vector_store.documents)):
            semantic = semantic_scores.get(i, 0) if semantic_scores else 0
            keyword = keyword_scores.get(i, 0)
            # SOLUTION: This is the hybrid formula. Try changing weights:
            # 80/20: hybrid_scores[i] = (0.8 * semantic) + (0.2 * keyword)
            # 60/40: hybrid_scores[i] = (0.6 * semantic) + (0.4 * keyword)
            hybrid_scores[i] = (0.7 * semantic) + (0.3 * keyword)
        
        # Step 4: Get top-k documents by hybrid score
        top_indices = sorted(
            hybrid_scores.keys(),
            key=lambda i: hybrid_scores[i],
            reverse=True
        )[:self.retrieve_top_k]
        
        # Step 5: Build context with detailed scoring information
        context_parts = []
        for idx in top_indices:
            score = hybrid_scores[idx]
            semantic = semantic_scores.get(idx, 0) if semantic_scores else 0
            keyword = keyword_scores.get(idx, 0)
            
            # Show first 30 chars of document as name
            doc_name = self.vector_store.documents[idx][:30] + "..."
            
            context_parts.append(
                f"[{doc_name}]\n"
                f"Hybrid Score: {score:.2f} (semantic: {semantic:.2f}, keyword: {keyword:.2f})\n"
                f"{self.vector_store.documents[idx][:200]}..."
            )
        
        return "\n---\n".join(context_parts)
    
    @staticmethod
    def _cosine_similarity(vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors (0.0 to 1.0)."""
        if not vec1 or not vec2:
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0


def main():
    """
    Create and run a RAG chatbot with hybrid search.
    
    Demonstrates:
    - Loading both text and embedding models
    - Combining keyword and semantic retrieval
    - Weighted scoring to balance both approaches
    
    Use cases for hybrid search:
    - When you need both exact matches AND semantic understanding
    - Financial/legal: exact terms important but context matters
    - Customer support: FAQ exact matches + paraphrasing
    - Search engines: precision + recall balance
    """
    
    # Load text generation model
    model = load_model("./models/tinyllama.gguf")
    
    # SOLUTION: Load embedding model for semantic component
    # Without it, hybrid search falls back to keyword-only
    try:
        embedding_model = Llama(
            model_path="./models/all-MiniLM-L6-v2-f16.gguf",
            embed=True,
            n_threads=4,
            verbose=False
        )
        print("✓ Embedding model loaded")
    except Exception as e:
        print(f"Warning: Embedding model not available: {e}")
        print("Hybrid search will use keyword-only mode\n")
        embedding_model = None
    
    # SOLUTION: Try different weight combinations
    # Current: 70% semantic + 30% keyword (balanced)
    # Try: 80/20 (more semantic), 60/40 (more keyword), 50/50 (equal)
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
    
    print("Type 'exit' to quit")
    print("Compare hybrid results with 3a (keyword) and 3b (semantic)\n")
    
    # Run the chatbot
    chatbot.chat()


if __name__ == "__main__":
    main()
