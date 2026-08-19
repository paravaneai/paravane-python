# Contributing to the Paravane Python SDK

Thank you for helping improve the Paravane Python SDK. We welcome bug reports,
feature requests, documentation improvements, tests, and focused code contributions.

## Before opening a pull request

Small documentation corrections, spelling fixes, and narrowly scoped test improvements may be
submitted directly.

Please [open an issue](https://github.com/paravaneai/paravane-python/issues) before starting work
that does any of the following:

- Adds or removes public classes, methods, parameters, or response fields.
- Changes request serialization, retry behavior, error handling, or authentication.
- Introduces or replaces a dependency.
- Changes supported Python versions or packaging behavior.
- Adds substantial functionality or changes documented behavior.
- Requires a migration or could break an existing integration.

An issue lets maintainers confirm the intended behavior before significant implementation work
begins. Include the use case, expected behavior, compatibility concerns, and a proposed approach.

## Development environment

The SDK supports Python 3.10 through 3.13. Contributions must work on every supported version.

Clone the repository over SSH:

```bash
git clone git@github.com:paravaneai/paravane-python.git
cd paravane-python
```

Create a virtual environment and install the development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Windows with MSYS2 UCRT64

Run the same commands from the MSYS2 UCRT64 terminal. If Python is not installed, install the
UCRT64 package first:

```bash
pacman -S --needed mingw-w64-ucrt-x86_64-python
```

Depending on the Python build, virtual-environment activation may be available at either
`.venv/bin/activate` or `.venv/Scripts/activate`. You can also call the environment's Python
executable directly without activating it.

## Making changes

- Keep the public API small, explicit, and backward compatible.
- Preserve unknown response fields through the existing raw-payload mechanism.
- Never silently change billing-sensitive behavior, credit use, retries, or idempotency.
- Add or update tests for every behavioral change.
- Update documentation and `CHANGELOG.md` when behavior visible to SDK users changes.
- Keep changes focused; avoid unrelated formatting or refactoring.
- Do not commit API keys, credentials, customer data, `.env` files, virtual environments,
  caches, build directories, or generated distributions.

## Verification

Before opening a pull request, run:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

For packaging or release-related changes, also run:

```bash
python scripts/prepare_release.py --allow-dirty
```

`--allow-dirty` permits a release rehearsal before the contribution is committed. The release
validator requires matching versions in `pyproject.toml` and
`src/paravane/_version.py`, validates the tag when supplied, tests and lints the project, builds
the wheel and source distribution, and checks both artifacts.

## Pull requests

A pull request should:

- Explain what changed and why.
- Link the associated issue when one is required.
- Describe any public API or compatibility impact.
- Include tests that demonstrate the new or corrected behavior.
- Update user-facing documentation when applicable.
- Pass all configured GitHub Actions checks.

Maintainers may ask for changes when a contribution affects API stability, security, billing,
compatibility, or the behavior of an existing integration.

## Security reports

Do not report suspected vulnerabilities or exposed credentials in a public issue. Follow the
private reporting instructions in [SECURITY.md](SECURITY.md).

## Releases and publishing

Package versions, Git tags, GitHub Releases, release workflows, and PyPI publication are managed
by Paravane maintainers. Contributors should not change version numbers or publish artifacts
unless a maintainer explicitly requests it as part of the contribution.

The project does not currently require a Contributor License Agreement. Contributions are
accepted under the repository's [MIT License](LICENSE).
