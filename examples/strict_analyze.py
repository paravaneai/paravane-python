#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Request a stricter smtpRS analysis profile.
"""

from paravane import ParavaneClient

client = ParavaneClient(max_network_retries=1)
result = client.smtprs.analyze(
    "person@example.com",
    profile="deep",
    idempotency_key="example-strict-analysis-001",
)
print(result.to_dict())
