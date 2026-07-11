"""Environment configuration for local and hosted execution."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded once when the application starts."""

    provider: str = os.getenv("MODEL_PROVIDER", "dry")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    max_concurrent_requests: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "4"))
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
    input_usd_per_million: float = float(os.getenv("INPUT_USD_PER_MILLION_TOKENS", "0"))
    output_usd_per_million: float = float(
        os.getenv("OUTPUT_USD_PER_MILLION_TOKENS", "0")
    )


settings = Settings()
