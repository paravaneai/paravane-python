#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""Basic smtpRS analyse example.

Run with:
    PARAVANE_API_KEY=pvn_live_... python examples/basic_analyze.py
"""

from paravane import ParavaneClient

client = ParavaneClient()
result = client.smtprs.analyze("person@example.com")
print("decision:", result.decision)
print("risk:", result.overall_risk)
print("credits:", result.credits_charged or result.credit_cost)
