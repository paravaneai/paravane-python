#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Low-level HTTP transport for Paravane API requests.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Mapping, Optional

import requests

from paravane._version import __version__
from paravane.errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    PermissionDeniedError,
    QuotaExceededError,
    RateLimitError,
    ValidationError,
)


class HTTPClient:
    """
    Small requests-based HTTP client used by resource classes.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout: float,
        max_network_retries: int,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_network_retries = max(0, int(max_network_retries))
        self.session = session or requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"paravane-python/{__version__}",
            "X-API-Key": self.api_key,
        }
        if idempotency_key:
            request_headers["Idempotency-Key"] = idempotency_key
        if headers:
            request_headers.update(headers)

        attempt = 0
        while True:
            try:
                response = self.session.request(
                    method,
                    url,
                    json=dict(json_body) if json_body is not None else None,
                    params=dict(params) if params is not None else None,
                    headers=request_headers,
                    timeout=self.timeout if timeout is None else timeout,
                )
            except requests.RequestException as exc:
                if not self._can_retry(method, idempotency_key, attempt):
                    raise APIConnectionError(f"Could not connect to Paravane API: {exc}") from exc
                self._sleep_before_retry(attempt)
                attempt += 1
                continue
            if response.status_code < 400:
                return self._decode_response(response)
            error = self._build_api_error(response)
            if self._should_retry(method, response.status_code, idempotency_key, attempt):
                self._sleep_before_retry(attempt)
                attempt += 1
                continue
            raise error

    def _decode_response(self, response: requests.Response) -> Dict[str, Any]:
        if not response.content:
            return {}
        try:
            payload = response.json()
        except ValueError as exc:
            raise APIError(
                "Paravane API returned a non-JSON response.",
                status_code=response.status_code,
                request_id=response.headers.get("X-Request-Id"),
            ) from exc
        if not isinstance(payload, dict):
            return {"data": payload}
        return payload

    def _build_api_error(self, response: requests.Response) -> APIError:
        request_id = response.headers.get("X-Request-Id")
        payload: Dict[str, Any]
        try:
            decoded = response.json()
            payload = decoded if isinstance(decoded, dict) else {"error": decoded}
        except (ValueError, json.JSONDecodeError):
            payload = {"error": response.text}
        code = self._extract_code(payload)
        message = self._extract_message(payload)
        error_cls = self._error_class(response.status_code, code, message)
        return error_cls(
            message,
            status_code=response.status_code,
            code=code,
            response=payload,
            request_id=request_id,
        )

    def _extract_code(self, payload: Mapping[str, Any]) -> Optional[str]:
        detail = payload.get("detail")
        if isinstance(detail, Mapping):
            code = detail.get("error") or detail.get("code") or detail.get("type")
            if isinstance(code, str) and code:
                return code
        error = payload.get("error")
        if isinstance(error, dict):
            code = error.get("code") or error.get("type")
            return str(code) if code else None
        code = payload.get("code")
        return str(code) if code else None

    def _extract_message(self, payload: Mapping[str, Any]) -> str:
        detail = payload.get("detail")
        if isinstance(detail, Mapping):
            message = detail.get("message") or detail.get("detail")
            if message:
                return str(message)
            error = detail.get("error")
            if isinstance(error, str) and error:
                return error
        error = payload.get("error")
        if isinstance(error, dict):
            message = error.get("message") or error.get("detail")
            if message:
                return str(message)
        if isinstance(error, str) and error:
            return error
        for key in ("message", "detail"):
            if payload.get(key):
                return str(payload[key])
        return "Paravane API request failed."

    def _error_class(self, status_code: int, code: Optional[str], message: str):
        folded = f"{code or ''} {message}".lower()
        if status_code == 400 or status_code == 422:
            return ValidationError
        if status_code == 401:
            return AuthenticationError
        if status_code == 403:
            return PermissionDeniedError
        if status_code == 402 or "quota" in folded or "credit_limit" in folded:
            return QuotaExceededError
        if status_code == 429:
            return RateLimitError
        return APIError

    def _can_retry(self, method: str, idempotency_key: Optional[str], attempt: int) -> bool:
        if attempt >= self.max_network_retries:
            return False
        return method.upper() not in {"POST", "PATCH"} or bool(idempotency_key)

    def _should_retry(
        self,
        method: str,
        status_code: int,
        idempotency_key: Optional[str],
        attempt: int,
    ) -> bool:
        return self._can_retry(method, idempotency_key, attempt) and (
            status_code == 429 or status_code >= 500
        )

    def _sleep_before_retry(self, attempt: int) -> None:
        time.sleep(min(0.5 * (2**attempt), 2.0))
