#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
import pytest

from paravane import ConfigurationError, ParavaneClient


def test_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("PARAVANE_API_KEY", raising=False)
    with pytest.raises(ConfigurationError):
        ParavaneClient()


def test_client_reads_api_key_from_environment(monkeypatch):
    monkeypatch.setenv("PARAVANE_API_KEY", "pvn_test_key")
    client = ParavaneClient(base_url="https://example.test")
    assert client.api_key == "pvn_test_key"
    assert client.base_url == "https://example.test"


def test_explicit_api_key_wins_over_environment(monkeypatch):
    monkeypatch.setenv("PARAVANE_API_KEY", "pvn_env_key")
    client = ParavaneClient(api_key="pvn_arg_key")
    assert client.api_key == "pvn_arg_key"
