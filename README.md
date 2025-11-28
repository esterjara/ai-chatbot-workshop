# From Zero to Chatbot: Create Your Own Chatbot with Python

This repository demonstrates the step-by-step development of a local AI chatbot using Python and compact open-source language models. It includes environment setup, model loading, structured interaction loops, and prompt design, along with a rolling memory component to maintain coherent multi-turn conversations.

The repository also illustrates agentic behavior through modular agents and tool-based orchestration, enabling autonomous decision-making and task handling. By exploring these components, it provides a clear, practical blueprint for building a fully functional, maintainable chatbot with local AI models, highlighting key design patterns and trade-offs in real-world deployments.

## Overview of Capabilities

1. **Environment & Provisioning**
   - Create reproducible Python environments with Poetry
   - Manage dependencies and provision compact GGUF models
   - Understand hardware and performance trade-offs (CPU vs GPU)

2. **Local Model Engineering**
   - Load and run compact GGUF models via `llama-cpp-python`
   - Troubleshoot common errors and wire stable inference loops
   - Optimize model parameters for your hardware

3. **Prompt Engineering & Templating**
   - Design effective system prompts and few-shot examples
   - Control temperature and decoding parameters
   - Reduce hallucinations through prompt techniques

4. **Conversation State & Memory**
   - Implement rolling windows for conversation history
   - Build conversation summarization strategies
   - Maintain coherence across long multi-turn dialogues

5. **Agentic Systems & Tools**
   - Design agents that decide when to call tools
   - Structure tool interfaces safely
   - Integrate calculator and custom tools
   - Build multi-agent systems with intent classification

6. **Packaging & Reproducibility**
   - Structure projects for easy replication
   - Use Poetry for dependency management
   - Share and deploy your chatbot

## Workshop Exercises

The workshop is organized into progressive exercises:

### Exercise 1: Basic Chatbot (01_basic_chatbot/)
- **1a**: Build a simple single-turn chatbot
- **1b**: Understand system prompts and prompt engineering
- Learn model loading and basic interaction patterns

### Exercise 2: Conversation Memory (02_conversation_memory/)
- **2a**: See the problem - chatbot without memory
- **2b**: Implement conversation history with rolling memory
- **2c**: Explore different memory strategies
- **2d**: Build conversation summarization for long dialogues

### Exercise 3: Agents and Tools (03_agents_and_tools/)
- **3a**: Build a multi-agentic system with intent classification
- **3b**: Implement tool calling and orchestration
- Create agents that decide when to use tools
- Add custom tools (calculator, etc.)

## Quick Start Examples

