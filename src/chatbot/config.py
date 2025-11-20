import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    model_path: str
    device: str = "cpu"
    max_tokens: int = 512


def load_config() -> Config:
    model_path = os.getenv("MODEL_PATH", "./models/your-model.gguf")
    device = os.getenv("MODEL_DEVICE", "cpu")
    max_tokens = int(os.getenv("MAX_TOKENS", "512"))
    return Config(model_path=model_path, device=device, max_tokens=max_tokens)
