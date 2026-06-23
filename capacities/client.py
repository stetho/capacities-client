from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.capacities.io"


class CapacitiesError(Exception):
    """Base exception for Capacities API errors."""
    pass


class AuthenticationError(CapacitiesError):
    """Raised when the API token is missing or invalid."""
    pass


class RateLimitError(CapacitiesError):
    """Raised when the API rate limit is exceeded."""
    pass


class CapacitiesClient:
    def __init__(self, token: str | None = None):
        resolved_token = token or os.getenv("CAPACITIES_API_TOKEN")
        if not resolved_token:
            raise AuthenticationError(
                "No API token provided. Pass token= or set CAPACITIES_API_TOKEN."
            )
        self._token = resolved_token
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._http.get(path, params=params)
        self._raise_for_status(response)
        return response.json()

    def _post(self, path: str, body: dict[str, Any]) -> Any:
        response = self._http.post(path, json=body)
        self._raise_for_status(response)
        return response.json()

    def _raise_for_status(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API token.")
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded. Try again shortly.")
        if response.status_code >= 400:
            raise CapacitiesError(
                f"API error {response.status_code}: {response.text}"
            )

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
