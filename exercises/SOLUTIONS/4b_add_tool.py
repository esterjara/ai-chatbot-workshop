"""
Exercise 4b: Add a New Tool (SOLUTION)

This is the reference implementation showing:
- How to implement a new tool function
- How to create a Tool object
- How to register it with the agent
- How to extend agents with new capabilities
"""

from src.chatbot.agent import SimpleAgent, Tool


def calculator(expression: str) -> str:
    """Simple calculator for basic math operations."""
    try:
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


# SOLUTION: Implement weather tool with mock data
def get_weather(location: str) -> str:
    """
    Get weather for a location.
    
    SOLUTION: Here's the completed implementation with weather data
    for multiple cities.
    
    Args:
        location: City name
        
    Returns:
        Weather description
    """
    # SOLUTION: Weather data for multiple cities
    weather_data = {
        "london": "15°C, Rainy ☔",
        "paris": "18°C, Sunny ☀️",
        "tokyo": "22°C, Cloudy ☁️",
        "new york": "12°C, Snowing ❄️",
        "sydney": "25°C, Clear 🌞",
        "buenos aires": "20°C, Partly cloudy 🌤️"
    }
    
    result = weather_data.get(location.lower(), "Location not found")
    return result


def main():
    """
    SOLUTION: Create an agent and register multiple tools.
    
    Learning:
    - Tool creation and registration
    - How agents make decisions
    - Extensibility: add new tools anytime
    """
    
    # Create agent
    agent = SimpleAgent()
    
    # SOLUTION: Register calculator tool
    calculator_tool = Tool(
        name="calculator",
        description="Performs basic math (+, -, *, /)",
        func=calculator,
        parameters={"expression": "Math expression"}
    )
    agent.register_tool(calculator_tool)
    
    # SOLUTION: Create and register weather tool
    # This is what participants need to implement in the exercise
    weather_tool = Tool(
        name="weather",
        description="Gets weather for a location",
        func=get_weather,
        parameters={"location": "City name"}
    )
    agent.register_tool(weather_tool)
    
    # Display available tools
    print("=" * 60)
    print("Exercise 4b: Add a Tool (SOLUTION)")
    print("=" * 60)
    print("\nAgent now has 2 tools:")
    print(agent.get_tools_description())
    print("\n" + "=" * 60)
    print("\nTry:")
    print("  - What is 5 + 3?")
    print("  - Calculate 100 / 4")
    print("  - What is the weather in London?")
    print("  - Tell me about Paris weather")
    print("  - Type 'exit' to quit")
    print("=" * 60 + "\n")
    
    # Main interaction loop
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # SOLUTION: Agent processes with multiple tools
        response = agent.execute(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
