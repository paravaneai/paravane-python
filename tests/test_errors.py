#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
import pytest

from paravane import (
    AuthenticationError,
    ParavaneClient,
    PermissionDeniedError,
    QuotaExceededError,
    RateLimitError,
)


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.headers = {"X-Request-Id": "req_123"}
        self.content = b"{}"
        self.text = "{}"

    def json(self):
        return self._payload


class ErrorSession:
    def __init__(self, response):
        self.response = response

    def request(self, *args, **kwargs):
        return self.response


@pytest.mark.parametrize(
    "status_code,payload,error_cls",
    [
        (401, {"detail": "Invalid API key"}, AuthenticationError),
        (429, {"error": {"message": "Too many requests"}}, RateLimitError),
        (402, {"code": "monthly_credit_limit_exceeded"}, QuotaExceededError),
    ],
)
def test_error_mapping(status_code, payload, error_cls):
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=ErrorSession(FakeResponse(status_code, payload)),
    )
    with pytest.raises(error_cls) as exc_info:
        client.smtprs.analyze("person@example.com")
    assert exc_info.value.status_code == status_code
    assert exc_info.value.request_id == "req_123"


def test_fastapi_detail_error_preserves_code_and_message():
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        session=ErrorSession(
            FakeResponse(
                403,
                {
                    "detail": {
                        "error": "feature_not_available",
                        "message": "This analysis profile is not available on the current plan.",
                        "requested_profile": "deep",
                    }
                },
            )
        ),
    )
    with pytest.raises(PermissionDeniedError) as exc_info:
        client.smtprs.analyze("person@example.com", profile="deep")
    assert exc_info.value.code == "feature_not_available"
    assert exc_info.value.message == "This analysis profile is not available on the current plan."
    assert exc_info.value.response == {
        "detail": {
            "error": "feature_not_available",
            "message": "This analysis profile is not available on the current plan.",
            "requested_profile": "deep",
        }
    }
