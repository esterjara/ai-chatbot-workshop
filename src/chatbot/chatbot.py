"""
Basic Chatbot using llama-cpp-python.
"""

from typing import Optional
from .model_loader import load_model, generate_text
from llama_cpp import Llama
import logging

_logger = logging.getLogger(__name__)


class BasicChatbot:
    """
    A simple chatbot that responds to user queries using a local LLM.
    
    This is the foundation for all other chatbot types.
    """
    
    def __init__(
        self,
        model_path: str = "./models/tinyllama.gguf",
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256
    ):
        """
        Initialize the BasicChatbot.
        
        Args:
            model_path: Path to GGUF model file
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens per response
        """
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.model: Optional[Llama] = None
        
        try:
            self.model = load_model(model_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model from {model_path}: {e}\n"
                "Ensure the model file exists and llama-cpp-python is installed."
            )
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input.
        
        Args:
            user_input: The user's message
            
        Returns:
            The model's response
        """
        full_prompt = f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:"
        
        try:
            response = generate_text(
                self.model,
                full_prompt,
                max_tokens=self.max_tokens
            )
            return response
        except Exception as e:
            _logger.error(f"Generation failed: {e}")
            raise
    
    def chat(self):
        """Start an interactive chat loop."""
        
        while True:
            user_input = input("👤 User: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = self.generate_response(user_input)
                print(f"🤖 Assistant: {response}\n")
            except Exception as e:
                print(f"Error: {e}\n")
