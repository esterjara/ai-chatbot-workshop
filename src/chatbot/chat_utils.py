"""
Chat Utilities Module

Provides shared chat interface functions
"""

from typing import Callable, Optional, Dict, Any
import logging

_logger = logging.getLogger(__name__)


def interactive_chat(
    generate_response_fn: Callable[[str], str],
    chatbot_name: str = "Chatbot",
    system_info: Optional[str] = None,
    special_commands: Optional[Dict[str, Callable]] = None,
    exit_commands: list = None
):
    """
    Start an interactive chat loop with consistent interface across all chatbots.
    
    This shared function ensures all chatbots (BasicChatbot, MemoryChatbot, etc.)
    have the same user experience and command handling.
    
    Args:
        generate_response_fn: Function that takes user input and returns a response
        chatbot_name: Name of the chatbot for display purposes
        system_info: Optional system information to display at startup
        special_commands: Dict of command -> handler function (e.g., {"clear": clear_fn})
        exit_commands: List of commands to exit chat (default: ["exit", "quit"])
        
    Example:
        >>> def my_response_fn(user_input: str) -> str:
        ...     return f"You said: {user_input}"
        >>> interactive_chat(my_response_fn, "EchoBot")
    """
    if exit_commands is None:
        exit_commands = ["exit", "quit"]
    
    # Display startup info
    print(f"{chatbot_name} initialized")
    
    # Display available commands
    commands = exit_commands.copy()
    if special_commands:
        commands.extend(special_commands.keys())
    print(f"Commands: {', '.join(commands)}\n")
    
    # Main chat loop
    while True:
        try:
            user_input = input("👤 User: ").strip()
            
            # Check for exit commands
            if user_input.lower() in exit_commands:
                print("Goodbye!")
                break
            
            # Check for special commands
            if special_commands and user_input.lower() in special_commands:
                special_commands[user_input.lower()]()
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Generate and display response
            try:
                response = generate_response_fn(user_input)
                print(f"🤖 Assistant: {response}\n")
            except Exception as e:
                _logger.error(f"Response generation failed: {e}")
                print(f"Error: {e}\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            _logger.error(f"Unexpected error in chat loop: {e}")
            print(f"\nUnexpected error: {e}")
            print("Type 'exit' to quit.\n")
