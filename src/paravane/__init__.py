#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Python SDK for the Paravane API.
"""

from paravane._version import __version__
from paravane.client import ParavaneClient
from paravane.errors import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    ConfigurationError,
    ParavaneError,
    PermissionDeniedError,
    QuotaExceededError,
    RateLimitError,
    ValidationError,
)
from paravane.types import (
    AnalysisProfile,
    CompanyValidityBeta,
    DocumentaryAssociation,
    DomainSignal,
    OrganizationLogo,
    OrganizationPresentation,
    SmtpRsAnalysis,
)

__all__ = [
    "APIConnectionError",
    "APIError",
    "AnalysisProfile",
    "AuthenticationError",
    "ConfigurationError",
    "CompanyValidityBeta",
    "DocumentaryAssociation",
    "DomainSignal",
    "OrganizationLogo",
    "OrganizationPresentation",
    "ParavaneClient",
    "ParavaneError",
    "PermissionDeniedError",
    "QuotaExceededError",
    "RateLimitError",
    "SmtpRsAnalysis",
    "ValidationError",
    "__version__",
]
