# Exercise 3: Agents & Multi-Agent Systems

## Overview

This exercise introduces how to build sophisticated **agentic AI systems** using:
- **LLM-based intent classification**
- **Specialized agents** for different domains
- **Tool-based capabilities** to extend agent functionality
- **Orchestration** to coordinate multiple agents

### Why Only 3 Agents?

This workshop focuses on **core concepts**, not simulating external services:
- **GreetingAgent**: Simple conversational AI (no tools needed)
- **CalculatorAgent**: Demonstrates real tool usage (self-contained)
- **OutOfScopeAgent**: Handles everything else (weather, search, etc. would require external APIs)

This keeps the workshop **pedagogical** while teaching production-ready patterns!

---

## Overview Capabilities

### 1. **Multi-Agent System Setup** (Exercise 3a)
Build a complete multi-agent system from scratch.

**Key Concepts:**
- LLM-based intent classification (not pattern matching!)
- Creating specialized agents for different tasks
- Registering agents with an orchestrator
- Routing requests to the right agent

**What You'll Build:**
- LLM Intent Classifier
- 3 Specialized Agents (Greeting, Calculator, OutOfScope)
- Agent Orchestrator
- Complete working system

**Run it:**
```bash
poetry run python exercises/03_agents_and_tools/3a_multi_agentic_system.py
```

### 2. **Adding Tools & Orchestration** (Exercise 3b)
Extend the system by adding a new tool and watch LLM orchestration in action.

**Key Concepts:**
- Creating custom tools (trigonometry calculator)
- How the LLM selects tools intelligently
- No hardcoded if/else - the LLM decides!
- Tool parameter extraction
- Natural language responses from tool outputs

**The Challenge:**
Implement a `trigonometry` tool and see the agent automatically use it when users ask "What is the sine of 30?" or "Calculate cos of 45"

**Run it:**
```bash
poetry run python exercises/03_agents_and_tools/3b_tools_and_orchestration.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                            │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│            LLM INTENT CLASSIFIER                                │
│  - Analyzes user request                                        │
│  - Classifies intent: greeting, calculate, out_of_scope         │
│  - Returns structured JSON response                             │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT ORCHESTRATOR                          │
│  - Routes to appropriate agent based on intent                  │
│  - Coordinates multiple specialized agents                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
                   ┌─────────┴─────────┐
                   │                   │
        ┌──────────┴────────┐  ┌──────┴───────────┐
        │  GreetingAgent    │  │ CalculatorAgent  │
        │  (no tools)       │  │  - calculator    │
        └──────────┬────────┘  │  - logarithm     │
                   │           │  - trigonometry* │
                   │           └──────┬───────────┘
        ┌──────────┴────────────────┐ │
        │    OutOfScopeAgent        │ │
        │    (handles unsupported)  │ │
        └───────────────────────────┘ │
                                      │
                      (* added in exercise 3b)
```


---

## The 3 Specialized Agents

### 1. **GreetingAgent**
**Scope:** Greetings and small talk  
**Intent:** `greeting`  
**Tools:** None (conversational only)

**Example Requests:**
- "Hello!"
- "How are you?"
- "Thanks for your help!"

**Why no tools?** Simple conversational responses don't require function calls.

---

### 2. **CalculatorAgent**
**Scope:** Mathematical calculations  
**Intent:** `calculate`  
**Tools:**
- `calculator`: Basic operations (+, -, *, /)
- `logarithm`: Calculate the logarithm
- `trigonometry`: Calculate trigonometric functions (added in 3b)

**Example Requests:**
- "What is 15 + 27?"
- "Calculate the logarithm of 100"
- "What's the sine of 30?"

**Why this demonstrates tools well?** All logic is self-contained, no external APIs needed.

---

### 3. **OutOfScopeAgent**
**Scope:** Everything else not supported  
**Intent:** `out_of_scope`  
**Tools:** None

**Example Requests:**
- "What's the weather in Paris?" (would need weather API)
- "Tell me about Python" (would need search/RAG)
- "Book me a flight" (completely unsupported)

**Why combine these?** Weather, search, and other features would require external services. For a workshop, we explain these are out of scope rather than mock them.

---

## Code Structure

