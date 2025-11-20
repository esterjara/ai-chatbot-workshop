from .config import load_config
from .memory import RollingMemory
from .model_loader import load_model
from .agent import Agent
from src.utils.logging_utils import setup_logger
from src.utils.prompts import DEFAULT_SYSTEM_PROMPT
from typing import Any

import logging

_logger = logging.getLogger(__name__)


class Chatbot:
    def __init__(self, config=None, model=None, memory: RollingMemory | None = None, agent: Agent | None = None):
        self.config = config or load_config()
        self.memory = memory or RollingMemory()
        self.agent = agent or Agent()
        self.model = model
        if self.model is None:
            try:
                self.model = load_model(self.config.model_path, device=self.config.device)
            except Exception as e:
                # Fail fast: require a local model for this workshop setup.
                raise RuntimeError(
                    f"Failed to load model: {e}\n"
                    "Please place a GGUF model in `models/` and set `MODEL_PATH` in a `.env` file, "
                    "or run `python scripts/download_model.py --hf <repo_id> --out models/your-model.gguf`. "
                    "See README.md for details."
                )

    def build_prompt(self, user_input: str) -> str:
        history = self.memory.get()
        parts = [DEFAULT_SYSTEM_PROMPT, "\n"]
        for role, text in history:
            parts.append(f"{role}: {text}")
        parts.append(f"user: {user_input}")
        return "\n".join(parts)

    def generate_response(self, user_input: str) -> str:
        prompt = self.build_prompt(user_input)
        # At this point, a valid model is expected. If generation fails, an error
        # will be returned to the caller.

        # llama-cpp-python usage: model.create(...) or model.generate depending on version
        try:
            output = self.model.create(prompt=prompt, max_tokens=self.config.max_tokens)
            # Try to extract text from possible response structures
            if isinstance(output, dict) and "choices" in output:
                return output["choices"][0]["text"].strip()
            if hasattr(output, "generations"):
                return str(output.generations[0].text).strip()
            return str(output).strip()
        except Exception:
            try:
                # try `generate` fallback
                out = self.model.generate(prompt)
                return str(out)
            except Exception as e:
                _logger.exception("Model generation failed: %s", e)
                raise RuntimeError(f"Model generation failed: {e}")

    def chat_once(self, user_input: str) -> str:
        # Agent decision (optional)
        action = self.agent.decide_action(user_input)
        if action["type"] == "tool":
            reply = self.agent.act(action)
        else:
            reply = self.generate_response(user_input)

        self.memory.add("user", user_input)
        self.memory.add("assistant", reply)
        return reply

    def run_console(self) -> None:
        setup_logger()
        print("Starting console chat. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            reply = self.chat_once(user_input)
            print("Bot:", reply)
