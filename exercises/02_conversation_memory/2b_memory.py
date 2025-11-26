"""
Exercise 2b: Add Memory - The Solution
This chatbot HAS memory. It remembers the conversation.
Compare with Exercise 2a to see the difference!
"""
import os 
from dotenv import load_dotenv
from chatbot import MemoryChatbot

load_dotenv()

def main():
    """
    Create and run a chatbot WITH conversation memory.
    The chatbot remembers previous messages in a buffer.
    """
    
    # Load model
    model_path = os.getenv("MODEL_PATH", "./models/tinyllama.gguf")
    max_tokens = os.getenv("MAX_TOKENS", 256)
    memory_turns = 3
    
    chatbot = MemoryChatbot(
        model_path=model_path,
        system_prompt="You are a helpful assistant with memory. Remember the conversation context.",
        max_tokens=max_tokens,
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
            # The memory returns a list of tuples: (role, content)
            # Loop through and unpack each tuple: for role, content in messages:
            # Print each message in format: "  ROLE: content"
            # Don't forget to print a newline at the end
            
            pass
        elif user_input.lower() == "clear":
            # TODO: EXERCISE - Clear the memory buffer
            # Hint: Call chatbot.memory.clear()
            # Then print "Memory cleared.\n" to confirm
            
            pass
        
        if not user_input:
            continue
        
        response = chatbot.generate_response(user_input)
        print("Assistant: {0}\n".format(response))


if __name__ == "__main__":
    main()