```
src/chatbot/
├── agent.py              # Agent & AgentOrchestrator classes
├── intent_classifier.py  # LLMIntentClassifier
├── tool.py               # Tool class definition
├── prompts.py            # All LLM prompts centralized
└── model_loader.py       # LLM loading utilities

exercises/03_agents_and_tools/
├── 3a_multi_agentic_system.py        # Build complete multi-agent system
├── 3b_tools_and_orchestration.py     # Add new tool and test orchestration
└── README.md                          # This file
```

---

## Key Differences from Simple Chatbots

| Feature | Simple Chatbot | Multi-Agent System |
|---------|---------------|-------------------|
| **Routing** | None - single model | LLM-based intent classification |
| **Specialization** | General purpose | Domain-specific agents |
| **Tools** | None | Multiple tools per agent |
| **Scalability** | Hard to extend | Easy to add new agents |
| **Orchestration** | Single flow | Multiple specialized agents |

---

## Why Use Multi-Agent Systems?

### ✅ **Modularity**
Each agent is independent and can be developed/tested separately.

### ✅ **Specialization**
Agents become experts in their domain with specialized tools.

### ✅ **Scalability**
Adding new capabilities means adding new agents, not rewriting everything.

### ✅ **Maintainability**
Easier to debug, update, and improve specific agents.

### ✅ **Intelligent Routing**
LLM-based intent classification understands natural language requests.

---

## LLM Intent Classification vs Pattern Matching

### Pattern Matching (Old Approach)
```python
if "weather" in text:
    return "weather"
elif "calculate" in text:
    return "calculate"
```

**Problems:**
- ❌ Misses synonyms ("forecast" → weather)
- ❌ No context awareness
- ❌ Brittle - breaks with typos
- ❌ Can't handle ambiguity

### LLM Classification (New Approach)
```python
classifier.classify("How hot is it in Paris?")
# → Intent: weather
# → Entities: {"location": "Paris"}
# → Confidence: 0.95
```

**Benefits:**
- ✅ Understands natural language
- ✅ Extracts entities automatically
- ✅ Provides confidence scores
- ✅ Handles ambiguity and synonyms
- ✅ Robust to typos and variations

---

## Interactive Commands

When running the main exercise, you can use:

- `status` - Show all registered agents and their capabilities
- `exit` or `quit` - Quit the program

---

## Example Conversation Flow

```
You: Hello!
[LLM Classifier] → Intent: greeting (0.95)
[Orchestrator] → Routes to GreetingAgent
[GreetingAgent] → Uses greeting tool
Response: Hello! How can I help you today?

You: What's 5 + 3?
[LLM Classifier] → Intent: calculate (0.90), entities: {"expression": "5 + 3"}
[Orchestrator] → Routes to MathAgent
[MathAgent] → Uses calculator tool
Response: 5 + 3 = 8

You: How's the weather in Tokyo?
[LLM Classifier] → Intent: out_of_scope (0.85)
[Orchestrator] → Routes to OutOfScopeAgent
[OutOfScopeAgent] → Uses out_of_scope tool
Response: I'm sorry, I can't provide weather information. I specialize in:
  • Mathematical calculations
  • Friendly conversation
For weather, you'd need a weather API integration.

You: Book me a flight
[LLM Classifier] → Intent: out_of_scope (0.92)
[Orchestrator] → Routes to OutOfScopeAgent
[OutOfScopeAgent] → Uses out_of_scope tool
Response: I'm sorry, I can't book flights. I specialize in calculations and conversation.
```

---

## Next Steps

After completing this exercise, you'll understand:
- ✅ How to build modular agentic systems
- ✅ LLM-based intent classification
- ✅ Tool creation and registration
- ✅ Agent orchestration and routing
- ✅ Dynamic tool selection with LLMs

---

## Troubleshooting

### Model not found?
```bash
python scripts/download_model.py
```

### Import errors?
Make sure you're in the poetry environment:
```bash
poetry install
poetry shell
```

### Performance issues?
The LLM intent classification can be resource-intensive. If you encounter issues:
- Reduce `max_tokens` in `LLMIntentClassifier`
- Use a smaller/faster model
- Reduce temperature for faster inference

---
