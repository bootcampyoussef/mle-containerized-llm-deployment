"""Deterministic and Groq-backed generation providers."""

from typing import Protocol

from openai import AsyncOpenAI

from deployment_service.config import Settings
from deployment_service.models import GenerateRequest, ProviderResult, TokenUsage


class Provider(Protocol):
    """Interface required by the service layer."""

    async def generate(self, request: GenerateRequest) -> ProviderResult: ...


class DryProvider:
    """Stable local provider for tests and deployment checks."""

    def __init__(self, model: str) -> None:
        self.model = model

    async def generate(self, request: GenerateRequest) -> ProviderResult:
        words = request.prompt.split()
        text = f"Dry response: {request.prompt[:120]}"
        return ProviderResult(
            text=text,
            model=self.model,
            usage=TokenUsage(
                input_tokens=max(1, len(words)),
                output_tokens=max(1, len(text.split())),
            ),
        )


class GroqProvider:
    """OpenAI-compatible Groq provider used by the hosted service."""

    def __init__(self, settings: Settings) -> None:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is required when MODEL_PROVIDER=groq")
        self.model = settings.model
        self.client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=settings.request_timeout_seconds,
        )

    async def generate(self, request: GenerateRequest) -> ProviderResult:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        usage = response.usage
        return ProviderResult(
            text=response.choices[0].message.content or "",
            model=self.model,
            usage=TokenUsage(
                input_tokens=usage.prompt_tokens if usage else 0,
                output_tokens=usage.completion_tokens if usage else 0,
            ),
        )


def build_provider(settings: Settings) -> Provider:
    """Select a provider from validated deployment configuration."""
    if settings.provider == "dry":
        return DryProvider(settings.model)
    if settings.provider == "groq":
        return GroqProvider(settings)
    raise ValueError(f"Unsupported MODEL_PROVIDER: {settings.provider}")
