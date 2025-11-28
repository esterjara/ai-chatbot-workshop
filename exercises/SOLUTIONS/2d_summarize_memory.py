"""
SOLUTION: Exercise 2d - Summarize Memory Implementation

This is a reference implementation of summarize_memory().
This shows one way to solve the challenge.

Key ideas:
1. Extract old messages when buffer gets full
2. Create a summary prompt
3. Generate summary with the model
4. Store summary for long-term memory
"""

import os
from llama_cpp import Llama
from typing import Optional
from dotenv import load_dotenv
from chatbot import MemoryChatbot, RollingMemory
from chatbot import load_model, generate_text

load_dotenv()


class HybridMemoryChatbot(MemoryChatbot):
    """
    Chatbot with hybrid memory: buffer + summaries.
    
    When memory buffer is full, old messages are summarized instead of discarded.
    This maintains long-term context while keeping token usage reasonable.
    """
    
    def __init__(
        self,
        model_path: str,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 256,
        max_memory_turns: int = 5,
        summary_trigger: int = 10
    ):
        """
        Initialize hybrid memory chatbot.
        
        Args:
            model_path: Path to the model file
            system_prompt: System prompt for the model
            max_tokens: Max tokens per response
            max_memory_turns: Number of turns before triggering summary
            summary_trigger: Message count that triggers summarization
        """
        super().__init__(
            model_path=model_path,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            max_memory_turns=max_memory_turns
        )
        self.summary_trigger = summary_trigger
        self.message_count = 0
        self.summaries: list = []  # Store summaries
        self.model: Optional[Llama] = None
        
        try:
            self.model = load_model(model_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model from {model_path}: {e}\n"
                "Ensure the model file exists and llama-cpp-python is installed."
            )
    
    def summarize_memory(self) -> Optional[str]:
        """
        SOLUTION: Generate a summary of old messages.
        
        This method:
        1. Gets the oldest messages from the buffer
        2. Creates a prompt asking the model to summarize
        3. Generates a concise summary
        4. Returns it for storage
        """
        
        # Get current memory buffer
        history = self.memory.get()
        
        # Need at least 4 messages to summarize
        if len(history) < 4:
            return None
        
        # STEP 1: Extract old messages (first half of buffer)
        # These are the ones that would be lost soon
        split_point = len(history) // 2
        old_messages = history[:split_point]
        
        # STEP 2: Build conversation text
        conversation_text = ""
        for role, text in old_messages:
            conversation_text += "{0}: {1}\n".format(role.upper(), text)
        
        # STEP 3: Create summary prompt
        # The prompt is key! Better prompt = better summary
        summary_prompt = """Please summarize this conversation briefly in 2-3 sentences. 
Focus on the key topics discussed and any important information about the user.

Conversation:
{0}

Summary:""".format(conversation_text)
        
        # STEP 4: Generate summary using the model
        try:
            summary_text = generate_text(
                self.model,
                summary_prompt,
                max_tokens=100,
                temperature=0.5,  # Lower temp = more focused summaries
                top_p=0.9
            )
        except Exception as e:
            print("[Error generating summary: {0}]".format(e))
            return None
        
        # STEP 5: Extract and clean summary
        # Take first few lines (summaries should be concise)
        summary_lines = summary_text.strip().split('\n')
        summary = '\n'.join(summary_lines[:3])  # First 3 lines max
        
        return summary
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate response with periodic summarization.
        """
        self.message_count += 1
        
        # SOLUTION: Check if it's time to summarize
        if self.message_count % self.summary_trigger == 0:
            print("[Summarizing memory at message {0}...]".format(self.message_count))
            summary = self.summarize_memory()
            if summary:
                self.summaries.append(summary)
                print("[Summary stored]\n")
        
        # Call parent implementation
        return super().generate_response(user_input)
    
    def get_context_with_summaries(self) -> str:
        """
        Build full context including summaries + recent messages.
        """
        context = ""
        
        # Include all stored summaries
        if self.summaries:
            context += "=== PREVIOUS CONVERSATION SUMMARIES ===\n"
            for i, summary in enumerate(self.summaries, 1):
                context += "Session {0}: {1}\n".format(i, summary)
            context += "\n"
        
        # Include recent messages
        context += "=== RECENT CONVERSATION ===\n"
        for role, text in self.memory.get():
            context += "{0}: {1}\n".format(role.upper(), text)
        
        return context
    
    def chat(self):
        """
        Interactive chat with summary functionality.
        """
        print("\nHybrid Memory Chat (with Summaries)")
        print("Commands: 'history', 'summary', 'context', 'stats', 'exit'\n")
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
            except EOFError:
                break
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "history":
                print("\n[Current Buffer]")
                for role, text in self.memory.get():
                    text_preview = text[:70] + "..." if len(text) > 70 else text
                    print("  {0}: {1}".format(role.upper(), text_preview))
                print()
                continue
            elif user_input.lower() == "summary":
                if self.summaries:
                    print("\n[Stored Summaries]")
                    for i, summary in enumerate(self.summaries, 1):
                        print("  Summary {0}:".format(i))
                        for line in summary.split('\n'):
                            print("    {0}".format(line))
                else:
                    print("[No summaries yet - continue chatting!]\n")
                continue
            elif user_input.lower() == "context":
                print("\n[Full Context]")
                print(self.get_context_with_summaries())
                continue
            elif user_input.lower() == "stats":
                print("[Memory Statistics]")
                print("  Total messages sent: {0}".format(self.message_count))
                print("  Current buffer: {0} messages".format(len(self.memory.get())))
                print("  Stored summaries: {0}".format(len(self.summaries)))
                if self.summaries:
                    total_summary_chars = sum(len(s) for s in self.summaries)
                    print("  Total summary chars: {0}".format(total_summary_chars))
                print()
                continue
            
            if not user_input:
                continue
            
            # Generate response
            response = self.generate_response(user_input)
            print("🤖 Assistant: {0}\n".format(response))


def main():
    """
    Demonstrate hybrid memory with summaries.
    """
    
    print("=" * 60)
    print("SOLUTION: Hybrid Memory with Summaries")
    print("=" * 60)
    print()
    print("How it works:")
    print("1. Chat normally - messages go into buffer")
    print("2. Every N messages, old messages are summarized")
    print("3. Summaries stored separately (long-term memory)")
    print("4. New space freed up in buffer")
    print("5. You can reference old messages via summaries!")
    print()
    print("Try this:")
    print("- Have a 20+ message conversation")
    print("- Type 'stats' to see summaries created")
    print("- Type 'summary' to read the summaries")
    print("- Ask: 'What did we discuss at the beginning?'")
    print()
    print("=" * 60 + "\n")
    
    # Load model
    model_path = os.getenv("MODEL_PATH", "./models/tinyllama.gguf")
    max_tokens = int(os.getenv("MAX_TOKENS", 256))
    
    # Create hybrid chatbot
    chatbot = HybridMemoryChatbot(
        model_path=model_path,
        system_prompt="You are a thoughtful assistant. Use context from previous parts of the conversation.",
        max_tokens=max_tokens,
        max_memory_turns=3,      # Keep last 6 messages
        summary_trigger=6         # Summarize every 6 messages
    )
    
    # Start chat
    chatbot.chat()


if __name__ == "__main__":
    main()

