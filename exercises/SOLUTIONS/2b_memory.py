"""
SOLUTION: Exercise 2b - With Memory (Reference Implementation)

This chatbot HAS memory. Compare with 2a to see the difference!
"""

import os 
from dotenv import load_dotenv
from chatbot import MemoryChatbot

load_dotenv()

def main():
    """
    Create and run a chatbot WITH conversation memory.
    
    This demonstrates:
    - Conversation history storage
    - Memory buffer management
    - Context-aware responses
    - Multi-turn coherence
    """
    
    # Load model
    model_path = os.getenv("MODEL_PATH", "./models/tinyllama.gguf")
    max_tokens = os.getenv("MAX_TOKENS", 256)
    
    # Create chatbot WITH memory
    # Now the chatbot can remember previous messages!
    memory_turns = 3
    
    chatbot = MemoryChatbot(
        model_path=model_path,
        system_prompt="You are a helpful assistant with memory. Remember the conversation context.",
        max_tokens=max_tokens,
        max_memory_turns=memory_turns
    )
    
    # Start chat with memory buffer
    print("Exercise 2b: With memory chatbot (buffer size: {0} turns)".format(memory_turns))
    print("Try this conversation to test memory:")
    print("  1. I like Python and AI development'")
    print("  2. 'What are my interests'")
    print("Commands: 'history' (show memory), 'clear' (erase), 'exit' (quit)\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
        except EOFError:
            break
        
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "history":
            # SOLUTION: Show conversation history from memory
            messages = chatbot.memory.get()
            if not messages:
                print("Memory is empty.\n")
            else:
                print("Conversation history:")
                for role, content in messages:
                    print("  {0}: {1}".format(role.upper(), content))
                print()
            continue
        elif user_input.lower() == "clear":
            # SOLUTION: Clear the memory buffer
            chatbot.memory.clear()
            print("Memory cleared.\n")
            continue
        
        if not user_input:
            continue
        
        # Generate response using memory
        response = chatbot.generate_response(user_input)
        print("🤖 Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
