"""
SOLUTION: Exercise 2c - Explore Different Memory Strategies

This demonstrates how to experiment with different memory buffer sizes
and understand the trade-offs between context retention and token usage.
"""

from src.chatbot.memory import MemoryChatbot
from src.chatbot.model_loader import load_model


def main():
    """
    Experiment with different memory buffer sizes.
    
    This demonstrates:
    - How memory_turns affects context retention
    - Trade-offs: context vs token usage
    - Finding the sweet spot for your use case
    """
    
    # Load model
    model = load_model("./models/tinyllama.gguf")
    
    # Change this value to test different memory buffer sizes
    # Try: 1 (tiny), 3 (small), 5 (medium), 10 (large)
    memory_turns = 3
    
    print("Exercise 2c: Explore Different Memory Strategies")
    print("Current memory_turns: {0}".format(memory_turns))
    print()
    print("To experiment with different buffer sizes:")
    print("1. Edit memory_turns variable above")
    print("2. Re-run this script")
    print("3. Observe how the chatbot behaves with different memory sizes")
    print()
    print("Try these values: 1, 3, 5, 10")
    print("Watch how context retention changes!\n")
    
    # Create chatbot with the current memory configuration
    chatbot = MemoryChatbot(
        model=model,
        system_prompt="You are a helpful assistant with configurable memory.",
        max_tokens=256,
        max_memory_turns=memory_turns
    )
    
    # Chat loop with analysis commands
    message_count = 0
    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break
        
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
            # Show memory statistics
            history = chatbot.memory.get()
            capacity = chatbot.memory.capacity * 2
            usage = 100 * len(history) // capacity if capacity > 0 else 0
            print("Capacity: {0}, Used: {1}/{2} ({3}%)".format(
                capacity, len(history), capacity, usage))
            print()
            continue
        
        if not user_input:
            continue
        
        message_count += 1
        response = chatbot.generate_response(user_input)
        print("Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
