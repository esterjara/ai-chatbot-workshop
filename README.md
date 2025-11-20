# ai-chatbot-workshop

This repository is an workshop scaffold focused on engineering practical, local AI chat systems. It emphasizes clear, reproducible patterns for deploying compact language models locally, composing them with retrieval and tool-based components, and building maintainable teaching examples. The goal is not only to demonstrate a running chatbot, but to expose trade-offs and design choices you will encounter when moving from prototype to production-ready local deployments.

What you'll learn
-----------------

- Environment & provisioning: create reproducible Python environments, manage dependencies, and provision compact GGUF models for local inference. Learn hardware and performance trade-offs for CPU vs GPU/accelerator setups.
- Local model engineering: how to load and run compact GGUF models (via `llama-cpp-python`), troubleshoot common errors, and wire a stable inference loop.
- Prompt engineering & templating: system prompts, few-shot examples, prompt templates, temperature and decoding controls, and techniques for reducing hallucinations.
- Conversation state & memory: rolling windows, conversation summarization, and approaches for maintaining coherence across long multi-turn dialogues.
- Retrieval-Augmented Generation (RAG): build an embedding-based retriever, index documents with FAISS, and augment prompts with retrieved context to improve factuality.
- Agentic systems & tools: design simple agents that decide when to call tools (search, calculator, web fetch), structure tool interfaces safely, and integrate with orchestration libraries (e.g., LangChain) when desired.
- Evaluation & iteration: simple metrics and human-in-the-loop methods to evaluate responses, measure latency/throughput, and iterate on prompts and memory strategies.
- Packaging & reproducibility: patterns for scripts, notebooks, and download helpers so workshop participants can replicate results easily.

Repository layout
-----------------

- `src/` : Core library code for loading models, memory, RAG and a simple agent.
- `examples/` : Scripts showing increasing complexity: `basic_chat.py`, `memory_chat.py`, `agentic_chat.py`, `rag_chat.py`.
 - `examples/` : Scripts showing increasing complexity: `basic_chat.py`, `memory_chat.py`, `agentic_chat.py`, `rag_chat.py`, and an optional `agentic_langchain.py` that demonstrates integration with LangChain.
- `notebooks/` : Jupyter notebooks for guided experiments.
- `models/` : Suggested location for GGUF model files (ignored by git).
- `exercises/` : Exercise folders to extend workshop tasks.

Prerequisites
-------------

- No prior ML experience required; basic Python familiarity is enough.
- Recommended: Python 3.9+ (3.10+ preferred).
- Disk space: downloading a model requires a few hundred MB to multiple GB depending on model size.

Installation (Windows PowerShell)
--------------------------------

Create and activate a virtual environment, then install the runtime dependencies listed in `requirements.txt`:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```

Notes on dependencies
---------------------

- `llama-cpp-python` (optional): enables inference using a GGUF model via the llama.cpp backend.
- `sentence-transformers` and `faiss-cpu` (optional): used for RAG. The code includes a simple fallback retriever if these are not installed.
- `langchain` and `pydantic` (optional, recommended): popular libraries for building agentic systems and structured pipelines. Install them to run `examples/agentic_langchain.py` and to use more advanced agent/RAG patterns.

Model provisioning
------------------

Two options to provide a model for local runs:

1. Manual: download a GGUF model and place it in `models/`, then set `MODEL_PATH` in a `.env` file (see `.env.example`).

2. Helper script: use `scripts\download_model.py` to download a model from a direct URL (if you have a link) or from Hugging Face (requires `huggingface_hub` and an access token). The helper is optional and documented in the script.


Model requirement
-----------------

This workshop expects a local GGUF model file to be available in `models/`.

You can provide a model in two ways:

1. Manual: download a GGUF model and place it in `models/` and then set `MODEL_PATH` in a `.env` file (see `.env.example`).

2. Helper script: use the included `scripts\download_model.py` to download a model from a direct URL or from Hugging Face (requires `huggingface-hub` and an access token). Example:

```powershell
python scripts\download_model.py --hf <huggingface-repo-id> --out models\your-model.gguf
```

Quick examples
--------------

Run the basic example (requires a local model):

```powershell
python examples\basic_chat.py
```

Try memory-enabled conversation:

```powershell
python examples\memory_chat.py
```

Agentic behaviour (simple tool calls):

```powershell
python examples\agentic_chat.py
```

RAG example: the retriever will try to use `sentence-transformers` if installed, otherwise it falls back to a simple keyword match.

```powershell
python examples\rag_chat.py
```

Workshop outline
----------------

1. Environment and model provisioning (15–20 minutes).
2. Prompt design and single-turn inference (15 minutes).
3. Rolling memory for multi-turn coherence (20 minutes).
4. Agentic behaviour: simple tools and decision logic (20 minutes).
5. RAG: building a retriever and augmenting prompts (25 minutes).

Exercises
---------

- `01_extend_memory`: add summarization or vector-indexed memory.
- `02_add_tools`: add real tools (web search, calculator) and secure execution.
- `03_custom_prompting`: create and compare multiple system prompts.

If you want, I can automatically add a small demo model download (if you provide a permissibly-hosted URL) or wire up a specific Hugging Face model name and include exact commands to fetch it.

License
-------

This project uses the repository-level license.
