# Exercise 4: Agents & Tools

## What is an Agent?

An **agent** is a system that:
1. **Observes**: Receives user request
2. **Reasons**: Decides what to do (use a tool or respond?)
3. **Acts**: Executes the decision
4. **Repeats**: Uses results for next action

## What is a Tool?

A **tool** extends what an agent can do:
- **Function**: The actual code (e.g., calculator)
- **Metadata**: Name, description, parameters
- **Purpose**: Give agents superpowers!

Examples:
- 🧮 Calculator (math)
- 🌡️ Weather API (weather)
- 🔍 Search (information)
- 📊 Database (data lookup)

---

## The Two Exercises

### Exercise 4a: Simple Agent

**Goal**: Understand how agents work with ONE tool

**What you'll do:**
- See a complete agent with calculator tool
- Run it and observe behavior
- Understand the agent-tool interaction

**Quick start:**
```powershell
python exercises/04_agents_and_tools/4a_simple_agent.py
```

**Try:**
```
You: What is 5 + 3?
You: Calculate 100 / 4
You: How much is 20 * 3?
```

**What you learn:**
- ✅ Tool structure (name, description, func, parameters)
- ✅ Tool registration (how agents store tools)
- ✅ Agent decision logic (when to use a tool)
- ✅ Agent execution (calling tools and returning results)

---

### Exercise 4b: Add a Tool

**Goal**: Learn to CREATE and REGISTER tools

**Starting point:** 4a works (calculator tool)

**Your task:** Add a SECOND tool (weather)

**Steps:**
1. Implement `get_weather()` function with mock city data
2. Create a `Tool` object for weather
3. Register it with `agent.register_tool()`

**Quick start:**
```powershell
python exercises/04_agents_and_tools/4b_add_tool.py
```

**Complete the TODO:**

```python
# TODO: Implement weather data
def get_weather(location: str) -> str:
    weather_data = {
        "london": "15°C, Rainy",
        "paris": "18°C, Sunny",
        # Add more cities...
    }
    return weather_data.get(location.lower(), "Location not found")

# TODO: Create and register tool
weather_tool = Tool(
    name="weather",
    description="Gets weather for a location",
    func=get_weather,
    parameters={"location": "City name"}
)
agent.register_tool(weather_tool)
```

**Then test:**
```
You: What is 5 + 3?
You: What is the weather in London?
You: Tell me about Paris weather
```

**What you learn:**
- ✅ How to implement tool functions
- ✅ How to create Tool objects
- ✅ How to extend agents
- ✅ How agents decide which tool to use

---

### Exercise 4c: Multiple Tools with Tool Chaining (Optional Advanced)

**Goal**: Master agents with 3+ tools and understand tool chaining

**Starting point:** 4b works (calculator + weather tools)

**Your task:** Create a THIRD tool (search) and handle multiple tools intelligently

**Challenge levels:**

**Level 1 - Basic (Use each tool):**
```
You: What is 25 * 4?           → Calculator
You: Weather in Tokyo?          → Weather
You: Search for machine learning → Search
```

**Level 2 - Intermediate (Combine requests):**
```
You: Calculate 10 + 5 and search for chatbot
You: What's the weather and also compute 50 / 2
```

**Level 3 - Advanced (Conditional logic):**
```
You: Is it cold in London?      → Check weather, analyze temp
You: What's 100 - 50?           → Calculate, then use result
```

**Your implementation:**

Complete the TODO in `4c_tool_chaining.py`:
1. Implement 3 tool functions (calculator, weather, search)
2. Create Tool objects for each
3. Register them with the agent
4. Add logic for better decision-making

**Quick start:**
```powershell
python exercises/04_agents_and_tools/4c_tool_chaining.py
```

**What you learn:**
- ✅ Managing multiple tools effectively
- ✅ Better agent decision logic
- ✅ Tool composition and chaining
- ✅ Error handling and validation
- ✅ Scaling agents with more capabilities

---

## Exercise Progression

Every tool needs 4 components:

```python
Tool(
    name="calculator",                    # Unique identifier
    description="Performs basic math",    # What it does
    func=calculator,                      # The function
    parameters={"expression": "Math"}     # Input spec
)
```

**Parameters** tell the agent what inputs the tool expects:
```python
parameters={
    "location": "City name",
    "expression": "Math expression"
}
```

---

## How Agents Decide

The agent uses simple keyword matching:

```python
if "calculate" in request.lower():
    use_calculator_tool()

if "weather" in request.lower():
    use_weather_tool()
```

**In production**, this would use an LLM to reason intelligently.

---

## Quick Reference

### Create a Tool

```python
def my_function(param1: str) -> str:
    return f"Result for {param1}"

tool = Tool(
    name="mytool",
    description="Does something useful",
    func=my_function,
    parameters={"param1": "Description"}
)
```

### Register a Tool

```python
agent = SimpleAgent()
agent.register_tool(tool)
```

### Use the Tool

```python
response = agent.execute("user request")
print(response)
```

---

## Testing Tips

**Test 4a:**
- Simple math: `What is 5 + 3?`
- Different operations: `5 * 10`, `100 / 4`
- Natural language: `Calculate two plus eight`

**Test 4b:**
- Math works: `What is 10 - 3?`
- Weather works: `What is the weather in Paris?`
- Mixed: `It's cold, what's the weather in London? Also calculate 5 + 5`

---

## Got Stuck?

Check the **SOLUTIONS** folder:

```
SOLUTIONS/
  4a_simple_agent.py      (reference for 4a)
  4b_add_tool.py          (reference for 4b)
  4c_tool_chaining.py     (reference for 4c - optional)
```
Run a solution:
```powershell
python exercises/04_agents_and_tools/SOLUTIONS/4b_add_tool.py
```

---

## Key Insights

✅ Agents enable multi-step reasoning  
✅ Tools extend agent capabilities  
✅ Tool selection can be keyword-based or LLM-based  
✅ Easy to add new tools (just implement function + register)  
✅ Real-world: ChatGPT uses plugins (tools with this pattern)

---

## Workshop Summary

### All Exercises Complete! 🎉

1. **Exercise 1**: Basic chatbot (API + system prompts)
2. **Exercise 2**: Memory (conversation context)
3. **Exercise 3**: RAG (document retrieval)
4. **Exercise 4**: Agents & Tools (reasoning + tool use) ← You are here

### These 4 Exercises Power Modern AI

The combination enables:
- 🧠 Reasoning and planning
- 📚 Access to documents
- 🛠️ Use of external tools
- 💾 Memory of conversations

This is exactly what ChatGPT and Claude do!

---

## Production Frameworks

After this workshop, explore:

- **LangChain**: Most popular (1000+ integrations)
  - Agents, tools, chains, memory, RAG
  - Works with any LLM

- **CrewAI**: Multi-agent systems
  - Team coordination
  - Role-based agents

- **Semantic Kernel**: Microsoft's framework
  - Native .NET/Python support
  - Enterprise features

---

## Next Steps

1. ✅ Complete both exercises
2. 🔄 Combine all concepts (memory + RAG + tools)
3. 🌐 Deploy as web API (FastAPI)
4. 🚀 Build your own agent system

Congratulations on completing the AI Chatbot Workshop! 🚀
