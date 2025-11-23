"""
Conversation memory management.
"""

from collections import deque
from typing import List, Tuple
from .model_loader import generate_text
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
        model: Llama,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        max_memory_turns: int = 5
    ):
        """
        Initialize the MemoryChatbot.
        
        Args:
            model: Llama model instance
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens per response
            max_memory_turns: Max number of (user, assistant) turns to keep
        """
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.memory = RollingMemory(capacity=max_memory_turns * 2)
    
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
    
    def chat(self):
        """Start an interactive chat loop with memory."""
        print(f"Memory Chatbot initialized")
        print(f"System prompt: {self.system_prompt}")
        print(f"Memory buffer: {self.memory.capacity} turns")
        print("Commands: 'exit', 'clear', 'history'\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "clear":
                self.memory.clear()
                print("Memory cleared.\n")
                continue
            
            if user_input.lower() == "history":
                print("\nConversation History:")
                print(self.get_history_string())
                print()
                continue
            
            if not user_input:
                continue
            
            try:
                response = self.generate_response(user_input)
                print(f"Assistant: {response}\n")
            except Exception as e:
                print(f"Error: {e}\n")
