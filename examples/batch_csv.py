#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Analyze email addresses from a CSV file with an `email` column.
"""

import csv
import sys

from paravane import ParavaneClient


def main(path: str) -> None:
    client = ParavaneClient()
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            email = row["email"]
            result = client.smtprs.analyze(email, profile="quick")
            print(email, result.decision, result.overall_risk)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python examples/batch_csv.py contacts.csv")
    main(sys.argv[1])
