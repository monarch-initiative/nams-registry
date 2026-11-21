#!/usr/bin/env python3
"""Fetch a research group's publications from OpenAlex for a research-group run.

`just research-group` sends templates/research_group_models.md to a deep-research
provider with a group's paper list in it. This script writes that list, so it does
not have to be typed in. It reads the `openalex` block of
templates/research_groups/<slug>.yaml and writes
templates/research_groups/<slug>.works.yaml, which is committed with the spec so
a run can be reproduced and reviewed.

The `openalex` block selects works by any of:

- ``authors``: OpenAlex author IDs (A…). Use several when OpenAlex has split one
  person across records, or to cover a team.
- ``institutions``: ROR IDs, for an organization. Usually needs ``search`` too.
- ``from_year``: earliest publication year.
- ``search``: an OpenAlex full-text search that narrows the corpus.

What it keeps, and why:

- Supplementary figures and tables, errata, paratext and peer reviews are
  dropped: publishers deposit each figure of a paper as its own DOI, and these
  would swamp the list without adding a paper.
- Datasets are kept in a separate list, because the template asks for them in
  its data section, not among the papers.
- A preprint and its published version are one paper. When two works share a
  normalised title, the published version is kept.
- Anything listed in the spec's ``exclude_works`` (OpenAlex work IDs or DOIs) is
  dropped. Prune there, not in the generated file, so a re-fetch keeps it.

The counts of what was dropped are written into the file's header, so a reader
can see how much was left out without re-running.

    uv run python scripts/fetch_openalex_works.py carreras_puigvert
    uv run python scripts/fetch_openalex_works.py carreras_puigvert --dry-run
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

API = "https://api.openalex.org/works"
USER_AGENT = "nams-registry (https://github.com/monarch-initiative/nams-registry)"
USE_CASES = Path("templates/research_groups")

# Works of these types are never papers in their own right.
DROPPED_TYPES = {
    "erratum",
    "paratext",
    "peer-review",
    "supplementary-materials",
    "retraction",
}
# Publishers deposit a paper's figures, tables and data as works of type "other".
SUPPLEMENT_TITLE = re.compile(
    r"^(supplementa\w*|figure|fig\.|table|movie|video|data) (s?\d+|from)\b", re.I
)
# Which of two works with the same title to keep: lower is preferred.
TYPE_RANK = {
    "article": 0,
    "review": 0,
    "book-chapter": 1,
    "conference-paper": 2,
    "preprint": 3,
    "conference-abstract": 4,
}
SELECT = (
    "id,doi,ids,display_name,publication_year,type,primary_location,"
    "cited_by_count,is_retracted"
)


def short_id(openalex_url: str) -> str:
    return openalex_url.rsplit("/", 1)[-1]


def bare_doi(doi_url: str | None) -> str | None:
    return doi_url.removeprefix("https://doi.org/").lower() if doi_url else None


def normalise_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def build_filter(selector: dict) -> str:
    parts = []
    if selector.get("authors"):
        parts.append("author.id:" + "|".join(selector["authors"]))
    if selector.get("institutions"):
        rors = [
            r if r.startswith("https://ror.org/") else f"https://ror.org/{r}"
            for r in selector["institutions"]
        ]
        parts.append("authorships.institutions.ror:" + "|".join(rors))
    if not parts:
        raise SystemExit("The openalex block needs `authors` or `institutions`.")
    if selector.get("from_year"):
        parts.append(f"from_publication_date:{selector['from_year']}-01-01")
    return ",".join(parts)


def get_json(url: str) -> dict:
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": USER_AGENT}
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503) or attempt == 3:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def fetch(selector: dict, max_works: int) -> list[dict]:
    params = {
        "filter": build_filter(selector),
        "select": SELECT,
        "per-page": "200",
        "sort": "publication_date:desc",
        "cursor": "*",
    }
    if selector.get("search"):
        params["search"] = selector["search"]
    works: list[dict] = []
    while True:
        page = get_json(f"{API}?{urllib.parse.urlencode(params)}")
        works.extend(page["results"])
        if len(works) > max_works:
            raise SystemExit(
                f"OpenAlex returned more than {max_works} works. Narrow the "
                "selection with `from_year` or `search`, or raise --max-works."
            )
        cursor = page["meta"].get("next_cursor")
        if not cursor or not page["results"]:
            return works
        params["cursor"] = cursor


def entry(work: dict) -> dict:
    source = (work.get("primary_location") or {}).get("source") or {}
    pmid = (work.get("ids") or {}).get("pmid")
    row = {
        "openalex": short_id(work["id"]),
        "title": work["display_name"],
        "year": work["publication_year"],
        "type": work["type"],
        "venue": source.get("display_name"),
        "doi": bare_doi(work.get("doi")),
        "pmid": pmid.rsplit("/", 1)[-1] if pmid else None,
        "cited_by": work.get("cited_by_count", 0),
    }
    return {k: v for k, v in row.items() if v not in (None, "")}


def select(works: list[dict], exclude: set[str]) -> tuple[list, list, dict]:
    """Split works into papers and datasets, and count what was dropped."""
    dropped: collections.Counter = collections.Counter()
    papers: dict[str, dict] = {}
    datasets: list[dict] = []
    for work in works:
        row = entry(work)
        if row["openalex"].lower() in exclude or (row.get("doi") or "") in exclude:
            dropped["excluded in spec"] += 1
        elif work.get("is_retracted"):
            dropped["retracted"] += 1
        elif work["type"] in DROPPED_TYPES:
            dropped[work["type"]] += 1
        elif work["type"] == "dataset":
            datasets.append(row)
        elif work["type"] == "other" and (
            SUPPLEMENT_TITLE.match(row["title"] or "") or not row.get("venue")
        ):
            dropped["supplementary item typed other"] += 1
        else:
            key = normalise_title(row["title"])
            kept = papers.get(key)
            if kept is None:
                papers[key] = row
            else:
                dropped["duplicate title (preprint or repository copy)"] += 1
                rank = TYPE_RANK.get(row["type"], 5)
                if rank < TYPE_RANK.get(kept["type"], 5):
                    papers[key] = row
    ordered = sorted(papers.values(), key=lambda r: (-r["year"], r["title"]))
    return ordered, datasets, dict(dropped)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("slug", help="group in templates/research_groups/, without .yaml")
    ap.add_argument("--max-works", type=int, default=500)
    ap.add_argument(
        "--dry-run", action="store_true", help="print the list instead of writing it"
    )
    args = ap.parse_args(argv)

    spec_path = USE_CASES / f"{args.slug}.yaml"
    if not spec_path.is_file():
        print(f"{spec_path} not found. Run from the repository root.", file=sys.stderr)
        return 1
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    selector = spec.get("openalex") or {}
    exclude = {
        str(x).lower().removeprefix("https://doi.org/")
        for x in spec.get("exclude_works") or []
    }
    exclude |= {x.rsplit("/", 1)[-1] for x in exclude if "openalex.org" in x}

    works = fetch(selector, args.max_works)
    papers, datasets, dropped = select(works, exclude)
    document = {
        "fetched_on": datetime.date.today().isoformat(),
        "openalex_filter": build_filter(selector),
        "openalex_search": selector.get("search"),
        "returned": len(works),
        "dropped": dropped,
        "papers": papers,
        "datasets": datasets,
    }
    if document["openalex_search"] is None:
        del document["openalex_search"]
    header = (
        f"# Generated by scripts/fetch_openalex_works.py from {spec_path.name}.\n"
        "# Do not edit: prune with exclude_works in the spec and re-fetch.\n"
    )
    text = header + yaml.safe_dump(
        document, sort_keys=False, allow_unicode=True, width=72
    )
    if args.dry_run:
        print(text)
    else:
        out = USE_CASES / f"{args.slug}.works.yaml"
        out.write_text(text, encoding="utf-8")
        print(
            f"Wrote {out}: {len(papers)} papers, {len(datasets)} datasets, "
            f"{sum(dropped.values())} dropped of {len(works)}.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
