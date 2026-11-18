"""Check that each quote in a NAM record is really in its cited reference.

A NAM record's statement may carry a verbatim quote from the paper it came
from, beside the reference the quote is from (``NAMStatement`` > ``quotes``).
This checks every such pair against the reference's cached text, so a quote
that is nearly right, or that no accessible source supports, is caught before
it reaches a record.

The checking engine is DisMech's ``dismech.reference_snippet_audit``, imported
rather than reimplemented. It takes the schema, the validator config and the
cache directory as arguments, so it audits this repository's files unchanged,
and "verified" here means what it means in DisMech: both repositories defer to
``linkml-reference-validator``'s own cache loader and text normalisation.

DisMech is in the ``research`` dependency group rather than among this
package's dependencies, so ``uv sync`` does not install it by default. Run
this module through ``just check-snippets``, which passes ``--group
research``; running it any other way needs DisMech on the path.

    just check-snippets                     # every record in nams/
    just check-snippets --strict            # exit 1 on an unverified quote
    just check-snippets nams/<id>.yaml      # one record

A quote whose reference is cached as an abstract is reported apart, because
nothing is established either way: the full text may well contain it. That is
not a pass, and ``--strict`` fails on it unless ``--allow-abstract-only`` is
given. The cure is to cache the full text where the paper's licence allows it
(``fetch_full_text`` in .linkml-reference-validator.yaml), not to relax the
check.
"""

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCHEMA = REPO / "src/nams_registry/schema/nam_records.yaml"
CONFIG = REPO / ".linkml-reference-validator.yaml"
NAMS_DIR = REPO / "nams"

MISSING_DISMECH = """\
cannot import dismech.reference_snippet_audit.

This module borrows DisMech's snippet audit, and DisMech is installed for the
duration of one command rather than being a dependency of this package. Run it
through the recipe, which does that:

    just check-snippets{args}

or put a DisMech checkout on the path yourself.\
"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="NAM record files to check (default: every record in nams/)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 if any quote is not found in its cited reference",
    )
    parser.add_argument(
        "--allow-abstract-only",
        action="store_true",
        help=(
            "with --strict, do not fail on a quote whose reference is cached as "
            "an abstract only (the full text may contain it)"
        ),
    )
    parser.add_argument(
        "--check-boundaries",
        action="store_true",
        help="also report a quote that matches only as a mid-word fragment",
    )
    args = parser.parse_args(argv)

    try:
        from dismech.reference_snippet_audit import audit_files
    except ImportError:
        given = " ".join(str(path) for path in args.files)
        sys.exit(MISSING_DISMECH.format(args=f" {given}" if given else "").rstrip())

    paths = args.files or sorted(NAMS_DIR.glob("*.yaml"))
    if not paths:
        sys.exit(f"no NAM records found in {NAMS_DIR}")

    report = audit_files(
        paths,
        schema_path=SCHEMA,
        config_path=CONFIG,
        cache_dir=None,  # the config's cache_dir, references_cache/
        check_boundaries=args.check_boundaries,
    )
    print(report.format())

    if not args.strict:
        return 0

    failed = list(report.mismatched)
    if not args.allow_abstract_only:
        failed += list(report.abstract_only_pairs)
    if failed:
        print(
            f"\n{len(failed)} quote(s) not verified against a cited reference.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
