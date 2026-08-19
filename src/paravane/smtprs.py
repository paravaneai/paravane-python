#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
smtpRS resource helpers.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from paravane.http import HTTPClient
from paravane.types import AnalysisProfile, SmtpRsAnalysis


class SmtpRsResource:
    """
    Access smtpRS email risk intelligence endpoints.
    """

    def __init__(self, http_client: HTTPClient) -> None:
        self._http = http_client

    def analyze(
        self,
        email: str,
        *,
        profile: Optional[AnalysisProfile] = None,
        disposable_only: Optional[bool] = None,
        strict_disposable: Optional[bool] = None,
        guess: Optional[bool] = None,
        run_catch_all: Optional[bool] = None,
        company_validity_beta: Optional[bool] = None,
        fast: Optional[bool] = None,
        extra_params: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        idempotency_key: Optional[str] = None,
    ) -> SmtpRsAnalysis:
        """
        Analyze one email address with smtpRS.

        ``profile`` selects a complete public analysis mode. The older Boolean
        mode flags remain available for compatibility but are deprecated by the
        API. ``company_validity_beta`` opts an eligible paid request into the
        optional company-domain context.
        Unknown future parameters can be supplied with ``extra_params``.
        """
        params: Dict[str, Any] = {
            "profile": profile,
            "disposable_only": disposable_only,
            "strict_disposable": strict_disposable,
            "guess": guess,
            "run_catch_all": run_catch_all,
            # Keep this absent unless explicitly set so existing callers retain
            # the server's default, scoring-neutral behavior.
            "company_validity_beta": company_validity_beta,
            "fast": fast,
        }
        if extra_params:
            params.update(extra_params)
        clean_params = {key: value for key, value in params.items() if value is not None}
        body: Dict[str, Any] = {"email": email}
        payload = self._http.request(
            "POST",
            "/v1/analyse",
            json_body=body,
            params=clean_params,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
        return SmtpRsAnalysis.from_dict(payload)
