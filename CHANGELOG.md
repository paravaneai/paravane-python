# Changelog

All notable changes to the Paravane Python SDK are documented here.

## [1.0.2] - 2026-08-19

- Align package and runtime versions at `1.0.2`.
- Support Python 3.10 through 3.13 and require a security-current `requests` release.
- Add typed smtpRS organization, documentary-association, and logo response metadata.
- Preserve layer output, usage event IDs, and idempotency replay status in typed analyses.
- Prevent automatic retries of billable POST requests without an idempotency key.
- Remove the internal-only tenant override from the public analysis interface.
- Add production PyPI Trusted Publishing and refresh release documentation.

[1.0.2]: https://github.com/paravaneai/paravane-python/releases/tag/v1.0.2
