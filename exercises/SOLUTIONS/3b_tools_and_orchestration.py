"""
SOLUTION: Exercise 3b - Adding a New Tool and Orchestration
This is the complete solution showing how to add a percentage calculator tool.
"""

from chatbot import (
    Agent, 
    AgentOrchestrator, 
    Tool,
    LLMIntentClassifier,
    load_model,
)
import logging
import re

logging.basicConfig(level=logging.INFO)


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def calculator(input: str) -> str:
    """
    Performs basic mathematical calculations.
    
    Supports: addition (+, plus), subtraction (-, minus), multiplication (*, times), division (/, divided by)
    
    Args:
        input: Math expression like "5 + 3", "10 * 2", or "8 plus 4"
        
    Returns:
        Calculated result or error message
    """
    try:
        input = input.strip().lower()
        
        # Extract numbers from the input
        numbers = re.findall(r'\d+\.?\d*', input)
        if len(numbers) < 2:
            return "Invalid expression. Need two numbers."
        
        a = float(numbers[0])
        b = float(numbers[1])
        
        # Determine operation based on symbols or words
        if "+" in input or "plus" in input or "add" in input:
            result = a + b
            op_display = "+"
        elif "-" in input or "minus" in input or "subtract" in input:
            result = a - b
            op_display = "-"
        elif "*" in input or "times" in input or "multiply" in input or "multiplied" in input:
            result = a * b
            op_display = "*"
        elif "/" in input or "divided" in input or "divide" in input:
            if b == 0:
                return "Error: Cannot divide by zero"
            result = a / b
            op_display = "/"
        else:
            return "Invalid expression. Supported operations: +, -, *, / (or plus, minus, times, divided by)"
        
        # Format result
        if result == int(result):
            return f"{a} {op_display} {b} = {int(result)}"
        else:
            return f"{a} {op_display} {b} = {result:.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


def advanced_math(input: str) -> str:
    """
    Advanced mathematical operations.
    
    Supports: square root, power/exponentiation
    
    Args:
        input: Description like "square root of 16" or "2 to the power of 3"
        
    Returns:
        Calculated result
    """
    try:
        import re
        input = input.lower().strip()
        
        # Square root
        if "square root" in input or "sqrt" in input:
            numbers = re.findall(r'\d+\.?\d*', input)
            if numbers:
                num = float(numbers[0])
                result = num ** 0.5
                return f"√{num} = {result:.2f}"
        
        # Power
        if "power" in input or "^" in input:
            numbers = re.findall(r'\d+\.?\d*', input)
            if len(numbers) >= 2:
                base, exp = float(numbers[0]), float(numbers[1])
                result = base ** exp
                return f"{base}^{exp} = {result:.2f}"
        
        return "Unsupported input. Try: 'square root of 16' or '2 power 3'"
    except Exception as e:
        return f"Error: {str(e)}"


def trigonometry(input: str) -> str:
    """
    Trigonometric calculations.
    
    Supports: sin, cos, tan (in degrees)
    
    Args:
        input: Description like "sin of 30", "cos 45", "tangent of 60"
        
    Returns:
        Calculated trigonometric result
        
    Examples:
        trigonometry("sin of 30") → "sin(30°) = 0.50"
        trigonometry("cos 45") → "cos(45°) = 0.71"
        trigonometry("tan of 60") → "tan(60°) = 1.73"
    """
    try:
        import math
        input = input.lower().strip()
        
        # Extract the angle value
        numbers = re.findall(r'\d+\.?\d*', input)
        if not numbers:
            return "No angle found in input"
        
        angle_deg = float(numbers[0])
        angle_rad = math.radians(angle_deg)
        
        # Determine which function
        if "sin" in input:
            result = math.sin(angle_rad)
            return f"sin({angle_deg}°) = {result:.2f}"
        elif "cos" in input:
            result = math.cos(angle_rad)
            return f"cos({angle_deg}°) = {result:.2f}"
        elif "tan" in input:
            result = math.tan(angle_rad)
            return f"tan({angle_deg}°) = {result:.2f}"
        
        return "Unsupported operation. Try: 'sin of 30', 'cos 45', or 'tan 60'"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """
    Build multi-agent system and add a new tool.
    """
    print("=" * 70)
    print("SOLUTION: Exercise 3b - Adding a New Tool")
    print("=" * 70)
    print("\nBuilding multi-agent system with trigonometry tool...\n")
    
    # Step 1: Load model
    model = load_model("models/tinyllama.gguf")
    
    # Step 2: Create intent classifier
    intent_classifier = LLMIntentClassifier(model=model)
    
    # Step 3: Create agents with tools
    
    # Greeting Agent (no changes)
    greeting_agent = Agent(
        name="Greeting Agent",
        description="Handles greetings",
        tools=[],
        model=model
    )
    
    # Calculator Agent - WITH 3 TOOLS (including percentage_calculator)
    calculator_tools = [
        Tool(
            name="calculator",
            description="Performs ONLY basic arithmetic operations: addition (+), subtraction (-), multiplication (*), division (/). Use ONLY for expressions with these operators.",
            function=calculator,
            entities={
                "input": "Math expression as a string (e.g., '5 + 3', '10 / 2', '8 * 4')"
            }
        ),
        Tool(
            name="advanced_math",
            description="Performs advanced math operations like square root and exponentiation. Use for 'sqrt', 'square root', 'power', or exponents.",
            function=advanced_math,
            entities={
                "input": "Operation description as a string (e.g., 'square root of 16', '2 power 3')"
            }
        ),
        # SOLUTION: New trigonometry tool added here
        Tool(
            name="trigonometry",
            description="Calculates trigonometric functions (sin, cos, tan) for angles in degrees. Use ONLY when request contains 'sin', 'cos', 'tan', 'sine', 'cosine', or 'tangent'.",
            function=trigonometry,
            entities={
                "input": "Trigonometric expression as a string (e.g., 'sin of 30', 'cos 45', 'tangent of 60')"
            }
        ),
    ]
    
    calculator_agent = Agent(
        name="Calculator Agent",
        description="Solves math problems using available tools",
        tools=calculator_tools,
        model=model
    )
    
    # OutOfScope Agent (no changes)
    out_of_scope_agent = Agent(
        name="OutOfScope Agent",
        description="Handles unsupported requests",
        tools=[],
        model=model
    )
    
    # Step 4: Create orchestrator and register agents
    orchestrator = AgentOrchestrator(
        intent_classifier=intent_classifier
    )
    
    orchestrator.register_agent("greeting", greeting_agent)
    orchestrator.register_agent("calculate", calculator_agent)
    orchestrator.register_agent("out_of_scope", out_of_scope_agent)
    
    print("✓ Multi-Agent System Ready")
    print(f"✓ Calculator Agent has {len(calculator_tools)} tools\n")
    
    # Step 5: Test the NEW tool orchestration
    print("=" * 70)
    print("Testing Tool Orchestration")
    print("=" * 70)
    print("\nWatch how the LLM intelligently selects the right tool!\n")
    
    test_requests = [
        # NEW: Trigonometry (should use 'trigonometry' tool)
        "What is the sine of 30?",
        "Calculate cos of 45",
    ]
    
    for request in test_requests:
        print(f"👤 User: {request}")
        response = orchestrator.execute(request)
        print(f"🤖 Bot: {response}")
        print(f"   (Tool orchestration happened automatically!)\n")

    
    # Step 6: Interactive mode
    print("=" * 70)
    print("Interactive Mode - Try Different Math Requests!")
    print("=" * 70)
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye!")
                break
            
            response = orchestrator.execute(user_input)
            print(f"🤖 Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
