"""
Retrieval-Augmented Generation (RAG).
Supports both keyword search and semantic search with embeddings.
"""

from typing import List, Tuple, Optional
import math
import os
from .model_loader import generate_text
from .memory import RollingMemory
from llama_cpp import Llama
import logging

_logger = logging.getLogger(__name__)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if len(vec1) == 0 or len(vec2) == 0:
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


class VectorStore:
    """
    In-memory vector store for document storage and retrieval.
    Supports both keyword matching and semantic similarity search.
    """
    
    def __init__(self, embedding_model: Optional[Llama] = None):
        self.documents: List[Tuple[str, str]] = []
        self.embeddings: List[List[float]] = []
        self.embedding_model = embedding_model
    
    def add_document(self, doc_id: str, text: str):
        """
        Add a document to the store.
        If embedding model is available, generates and stores embedding.
        """
        self.documents.append((doc_id, text))
        
        # Generate embedding if model available
        if self.embedding_model:
            try:
                embedding = self.embedding_model.embed(text)
                self.embeddings.append(embedding)
                _logger.info(f"Embedded document: {doc_id}")
            except Exception as e:
                _logger.warning(f"Failed to embed {doc_id}: {e}")
                self.embeddings.append([])
        else:
            self.embeddings.append([])
    
    def load_documents_from_directory(self, directory: str):
        """Load all .txt files from a directory."""
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.add_document(filename, content)
                    _logger.info(f"Loaded document: {filename}")
    
    def retrieve_by_keyword(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        """
        Retrieve documents using keyword matching.
        Splits query and documents into terms and counts overlap.
        """
        query_terms = set(query.lower().split())
        scores = []
        
        for doc_id, text in self.documents:
            doc_terms = set(text.lower().split())
            overlap = len(query_terms & doc_terms)
            scores.append((doc_id, text, overlap))
        
        scores.sort(key=lambda x: x[2], reverse=True)
        return [(doc_id, text) for doc_id, text, _ in scores[:top_k]]
    
    def retrieve_by_similarity(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
        """
        Retrieve documents using semantic similarity with embeddings.
        Returns (doc_id, text, score) tuples.
        """
        if not self.embedding_model:
            _logger.warning("Embedding model not available, falling back to keyword search")
            results = self.retrieve_by_keyword(query, top_k)
            return [(doc_id, text, 0.0) for doc_id, text in results]
        
        try:
            query_embedding = self.embedding_model.embed(query)
        except Exception as e:
            _logger.error(f"Failed to embed query: {e}")
            results = self.retrieve_by_keyword(query, top_k)
            return [(doc_id, text, 0.0) for doc_id, text in results]
        
        scores = []
        for idx, (doc_id, text) in enumerate(self.documents):
            if idx < len(self.embeddings) and self.embeddings[idx]:
                similarity = cosine_similarity(query_embedding, self.embeddings[idx])
            else:
                similarity = 0.0
            
            scores.append((doc_id, text, similarity))
        
        scores.sort(key=lambda x: x[2], reverse=True)
        return scores[:top_k]
    
    def __len__(self) -> int:
        return len(self.documents)


class RAGChatbot:
    """
    A chatbot with Retrieval-Augmented Generation.
    Supports both keyword search and semantic search with embeddings.
    """
    
    def __init__(
        self,
        model: Llama,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        retrieve_top_k: int = 3,
        embedding_model: Optional[Llama] = None,
        retrieval_mode: str = "keyword"
    ):
        """
        Initialize the RAGChatbot.
        
        Args:
            model: Llama model instance for text generation
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens per response
            retrieve_top_k: Number of documents to retrieve per query
            embedding_model: Llama model with embed=True for semantic search
            retrieval_mode: "keyword" or "semantic" search mode
        """
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.retrieve_top_k = retrieve_top_k
        self.retrieval_mode = retrieval_mode
        self.vector_store = VectorStore(embedding_model)
        self.memory = RollingMemory(capacity=10)
    
    def load_documents(self, directory: str):
        """Load documents from a directory."""
        self.vector_store.load_documents_from_directory(directory)
        _logger.info(f"Loaded {len(self.vector_store)} documents")
    
    def get_history_string(self) -> str:
        """Format conversation history as a string."""
        if not self.memory.get():
            return "No previous messages."
        
        lines = []
        for role, text in self.memory.get():
            lines.append(f"{role.capitalize()}: {text}")
        
        return "\n".join(lines)
    
    def retrieve_context(self, query: str) -> str:
        """
        Retrieve relevant documents for the query.
        Uses either keyword or semantic search based on retrieval_mode.
        """
        if len(self.vector_store) == 0:
            return "No documents available."
        
        # Retrieve based on mode
        if self.retrieval_mode == "semantic":
            results = self.vector_store.retrieve_by_similarity(query, top_k=self.retrieve_top_k)
            # Format: (doc_id, text, score)
            context_lines = []
            for doc_id, doc_text, score in results:
                truncated = doc_text[:300] + "..." if len(doc_text) > 300 else doc_text
                context_lines.append(f"[{doc_id}] (similarity: {score:.2f})\n{truncated}")
        else:  # keyword mode
            results = self.vector_store.retrieve_by_keyword(query, top_k=self.retrieve_top_k)
            # Format: (doc_id, text)
            context_lines = []
            for doc_id, doc_text in results:
                truncated = doc_text[:300] + "..." if len(doc_text) > 300 else doc_text
                context_lines.append(f"[{doc_id}]\n{truncated}")
        
        return "\n\n".join(context_lines)
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response using RAG.
        
        Args:
            user_input: The user's message
            
        Returns:
            The model's response
        """
        # Retrieve context
        context = self.retrieve_context(user_input)
        history = self.get_history_string()
        
        full_prompt = f"""{self.system_prompt}

Conversation History:
{history}

Retrieved Context:
{context}

User: {user_input}
Assistant:"""
        
        try:
            response = generate_text(
                self.model,
                full_prompt,
                max_tokens=self.max_tokens
            )
            
            # Store in memory
            self.memory.add("user", user_input)
            self.memory.add("assistant", response)
            
            return response
        except Exception as e:
            _logger.error(f"Generation failed: {e}")
            raise
    
    def chat(self):
        """Start an interactive chat loop with RAG."""
        print(f"RAG Chatbot initialized")
        print(f"Documents: {len(self.vector_store)}")
        print(f"Retrieval mode: {self.retrieval_mode}")
        print(f"Top-k: {self.retrieve_top_k}")
        print(f"Max tokens: {self.max_tokens}")
        print("Commands: 'exit', 'clear', 'history', 'docs', 'mode'\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "clear":
                self.memory.clear()
                print("Memory cleared.\n")
                continue
            
            if user_input.lower() == "history":
                print("\nConversation History:")
                print(self.get_history_string())
                print()
                continue
            
            if user_input.lower() == "docs":
                if len(self.vector_store) > 0:
                    print("Loaded documents:")
                    for doc_id, _ in self.vector_store.documents:
                        print(f"  - {doc_id}")
                else:
                    print("No documents loaded")
                print()
                continue
            
            if user_input.lower() == "mode":
                print(f"Current mode: {self.retrieval_mode}")
                print("Available modes: 'keyword', 'semantic'")
                print("To change mode, edit retrieval_mode in the script\n")
                continue
            
            if not user_input:
                continue
            
            try:
                response = self.generate_response(user_input)
                print(f"Assistant: {response}\n")
            except Exception as e:
                print(f"Error: {e}\n")
