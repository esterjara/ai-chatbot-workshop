"""
Exercise 4c: Multiple Tools with Tool Chaining (Optional Advanced)
Challenge: Create an agent with 3+ tools that work together.

This optional exercise is more complex:
- Multiple tools (calculator, weather, search)
- Tool chaining (using output from one tool as input to another)
- More realistic decision logic
- Error handling and validation
"""

from src.chatbot.agent import SimpleAgent, Tool
import re


def calculator(expression: str) -> str:
    """Simple calculator for basic math operations."""
    try:
        # Extract numbers and operator
        match = re.match(r'([\d.]+)\s*([+\-*/])\s*([\d.]+)', expression.strip())
        if not match:
            return "Invalid format. Use: 5 + 3"
        
        num1, op, num2 = float(match.group(1)), match.group(2), float(match.group(3))
        
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                return "Error: Division by zero"
            result = num1 / num2
        
        # Format result nicely
        if result == int(result):
            return f"{num1} {op} {num2} = {int(result)}"
        else:
            return f"{num1} {op} {num2} = {result:.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


def get_weather(location: str) -> str:
    """
    Get weather for a location with more realistic data.
    Includes temperature ranges for decision making.
    """
    weather_data = {
        "london": {"temp": 15, "condition": "Rainy", "emoji": "☔"},
        "paris": {"temp": 18, "condition": "Sunny", "emoji": "☀️"},
        "tokyo": {"temp": 22, "condition": "Cloudy", "emoji": "☁️"},
        "new york": {"temp": 12, "condition": "Snowing", "emoji": "❄️"},
        "sydney": {"temp": 25, "condition": "Clear", "emoji": "🌞"},
        "buenos aires": {"temp": 20, "condition": "Partly cloudy", "emoji": "🌤️"},
    }
    
    data = weather_data.get(location.lower())
    if data:
        return f"{data['temp']}°C, {data['condition']} {data['emoji']}"
    return "Location not found"


def search_knowledge(query: str) -> str:
    """
    Search for information in a knowledge base.
    Returns relevant information based on keywords.
    """
    knowledge_base = {
        "python": "Python is a versatile programming language known for readability and simplicity.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by computers.",
        "machine learning": "Machine Learning is a subset of AI where systems learn from data.",
        "chatbot": "A chatbot is a conversational AI that simulates human conversation.",
        "agent": "An agent is an autonomous system that can perceive, decide, and act.",
        "tool": "A tool is a function that extends what an agent can do.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"No information found about '{query}'. Try: python, ai, machine learning, chatbot, agent, tool"


def main():
    """
    OPTIONAL ADVANCED: Create an agent with multiple tools.
    
    Challenge tasks:
    1. Implement all 3 tools
    2. Make the agent understand which tool to use
    3. Try tool chaining: "What's 10 + 5, then search for that number"
    4. Add error handling
    """
    
    # Create agent
    agent = SimpleAgent()
    
    # Tool 1: Calculator
    calculator_tool = Tool(
        name="calculator",
        description="Performs basic math operations (+, -, *, /)",
        func=calculator,
        parameters={"expression": "Math expression like '5 + 3'"}
    )
    agent.register_tool(calculator_tool)
    
    # Tool 2: Weather
    weather_tool = Tool(
        name="weather",
        description="Gets weather information for a city",
        func=get_weather,
        parameters={"location": "City name"}
    )
    agent.register_tool(weather_tool)
    
    # Tool 3: Search
    search_tool = Tool(
        name="search",
        description="Search for information in knowledge base",
        func=search_knowledge,
        parameters={"query": "Search query about AI topics"}
    )
    agent.register_tool(search_tool)
    
    # Display available tools
    print("=" * 70)
    print("Exercise 4c: Multiple Tools with Tool Chaining (Optional Advanced)")
    print("=" * 70)
    print("\nAgent has 3 tools available:")
    print(agent.get_tools_description())
    print("\n" + "=" * 70)
    print("CHALLENGES:")
    print("  1. Basic: Use each tool individually")
    print("     - 'What is 25 * 4?'")
    print("     - 'What is the weather in Tokyo?'")
    print("     - 'Search for machine learning'")
    print()
    print("  2. Intermediate: Combine tools in one request")
    print("     - 'Calculate 10 + 5 and search for chatbot'")
    print("     - 'What is the weather and also calculate 50 / 2'")
    print()
    print("  3. Complex: Use tool results to understand requests")
    print("     - 'Is it cold in London? (< 15°C)'")
    print("     - 'Calculate 100 - 50 and tell me about that topic'")
    print()
    print("=" * 70)
    print("Type 'exit' to quit\n")
    
    # Main interaction loop
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
