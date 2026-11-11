#!/usr/bin/env python3
"""Make the NAMO schema available to nam_records.yaml, which imports ``namo``.

The NAMO schema lives only in https://github.com/monarch-initiative/namo; the
registry never commits a copy. This script puts it at
``src/nams_registry/schema/namo.yaml`` (gitignored), from one of:

1. A local NAMO checkout: the directory in ``NAMO_DIR``, or else ``namo`` next
   to this repository. The file is a symlink to that checkout's schema, so
   edits there are seen here at once. A warning says when the checkout is
   not at the commit pyproject.toml pins, since the tests may then fail.
2. GitHub, when there is no local checkout, at the branch, tag or commit set
   by ``ref`` under ``[tool.nams-registry.namo]`` in pyproject.toml, or by
   ``NAMO_REF``. It is downloaded again on every run.

    uv run python scripts/link_namo.py
    NAMO_DIR=~/src/namo uv run python scripts/link_namo.py
    NAMO_REF=some-branch uv run python scripts/link_namo.py
"""

import os
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

SCHEMA_IN_NAMO = Path("src/namo/schema/namo.yaml")
REPO = Path(__file__).resolve().parent.parent
TARGET = REPO / "src/nams_registry/schema/namo.yaml"


def local_namo():
    """Return the schema in a local NAMO checkout, or None."""
    if os.environ.get("NAMO_DIR"):
        schema = Path(os.environ["NAMO_DIR"]).expanduser().resolve() / SCHEMA_IN_NAMO
        if not schema.is_file():
            sys.exit(f"NAMO_DIR is set, but {schema} does not exist")
        return schema
    schema = REPO.parent / "namo" / SCHEMA_IN_NAMO
    return schema if schema.is_file() else None


def configured_ref():
    """Return the NAMO ref set in pyproject.toml."""
    with open(REPO / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    try:
        return config["tool"]["nams-registry"]["namo"]["ref"]
    except KeyError:
        sys.exit("Set ref under [tool.nams-registry.namo] in pyproject.toml")


def warn_if_not_pinned(schema):
    """Warn when a local checkout is not at the commit pyproject.toml pins.

    The checkout is still used, so NAMO changes can be tried here at once;
    the warning explains test failures that come from the difference.
    """
    ref = configured_ref()
    checkout = schema.parents[len(SCHEMA_IN_NAMO.parts) - 1]
    try:
        head = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return
    if not head.startswith(ref):
        print(
            f"NAMO: warning: {checkout} is at {head[:7]}, not at {ref[:7]}, the commit "
            "pyproject.toml pins; set NAMO_DIR to a checkout of that commit to test against it",
            file=sys.stderr,
        )


def main(quiet=False):
    say = (lambda _: None) if quiet else print
    schema = local_namo()
    if schema:
        warn_if_not_pinned(schema)
    if schema and TARGET.is_symlink() and TARGET.resolve() == schema:
        return
    if TARGET.is_symlink() or TARGET.exists():
        TARGET.unlink()
    if schema:
        TARGET.symlink_to(schema)
        say(f"NAMO: using the local checkout, {schema}")
        return
    ref = os.environ.get("NAMO_REF") or configured_ref()
    url = f"https://raw.githubusercontent.com/monarch-initiative/namo/{ref}/{SCHEMA_IN_NAMO}"
    with urllib.request.urlopen(url, timeout=30) as response:
        TARGET.write_bytes(response.read())
    say(f"NAMO: downloaded {ref} from GitHub")


if __name__ == "__main__":
    main()
