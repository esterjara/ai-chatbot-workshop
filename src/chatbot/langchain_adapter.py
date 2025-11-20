"""Optional LangChain adapter.

Provides a thin `LocalLLM` wrapper so LangChain can use the local model (or fallback).
The adapter is optional: all imports are guarded so the module degrades gracefully when
`langchain` is not installed.
"""
from typing import Optional, List, Mapping, Any


try:
    from langchain.llms.base import LLM
    from langchain.schema import LLMResult, Generation
except Exception:  # pragma: no cover - optional dependency
    LLM = None


class LocalLLM:
    """A minimal LangChain compatible LLM wrapper around the Chatbot instance.

    This class only loads if `langchain` is available at import time. If you want to
    keep `langchain` optional, import this module inside your example script and handle
    the ImportError or check whether `LLM` is None.
    """

    def __init__(self, chatbot):
        self.chatbot = chatbot

    @property
    def _llm_type(self) -> str:
        return "local"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Use the chatbot's model or fallback to the simple generator
        # Many LLM classes expect a text->text call. We keep it simple here.
        return self.chatbot.generate_response(prompt)

    # For LangChain compatibility; not strictly necessary for all versions
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"type": "LocalLLM"}
*** End Patch