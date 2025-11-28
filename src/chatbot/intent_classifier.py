"""
Intent Classification Module

This module provides LLM-based intent classification for routing
user requests to the appropriate agent in multi-agent systems.

All prompts are defined in prompts.py for easier maintenance.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from .model_loader import generate_text
from . import prompts
from llama_cpp import Llama
import logging
import json
import re

_logger = logging.getLogger(__name__)


@dataclass
class Intent:
    """Represents a classified user intent."""
    name: str
    confidence: float
    entities: Dict[str, Any]  # Extracted entities from the request
    reasoning: str = ""  # Why this intent was chosen


class LLMIntentClassifier:
    """
    LLM-based intent classifier.
    
    This classifier:
    - Uses an LLM to understand user intent from natural language
    - Classifies each request independently based on current input only
    - Extracts entities relevant to the intent
    - Provides confidence scores and reasoning
    - Uses JSON schema for structured output (no parsing needed)
    """
    
    def __init__(
        self,
        model: Llama,
        max_tokens: int = 150
    ):
        """
        Initialize the LLM-based intent classifier.
        
        Args:
            model: Llama model instance to use for classification
            max_tokens: Maximum tokens for classification response
        """
        self.model = model
        self.max_tokens = max_tokens
        self.intent_definitions: Dict[str, str] = {}
    
    def _build_classification_prompt(self, user_input: str) -> str:
        """
        Build the prompt for intent classification using prompts module.
        
        Args:
            user_input: The user's current input
            
        Returns:
            Formatted prompt for the LLM
        """
        # Use centralized prompt builder from prompts.py
        definitions = self.get_intent_definitions()
        if not definitions:
            _logger.warning("No intent definitions registered; classification may be unreliable.")
            definitions = {"out_of_scope": "Default intent when no agents are registered."}
        
        return prompts.get_intent_classification_prompt(
            intent_definitions=definitions,
            user_input=user_input
        )
    
    def register_intent(self, intent: str, description: str):
        """Register or update an intent definition used for prompting."""
        if not intent:
            raise ValueError("Intent name cannot be empty.")
        description = (description or "No description provided.").strip()
        self.intent_definitions[intent] = description
        _logger.debug("Registered intent '%s': %s", intent, description)
    
    def unregister_intent(self, intent: str):
        """Remove an intent definition if it exists."""
        if intent in self.intent_definitions:
            self.intent_definitions.pop(intent)
            _logger.debug("Unregistered intent '%s'", intent)

    def classify(self, user_input: str) -> Intent:
        """
        Classify user intent using the LLM with structured JSON output.
        
        Args:
            user_input: The user's input text
            
        Returns:
            Intent object with classification results
        """
        prompt = self._build_classification_prompt(user_input)
        definitions = self.get_intent_definitions()
        default_intent = "out_of_scope" if "out_of_scope" in definitions else (next(iter(definitions), "out_of_scope"))
        
        try:
            # Generate classification from LLM
            response = generate_text(
                self.model,
                prompt,
                max_tokens=self.max_tokens,
                temperature=0.0  # Lower temperature for more consistent classification
            )
            
            _logger.debug(f"Raw LLM response: {response}")
            
            # Clean the response: remove markdown code fences and extra formatting
            cleaned_response = response.strip()
            
            # Remove markdown code fences (```json, ```, `, ´, etc.)
            cleaned_response = re.sub(r'^```json\s*', '', cleaned_response)
            cleaned_response = re.sub(r'^```\s*', '', cleaned_response)
            cleaned_response = re.sub(r'\s*```$', '', cleaned_response)
            cleaned_response = re.sub(r'^[`´]+\s*', '', cleaned_response)
            cleaned_response = re.sub(r'\s*[`´]+$', '', cleaned_response)
            cleaned_response = cleaned_response.strip()
            
            # Try to parse the JSON response
            try:
                result = json.loads(cleaned_response)
            except json.JSONDecodeError:
                # If direct parsing fails, try fallback extraction
                _logger.warning(f"JSON parsing failed even after cleaning. Cleaned response: {cleaned_response}")
                return Intent(
                    name="out_of_scope",
                    confidence=0.5,
                    entities={},
                    reasoning="Failed to parse LLM response - using default"
                )
            
            intent = Intent(
                name=result.get("intent", "out_of_scope"),
                confidence=float(result.get("confidence", 0.5)),
                entities=result.get("entities", {}),
                reasoning=result.get("reasoning", "")
            )
            
            _logger.info(f"Classified '{user_input}' as '{intent.name}' (confidence: {intent.confidence:.2f})")
            
            return intent
            
        except Exception as e:
            _logger.error(f"Intent classification failed: {e}")
            return Intent(
                name=default_intent,
                confidence=0.0,
                entities={},
                reasoning=f"Classification error: {str(e)}"
            )
    
    def get_intent_definitions(self) -> Dict[str, str]:
        """Get all available intent definitions."""
        return dict(self.intent_definitions)
