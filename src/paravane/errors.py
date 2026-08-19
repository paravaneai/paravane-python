#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Exception hierarchy for the Paravane SDK.
"""

from typing import Any, Dict, Optional


class ParavaneError(Exception):
    """
    Base class for all SDK errors.
    """


class ConfigurationError(ParavaneError):
    """
    Raised when the client is missing required configuration.
    """


class APIConnectionError(ParavaneError):
    """
    Raised when the SDK cannot reach the API.
    """


class APIError(ParavaneError):
    """
    Raised when the API returns an unsuccessful response.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        response: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.response = response
        self.request_id = request_id

    def __str__(self) -> str:
        details = []
        if self.status_code:
            details.append(f"status_code={self.status_code}")
        if self.code:
            details.append(f"code={self.code}")
        if self.request_id:
            details.append(f"request_id={self.request_id}")
        if not details:
            return self.message
        return f"{self.message} ({', '.join(details)})"


class AuthenticationError(APIError):
    """
    Raised when an API key is missing or invalid.
    """


class PermissionDeniedError(APIError):
    """
    Raised when the API key does not have access to a resource.
    """


class ValidationError(APIError):
    """
    Raised when request validation fails.
    """


class QuotaExceededError(APIError):
    """
    Raised when a workspace has exhausted its plan quota.
    """


class RateLimitError(APIError):
    """
    Raised when the API rate limit is exceeded.
    """
