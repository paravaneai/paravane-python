#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Client entrypoint for the Paravane SDK.
"""

from __future__ import annotations

import os
from typing import Optional

import requests

from paravane.errors import ConfigurationError
from paravane.http import HTTPClient
from paravane.smtprs import SmtpRsResource


class ParavaneClient:
    """
    Client for Paravane APIs.

    Parameters can be supplied directly or through environment variables:
    ``PARAVANE_API_KEY`` and ``PARAVANE_BASE_URL``.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = 15.0,
        max_network_retries: int = 0,
        session: Optional[requests.Session] = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("PARAVANE_API_KEY")
        if not resolved_api_key:
            raise ConfigurationError(
                "Missing Paravane API key. Pass api_key=... or set PARAVANE_API_KEY."
            )
        resolved_base_url = base_url or os.getenv("PARAVANE_BASE_URL") or "https://api.paravane.io"
        self.api_key = resolved_api_key
        self.base_url = resolved_base_url.rstrip("/")
        self.timeout = timeout
        self.max_network_retries = max_network_retries
        self._http = HTTPClient(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_network_retries=max_network_retries,
            session=session,
        )
        self.smtprs = SmtpRsResource(self._http)
