#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT

import pytest
import requests

from paravane import APIConnectionError, APIError, ParavaneClient


class FakeResponse:
    def __init__(self, status_code: int, payload=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.headers = {}
        self.content = b"{}"
        self.text = "{}"

    def json(self):
        return self._payload


class SequenceSession:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def request(self, *args, **kwargs):
        outcome = self.outcomes[self.calls]
        self.calls += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def test_billable_post_is_not_retried_without_idempotency_key():
    session = SequenceSession(
        [requests.ConnectionError("connection lost"), FakeResponse(200, {"decision": "allow"})]
    )
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        max_network_retries=2,
        session=session,
    )

    with pytest.raises(APIConnectionError):
        client.smtprs.analyze("person@example.com")

    assert session.calls == 1


def test_billable_post_is_retried_with_idempotency_key(monkeypatch):
    monkeypatch.setattr("paravane.http.time.sleep", lambda _: None)
    session = SequenceSession(
        [FakeResponse(503, {"error": "temporary"}), FakeResponse(200, {"decision": "allow"})]
    )
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        max_network_retries=2,
        session=session,
    )

    result = client.smtprs.analyze("person@example.com", idempotency_key="signup-123")

    assert result.decision == "allow"
    assert session.calls == 2


def test_billable_post_5xx_is_returned_without_unsafe_retry():
    session = SequenceSession(
        [FakeResponse(503, {"error": "temporary"}), FakeResponse(200, {"decision": "allow"})]
    )
    client = ParavaneClient(
        api_key="pvn_test_key",
        base_url="https://api.example.test",
        max_network_retries=2,
        session=session,
    )

    with pytest.raises(APIError) as exc_info:
        client.smtprs.analyze("person@example.com")

    assert exc_info.value.status_code == 503
    assert session.calls == 1
