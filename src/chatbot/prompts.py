"""
Prompts Module

Centralized location for all LLM prompts used in the chatbot system.
This makes prompts easy to find, modify, and maintain.

All prompts should be defined here - never embed prompts in other modules.
"""

import json

# ============================================================================
# INTENT CLASSIFICATION PROMPTS
# ============================================================================

# JSON schema for structured intent output
INTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "description": "The classified intent"
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence score between 0 and 1"
        },
        "entities": {
            "type": "object",
            "description": "Extracted entities like expression, location, etc."
        },
        "reasoning": {
            "type": "string",
            "description": "Brief explanation of the classification"
        }
    },
    "required": ["intent", "confidence", "entities", "reasoning"]
}


def get_intent_classification_prompt(intent_definitions: dict, user_input: str) -> str:
    """
    Build the prompt for intent classification.
    
    Args:
        intent_definitions: Dictionary of intent names and descriptions
        user_input: Current user input to classify
        
    Returns:
        Complete classification prompt
    """
    # Build intent descriptions
    intent_list = "\n".join([
        f"- {name}: {desc}"
        for name, desc in intent_definitions.items()
    ])
    
    intent_names = list(intent_definitions.keys())
    
    prompt = f"""You are an intent classifier for a multi-agent chatbot system.

    Available Intents:
    {intent_list}

    Examples:
    User: "Hello there"
    {{
    "intent": "greeting",
    "confidence": 0.95,
    "entities": {{}},
    "reasoning": "User is greeting"
    }}

    User: "Calculate 5 + 3"
    {{
    "intent": "calculate",
    "confidence": 0.98,
    "entities": {{ "expression": "5 + 3" }},
    "reasoning": "User wants to perform addition"
    }}

    User: "What is the weather in London?"
    {{
    "intent": "out_of_scope",
    "confidence": 0.90,
    "entities": {{ "location": "London" }},
    "reasoning": "Weather information is not supported"
    }}

    Current User Input: "{user_input}"

    Task: Classify the user's intent based on their current input.
    Output ONLY valid JSON matching the examples above.

    JSON Response:"""    
    return prompt


# ============================================================================
# CONVERSATIONAL RESPONSE PROMPTS
# ============================================================================

def get_conversational_response_prompt(
    user_input: str, 
    intent: str
) -> str:
    """
    Build the prompt for conversational responses (greetings, out-of-scope).
    
    The LLM generates natural responses for these intents without tools.
    
    Args:
        user_input: Current user input
        intent: The classified intent (greeting or out_of_scope)
        
    Returns:
        Complete conversational prompt
    """
    if intent == "greeting":
        prompt = f"""You are a friendly AI assistant.
        User: {user_input}

        Instructions:
        - Respond warmly and naturally to the user's greeting or small talk.
        - Keep the reply concise (1-2 sentences).
        - Write only what the assistant would say, with no analysis or meta-commentary.

        Assistant:"""
    
    elif intent == "out_of_scope":
        capabilities = "I can help with:\n- Greetings and friendly conversation\n- Mathematical calculations (basic and advanced)"
        
        prompt = f"""You are a helpful AI assistant with limited but useful capabilities.

User: {user_input}

Capabilities:
{capabilities}

Instructions:
- Politely explain that you cannot complete their specific request.
- Offer what you CAN help with instead.
- Stay friendly and concise (2-3 sentences).
- Write only the assistant's reply, no additional commentary.

Assistant:"""
    
    else:
        # Fallback for unknown intents
        prompt = f"""You are a helpful AI assistant.

User: {user_input}

Instructions:
- Respond naturally and helpfully to the user.
- Keep the reply concise (1-2 sentences).
- Output only the assistant's message, without analysis.

Assistant:"""
    
    return prompt


# ============================================================================
# TOOL SELECTION AND ORCHESTRATION PROMPTS
# ============================================================================

