"""
Tools Module

This module provides the core Tool class structure for agent capabilities.

The Tool class is a dataclass that wraps a function with metadata:
- name: Unique identifier
- description: What the tool does (helps LLM select it)
- function: The actual callable to execute
- parameters: Dict of parameter names -> descriptions
"""

from typing import Dict, Callable, Optional
from dataclasses import dataclass
import logging

_logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """
    Represents a tool that an agent can use.
    
    A tool is a function with metadata that helps agents:
    - Discover what the tool does (description)
    - Know what parameters to pass (entities dict)
    - Execute the tool safely (call method)
    
    Attributes:
        name: Unique identifier for the tool
        description: What the tool does (used by LLM for tool selection)
        function: The actual Python function to execute
        entities: Dict mapping parameter names to descriptions
        
    Example:
        time_tool = Tool(
            name="get_time",
            description="Returns current time",
            function=datetime.now,
            entities={}
        )
    """
    name: str
    description: str
    function: Callable
    entities: Dict[str, str] = None  # parameter_name -> description
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = {}
    
    def call(self, **kwargs) -> str:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Parameters to pass to the tool function
            
        Returns:
            Tool result as string
            
        Raises:
            Returns error message string if execution fails
        """
        try:
            result = self.function(**kwargs)
            return str(result)
        except Exception as e:
            _logger.error(f"Tool '{self.name}' execution failed: {e}")
            return f"Error: {str(e)}"
