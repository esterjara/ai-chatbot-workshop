"""
Exercise 3b: Semantic Search for RAG
Learn about embedding-based semantic retrieval.

This exercise uses sentence embeddings to find semantically similar documents.
Compare with Exercise 3a (keyword search) to see the difference.
"""

from src.chatbot.rag import RAGChatbot
from src.chatbot.model_loader import load_model
from llama_cpp import Llama


def main():
    """
    Create and run a RAG chatbot with semantic search.
    
    This demonstrates:
    - Loading an embedding model
    - Generating embeddings for documents
    - Semantic similarity-based retrieval
    """
    
    # Load text generation model
    model = load_model("./models/tinyllama.gguf")
    
    # TODO: Choose and load an embedding model
    # Options: "all-MiniLM-L6-v2-f16.gguf" or "bge-small-en-v1.5-f16.gguf"
    try:
        embedding_model = Llama(
            model_path="./models/all-MiniLM-L6-v2-f16.gguf",
            embed=True,
            n_threads=4,
            verbose=False
        )
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        return
    
    # TODO: Change retrieve_top_k and compare with Exercise 3a
    # Try: 1, 3, 5. Do you get better results than keyword search?
    top_k = 3
    
    # Create RAG chatbot with semantic search mode
    chatbot = RAGChatbot(
        model=model,
        system_prompt="You are a helpful assistant. Use retrieved documents to answer questions accurately.",
        max_tokens=256,
        retrieve_top_k=top_k,
        embedding_model=embedding_model,
        retrieval_mode="semantic"
    )
    
    # Load documents
    try:
        chatbot.load_documents("./data")
        print(f"Loaded {len(chatbot.vector_store.documents)} documents (semantic search, top_k={top_k})")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    print("Type 'exit' to quit\n")
    chatbot.chat()


if __name__ == "__main__":
    main()
