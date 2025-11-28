"""
Model Loader Module

This module handles loading LLM models from local GGUF files using `llama-cpp-python`.
"""

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


def load_embedding_model(model_path: str, **kwargs) -> Any:
    """Load a local GGUF model for embeddings via `llama-cpp-python`.
    
    This function loads a model specifically configured for generating embeddings.
    It sets embedding=True to enable the embed() method on the model.
    
    Args:
        model_path: Path to the GGUF model file
        **kwargs: Additional Llama initialization parameters
        
    Returns:
        A Llama model instance configured for embeddings
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

    _logger.info("Loading embedding model via llama_cpp: %s", model_path)
    model = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=0, verbose=False, embedding=True)
    return model