**⚠️ IMPORTANT**: You must complete the full setup process in the [Getting Started](#getting-started) section below before running any of these exercises. This includes installing Poetry, installing dependencies, and downloading a model.

After completing the setup, try these examples:

```bash
# Exercise 0a: Python check
poetry run python exercises/00_environment_setupw/0a_python_check.py

# Exercise 0b: Poetry installation
poetry run python exercises/00_environment_setup/0b_poetry_install.py

# Exercise 0c: Dependencies
poetry run python exercises/00_environment_setup/0c_dependencies.py

# Exercise 0d: Download LLM model
poetry run python exercises/00_environment_setup/0d_download_model.py

# Exercise 1a: Basic chatbot
poetry run python exercises/01_basic_chatbot/1a_basic_chatbot.py

# Exercise 1b: System prompts
poetry run python exercises/01_basic_chatbot/1b_system_prompt.py

# Exercise 2a: Chatbot without memory
poetry run python exercises/02_conversation_memory/2a_no_memory.py

# Exercise 2b: Chatbot with memory
poetry run python exercises/02_conversation_memory/2b_memory.py

# Exercise 2c: Memory strategies
poetry run python exercises/02_conversation_memory/2c_memory_strategies.py

# Exercise 2d: Summarization memory (OPTIONAL)
poetry run python exercises/02_conversation_memory/2d_summarize_memory.py

# Exercise 3a: Multi-agentic system
poetry run python exercises/03_agents_and_tools/3a_multi_agentic_system.py

# Exercise 3b: Tools and orchestration
poetry run python exercises/03_agents_and_tools/3b_tools_and_orchestration.py
```

## Dependencies

This project uses the following main dependencies (all managed through Poetry):

- **llama-cpp-python**: Python bindings for llama.cpp, enabling local inference of GGUF models
- **python-dotenv**: Load environment variables from `.env` files
- **requests**: HTTP library used by the model download script
- **huggingface-hub**: Download models from Hugging Face repositories

Development dependencies:
- **pytest**: Testing framework

All dependencies are automatically installed when you run `poetry install`. See `pyproject.toml` for the complete dependency list.

## Workshop Outline

**Total Duration**: ~2 hours

1. **Environment Setup** (15-20 minutes)
   - Python and Poetry installation
   - Model provisioning (download GGUF model)
   - Environment configuration

2. **Prompt Design & Single-Turn Inference** (20 minutes)
   - Basic chatbot structure (Exercise 1a)
   - System prompts and prompt engineering (Exercise 1b)
   - Model parameters and configuration

3. **Conversation Memory** (30 minutes)
   - Understanding the problem: no memory (Exercise 2a)
   - Implementing rolling memory (Exercise 2b)
   - Memory strategies: window vs. buffer (Exercise 2c)
   - Summarization techniques (Exercise 2d)

4. **Agentic Systems & Tools** (30 minutes)
   - Intent classification and routing (Exercise 3a)
   - Tool definition and calling patterns (Exercise 3b)
   - Multi-agent orchestration
   - Tool selection with LLMs

5. **Q&A and Next Steps** (15-20 minutes)
   - Troubleshooting
   - Next steps and extensions

## Troubleshooting

### Model Loading Issues
- Ensure `MODEL_PATH` in `.env` points to a valid GGUF file
- Check that the model file exists in the `models/` directory
- Verify you have enough RAM for the model size

### llama-cpp-python Installation
- If installation fails, try: `pip install llama-cpp-python --no-cache-dir`
- For GPU support, see: https://github.com/abetlen/llama-cpp-python#installation

### Poetry Issues
- Update Poetry: `pip install --upgrade poetry`
- Clear cache: `poetry cache clear --all pypi`
- Reinstall: `poetry install --no-cache`

## Additional Resources

- [llama-cpp-python Documentation](https://github.com/abetlen/llama-cpp-python)
- [Hugging Face GGUF Models](https://huggingface.co/models?library=gguf)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## License

MIT License - See LICENSE file for details.

Repository layout
-----------------

## Repository Structure

```
ai-chatbot-workshop/
├── src/chatbot/              # Core library code
│   ├── chatbot.py           # Basic chatbot implementation
│   ├── memory.py            # Conversation memory management
│   ├── model_loader.py      # Model loading utilities
│   ├── text_generator.py    # Text generation functions
│   ├── chat_utils.py        # Shared chat interface utilities
│   ├── agent.py             # Agent and orchestration
│   ├── intent_classifier.py # Intent classification
│   ├── tool.py              # Tool definitions
│   └── prompts.py           # Centralized prompt templates
│
├── exercises/               # Workshop exercises
│   ├── 00_environment_setup/   # Environment set up
│   │   ├── 0a_python_check.py
│   │   ├── 0b_poetry_install.py
│   │   ├── 0c_dependencies.py
│   │   └── 0d_download_model.py
│   ├── 01_basic_chatbot/   # Introduction to chatbots
│   │   ├── solutions/
│   │   ├── 1a_basic_chatbot.py
│   │   └── 1b_system_prompt.py
│   ├── 02_conversation_memory/  # Memory strategies
│   │   ├── solutions/
│   │   ├── 2a_no_memory.py
│   │   ├── 2b_memory.py
│   │   ├── 2c_memory_strategies.py
│   │   └── 2d_summarize_memory.py
│   └── 03_agents_and_tools/     # Agentic systems
│       ├── solutions/
│       ├── 3a_multi_agentic_system.py
│       ├── 3b_tools_and_orchestration.py
│       └── tools.py
│
│
├── scripts/                 # Utility scripts
│   └── download_model.py   # Model download helper
│
├── models/                  # GGUF models (gitignored)
├── pyproject.toml          # Poetry dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## What You'll Learn## Prerequisites

- **Python**: Version 3.10 or higher (3.12 recommended)
- **Operating System**: Linux, macOS, or Windows
- **Disk Space**: 2-5 GB for models and dependencies
- **Memory**: Minimum 8 GB RAM (16 GB recommended for larger models)
- **Python Knowledge**: Basic familiarity with Python (no ML experience required)
- **Package Manager**: Poetry (will be installed in setup steps)

## Getting Started

**Complete these steps in order before running any exercises:**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-chatbot-workshop
```

### 2. Set Up Python Environment

Ensure you have Python 3.9 or higher installed:

```bash
python --version  # Should show Python 3.9 or higher
```

If using `pyenv`, set the Python version:

```bash
pyenv global 3.12.7  # Or your preferred 3.9+ version
```

### 3. Install Poetry

Poetry is a dependency management tool for Python. Install it globally:

```bash
pip install poetry
```

Verify the installation:

```bash
poetry --version
```

### 4. Install Project Dependencies

Install all required Python packages for the workshop:

```bash
poetry install
```

This command will:
- Create a virtual environment for the project
- Install all dependencies listed in `pyproject.toml`:
  - `llama-cpp-python` - For running GGUF models locally
  - `python-dotenv` - For environment configuration
  - `requests` - For downloading models
  - `huggingface-hub` - For accessing Hugging Face models
  - `pytest` - For testing (dev dependency)

**Note**: Installing `llama-cpp-python` may take a few minutes as it compiles llama.cpp bindings.

### 5. Understanding GGUF Models

**What is GGUF?**

GGUF (GPT-Generated Unified Format) is a file format designed for storing and running large language models efficiently on consumer hardware. Key benefits:

- **Compact**: Models are quantized (compressed) to use less memory
- **Fast**: Optimized for CPU inference without requiring a GPU
- **Portable**: Single-file format that's easy to download and share
- **Flexible**: Supports various quantization levels (Q4, Q5, Q8, etc.)

**Quantization levels explained:**
- **Q4_K_M** (4-bit): Smallest size, fastest, slight quality reduction (~638MB for TinyLlama)
- **Q5_K_M** (5-bit): Balanced size and quality
- **Q8_0** (8-bit): Larger size, better quality, closer to original model

For this workshop, we use 4-bit quantized models for optimal performance on standard laptops.

### 6. Download a GGUF Model

You need a GGUF model file to run the chatbot exercises. 

**Workshop Default: TinyLlama (REQUIRED)**

For this workshop, we use **TinyLlama-1.1B** because it:
- Downloads quickly (~638MB)
- Runs fast on CPU-only machines
- Requires minimal RAM (4-8GB)
- Works well for learning chatbot concepts

Download TinyLlama now:

```bash
poetry run python scripts/download_model.py \
  --hf "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF" \
  --filename "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" \
  --out models/tinyllama.gguf
```

This will download the model to `models/tinyllama.gguf` (created automatically).

**Alternative Models (Optional)**

If you have more resources available, you can try larger models:

**Option B - Download Other Models from Hugging Face:**

```bash
# Example: Phi-3-mini (better quality, requires ~4GB RAM)
poetry run python scripts/download_model.py \
  --hf "microsoft/Phi-3-mini-4k-instruct-gguf" \
  --filename "Phi-3-mini-4k-instruct-q4.gguf" \
  --out models/phi3.gguf

# Example: Mistral-7B (high quality, requires ~8GB RAM)
poetry run python scripts/download_model.py \
  --hf "TheBloke/Mistral-7B-Instruct-v0.2-GGUF" \
  --filename "mistral-7b-instruct-v0.2.Q4_K_M.gguf" \
  --out models/mistral.gguf
```

**Option C - Download from Direct URL:**

```bash
poetry run python scripts/download_model.py \
  --url "<direct-download-url>" \
  --out models/model.gguf
```

**Option D - Manual Download:**
1. Visit [Hugging Face GGUF Models](https://huggingface.co/models?library=gguf)
2. Find and download a GGUF model file
3. Place it in the `models/` directory
4. Update `MODEL_PATH` in your `.env` file

**Recommended Models:**
- **TinyLlama-1.1B** (~638MB) - Lightweight, fast, ideal for learning
- **Phi-3-mini** (~2.3GB) - Better quality, still compact
- **Mistral-7B** (~4GB) - High quality, requires more resources

### 5. Install Dependencies

Install all project dependencies using Poetry:

```bash
poetry install
```

This will:
- Create a virtual environment
- Install all required packages (llama-cpp-python, python-dotenv, requests, huggingface-hub)
- Install development dependencies (pytest)


### 7. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure your model path:

```bash
# .env file
MODEL_PATH=./models/tinyllama.gguf  # Path to your downloaded model
MODEL_DEVICE=cpu                     # Use 'cpu' (or 'gpu' if available)
MAX_TOKENS=512                       # Maximum tokens to generate
```

**Important**: Make sure `MODEL_PATH` points to the model you downloaded in step 6.

### 8. Verify Installation

Test that everything is set up correctly:

```bash
# Run the basic chatbot exercise
poetry run python exercises/01_basic_chatbot/1a_basic_chatbot.py
```

Expected output:
```
Chatbot initialized
System prompt: You are a helpful assistant.
Max tokens: 256
Type 'exit' to quit.

You: 
```

**Success!** If you see this prompt, your setup is complete. You can:
- Type a message to test the chatbot
- Type `exit` to quit
- Proceed to the workshop exercises
