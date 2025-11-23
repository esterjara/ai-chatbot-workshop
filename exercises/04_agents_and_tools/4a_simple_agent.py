"""
Exercise 4a: Simple Agent with One Tool
Learn the basics: how agents use tools.

This is the SIMPLEST possible agent:
- 1 predefined tool (calculator)
- Show how tools work
"""

from src.chatbot.agent import SimpleAgent, Tool


def calculator(expression: str) -> str:
    """Simple calculator for basic math operations."""
    try:
        # Handle basic operations
        if "+" in expression:
            parts = expression.split("+")
            result = float(parts[0].strip()) + float(parts[1].strip())
            return f"{parts[0].strip()} + {parts[1].strip()} = {result}"
        elif "-" in expression:
            parts = expression.split("-")
            result = float(parts[0].strip()) - float(parts[1].strip())
            return f"{parts[0].strip()} - {parts[1].strip()} = {result}"
        elif "*" in expression:
            parts = expression.split("*")
            result = float(parts[0].strip()) * float(parts[1].strip())
            return f"{parts[0].strip()} * {parts[1].strip()} = {result}"
        elif "/" in expression:
            parts = expression.split("/")
            result = float(parts[0].strip()) / float(parts[1].strip())
            return f"{parts[0].strip()} / {parts[1].strip()} = {result}"
        return "Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """
    Create and run a simple agent with ONE tool.
    
    This demonstrates the core concept:
    - Tool = function + metadata (name, description, parameters)
    - Agent = system that can decide to use tools
    - Loop = execute, get result, respond
    """
    
    # Step 1: Create the agent
    agent = SimpleAgent()
    
    # Step 2: Create a tool
    calculator_tool = Tool(
        name="calculator",
        description="Performs basic math (+, -, *, /)",
        func=calculator,
        parameters={"expression": "Math expression like '5 + 3'"}
    )
    
    # Step 3: Register the tool
    agent.register_tool(calculator_tool)
    
    # Show what we have
    print("=" * 60)
    print("Exercise 4a: Simple Agent (Calculator Tool)")
    print("=" * 60)
    print("\nAgent has 1 tool:")
    print(agent.get_tools_description())
    print("=" * 60 + "\n")
    
    # Main loop
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Agent processes request
        response = agent.execute(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
