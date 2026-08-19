<!-- <p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="doc/images/readme/paravane-smtprs-sdk-readme-banner-logo-updated-orange-dark-developer-api-yellow.png" />
    <source
      media="(prefers-color-scheme: light)"
      srcset="doc/images/readme/paravane-smtprs-sdk-readme-banner-logo-updated-orange-dark-developer-api-white.png" />
    <img
      src="doc/images/readme/paravane-smtprs-sdk-readme-banner-logo-updated-orange-dark-developer-api-yellow.png"
      alt="Paravane" />
  </picture>
</p> -->

<p align="center">
  <img
    src="doc/images/readme/paravane-smtprs-sdk-readme-banner-logo-updated-orange-dark-developer-api-yellow.png"
    alt="Paravane" />
</p>

<h1 align="center">
  Paravane Python Library
</h1>

<p align="center">
  The Paravane Python library provides convenient access to the Paravane API from applications written in Python.
  <br /><br />
  The first supported product API is <strong>smtpRS</strong>, Paravane's email risk intelligence API.
  smtpRS helps score email addresses for onboarding, trust, review, abuse-prevention, and operations workflows.
  <br /><br />
  This SDK is intentionally small at the start. It provides a stable client entrypoint,
  request serialization, response helpers, structured errors, examples, tests, and packaging
  conventions that can grow as Paravane adds more APIs.
</p>

<!-- <p align="center">
  <a href="https://pypi.org/project/paravane/">
    <img
      src="https://img.shields.io/pypi/v/paravane.svg"
      alt="PyPI" />
  </a>
  <a href="https://pypi.org/project/paravane/">
    <img
      src="https://img.shields.io/pypi/pyversions/paravane.svg"
      alt="Supported Python versions" />
  </a>
  <a href="https://github.com/paravaneai/paravane-python/actions/workflows/tests.yml">
    <img
      src="https://github.com/paravaneai/paravane-python/actions/workflows/tests.yml/badge.svg"
      alt="Tests" />
  </a>
</p> -->

<p align="center">
  <a href="https://pypi.org/project/paravane/"><img
    src="https://img.shields.io/pypi/v/paravane.svg"
    alt="PyPI"></a>
  <a href="https://www.python.org/"><img
    src="https://img.shields.io/badge/Python-3.10%2B-blue.svg"
    alt="Python"></a>
</p>

<h3 align="center">
  <a href="#documentation">Documentation</a>
  <span> · </span>
  <a href="#installation">Installation</a>
  <span> · </span>
  <a href="#quickstart">Quickstart</a>
  <span> · </span>
  <a href="#examples">Examples</a>
  <span> · </span>
  <a href="#development">Development</a>
</h3>

## Contents

