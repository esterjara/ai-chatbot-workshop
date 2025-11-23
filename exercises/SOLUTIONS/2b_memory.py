"""
SOLUTION: Exercise 2b - With Memory (Reference Implementation)

This chatbot HAS memory. Compare with 2a to see the difference!
"""

from src.chatbot.memory import MemoryChatbot
from src.chatbot.model_loader import load_model


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
    model = load_model("./models/tinyllama.gguf")
    
    # Create chatbot WITH memory
    # Now the chatbot can remember previous messages!
    memory_turns = 3
    
    chatbot = MemoryChatbot(
        model=model,
        system_prompt="You are a helpful assistant with memory. Remember the conversation context.",
        max_tokens=256,
        max_memory_turns=memory_turns
    )
    
    # Start chat with memory buffer
    print("Exercise 2b: With memory chatbot (buffer size: {0} turns)".format(memory_turns))
    print("Try: 'My name is Alice' then 'What is my name?' to see memory in action")
    print("Commands: 'history' (show memory), 'clear' (erase), 'exit' (quit)\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
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
                for msg in messages:
                    role = msg.get("role", "unknown").upper()
                    content = msg.get("content", "")
                    print("  {0}: {1}".format(role, content))
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
        print("Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
