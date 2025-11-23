"""
Exercise 4b: Add a New Tool
Learn to create and register tools.

Starting point: 1 tool (calculator) is already working
Exercise: Add a second tool (weather)
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


# TODO: Implement the weather tool
# Complete this function with mock weather data for at least 3 cities
def get_weather(location: str) -> str:
    """
    Get weather for a location.
    
    TODO: Add weather data for cities.
    Example:
        weather_data = {
            "london": "15°C, Rainy",
            "paris": "18°C, Sunny",
            "tokyo": "22°C, Cloudy"
        }
    
    Args:
        location: City name
        
    Returns:
        Weather description
    """
    # TODO: Define weather_data dictionary with at least 3 cities
    weather_data = {
        # Add city weather data here
    }
    
    return weather_data.get(location.lower(), "Location not found")


def main():
    """
    Create an agent and add tools to it.
    
    Learning goals:
    - How to create a Tool object
    - How to register tools with an agent
    - How agents decide which tool to use
    """
    
    # Create agent
    agent = SimpleAgent()
    
    # Register calculator tool (already implemented)
    calculator_tool = Tool(
        name="calculator",
        description="Performs basic math (+, -, *, /)",
        func=calculator,
        parameters={"expression": "Math expression"}
    )
    agent.register_tool(calculator_tool)
    
    # TODO: Create and register weather tool
    # Steps:
    # 1. Implement get_weather() function above (add weather_data dict with cities)
    # 2. Create a Tool object for weather:
    #    - name="weather"
    #    - description="Gets weather for a location"
    #    - func=get_weather
    #    - parameters={"location": "City name"}
    # 3. Register it: agent.register_tool(weather_tool)
    #
    # Uncomment and complete this:
    # weather_tool = Tool(
    #     name="weather",
    #     description="Gets weather for a location",
    #     func=get_weather,
    #     parameters={"location": "City name"}
    # )
    # agent.register_tool(weather_tool)
    
    # Show available tools
    print("=" * 60)
    print("Exercise 4b: Add a Tool (Weather)")
    print("=" * 60)
    print("\nAvailable tools:")
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
