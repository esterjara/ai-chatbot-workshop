"""
Agent and tool definitions for agentic chatbots.
"""

from typing import Callable, Dict, Any, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

_logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions an agent can take."""
    USE_TOOL = "use_tool"
    RESPOND = "respond"


@dataclass
class Tool:
    """Represents a tool that an agent can use."""
    name: str
    description: str
    func: Callable
    parameters: Dict[str, str]  # parameter_name -> description
    
    def call(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        try:
            result = self.func(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"


class SimpleAgent:
    """
    A simple agent that can reason and use tools.
    Decides whether to use a tool or respond directly.
    """
    
    def __init__(self):
        """Initialize the agent."""
        self.tools: Dict[str, Tool] = {}
        self.action_history: List[Dict[str, Any]] = []
    
    def register_tool(self, tool: Tool):
        """Register a tool that the agent can use."""
        self.tools[tool.name] = tool
        _logger.info(f"Registered tool: {tool.name}")
    
    def get_tools_description(self) -> str:
        """Format available tools for display."""
        if not self.tools:
            return "No tools available."
        
        descriptions = []
        for tool in self.tools.values():
            params = ", ".join(f"{k}: {v}" for k, v in tool.parameters.items())
            descriptions.append(f"- {tool.name}({params}): {tool.description}")
        
        return "\n".join(descriptions)
    
    def decide_action(self, user_request: str) -> Tuple[ActionType, Any]:
        """
        Decide what action to take (simplified heuristic-based).
        
        In production, this would use an LLM to reason about the request.
        
        Args:
            user_request: The user's request
            
        Returns:
            Tuple of (action_type, data)
        """
        request_lower = user_request.lower()
        
        # Simple keyword matching (could be LLM-based)
        if any(word in request_lower for word in ["search", "find", "look"]):
            return ActionType.USE_TOOL, {"tool_name": "search", "topic": request_lower}
        
        if any(word in request_lower for word in ["calculate", "math", "compute", "+", "-", "*"]):
            return ActionType.USE_TOOL, {"tool_name": "calculator", "expression": request_lower}
        
        if any(word in request_lower for word in ["weather", "temperature"]):
            return ActionType.USE_TOOL, {"tool_name": "weather", "city": "default"}
        
        if any(word in request_lower for word in ["time", "date", "now"]):
            return ActionType.USE_TOOL, {"tool_name": "time", "query": "current"}
        
        # Default: respond
        return ActionType.RESPOND, {"message": f"Responding to: {user_request}"}
    
    def execute(self, user_request: str) -> str:
        """
        Execute the agent's decision loop.
        
        Args:
            user_request: The user's request
            
        Returns:
            Response or tool result
        """
        action_type, action_data = self.decide_action(user_request)
        
        if action_type == ActionType.USE_TOOL:
            tool_name = action_data.get("tool_name")
            
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                # Extract parameters based on tool requirements
                params = {k: v for k, v in action_data.items() if k in tool.parameters}
                result = tool.call(**params)
                response = f"Tool result: {result}"
            else:
                response = f"Tool not found: {tool_name}"
        
        else:  # RESPOND
            response = action_data["message"]
        
        # Record in history
        self.action_history.append({
            "request": user_request,
            "action_type": action_type.value,
            "response": response
        })
        
        return response


# Legacy Agent class for backwards compatibility
class Agent:
    """Legacy agent class for backwards compatibility."""

    def __init__(self, tools: dict | None = None):
        self.tools = tools or {}

    def decide_action(self, message: str) -> dict:
        """Return an action dict with type and payload."""
        text = message.strip().lower()
        if text.startswith("search:") and "search" in self.tools:
            query = message.split(":", 1)[1].strip()
            return {"type": "tool", "tool": "search", "input": query}
        return {"type": "reply", "input": message}

    def act(self, action: dict) -> str:
        if action["type"] == "tool":
            tool_name = action["tool"]
            tool = self.tools.get(tool_name)
            if tool:
                return tool(action.get("input"))
            return f"Tool '{tool_name}' not available."
        return f"Agent decided to reply: {action.get('input')}"
