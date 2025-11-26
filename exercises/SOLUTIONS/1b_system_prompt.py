"""
Exercise 1b: Modify the System Prompt
Learn how system prompts control chatbot behavior and personality.
"""
import os 
from dotenv import load_dotenv
from chatbot import BasicChatbot

load_dotenv()


def main():
    """
    Create and run chatbots with DIFFERENT system prompts.
    
    This demonstrates:
    - How system prompts control chatbot personality
    - How prompts affect response quality
    - Prompt engineering basics
    """
    
    model_path = os.getenv("MODEL_PATH", "./models/tinyllama.gguf")
    max_tokens = os.getenv("MAX_TOKENS", 256)
    
    # TODO: Try each of these system prompts
    # Uncomment one and run to see the difference
    
    # Option 1: Default helpful assistant
    system_prompt = "You are a helpful assistant. Answer concisely."
    
    # Option 2: Python expert
    # system_prompt = "You are a Python expert. Provide code examples and explain thoroughly."
    
    # Option 3: Creative storyteller
    # system_prompt = "You are a creative storyteller. Make responses entertaining and engaging."
    
    # Option 4: Patient teacher
    # system_prompt = "You are a patient teacher. Explain concepts clearly, step-by-step, starting with basics."
    
    # Option 5: Your custom prompt (modify this!)
    # system_prompt = "You are..."
    
    # Create chatbot with your chosen prompt
    chatbot = BasicChatbot(
        model_path=model_path,
        system_prompt=system_prompt,
        max_tokens=max_tokens
    )
    
    # Display configuration
    print("=" * 60)
    print("EXERCISE 1b: Modify the System Prompt")
    print("=" * 60)
    print(f"\nSystem Prompt:\n{system_prompt}\n")
    print("\nChat started. Type 'exit' to quit.\n")
    
    # Start interactive chat
    chatbot.chat()


if __name__ == "__main__":
    main()
