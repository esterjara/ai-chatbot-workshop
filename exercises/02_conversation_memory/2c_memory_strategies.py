"""
Exercise 2c: Explore Different Memory Strategies
Compare how different memory configurations affect conversations.
"""

import os 
from dotenv import load_dotenv
from chatbot import MemoryChatbot

load_dotenv()

def main():
    """
    Experiment with different memory buffer sizes.
    Change memory_turns to see how it affects context retention.
    """
    
    # Load model
    model_path = os.getenv("MODEL_PATH", "./models/tinyllama.gguf")
    max_tokens = os.getenv("MAX_TOKENS", 256)
    
    # TODO: Change this value to test different memory buffer sizes
    # Try: 1 (tiny), 3 (small), 5 (medium), 10 (large)
    memory_turns = 3
    
    # Create chatbot with the current memory configuration
    chatbot = MemoryChatbot(
        model_path=model_path,
        system_prompt="You are a helpful assistant with configurable memory.",
        max_tokens=max_tokens,
        max_memory_turns=memory_turns
    )
    
    print("Exercise 2c: Explore Different Memory Strategies")
    print("Current buffer: {0} turns".format(memory_turns))
    print("Commands: 'history', 'stats', 'exit'\n")
    
    
    # Chat loop
    message_count = 0
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "history":
            # Show stored messages in buffer
            messages = chatbot.memory.get()
            if not messages:
                print("Memory is empty.\n")
            else:
                print("Conversation history:")
                for role, content in messages:
                    print("  {0}: {1}".format(role.upper(), content))
                print()
            continue
        elif user_input.lower() == "stats":
            # TODO: EXERCISE - Show memory statistics
            # Hint: 
            # 1. Get history from chatbot.memory.get()
            # 2. Get capacity from chatbot.memory.capacity * 2
            # 3. Calculate usage percentage: 100 * len(history) // capacity
            # 4. Print: "Capacity: X, Used: Y/Z (P%)"
            
            pass
        
        if not user_input:
            continue
        
        message_count += 1
        response = chatbot.generate_response(user_input)
        print("Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
