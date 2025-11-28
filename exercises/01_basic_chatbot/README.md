# Exercise 1a: Create Your First Chatbot

## Objective
Learn how to load and run a basic chatbot using a local LLM.

## What You'll Do

Run `1a_basic_chatbot.py` and chat with your first AI chatbot!

## Quick Start

```bash
poetry run python exercises/01_basic_chatbot/1a_basic_chatbot.py
```

## Todo in basic_chatbot.py

**Task 1**: Run the chatbot
```bash
poetry run python exercises/01_basic_chatbot/1a_basic_chatbot.py
```

Have a simple conversation:
- Ask "What is Python?"
- Ask "How do I code?"
- Type 'exit' to quit

## Key Concepts

- **Model Path**: Points to your GGUF file (tinyllama.gguf)
- **System Prompt**: Instructions for the LLM (controls personality)
- **Max Tokens**: Limits response length
- **Chat Loop**: Basic interaction pattern

## What's Happening

```
1. Load model from disk
2. User types message
3. Model generates response
4. Display response
5. Repeat until 'exit'
```

## Next Exercise

→ Run `1b_system_prompt.py` to modify the system prompt!

---

# Exercise 1b: Modify the System Prompt

## Objective
Learn how system prompts control chatbot behavior and personality.

## What is a System Prompt?

A system prompt:
- Gives the LLM instructions on how to behave
- Controls tone, expertise level, and response style
- More important than you might think!
- Examples: "Be a teacher", "Be a pirate", "Be an expert"

## Quick Start

```bash
poetry run python exercises/01_basic_chatbot/1b_system_prompt.py
```

## Todo in system_prompt.py

**Task 1**: Run with default prompt
Ask: "What is Python?"

**Task 2**: Uncomment "Python expert" prompt
Change `system_prompt` to:
```python
system_prompt = "You are a Python expert. Provide code examples and explain thoroughly."
```
Ask: "What is Python?"
Compare the response!

**Task 3**: Try "Creative storyteller" mode
```python
system_prompt = "You are a creative storyteller. Make responses entertaining and engaging."
```
Ask: "Tell me about artificial intelligence"

**Task 4**: Try "Patient teacher" mode
```python
system_prompt = "You are a patient teacher. Explain concepts clearly, step-by-step, starting with basics."
```
Ask: "What is recursion?"

**Task 5**: Create your own prompt
```python
system_prompt = ""
```

## Key Insights

✅ Same question, different prompt = different answer  
✅ Prompt engineering affects response quality  
✅ Tone and expertise come from the system prompt  
✅ Experiment to find the best prompt for your use case

## Next Exercise

→ Go to `../02_conversation_memory/` to start Exercise 2!

