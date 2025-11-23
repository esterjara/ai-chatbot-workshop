"""
Exercise 2b: Add Memory - The Solution
This chatbot HAS memory. It remembers the conversation.
Compare with Exercise 2a to see the difference!
"""

from src.chatbot.memory import MemoryChatbot
from src.chatbot.model_loader import load_model


def main():
    """
    Create and run a chatbot WITH conversation memory.
    The chatbot remembers previous messages in a buffer.
    """
    
    # Load model
    model = load_model("./models/tinyllama.gguf")
    
    memory_turns = 3
    
    chatbot = MemoryChatbot(
        model=model,
        system_prompt="You are a helpful assistant with memory. Remember the conversation context.",
        max_tokens=256,
        max_memory_turns=memory_turns
    )
    
    print("Exercise 2b: With memory chatbot (buffer: {0} turns)".format(memory_turns))
    print("Try: 'My name is Alice' then 'What is my name?'")
    print("Commands: 'history', 'clear', 'exit'\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break
        
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "history":
            # TODO: EXERCISE - Show conversation history
            # Hint: Get messages from chatbot.memory.get()
            # Loop through and print each message
            # Format: "  ROLE: message_text"
            
            pass
        elif user_input.lower() == "clear":
            # TODO: EXERCISE - Clear the memory buffer
            # Hint: Use chatbot.memory.clear()
            # Then print a message confirming it was cleared
            
            pass
        
        if not user_input:
            continue
        
        response = chatbot.generate_response(user_input)
        print("Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
