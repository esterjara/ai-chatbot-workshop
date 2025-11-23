"""
Retrieval-Augmented Generation (RAG).
"""

from typing import List, Tuple, Optional
import math
import os
from .model_loader import generate_text
from .memory import RollingMemory
from llama_cpp import Llama
import logging

_logger = logging.getLogger(__name__)


class VectorStore:
    """
    Simple in-memory vector store for document embeddings.
    Uses cosine similarity for retrieval.
    """
    
    def __init__(self):
        self.documents: List[Tuple[str, str]] = []
    
    def add_document(self, doc_id: str, text: str):
        """Add a document to the store."""
        self.documents.append((doc_id, text))
    
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
        Retrieve documents using simple keyword matching.
        Fall back method when embeddings are not available.
        """
        query_terms = set(query.lower().split())
        scores = []
        
        for doc_id, text in self.documents:
            doc_terms = set(text.lower().split())
            overlap = len(query_terms & doc_terms)
            scores.append((doc_id, text, overlap))
        
        scores.sort(key=lambda x: x[2], reverse=True)
        return [(doc_id, text) for doc_id, text, _ in scores[:top_k]]
    
    def __len__(self) -> int:
        return len(self.documents)


class RAGChatbot:
    """
    A chatbot with Retrieval-Augmented Generation.
    Retrieves relevant documents and uses them to augment responses.
    """
    
    def __init__(
        self,
        model: Llama,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        retrieve_top_k: int = 3
    ):
        """
        Initialize the RAGChatbot.
        
        Args:
            model: Llama model instance
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens per response
            retrieve_top_k: Number of documents to retrieve per query
        """
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.retrieve_top_k = retrieve_top_k
        self.vector_store = VectorStore()
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
        """Retrieve relevant documents for the query."""
        if len(self.vector_store) == 0:
            return "No documents available."
        
        results = self.vector_store.retrieve_by_keyword(query, top_k=self.retrieve_top_k)
        
        context_lines = []
        for doc_id, doc_text in results:
            # Truncate long documents
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
        print(f"Max tokens: {self.max_tokens}")
        print("Commands: 'exit', 'clear', 'history', 'docs'\n")
        
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
            
            if not user_input:
                continue
            
            try:
                response = self.generate_response(user_input)
                print(f"Assistant: {response}\n")
            except Exception as e:
                print(f"Error: {e}\n")
