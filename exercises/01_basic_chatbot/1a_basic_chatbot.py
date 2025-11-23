"""
Exercise 1a: Create Your First Chatbot
Minimal example of using BasicChatbot with a local LLM.

TODO: Run this chatbot and have a simple conversation.
"""

from src.chatbot.chatbot import BasicChatbot


def main():
    """
    Create and run a basic chatbot.
    
    This demonstrates:
    - Loading a local GGUF model
    - System prompts (instructions for the LLM)
    - Interactive chat loop
    """
    
    # Your model file
    model_path = "./models/tinyllama.gguf"
    
    # Basic system prompt
    system_prompt = "You are a helpful assistant. Answer concisely."
    max_tokens = 256
    
    # Create a BasicChatbot instance
    chatbot = BasicChatbot(
        model_path=model_path,
        system_prompt=system_prompt,
        max_tokens=max_tokens
    )
    
    # Display configuration
    print("=" * 60)
    print("EXERCISE 1a: Create Your First Chatbot")
    print("=" * 60)
    print(f"Model: {model_path}")
    print(f"System Prompt: {system_prompt}")
    print(f"Max Tokens: {max_tokens}")
    print("\nChat started. Type 'exit' to quit.\n")
    
    # Start interactive chat
    chatbot.chat()


if __name__ == "__main__":
    main()