# JSON schema for tool selection
TOOL_SELECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "tool_name": {
            "type": "string",
            "description": "Name of the tool to use, or 'none' if no tool needed"
        },
        "parameters": {
            "type": "object",
            "description": "Parameters to pass to the tool"
        },
        "reasoning": {
            "type": "string",
            "description": "Brief explanation of why this tool was chosen"
        }
    },
    "required": ["tool_name", "parameters", "reasoning"]
}


def get_tool_selection_prompt(user_input: str, available_tools: dict) -> str:
    """
    Build the prompt for LLM to decide which tool to use.
    
    The LLM analyzes the request and decides which tool (if any) to use
    and what parameters to pass. Tool descriptions come from the Tool objects
    defined in the exercise/application code.
    
    Args:
        user_input: The user's request
        available_tools: Dict of {tool_name: {"description": str, "parameters": dict}}
                        This data comes directly from Tool objects registered with the agent
        
    Returns:
        Complete tool selection prompt with dynamic tool information
    """
    # Format available tools dynamically from Tool metadata
    tools_list = []
    examples_list = []
    
    for tool_name, tool_info in available_tools.items():
        desc = tool_info.get("description", "")
        params = tool_info.get("parameters", {})
        
        # Add tool description
        tools_list.append(f"  - {tool_name}: {desc}")
        
        # Generate example from the parameters if available
        if "input" in params:
            # Extract the first example from the parameter description
            param_desc = params["input"]
            # Look for examples in parentheses like (e.g., 'example1', 'example2')
            import re
            examples = re.findall(r"'([^']+)'", param_desc)
            for example_input in examples:
                examples_list.append(
                    f'User: "...{example_input}..."\n'
                    f'{{"tool_name": "{tool_name}", "entities": {{"input": "{example_input}"}}, "reasoning": "Use {tool_name} tool"}}'
                )
    
    tools_text = "\n".join(tools_list)
    examples_text = "\n\n".join(examples_list) if examples_list else "No examples available."
    
    prompt = f"""You are a tool selector. Choose the right tool for the user's request.

Available tools:
{tools_text}

Examples of correct tool selection:
{examples_text}

CRITICAL INSTRUCTIONS:
1. Match the user's request to the most appropriate tool based on the tool descriptions
2. Extract the mathematical expression/operation EXACTLY from the user's input
3. Put the extracted expression in the "input" field inside "entities"
4. Return ONLY valid JSON in this exact format: {{"tool_name": "SELECTED_TOOL", "entities": {{"input": "EXTRACTED_EXPRESSION"}}, "reasoning": "Brief explanation"}}

Current user request: "{user_input}"

Analyze the request and select the appropriate tool. Return ONLY the JSON:

JSON:"""
    
    return prompt


# ============================================================================
# TOOL-BASED RESPONSE PROMPTS
# ============================================================================

def get_tool_response_prompt(user_input: str, tool_result: str) -> str:
    """
    Build the prompt for generating natural responses based on tool output.
    
    The LLM takes the raw tool result and formats it into a natural,
    conversational response to the user.
    
    Args:
        history_text: Formatted conversation history
        user_input: The user's original request
        tool_result: The result from tool execution
        
    Returns:
        Complete prompt for LLM response generation
    """
    prompt = f"""You are a helpful AI assistant. Answer the user's question using the tool result.
    
    User: {user_input}

    Tool Result:
    {tool_result}

    Instructions:
    - Use the tool result to answer the user's question
    - Provide a clear, direct answer based on the result
    - Be concise (1-2 sentences)
    - Do NOT mention "the tool" - just give the answer naturally

    Your response:"""
    
    return prompt


def get_agent_prompt_template() -> str:
    """
    Template for agent-based responses that use tools.
    
    DEPRECATED: Use get_tool_response_prompt instead.
    This is kept for backwards compatibility.
    
    Returns:
        Agent prompt template
    """
    return """You are a specialized agent. Based on the tool result, provide a natural response to the user."""
