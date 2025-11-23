"""
Exercise 2c: Explore Different Memory Strategies
Compare how different memory configurations affect conversations.
"""

from src.chatbot.memory import MemoryChatbot
from src.chatbot.model_loader import load_model


def main():
    """
    Experiment with different memory buffer sizes.
    Change memory_turns to see how it affects context retention.
    """
    
    # Load model
    model = load_model("./models/tinyllama.gguf")
    
    # TODO: Change this value to test different memory buffer sizes
    # Try: 1 (tiny), 3 (small), 5 (medium), 10 (large)
    memory_turns = 3
    
    # Create chatbot with the current memory configuration
    chatbot = MemoryChatbot(
        model=model,
        system_prompt="You are a helpful assistant with configurable memory.",
        max_tokens=256,
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
            history = chatbot.memory.get()
            print("\n[Buffer: {0} messages]".format(len(history)))
            
            for role, text in history:
                preview = (text[:50] + "...") if len(text) > 50 else text
                print("  {0}: {1}".format(role.upper(), preview))
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
