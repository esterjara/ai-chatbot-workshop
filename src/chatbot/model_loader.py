from typing import Any
import logging
import os

_logger = logging.getLogger(__name__)


def load_model(model_path: str, device: str = "cpu", **kwargs) -> Any:
    """Load a local GGUF model via `llama-cpp-python`.

    This function requires a valid local model file at `model_path`.
    If the file does not exist or `llama-cpp-python` cannot be imported, a clear
    exception with remediation steps is raised.
    """
    if not model_path or not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at '{model_path}'.\n"
            "Place a GGUF model in the `models/` folder or run `scripts/download_model.py`.\n"
            "See README.md for instructions and examples."
        )

    try:
        from llama_cpp import Llama
    except Exception as e:
        raise ImportError(
            "`llama-cpp-python` is required to load local GGUF models but could not be imported.\n"
            "Install it with `pip install llama-cpp-python` and ensure your environment supports it.\n"
            "Alternatively, use a different backend and adapt `src/chatbot/model_loader.py`."
        ) from e

    _logger.info("Loading model via llama_cpp: %s", model_path)
    model = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=0, verbose=False)
    return model


def generate_text(model: Any, prompt: str, max_tokens: int = 256, temperature: float = 0.7, **kwargs) -> str:
    """Generate text from a prompt using the loaded model.
    
    Args:
        model: The loaded Llama model
        prompt: The input prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = more random)
        **kwargs: Additional generation parameters
        
    Returns:
        Generated text as a string
    """
    try:
        output = model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n"],
            echo=False,
            **kwargs
        )
        
        # Extract text from the response
        if isinstance(output, dict) and "choices" in output:
            return output["choices"][0]["text"].strip()
        return str(output).strip()
        
    except Exception as e:
        _logger.error(f"Text generation failed: {e}")
        raise
