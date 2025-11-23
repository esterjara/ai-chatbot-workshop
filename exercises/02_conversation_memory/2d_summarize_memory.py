"""
Exercise 2d: Advanced Memory - Summarization
Learn about hybrid memory strategies that combine buffer + summaries.

This is an OPTIONAL CHALLENGE to extend memory capacity intelligently.
"""

from src.chatbot.memory import MemoryChatbot, RollingMemory
from src.chatbot.model_loader import load_model, generate_text
from llama_cpp import Llama
from typing import Optional


class HybridMemoryChatbot(MemoryChatbot):
    """
    Chatbot with hybrid memory: buffer + summaries.
    
    When memory buffer is full, old messages are summarized instead of discarded.
    This maintains long-term context while keeping token usage reasonable.
    """
    
    def __init__(
        self,
        model: Llama,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        max_memory_turns: int = 5,
        summary_trigger: int = 10
    ):
        """
        Initialize hybrid memory chatbot.
        
        Args:
            model: Llama model instance
            system_prompt: System prompt for the model
            max_tokens: Max tokens per response
            max_memory_turns: Number of turns before triggering summary
            summary_trigger: Message count that triggers summarization
        """
        super().__init__(
            model=model,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            max_memory_turns=max_memory_turns
        )
        self.summary_trigger = summary_trigger
        self.message_count = 0
        self.summaries: list = []  # Store summaries
    
    def summarize_memory(self) -> Optional[str]:
        """
        TODO: IMPLEMENT THIS METHOD
        
        This method should:
        1. Take the first N messages from memory
        2. Create a summary prompt like:
           "Summarize this conversation in 2-3 lines:
            User: ...
            Assistant: ...
            User: ...
            Assistant: ..."
        3. Call generate_text() with the model
        4. Extract first 3-4 lines of response
        5. Return the summary
        
        Hint: Use generate_text(self.model, prompt, max_tokens=100, ...)
        
        Example return: "Summary: The user is learning Python. They asked about loops and functions."
        """
        # TODO: Implement summary generation
        # This is a challenging exercise - think about:
        # - What makes a good summary?
        # - How many old messages should we summarize?
        # - How to format the summary for future context?
        
        # Pseudocode:
        # if len(memory) >= self.summary_trigger:
        #     old_messages = get first N messages
        #     prompt = "Resume brevemente..."
        #     summary = call model
        #     return summary
        # return None
        
        pass
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate response with automatic summarization.
        
        When buffer gets full, summarizes old messages.
        """
        self.message_count += 1
        
        # TODO: Add logic to call summarize_memory() periodically
        # Example:
        # if self.message_count % self.summary_trigger == 0:
        #     summary = self.summarize_memory()
        #     if summary:
        #         self.summaries.append(summary)
        #         # Clear old messages to make room
        #         # But keep the summary!
        
        # For now, use parent implementation
        return super().generate_response(user_input)
    
    def get_context_string(self) -> str:
        """
        Get full context including summaries + recent messages.
        """
        context = ""
        
        # Include summaries from long-term memory
        if self.summaries:
            context += "=== CONVERSATION SUMMARY ===\n"
            for i, summary in enumerate(self.summaries, 1):
                context += f"{i}. {summary}\n"
            context += "\n"
        
        # Include recent messages from buffer
        context += "=== RECENT MESSAGES ===\n"
        for role, text in self.memory.get():
            context += f"{role.upper()}: {text}\n"
        
        return context
    
    def chat(self):
        """
        Interactive chat loop with summaries.
        Commands: 'history', 'summary', 'stats', 'exit'
        """
        
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                break
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "history":
                print("\n[Recent Messages]")
                for role, text in self.memory.get():
                    print(f"  {role.upper()}: {text[:70]}..." if len(text) > 70 else f"  {role.upper()}: {text}")
                print()
                continue
            elif user_input.lower() == "summary":
                # Show long-term summaries
                if self.summaries:
                    print("\n[Long-term Memory Summaries]")
                    for i, summary in enumerate(self.summaries, 1):
                        print(f"  {i}. {summary}")
                else:
                    print("\n[No summaries yet - keep chatting!]")
                print()
                continue
            elif user_input.lower() == "stats":
                # Show memory statistics
                print("Messages: {0}, Buffer: {1}, Summaries: {2}".format(
                    self.message_count, len(self.memory.get()), len(self.summaries)))
                continue
            
            if not user_input:
                continue
            
            response = self.generate_response(user_input)
            print("Assistant: {0}\n".format(response))


def main():
    """
    Challenge: Implement hybrid memory with summaries.
    TODO in summarize_memory() - see class definition above.
    """
    
    # Load model
    model = load_model("./models/tinyllama.gguf")
    
    # Create hybrid memory chatbot
    # Keeps recent messages + summaries of old ones
    chatbot = HybridMemoryChatbot(
        model=model,
        system_prompt="You are a thoughtful assistant. Remember previous topics.",
        max_tokens=256,
        max_memory_turns=3,      # Keep last 3 turns in buffer
        summary_trigger=6         # Summarize after 6 messages
    )
    
    print("Exercise 2d: Hybrid memory with summaries")
    print("TODO: Implement summarize_memory() method")
    print("Commands: 'history', 'summary', 'stats', 'exit'\n")
    
    # Start chat
    chatbot.chat()


if __name__ == "__main__":
    main()
