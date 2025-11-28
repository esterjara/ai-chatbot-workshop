"""
Conversation memory management.
"""

from collections import deque
from typing import List, Tuple, Optional
from .model_loader import load_model
from .text_generator import generate_text
from .chat_utils import interactive_chat
from llama_cpp import Llama
import logging

_logger = logging.getLogger(__name__)


class RollingMemory:
    """A simple rolling memory that keeps the last N messages.

    Stores tuples of (role, text) where role is 'user' or 'assistant'.
    """

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._deque = deque(maxlen=capacity)

    def add(self, role: str, text: str) -> None:
        self._deque.append((role, text))

    def get(self) -> List[Tuple[str, str]]:
        return list(self._deque)

    def clear(self) -> None:
        self._deque.clear()


class MemoryChatbot:
    """
    A chatbot with conversation memory.
    Maintains a buffer of recent conversation turns for context.
    """
    
    def __init__(
        self,
        model_path: str,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        max_memory_turns: int = 5
    ):
        """
        Initialize the MemoryChatbot.
        
        Args:
            model_path: Path to GGUF model file
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens per response
            max_memory_turns: Max number of (user, assistant) turns to keep
        """
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.memory = RollingMemory(capacity=max_memory_turns * 2)
        self.model: Optional[Llama] = None
        
        try:
            self.model = load_model(model_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model from {model_path}: {e}\n"
                "Ensure the model file exists and llama-cpp-python is installed."
            )
    
    def get_history_string(self) -> str:
        """Format conversation history as a string."""
        if not self.memory.get():
            return "No previous messages."
        
        lines = []
        for role, text in self.memory.get():
            lines.append(f"{role.capitalize()}: {text}")
        
        return "\n".join(lines)
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response using conversation history.
        
        Args:
            user_input: The user's message
            
        Returns:
            The model's response
        """
        history = self.get_history_string()
        
        full_prompt = f"""{self.system_prompt}
        
        Conversation History:
        {history}

        User: {user_input}
        Assistant:"""
        
        try:
            response = generate_text(
                self.model,
                full_prompt,
                max_tokens=self.max_tokens
            )
            
            # Store in memory
            self.memory.add("user", user_input)
            self.memory.add("assistant", response)
            
            return response
        except Exception as e:
            _logger.error(f"Generation failed: {e}")
            raise