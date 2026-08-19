#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2023–2026 Paravane Labs
# SPDX-License-Identifier: MIT
"""
Validate and build the distributions that will be published to PyPI.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 only
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
RUNTIME_VERSION = ROOT / "src" / "paravane" / "_version.py"
DIST = ROOT / "dist"


def run(*args: str) -> None:
    print(f"+ {' '.join(args)}", flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def load_project() -> dict[str, object]:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)["project"]


def runtime_version() -> str:
    namespace: dict[str, str] = {}
    exec(RUNTIME_VERSION.read_text(encoding="utf-8"), namespace)
    return namespace["__version__"]


def check_versions(project: dict[str, object], tag: str | None) -> str:
    package_version = str(project["version"])
    code_version = runtime_version()
    if package_version != code_version:
        raise SystemExit(
            "Version mismatch: pyproject.toml has "
            f"{package_version}, but src/paravane/_version.py has {code_version}."
        )
    normalized_tag = tag[1:] if tag is not None and tag.startswith("v") else tag
    if normalized_tag is not None and normalized_tag != package_version:
        raise SystemExit(f"Release tag {tag!r} does not match package version {package_version!r}.")
    return package_version


def check_clean_tree(allow_dirty: bool) -> None:
    if allow_dirty:
        return
    git = shutil.which("git")
    if git is None:
        raise SystemExit("Git is required to verify that the release tree is clean.")
    result = subprocess.run(
        [git, "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        raise SystemExit(
            "Refusing to build a release from a dirty Git tree. Commit or stash changes, "
            "or pass --allow-dirty for a local rehearsal."
        )


def clean_build_outputs() -> None:
    for path in (DIST, ROOT / "build", ROOT / "src" / "paravane.egg-info"):
        if path.exists():
            shutil.rmtree(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_wheel(wheel: Path, name: str, version: str) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_paths = [item for item in names if item.endswith(".dist-info/METADATA")]
        if len(metadata_paths) != 1:
            raise SystemExit(f"Expected one METADATA file in {wheel.name}.")

        metadata = BytesParser().parsebytes(archive.read(metadata_paths[0]))
        if metadata["Name"] != name or metadata["Version"] != version:
            raise SystemExit(
                f"Unexpected wheel identity: {metadata['Name']} {metadata['Version']}."
            )
        if "paravane/py.typed" not in names:
            raise SystemExit(f"{wheel.name} does not contain paravane/py.typed.")


def inspect_sdist(sdist: Path, name: str, version: str) -> None:
    expected_root = f"{name}-{version}"
    with tarfile.open(sdist, "r:gz") as archive:
        names = archive.getnames()
        if f"{expected_root}/pyproject.toml" not in names:
            raise SystemExit(f"{sdist.name} does not contain pyproject.toml.")


def inspect_distributions(name: str, version: str) -> None:
    wheels = sorted(DIST.glob("*.whl"))
    sdists = sorted(DIST.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit("Expected exactly one wheel and one source distribution in dist/.")
    inspect_wheel(wheels[0], name, version)
    inspect_sdist(sdists[0], name, version)
    print("\nRelease artifacts:")
    for artifact in (*wheels, *sdists):
        print(f"  {artifact.name}\n    sha256: {sha256(artifact)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run checks and build validated Paravane PyPI distributions."
    )
    parser.add_argument(
        "--tag",
        help="Require a release tag matching the package version (for example, v1.0.2).",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Permit uncommitted changes for a local release rehearsal.",
    )
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-lint", action="store_true")
    parser.add_argument(
        "--no-isolation",
        action="store_true",
        help=(
            "Build with the current environment instead of creating an isolated build environment."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project = load_project()
    name = str(project["name"])
    version = check_versions(project, args.tag)
    check_clean_tree(args.allow_dirty)
    if not args.skip_tests:
        run(sys.executable, "-m", "pytest")
    if not args.skip_lint:
        run(sys.executable, "-m", "ruff", "check", ".")
    clean_build_outputs()
    build_command = [sys.executable, "-m", "build"]
    if args.no_isolation:
        build_command.append("--no-isolation")
    run(*build_command)
    distributions = [str(path) for path in sorted(DIST.iterdir())]
    run(sys.executable, "-m", "twine", "check", *distributions)
    inspect_distributions(name, version)
    print(
        "\nRelease is ready. Publishing is intentionally handled by "
        ".github/workflows/publish.yml using PyPI Trusted Publishing."
    )


if __name__ == "__main__":
    main()
