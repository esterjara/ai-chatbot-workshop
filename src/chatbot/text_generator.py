"""
Text Generation Module

This module provides text generation functions for LLM responses
"""

from typing import Any
import logging

_logger = logging.getLogger(__name__)


def generate_text(
    model: Any,
    prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.0,
    response_format: dict = None,
    **kwargs
) -> str:
    """Generate text from a prompt using the loaded model.
    
    Args:
        model: The loaded Llama model
        prompt: The input prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = more random)
        response_format: Optional response format specification
        **kwargs: Additional generation parameters
        
    Returns:
        Generated text as a string
    """
    try:
        # Build generation parameters
        gen_params = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": ["User:", "\n\n"],
            "echo": False,
            **kwargs
        }
        
        output = model(prompt, **gen_params)
        
        # Extract text from the response
        if isinstance(output, dict) and "choices" in output:
            return output["choices"][0]["text"].strip()
        return str(output).strip()
        
    except Exception as e:
        _logger.error(f"Text generation failed: {e}")
        raise


def generate_response(
    model: Any,
    user_input: str,
    system_prompt: str = "You are a helpful assistant.",
    conversation_history: str = "",
    max_tokens: int = 256,
    temperature: float = 0.0
) -> str:
    """
    Shared response generation function used across all exercises.
    
    This provides a consistent way to generate responses whether you're using:
    - Exercise 1: BasicChatbot (no history)
    - Exercise 2: MemoryChatbot (with conversation history)
    - Exercise 3: Agents (with tools and intent classification)
    
    Args:
        model: The loaded Llama model
        user_input: The user's current message
        system_prompt: Instructions for the LLM
        conversation_history: Previous conversation (formatted)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        
    Returns:
        The model's response
    """
    # Build the full prompt
    if conversation_history:
        full_prompt = f"{system_prompt}\n\n{conversation_history}User: {user_input}\nAssistant:"
    else:
        full_prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    
    # Generate response
    response = generate_text(
        model,
        full_prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    return response
