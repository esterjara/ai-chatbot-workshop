"""
Exercise 4c: Multiple Tools with Tool Chaining (SOLUTION - Optional Advanced)

This reference implementation shows:
- Creating multiple tools (3+)
- Better decision logic for tool selection
- Error handling and validation
- Tool chaining concepts
- More realistic use cases
"""

from src.chatbot.agent import SimpleAgent, Tool
import re


def calculator(expression: str) -> str:
    """
    Advanced calculator with better parsing and error handling.
    SOLUTION: Shows robust implementation with regex parsing.
    """
    try:
        # Use regex for better parsing
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
    SOLUTION: Weather tool with structured data for more complex logic.
    Returns temperature for comparison operations.
    """
    weather_data = {
        "london": {"temp": 15, "condition": "Rainy", "emoji": "☔"},
        "paris": {"temp": 18, "condition": "Sunny", "emoji": "☀️"},
        "tokyo": {"temp": 22, "condition": "Cloudy", "emoji": "☁️"},
        "new york": {"temp": 12, "condition": "Snowing", "emoji": "❄️"},
        "sydney": {"temp": 25, "condition": "Clear", "emoji": "🌞"},
        "buenos aires": {"temp": 20, "condition": "Partly cloudy", "emoji": "🌤️"},
        "moscow": {"temp": -5, "condition": "Snowing", "emoji": "❄️"},
        "dubai": {"temp": 35, "condition": "Sunny", "emoji": "🔥"},
    }
    
    data = weather_data.get(location.lower())
    if data:
        return f"{data['temp']}°C, {data['condition']} {data['emoji']}"
    return "Location not found"


def search_knowledge(query: str) -> str:
    """
    SOLUTION: Knowledge base search with comprehensive information.
    Enables learning about AI concepts while using the agent.
    """
    knowledge_base = {
        "python": "Python is a versatile programming language known for readability and simplicity. Great for AI/ML!",
        "ai": "Artificial Intelligence is the simulation of human intelligence by computers. Includes ML, NLP, CV.",
        "machine learning": "Machine Learning is a subset of AI where systems learn from data without explicit programming.",
        "chatbot": "A chatbot is a conversational AI that simulates human conversation. Powers assistant apps.",
        "agent": "An agent is an autonomous system that can perceive, decide, and act. Uses tools to extend capabilities.",
        "tool": "A tool is a function that extends what an agent can do. Plugins for agents!",
        "nlp": "Natural Language Processing enables computers to understand human language.",
        "rag": "Retrieval-Augmented Generation combines document search with language generation.",
        "memory": "Memory systems allow chatbots to remember conversation history.",
        "embedding": "Embeddings represent text as vectors for semantic similarity.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"No information found about '{query}'. Try: python, ai, machine learning, chatbot, agent, tool, nlp, rag, memory, embedding"


def get_weather_analysis(location: str) -> str:
    """
    SOLUTION: Additional helper to analyze weather conditions.
    Demonstrates tool composition possibilities.
    """
    weather_data = {
        "london": {"temp": 15, "cold": False, "rainy": True},
        "paris": {"temp": 18, "cold": False, "rainy": False},
        "tokyo": {"temp": 22, "cold": False, "rainy": False},
        "new york": {"temp": 12, "cold": True, "rainy": False},
        "sydney": {"temp": 25, "cold": False, "rainy": False},
        "moscow": {"temp": -5, "cold": True, "rainy": False},
    }
    
    data = weather_data.get(location.lower())
    if not data:
        return "Location not found"
    
    conditions = []
    if data["cold"]:
        conditions.append("cold")
    if data["rainy"]:
        conditions.append("rainy")
    if not conditions:
        conditions.append("pleasant")
    
    return f"{location} is {', '.join(conditions)} ({data['temp']}°C)"


def main():
    """
    SOLUTION: Advanced agent with 3+ tools demonstrating:
    - Tool registry and management
    - Better decision logic
    - Error handling
    - Extensibility for tool chaining
    """
    
    # Create agent
    agent = SimpleAgent()
    
    # SOLUTION: Tool 1 - Calculator with robust parsing
    calculator_tool = Tool(
        name="calculator",
        description="Performs basic math operations (+, -, *, /)",
        func=calculator,
        parameters={"expression": "Math expression like '5 + 3'"}
    )
    agent.register_tool(calculator_tool)
    
    # SOLUTION: Tool 2 - Weather with structured data
    weather_tool = Tool(
        name="weather",
        description="Gets weather information for a city",
        func=get_weather,
        parameters={"location": "City name"}
    )
    agent.register_tool(weather_tool)
    
    # SOLUTION: Tool 3 - Search knowledge base
    search_tool = Tool(
        name="search",
        description="Search for information in knowledge base about AI topics",
        func=search_knowledge,
        parameters={"query": "Search query about AI concepts"}
    )
    agent.register_tool(search_tool)
    
    # SOLUTION: Optional Tool 4 - Weather analysis (advanced)
    # This demonstrates extensibility
    analysis_tool = Tool(
        name="analyze_weather",
        description="Analyzes if weather is cold/rainy",
        func=get_weather_analysis,
        parameters={"location": "City name"}
    )
    agent.register_tool(analysis_tool)
    
    # Display
    print("=" * 70)
    print("Exercise 4c: Multiple Tools with Tool Chaining (SOLUTION)")
    print("=" * 70)
    print("\nAgent has 4 tools available:")
    print(agent.get_tools_description())
    print("\n" + "=" * 70)
    print("WHAT YOU'VE LEARNED:")
    print("  ✓ How to create multiple tools")
    print("  ✓ Tool structure and registration")
    print("  ✓ Agent decision logic")
    print("  ✓ Error handling in tools")
    print("  ✓ Extensibility and scaling")
    print()
    print("CHALLENGE IDEAS:")
    print("  - Add a 'time' tool")
    print("  - Add a 'file' tool for reading documents")
    print("  - Create a custom domain-specific tool")
    print("  - Implement tool chaining (output → input)")
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
