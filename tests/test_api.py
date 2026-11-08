"""In-process API contract tests."""

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from deployment_service.app import app, service


async def get(path: str) -> tuple[int, dict[str, object]]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(path)
        return response.status_code, response.json()


async def post(payload: dict[str, object]) -> tuple[int, dict[str, object]]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/generate", json=payload)
        return response.status_code, response.json()


def test_health_and_readiness() -> None:
    assert asyncio.run(get("/health"))[0] == 200
    assert asyncio.run(get("/ready"))[1]["provider"] == "dry"


def test_generate_and_validation() -> None:
    status, body = asyncio.run(post({"prompt": "hello"}))
    assert status == 200
    assert body["model"] == "dry:openai/gpt-oss-20b"
    assert asyncio.run(post({"prompt": ""}))[0] == 422


@pytest.mark.parametrize(
    ("error", "expected_status", "expected_detail"),
    [
        (RuntimeError, 502, "Generation provider unavailable"),
        (TimeoutError, 504, "Generation request timed out"),
    ],
)
def test_provider_errors_do_not_leak_details(
    monkeypatch, error, expected_status, expected_detail
) -> None:
    class FailingProvider:
        async def generate(self, request):
            raise error("secret provider response")

    monkeypatch.setattr(service, "provider", FailingProvider())
    status, body = asyncio.run(post({"prompt": "error-path-check"}))

    assert status == expected_status
    assert body["detail"] == expected_detail
