"""Run a deep-research provider on a paper, under DisMech's provider policy.

The registry's papers mostly have no DisMech entity, and every DisMech
``just research-*`` recipe is keyed on one -- a disease entry, a module, a drug
-- so none of them takes a PMID or a DOI. A paper with no DisMech anchor could
not be run through them at all, which is why paper runs here used to be
hand-assembled ``deep-research-client`` calls (see research/README.md). This is
that call, as a recipe, keyed on the paper.

The research client is the third-party ``deep-research-client``; DisMech does
not implement one either. What this borrows from DisMech is its *policy*, from
``dismech.deep_research_policy``:

- Biomni is not offered, including as an automatic fallback, unless
  ``DISMECH_ENABLE_BIOMNI=1``. The policy has to be applied before provider
  discovery, which is why this wrapper exists rather than a bare client call.

Arguments are passed through to ``deep-research-client research``, so its own
options work unchanged:

    just deep-research --provider openscientist --input-file prompt.md \\
        --output research/<stem>-deep-research-openscientist.md
    just deep-research --provider mock "a cheap end-to-end check"

Read research/README.md before committing a report. A report is a lead, never a
source: its claims are checked against the paper, and a record is written from
the paper rather than from the report.
"""

import sys

MISSING_DEPENDENCY = """\
cannot import {module}.

This wrapper needs both the pinned DisMech (for the provider policy) and
deep-research-client. Both are in the `research` dependency group, which
`uv sync` does not install by default; the recipe passes `--group research`:

    just deep-research {args}\
"""


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    try:
        from dismech.deep_research_policy import (
            BIOMNI_DISABLED_DETAIL,
            configure_biomni_environment,
            requests_biomni_research,
        )
    except ImportError:
        sys.exit(
            MISSING_DEPENDENCY.format(
                module="dismech.deep_research_policy", args=" ".join(argv)
            ).rstrip()
        )

    # Before provider discovery, so an un-opted-in session is not offered
    # Biomni as a fallback.
    if not configure_biomni_environment() and requests_biomni_research(argv):
        print(BIOMNI_DISABLED_DETAIL, file=sys.stderr)
        return 2

    try:
        from deep_research_client.cli import app
    except ImportError:
        sys.exit(
            MISSING_DEPENDENCY.format(
                module="deep_research_client", args=" ".join(argv)
            ).rstrip()
        )

    # The client's own CLI, with "research" supplied so the recipe reads as a
    # research command and the caller's arguments are the provider's.
    sys.argv = ["deep-research-client", "research", *argv]
    app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
