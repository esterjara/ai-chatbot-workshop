"""
Basic Chatbot using llama-cpp-python.
"""

from typing import Optional
from .model_loader import load_model
from .text_generator import generate_response
from .chat_utils import interactive_chat
from llama_cpp import Llama
import logging

_logger = logging.getLogger(__name__)


class BasicChatbot:
    """
    A simple chatbot that responds to user queries using a local LLM.
    
    This is the foundation for all other chatbot types.
    Uses the shared generate_response() function for consistency across exercises.
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
        
        Uses the shared generate_response() function for consistency.
        
        Args:
            user_input: The user's message
            
        Returns:
            The model's response
        """
        try:
            response = generate_response(
                model=self.model,
                user_input=user_input,
                system_prompt=self.system_prompt,
                conversation_history="",  # No history in BasicChatbot
                max_tokens=self.max_tokens
            )
            return response
        except Exception as e:
            _logger.error(f"Generation failed: {e}")
            raise
    
    def chat(self):
        """Start an interactive chat loop using shared chat utility."""
        system_info = f"System prompt: {self.system_prompt}"
        interactive_chat(
            generate_response_fn=self.generate_response,
            chatbot_name="Basic Chatbot",
            system_info=system_info
        )
