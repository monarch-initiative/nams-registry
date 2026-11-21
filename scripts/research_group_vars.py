#!/usr/bin/env python3
"""Collect the variables a research-group prompt needs.

templates/research_group_models.md asks a deep-research provider for the models a
research group (a researcher, a team or an organization) develops and uses, the
mechanisms it has characterised with them, and its contexts of use. Each group is
one spec, templates/research_groups/<slug>.yaml, beside the paper list that
scripts/fetch_openalex_works.py writes for it, <slug>.works.yaml.

Five variables are written by hand in the spec; three are generated:

- ``anchor_papers`` and ``known_datasets``, from <slug>.works.yaml;
- ``data_analysis_instructions``, from the spec's ``data_analysis`` switch.

This script only gathers the variables. `just research-group` passes each one to
deep-research-client as a ``--var`` and lets the client render the committed
template, so the report's frontmatter records the template and every variable,
and no rendered prompt is written anywhere.

    uv run python scripts/research_group_vars.py carreras_puigvert --format stem
    uv run python scripts/research_group_vars.py carreras_puigvert --format null
    uv run python scripts/research_group_vars.py carreras_puigvert --format prompt

``--format prompt`` renders through the client's own TemplateProcessor, so the
preview cannot drift from what a run sends.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

TEMPLATE = pathlib.Path("templates/research_group_models.md")
USE_CASES = pathlib.Path("templates/research_groups")
HAND_WRITTEN = ("group_name", "group_kind", "group_description", "focus", "date_range")
GENERATED = ("anchor_papers", "known_datasets", "data_analysis_instructions")
GROUP_KINDS = ("researcher", "team", "organization")
STEM = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

ANALYSE = """\
**Data analysis.** Where one of these datasets is accessible from your
environment, carry out a modest reanalysis that tests one claim from the group's
papers: for example, whether reference compounds of distinct mechanisms separate
in the profiles, or whether a simple baseline such as cell count recovers a
reported signal. Report exactly what you downloaded, what you ran and what you
found, including negative or inconclusive results."""

LITERATURE_ONLY = """\
**Literature only.** Do not download or reanalyse data in this run; describe the
datasets from their papers and repository records."""


def spec_paths(directory: pathlib.Path = USE_CASES) -> list[pathlib.Path]:
    """Every group spec: the YAML files that are not generated paper lists."""
    return sorted(
        p for p in directory.glob("*.yaml") if not p.name.endswith(".works.yaml")
    )


def use_case(slug: str) -> dict:
    """Load one group spec, insisting on every field the template needs."""
    spec_path = USE_CASES / f"{slug}.yaml"
    if slug.endswith(".works") or not spec_path.is_file():
        available = ", ".join(p.stem for p in spec_paths()) or "none"
        raise SystemExit(f"No research group {slug!r}. Available: {available}")
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
    missing = [k for k in ("stem", *HAND_WRITTEN) if not spec.get(k)]
    if "data_analysis" not in spec:
        missing.append("data_analysis")
    if missing:
        raise SystemExit(f"{spec_path} is missing: {', '.join(missing)}")
    if spec["group_kind"] not in GROUP_KINDS:
        raise SystemExit(
            f"{spec_path}: group_kind must be one of {', '.join(GROUP_KINDS)}"
        )
    if not STEM.match(spec["stem"]):
        raise SystemExit(f"{spec_path}: stem must be lower-case words joined by '-'")
    return spec


def works(slug: str) -> dict:
    path = USE_CASES / f"{slug}.works.yaml"
    if not path.is_file():
        raise SystemExit(
            f"{path} not found. Run `just research-group-works {slug}` first."
        )
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def cite(row: dict) -> str:
    ids = [f"PMID:{row['pmid']}" if row.get("pmid") else None]
    ids.append(f"doi:{row['doi']}" if row.get("doi") else f"OpenAlex {row['openalex']}")
    venue = f", {row['venue']}" if row.get("venue") else ""
    kind = f" [{row['type']}]" if row.get("type") not in ("article", None) else ""
    return f"- {row['title']} ({row['year']}{venue}){kind}. {', '.join(i for i in ids if i)}"


def variables(spec: dict, paper_list: dict) -> dict[str, str]:
    """Return every template variable for a group."""
    values = {k: str(spec[k]).rstrip() for k in HAND_WRITTEN}
    papers = paper_list.get("papers") or []
    datasets = paper_list.get("datasets") or []
    values["anchor_papers"] = (
        "\n".join(cite(r) for r in papers)
        or "None were found in OpenAlex; search for them."
    )
    values["known_datasets"] = (
        "\n".join(cite(r) for r in datasets)
        or "None are attributed to the group in OpenAlex."
    )
    values["data_analysis_instructions"] = (
        ANALYSE if spec["data_analysis"] else LITERATURE_ONLY
    )
    return values


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("slug", help="group in templates/research_groups/, without .yaml")
    ap.add_argument(
        "--format",
        choices=("null", "stem", "prompt"),
        default="null",
        help="NUL-separated name=value records (default), the report stem, or the rendered prompt",
    )
    args = ap.parse_args(argv)

    if not TEMPLATE.is_file():
        print(f"{TEMPLATE} not found. Run from the repository root.", file=sys.stderr)
        return 1

    spec = use_case(args.slug)
    if args.format == "stem":
        print(spec["stem"])
        return 0

    values = variables(spec, works(args.slug))
    if args.format == "prompt":
        from deep_research_client.processing.template_processor import (
            TemplateProcessor,
        )

        print(TemplateProcessor().render_template(TEMPLATE, values))
        return 0

    for name, value in values.items():
        sys.stdout.write(f"{name}={value}\0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
