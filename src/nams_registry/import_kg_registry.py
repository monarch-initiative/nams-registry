"""Import KG-Registry resources in the nams collection into resources/.

Each Resource page in a local KG-Registry checkout whose ``collection``
includes ``nams`` becomes one file, ``resources/<id>.yaml``. Fields that
the NAMs registry does not keep are dropped, KG-Registry's ``category``
and ``domains`` become ``resource_type`` and ``domain_areas``, and every
entry gets an ``imported_from`` record naming the KG-Registry commit.
``holds_nams`` is left out until the resource has been evaluated.

Existing files are skipped unless ``--overwrite`` is given, so that
curation done after an import is not lost.
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

import yaml

KG_REGISTRY_PAGE = "https://kghub.org/kg-registry/resource/{id}/{id}.html"

# KG-Registry fields copied unchanged, in the order they are written.
COPIED_FIELDS = [
    "id",
    "name",
    "description",
    "synonyms",
    "homepage_url",
    "repository",
]
# KG-Registry publication fields kept, in the order they are written. A
# publication has the fields of NAMO's Reference; KG-Registry's doi is moved
# into the id, and its preferred flag is dropped.
PUBLICATION_FIELDS = ["id", "title", "authors", "journal", "year", "url"]
DOI_URL = re.compile(r"^https?://(?:dx\.)?doi\.org/(.+)$")


def read_front_matter(path):
    """Return the YAML front matter of a KG-Registry Markdown page."""
    text = path.read_text()
    if not text.startswith("---"):
        return None
    return yaml.safe_load(text.split("---")[1])


def kg_registry_commit(kg_registry):
    """Return the short commit hash of the checkout, refusing a dirty tree."""
    status = subprocess.run(
        ["git", "-C", str(kg_registry), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    if status.strip():
        sys.exit(
            f"{kg_registry} has uncommitted changes, so its commit would not "
            "describe what is imported. Commit or stash them first."
        )
    return subprocess.run(
        ["git", "-C", str(kg_registry), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def convert_publication(publication):
    """Convert a KG-Registry publication into a NAMs registry Publication.

    The id becomes a doi: CURIE whenever the publication has a DOI, either
    in KG-Registry's doi field or as a doi.org URL id, and the year becomes
    an integer.
    """
    pub = {
        k: publication[k]
        for k in PUBLICATION_FIELDS
        if publication.get(k) not in (None, "", [])
    }
    doi = publication.get("doi")
    if not doi and (m := DOI_URL.match(str(pub.get("id", "")))):
        doi = m.group(1)
    if doi:
        pub["id"] = f"doi:{doi}"
    if "year" in pub:
        pub["year"] = int(pub["year"])
    return pub


def convert(page, commit, today):
    """Convert one KG-Registry Resource page into a NAMs registry Resource."""
    entry = {f: page[f] for f in COPIED_FIELDS if page.get(f) not in (None, "", [])}
    if page.get("category"):
        entry["resource_type"] = page["category"]
    if page.get("domains"):
        entry["domain_areas"] = page["domains"]
    for f in ("activity_status", "use_instead"):
        if page.get(f):
            entry[f] = page[f]

    license_ = page.get("license") or {}
    # KG-Registry records some licenses, such as US government works, with an
    # empty id; the NAMs registry leaves the id out instead.
    license_ = {k: license_[k] for k in ("id", "label") if license_.get(k)}
    if license_:
        entry["license"] = license_

    publications = [convert_publication(p) for p in page.get("publications") or []]
    if publications:
        entry["publications"] = publications

    entry["creation_date"] = today
    entry["last_modified_date"] = today
    entry["imported_from"] = [
        {
            "source": "kg_registry",
            "source_id": page["id"],
            "source_url": KG_REGISTRY_PAGE.format(id=page["id"]),
            "source_version": commit,
            "imported_on": today,
        }
    ]
    return entry


def main(argv=None):
    """Run the import."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--kg-registry",
        type=Path,
        default=Path("../kg-registry"),
        help="Path to a local KG-Registry checkout (default: ../kg-registry)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("resources"),
        help="Directory for the resource files (default: resources)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing resource files, discarding any curation in them",
    )
    args = parser.parse_args(argv)

    commit = kg_registry_commit(args.kg_registry)
    today = datetime.date.today().isoformat()
    args.output.mkdir(exist_ok=True)

    written, skipped = [], []
    for path in sorted((args.kg_registry / "resource").glob("*/*.md")):
        page = read_front_matter(path)
        if not page or page.get("layout") != "resource_detail":
            continue
        if "nams" not in (page.get("collection") or []):
            continue
        out = args.output / f"{page['id']}.yaml"
        if out.exists() and not args.overwrite:
            skipped.append(page["id"])
            continue
        with open(out, "w") as fh:
            yaml.safe_dump(
                convert(page, commit, today), fh, sort_keys=False, allow_unicode=True
            )
        written.append(page["id"])

    print(
        f"KG-Registry commit {commit}: wrote {len(written)}, skipped {len(skipped)} existing"
    )
    for rid in skipped:
        print(f"  skipped {rid} (use --overwrite to replace)")


if __name__ == "__main__":
    main()
