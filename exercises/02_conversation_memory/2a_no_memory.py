"""
Exercise 2a: Chat WITHOUT Memory - The Problem
This chatbot has NO memory. Each message is independent.
Notice how it fails to maintain conversation context.
"""

from src.chatbot.chatbot import BasicChatbot


def main():
    """
    Create and run a basic chatbot WITHOUT memory.
    Each message is independent - no conversation history.
    """
    
    # Load model
    model_path = "./models/tinyllama.gguf"
    
    # Create a BASIC chatbot - no memory
    chatbot = BasicChatbot(
        model_path=model_path,
        system_prompt="You are a helpful assistant. Answer concisely.",
        max_tokens=256
    )
    
    # Start chat - no memory, each message independent
    # Try: "My name is Alice" then "What is my name?" to see the problem
    print("Exercise 2a: No memory chatbot")
    print("Type 'exit' to quit.\n")
    chatbot.chat()


if __name__ == "__main__":
    main()
