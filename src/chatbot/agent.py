"""
Agent Module

This module provides:
- Agent: Handles user requests with LLM and optionally tools
- AgentOrchestrator: Routes requests to the right agent

SIMPLE DESIGN:
=============
1. Agent WITHOUT tools (greeting, out-of-scope):
   - Just uses LLM to respond

2. Agent WITH tools (calculator):
   - Uses LLM to decide which tool to use
   - Executes the tool
   - Uses LLM to format the result

Example: "What's 5 + 3?"
→ Calculator agent's LLM picks "calculator" tool
→ Tool returns "5 + 3 = 8"
→ LLM formats: "The answer is 8."
"""

from typing import Dict, Any, List, Optional
import logging

from .tool import Tool
from .intent_classifier import Intent, LLMIntentClassifier
from .text_generator import generate_text, generate_response
from . import prompts
from llama_cpp import Llama

_logger = logging.getLogger(__name__)


class Agent:
    """
    Simple agent that responds to user requests.
    
    Can work in two modes:
    1. Pure LLM: Just generates conversational responses
    2. LLM + Tools: Uses tools to help answer, then formats the result
    
    When tools are registered:
    - LLM decides which tool to use
    - Tool executes
    - LLM makes the response natural
    """
    
    def __init__(
        self,
        name: str,
        model: Llama,
        description: str = "",
        tools: Optional[List[Tool]] = None
    ):
        """
        Create an agent.
        
        Args:
            name: Agent name (e.g., "Calculator", "Greeter")
            model: LLM model instance (shared across agents)
            description: Optional description of what this agent does
            tools: Optional list of tools this agent can use
        """
        self.name = name
        self.description = description
        self.model = model
        self.tools: Dict[str, Tool] = {}
        
        # Register tools if provided
        if tools:
            for tool in tools:
                self.register_tool(tool)
        
        _logger.info(f"Agent '{name}' initialized with shared model and {len(self.tools)} tools")
    
    def register_tool(self, tool: Tool):
        """Add a tool this agent can use."""
        self.tools[tool.name] = tool
        _logger.info(f"[{self.name}] Registered tool: {tool.name}")
    
    def execute(self, user_request: str, intent: Optional[Intent] = None) -> str:
        """
        Handle a user request.
        
        Process:
        1. If agent has tools, let LLM pick one and use it
        2. Generate a natural response with LLM
        
        Args:
            user_request: What the user asked
            intent: Classified intent (from orchestrator)
            
        Returns:
            Natural language response
        """
        tool_result = None
        intent_name = intent.name if intent else "unknown"

        # Step 1: Let the LLM decide if any registered tool should run
        if self.tools:
            tool_result = self._use_tool(user_request, intent_name)
            _logger.info(f"[{self.name}] Tool result: {tool_result}")
        
        # Step 2: Generate natural response with LLM
        if self.model:
            response = self._generate_response(user_request, intent_name, tool_result)
        else:
            response = tool_result or "I'm not configured properly."
        
        return response
    
    def _use_tool(self, user_request: str, intent: str) -> Optional[str]:
        """
        Let LLM pick a tool and use it.
        
        Args:
            user_request: User's question
            intent: Classified intent name for additional context
            
        Returns:
            Tool result or None
        """
        # Get tool info for LLM
        tools_info = {}
        for name, tool in self.tools.items():
            tools_info[name] = {
                "description": tool.description,
                "parameters": tool.entities
            }
        
        # Ask LLM which tool to use
        prompt = prompts.get_tool_selection_prompt(
            user_input=user_request,
            available_tools=tools_info
        )
        
        try:
            import json
            import re
            response = generate_text(
                self.model,
                prompt,
                max_tokens=150,
                temperature=0.0
            )
            
            # Clean the response: remove markdown code fences and extra formatting
            cleaned_response = response.strip()
            
            # Remove markdown code fences (```json, ```, `, ´, etc.)
            cleaned_response = re.sub(r'^```json\s*', '', cleaned_response)
            cleaned_response = re.sub(r'^```\s*', '', cleaned_response)
            cleaned_response = re.sub(r'\s*```$', '', cleaned_response)
            cleaned_response = re.sub(r'^[`´]+\s*', '', cleaned_response)
            cleaned_response = re.sub(r'\s*[`´]+$', '', cleaned_response)
            cleaned_response = cleaned_response.strip()
            
            _logger.debug(f"[{self.name}] Tool selection response: {cleaned_response}")
            
            result = json.loads(cleaned_response)
            
            print(result)
            # Validate the response has the expected structure
            if "tool_name" not in result:
                _logger.error(f"[{self.name}] Invalid tool selection response - missing 'tool_name': {result}")
                return None
            
            tool_name = result.get("tool_name")

            # Handle common LLM typos (entieties, entitites, etc.)
            entities = result.get("entities") or result.get("entieties") or result.get("entitites") or {}
            input = entities.get("input", {}) if "input" in entities else entities

            # Execute the tool
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                tool_result = tool.call(input=input)
                _logger.info(f"[{self.name}] Used {tool_name}: {input}")
                return tool_result
        
        except Exception as e:
            _logger.error(f"[{self.name}] Tool use failed: {e}")
        
        return None
    
    def _generate_response(self, user_request: str, intent: str, tool_result: Optional[str]) -> str:
        """
        Generate natural response with LLM.
        
        Args:
            user_request: User's question
            intent: Intent type
            tool_result: Tool output (if any)
            
        Returns:
            Natural response
        """
        
        if tool_result:
            # Format tool result naturally
            prompt = prompts.get_tool_response_prompt(
                user_input=user_request,
                tool_result=tool_result
            )
        else:
            # Pure conversational response
            prompt = prompts.get_conversational_response_prompt(
                user_input=user_request,
                intent=intent
            )
        
        try:
            response = generate_text(self.model, prompt, max_tokens=150, temperature=0.7)
            return response.strip()
        except Exception as e:
            _logger.error(f"[{self.name}] Response generation failed: {e}")
            return tool_result or "I apologize, I'm having trouble responding."


class AgentOrchestrator:
    """
    Routes user requests to the right agent.
    
    How it works:
    1. Classifies what the user wants (intent)
    2. Sends request to the right agent
    3. Returns the agent's response
    """
    
    def __init__(
        self,
        intent_classifier: LLMIntentClassifier,
    ):
        """
        Create an orchestrator.
        
        Args:
            intent_classifier: Classifies user intents
        """
        self.agents: Dict[str, Agent] = {}
        self.intent_classifier = intent_classifier
    
    def register_agent(self, intent: str, agent: Agent):
        """
        Register an agent for a specific intent.
        
        Args:
            intent: The intent this agent handles (e.g., "greeting", "calculate")
            agent: The agent to register
        """
        self.agents[intent] = agent
        description = agent.description or f"Agent responsible for '{intent}'"
        self.intent_classifier.register_intent(intent, description)
        _logger.info(f"Registered '{agent.name}' for intent: {intent}")
    
    def execute(self, user_request: str) -> str:
        """
        Process a user request.
        
        Args:
            user_request: What the user asked
            
        Returns:
            Response from the appropriate agent
        """
        # Classify intent
        intent = self.intent_classifier.classify(user_request)
        agent = self.agents.get(intent.name)
        
        if not agent:
            return f"I don't know how to handle: {intent.name}"
        
        _logger.info(f"Routing '{intent.name}' to {agent.name}")
        
        # Let agent handle it
        response = agent.execute(user_request, intent)
        
        return f"[{agent.name}] {response}"

