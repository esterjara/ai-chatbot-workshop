"""
Exercise 3a: Keyword Search for RAG
Learn about keyword-based document retrieval.

This exercise uses simple keyword matching to find relevant documents.
Ask questions and observe how the chatbot retrieves and uses documents.
"""

from src.chatbot.rag import RAGChatbot
from src.chatbot.model_loader import load_model


def main():
    """
    Create and run a RAG chatbot with keyword search.
    
    This demonstrates:
    - Loading external documents
    - Keyword-based retrieval
    - Augmenting prompts with retrieved context
    """
    
    # Load text generation model
    model = load_model("./models/tinyllama.gguf")
    
    # TODO: Change retrieve_top_k and observe the difference
    # Try: 1, 3, 5. Which gives best results for your questions?
    top_k = 3
    
    # Create RAG chatbot with keyword search mode
    chatbot = RAGChatbot(
        model=model,
        system_prompt="You are a helpful assistant. Use retrieved documents to answer questions accurately.",
        max_tokens=256,
        retrieve_top_k=top_k,
        retrieval_mode="keyword"
    )
    
    # Load documents
    try:
        chatbot.load_documents("./data")
        print(f"Loaded {len(chatbot.vector_store.documents)} documents (keyword search, top_k={top_k})")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    print("Type 'exit' to quit\n")
    chatbot.chat()


if __name__ == "__main__":
    main()
