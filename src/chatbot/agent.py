from typing import Any


class Agent:
    """A tiny agent that decides whether to call a tool or respond directly.

    This is intentionally minimal for workshop clarity.
    """

    def __init__(self, tools: dict | None = None):
        self.tools = tools or {}

    def decide_action(self, message: str) -> dict:
        """Return an action dict with type and payload.

        Simple heuristic: if message starts with 'search:' call a 'search' tool.
        """
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
