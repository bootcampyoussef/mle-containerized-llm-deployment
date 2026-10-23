"""Environment configuration for local and hosted execution."""

import os
import math
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

    def __post_init__(self) -> None:
        if self.max_concurrent_requests < 1 or self.cache_ttl_seconds < 0:
            raise ValueError("Concurrency must be positive and cache TTL nonnegative")
        if (
            not math.isfinite(self.request_timeout_seconds)
            or self.request_timeout_seconds <= 0
        ):
            raise ValueError("Request timeout must be finite and positive")
        if any(
            not math.isfinite(rate) or rate < 0
            for rate in (self.input_usd_per_million, self.output_usd_per_million)
        ):
            raise ValueError("Token prices must be finite and nonnegative")


settings = Settings()
