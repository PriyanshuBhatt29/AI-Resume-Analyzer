import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_name: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "50000"))


settings = Settings()
