# Releasing `paravane` to PyPI

Publishing uses PyPI Trusted Publishing. No PyPI password or long-lived API token belongs in
this repository or in GitHub Actions secrets.

## One-time PyPI setup

In **PyPI → Account → Publishing**, add a pending GitHub publisher with these exact values:

| Field | Value |
| --- | --- |
| PyPI project name | `paravane` |
| Owner | `paravaneai` |
| Repository | `paravane-python` |
| Workflow | `publish.yml` |
| Environment | Leave blank |

The pending publisher does not reserve the project name. It becomes the project's trusted
publisher after the first successful upload.

## Prepare a release

1. Update the version in `pyproject.toml` and `src/paravane/_version.py`.
2. Add the release notes to `CHANGELOG.md`.
3. Install the development and release tools:

   ```bash
   python -m pip install -e ".[dev]"
   ```

4. Validate the exact artifacts that will be published:

   ```bash
   python scripts/prepare_release.py
   ```

   If an offline or proxied development environment cannot create an isolated build
   environment, use `python scripts/prepare_release.py --no-isolation`. CI always uses the
   default isolated build.

5. Commit and merge the release changes into `main`.
6. Create and publish a GitHub Release whose tag exactly matches the version, prefixed with `v`
   (for example, `v1.0.2`).

Publishing the GitHub Release runs `.github/workflows/publish.yml`. The workflow repeats the
tests and artifact checks, then uploads the wheel and source distribution to PyPI using a
short-lived identity credential. PyPI renders the project page from `pyproject.toml` and
`README.md`.