- [Documentation](#documentation)
- [Installation](#installation)
- [Requirements](#requirements)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [smtpRS](#smtprs)
- [Configuration](#configuration)
- [Per-request options](#per-request-options)
- [Custom HTTP sessions](#custom-http-sessions)
- [Retries](#retries)
- [Idempotency](#idempotency)
- [Errors](#errors)
- [Responses and raw data](#responses-and-raw-data)
- [Types](#types)
- [Logging](#logging)
- [Examples](#examples)
- [Development](#development)
- [Repository layout](#repository-layout)
- [Versioning](#versioning)
- [Security](#security)
- [Support](#support)

## Documentation

This README is the canonical SDK reference. The hosted Paravane documentation portal may
temporarily show an access-status page during capacity pauses.

- Product docs: https://paravane.io/pages/docs/index.html
- smtpRS docs: https://paravane.io/pages/docs/smtprs/index.html
- Authentication: https://paravane.io/pages/docs/smtprs/authentication.html
- Analyse endpoint: https://paravane.io/pages/docs/smtprs/analyse.html
- Plans and limits: https://paravane.io/pages/docs/smtprs/plans-limits.html

## Installation
Install the latest release from PyPI:

```bash
python -m pip install --upgrade paravane
```

To install the current development version directly from GitHub:

```bash
python -m pip install "git+https://github.com/paravaneai/paravane-python.git"
```

For local development:

```bash
git clone git@github.com:paravaneai/paravane-python.git
cd paravane-python
python -m pip install -e ".[dev]"
```

## Requirements
Python 3.10 or newer.

Runtime dependency:

- `requests>=2.33.0`

Development dependencies are installed with:

```bash
python -m pip install -e ".[dev]"
```

## Quickstart
Create an API key from the [Paravane API keys page](https://paravane.io/pages/app/api-keys.html),
copy it when it is shown, and store it in your server-side environment. The production client
already defaults to `https://api.paravane.io`; do not append `/v1` to the base URL.

Set your API key:

```bash
export PARAVANE_API_KEY="pvn_live_..."
```

On Windows PowerShell:

```powershell
$env:PARAVANE_API_KEY = "pvn_live_..."
```

Call smtpRS:

```python
from paravane import ParavaneClient

client = ParavaneClient()

result = client.smtprs.analyze("alice@example.com")

print(result.decision)
print(result.overall_risk)
print(result.credits_charged)
```

The SDK method is named `analyze(...)` for Python readability. The HTTP API endpoint remains:

```text
POST /v1/analyse
```

## Usage

Create a client with an API key:

```python
from paravane import ParavaneClient

client = ParavaneClient(api_key="pvn_live_...")
```

Or use `PARAVANE_API_KEY`:

```python
from paravane import ParavaneClient

client = ParavaneClient()
```

Run an email risk analysis:

```python
result = client.smtprs.analyze("person@example.com")

if result.decision == "allow":
    print("Continue")
else:
    print("Review or block")
```

Inspect the normalized response:

```python
print(result.email)
print(result.decision)
print(result.overall_risk)
print(result.analysis_profile)
print(result.credit_cost)
print(result.usage)
```

Access the original API response:

```python
raw = result.to_dict()
print(raw)
```

## smtpRS

smtpRS is available through:

```python
client.smtprs
```

### Analysis profiles

smtpRS provides named profiles so applications can choose the appropriate balance of
coverage, latency, and credit usage without configuring individual checks.

| Profile | Credits | Availability | Intended use |
| --- | ---: | --- | --- |
| `quick` | 1 | All plans | Lightweight screening; this is the default. |
| `standard` | 3 | Basic and above | Broader passive analysis. |
| `adaptive` | 5 | Pro and above | Adds checks when the initial result needs more context. |
| `deep` | 5 | Pro and above | Comprehensive analysis without catch-all probing. |
| `catch_all` | 20 | Enterprise or entitled accounts | Deep analysis with catch-all probing. |

Use the default quick profile:

```python
result = client.smtprs.analyze("person@example.com")
```

Or request another profile available to your account:

```python
result = client.smtprs.analyze(
    "person@example.com",
    profile="standard",
)
```

Profile availability is enforced by the API. Requesting a profile that is not included
with the current plan raises `PermissionDeniedError`.

### Legacy mode flags

The older `disposable_only`, `strict_disposable`, `guess`, and `run_catch_all` arguments
remain available for compatibility. New integrations should use `profile` instead. Do not
combine `profile` with an enabled legacy mode flag.

For example, replace:

```python
result = client.smtprs.analyze(
    "person@example.com",
    strict_disposable=True,
)
```

with:

```python
result = client.smtprs.analyze(
    "person@example.com",
    profile="deep",
)
```

### Low-latency posture

Use the `fast` flag when your workflow favors lower latency:

```python
result = client.smtprs.analyze(
    "person@example.com",
    fast=True,
)
```

### Company Validity Beta

Paid smtpRS callers can explicitly request the optional Company Validity Beta:

```python
result = client.smtprs.analyze(
    "person@example.com",
    profile="standard",
    company_validity_beta=True,
)

beta = result.company_validity_beta
if beta is not None:
    print(beta.status)  # "beta"
    print(beta.requested)  # True
    print(beta.enabled)  # True when the feature was active for this request
    print(beta.notes)

signal = result.domain_signal
if signal is not None:
    print(signal.domain_status)
    print(signal.mail_status)
    print(signal.company_valid)
```

The option is omitted by default, so existing calls retain their current
behavior. It is available only to paid smtpRS plans and provides additive
company-domain context rather than an allowlist. It currently adds no credits
beyond the selected profile. Free-plan requests that explicitly enable it
receive `PermissionDeniedError`. Because the response contract is beta,
applications can use `result.to_dict()` to retain access to newly added fields.

## Configuration

```python
from paravane import ParavaneClient

client = ParavaneClient(
    api_key="pvn_live_...",
    base_url="https://api.paravane.io",
    timeout=20.0,
    max_network_retries=1,
)
```

Environment variables:

| Name | Purpose | Default |
| --- | --- | --- |
| `PARAVANE_API_KEY` | API key used for requests. | None |
| `PARAVANE_BASE_URL` | API base URL. | `https://api.paravane.io` |

Most applications should leave `PARAVANE_BASE_URL` unset. If an approved alternate endpoint is
required, provide only its scheme and host; the SDK adds `/v1/analyse` itself.

## Per-request options

You can set a timeout for one request:

```python
result = client.smtprs.analyze(
    "person@example.com",
    timeout=5.0,
)
```

You can pass an idempotency key:

```python
result = client.smtprs.analyze(
    "person@example.com",
    idempotency_key="signup-check-123",
)
```

You can pass future or preview query parameters without waiting for a new SDK release:

```python
result = client.smtprs.analyze(
    "person@example.com",
    extra_params={"preview_flag": "enabled"},
)
```

## Custom HTTP sessions

The SDK uses `requests` by default. If your environment needs custom connection pooling, proxies, certificates, or adapters, pass a configured `requests.Session`:

```python
import requests
from paravane import ParavaneClient

session = requests.Session()
session.proxies.update(
    {
        "https": "https://proxy.example.com:8443",
    }
)

client = ParavaneClient(
    api_key="pvn_live_...",
    session=session,
)
```

## Retries

By default, the SDK does not retry network calls:

```python
client = ParavaneClient(max_network_retries=0)
```

Enable limited retries for transient network failures, `429` rate limits, and `5xx` API responses:

```python
client = ParavaneClient(max_network_retries=2)
```

Billable POST requests are retried only when you supply an idempotency key. Without one,
`analyze` makes one attempt even when `max_network_retries` is greater than zero:

```python
result = client.smtprs.analyze(
    "person@example.com",
    idempotency_key="customer-signup-456",
)
```

## Idempotency

The SDK accepts an `idempotency_key` and sends it as:

```text
Idempotency-Key: your-key
```

Use stable keys for requests that your application may retry after timeouts or transient failures.

## Errors

Unsuccessful requests raise structured exceptions from `paravane.errors`.

```python
from paravane import (
    AuthenticationError,
    ParavaneClient,
    QuotaExceededError,
    RateLimitError,
    ValidationError,
)

client = ParavaneClient()

try:
    result = client.smtprs.analyze("person@example.com")
except AuthenticationError:
    print("Check your API key.")
except QuotaExceededError:
    print("The workspace has exhausted its available credits.")
except RateLimitError:
    print("Slow down and retry later.")
except ValidationError as exc:
    print("Request was invalid:", exc)
```

Exception classes:

| Class | Typical cause |
| --- | --- |
| `ConfigurationError` | Missing API key or invalid client setup. |
| `APIConnectionError` | Network failure, timeout, DNS failure, or connection error. |
| `APIError` | Generic non-success API response. |
| `AuthenticationError` | Missing, invalid, or revoked API key. |
| `PermissionDeniedError` | API key lacks access to the requested resource. |
| `ValidationError` | Invalid request payload or parameters. |
| `QuotaExceededError` | Plan or credit quota has been exhausted. |
| `RateLimitError` | Too many requests. |

API errors include useful details when available:

```python
try:
    client.smtprs.analyze("not-an-email")
except ValidationError as exc:
    print(exc.status_code)
    print(exc.code)
    print(exc.request_id)
    print(exc.response)
```

## Responses and raw data

The SDK returns `SmtpRsAnalysis` for smtpRS analysis requests.

```python
result = client.smtprs.analyze("person@example.com")
```

Common fields:

| Field | Description |
| --- | --- |
| `email` | Email address represented by the response, when returned by the API. |
| `decision` | Customer-facing decision or recommendation, when returned by the API. |
| `overall_risk` | Overall risk score, when returned by the API. |
| `tier` | Workspace/API-key tier reflected by the response. |
| `analysis_profile` | Analysis path used by the API. |
| `response_profile` | Response shape, such as summary/full. |
| `credit_cost` | Planned credit cost for the selected profile. |
| `credits_charged` | Credits recorded for the request, when returned. |
| `company_validity_beta` | Typed beta status, opt-in state, availability, credit cost, and API notes. |
| `domain_signal` | Typed domain, mail, and company-context facts when returned. |
| `reasons` | Human-readable reason strings, when returned. |
| `usage` | Usage/quota snapshot, when returned. |
| `raw` | Original API payload. |

To avoid losing fields added by the API before the SDK is updated, the full payload is always preserved:

```python
raw = result.to_dict()
print(raw["usage"])
```

## Types

This package includes inline type hints and ships a `py.typed` marker.

The response helper is a dataclass:

```python
from paravane import SmtpRsAnalysis


def handle_result(result: SmtpRsAnalysis) -> None:
    print(result.decision)
    signal = result.domain_signal
    if signal is not None:
        print(signal.mail_capable)
```

Type hints are intended to describe stable SDK behavior. The raw API response may include additional fields that are not represented as first-class dataclass attributes yet.

## Logging

The SDK does not install or configure logging handlers. Applications should configure logging at the application boundary.

For now, request failures are surfaced through exceptions. If you need detailed HTTP logging during development, configure your own `requests.Session` or enable logging in your HTTP stack.

## Examples

This repository includes small examples:

```text
examples/basic_analyze.py
examples/strict_analyze.py
examples/batch_csv.py
```

Run one with:

```bash
PARAVANE_API_KEY="pvn_live_..." python examples/basic_analyze.py
```

Windows PowerShell:

```powershell
$env:PARAVANE_API_KEY = "pvn_live_..."
python examples/basic_analyze.py
```

## Development

Create an environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run lint:

```bash
ruff check .
```

Build the package:

```bash
python -m build
```

Recommended pre-commit check:

```bash
pytest && ruff check . && python -m build
```

## Repository layout

```text
paravane-python/
  .github/workflows/   GitHub Actions checks
  examples/            Small runnable examples
  src/paravane/        SDK package source
  tests/               Unit tests
  pyproject.toml       Packaging metadata and tool config
  RELEASING.md         Maintainer release process
```

## Versioning

Current package version:

```text
1.0.2
```


## Security

Do not put API keys in source code, client-side apps, mobile apps, screenshots, or public repositories.

Recommended handling:

- load API keys from environment variables or a secret manager
- rotate keys if they are exposed
- create separate keys for development, staging, and production
- revoke keys that are no longer needed

Report suspected vulnerabilities privately:

```text
security@paravane.io
```

## Support

For product or account support:

```text
contact@paravane.io
```

For security reports:

```text
security@paravane.io
```
