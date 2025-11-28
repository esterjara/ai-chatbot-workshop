"""
Exercise 3a: Multi-Agent System Setup
Build a complete multi-agent system with intent classification and orchestration.

What You'll Build:
-----------------
1. LLM Intent Classifier (routes requests to right agent)
2. Three Specialized Agents:
   - Greeting Agent: Handles "hi", "hello", small talk
   - Calculator Agent: Handles math with tools
   - OutOfScope Agent: Handles unsupported requests
3. Agent Orchestrator (coordinates everything)

This is the foundation for agentic AI systems!
"""
import logging

from chatbot import (
    Agent, 
    AgentOrchestrator, 
    Tool,
    LLMIntentClassifier,
    load_model,
)
from tools import calculator, advanced_math

logging.basicConfig(level=logging.INFO)

def main():
    """
    Build and run a complete multi-agent system.
    """
    print("=" * 70)
    print("Exercise 3a: Multi-Agent System Setup")
    print("=" * 70)
    
    # Step 1: Load LLM model
    print("Step 1: Loading LLM model...")
    model = load_model("models/tinyllama.gguf")
    print("✓ Model loaded\n")
    
    # Step 2: Create Intent Classifier
    print("Step 2: Creating intent classifier...")
    intent_classifier = LLMIntentClassifier(model=model)
    print("✓ Intent classifier ready (intents will be registered with agents)\n")
    
    # Step 3: Create Specialized Agents
    print("Step 3: Creating specialized agents...\n")
    
    # Greeting Agent (no tools needed)
    greeting_agent = Agent(
        name="Greeting Agent",
        description="Handles greetings and friendly conversation",
        tools=[],  # No tools needed for greetings
        model=model
    )
    print("  ✓ Greeting Agent: Handles 'hi', 'hello', small talk")
    
    # Calculator Agent (with 2 math tools)
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
        )
    ]
    
    calculator_agent = Agent(
        name="Calculator Agent",
        description="Solves math problems using available tools",
        model=model,
        tools=calculator_tools
    )
    print(f"  ✓ Calculator Agent: Handles math with {len(calculator_tools)} tools")
    
    # OutOfScope Agent (for unsupported requests)
    out_of_scope_agent = Agent(
        name="OutOfScope Agent",
        description="Handles unsupported or unclear requests",
        tools=[],
        model=model
    )
    print("  ✓ OutOfScope Agent: Handles unsupported requests\n")
    
    # Step 4: Create Orchestrator
    print("Step 4: Creating agent orchestrator...")
    orchestrator = AgentOrchestrator(
        intent_classifier=intent_classifier
    )
    
    # Register all agents with their intents
    orchestrator.register_agent("greeting", greeting_agent)
    orchestrator.register_agent("calculate", calculator_agent)
    orchestrator.register_agent("out_of_scope", out_of_scope_agent)
    
    print("✓ Orchestrator ready")
    print(f"  Registered {len(orchestrator.agents)} agents")

    intent_definitions = intent_classifier.get_intent_definitions()
    if intent_definitions:
        print("  Intent descriptions:")
        for intent, description in intent_definitions.items():
            print(f"    - {intent}: {description}")
    else:
        print("  No intent descriptions registered (this should not happen).")

    print()
    
    # Step 5: Test the Multi-agent system
    print("=" * 70)
    print("Multi-Agent System Ready!")
    print("=" * 70)

    test_requests = [
        # Basic arithmetic (should use 'calculator' tool)
        "What is 25 + 17?",
        
        # Advanced math (should use 'advanced_math' tool)
        "Calculate 2 power 4"
    ]
    
    for request in test_requests:
        print(f"👤 User: {request}")
        response = orchestrator.execute(request)
        print(f"🤖 Assistant: {response}")
        print(f"   (Tool orchestration happened automatically!)\n")

    # Step 6: Interactive mode
    print("Interactive Mode - Try Different Requests!")
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
            print(f"🤖 Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
