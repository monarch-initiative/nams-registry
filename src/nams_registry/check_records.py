"""Check the ontology terms and the references in the registry's records.

    python -m nams_registry.check_records terms [FILE ...] [--offline]
    python -m nams_registry.check_records references [FILE ...] [--offline]

With no FILE, every NAM record in nams/ is checked, and for references every
resource in resources/ as well.

terms: each ontology term a NAM record binds must exist, sit under the root
of the NAMO enum it is bound to, and carry the ontology's own label. This is
linkml-term-validator. A NAM record's model is checked as the NAMO class its
`type` names, as well as within the record: NAMO puts the bindings on the
subclasses (Organoid, TwoDCellCulture, ...), and the validator does not follow
`type` from the ModelSystem range down to them. conf/oak_config.yaml says
where each ontology is looked up; the answers are kept in cache/.

references: each reference must resolve, and where the record gives its
title, the title must be the reference's own. This is
linkml-reference-validator, set up in .linkml-reference-validator.yaml; each
fetched reference is kept in references_cache/. The references are a NAM
model's `references`, the `supporting_references` of its applications and
limitations, and a resource's `publications`.

--offline uses only cache/ and references_cache/, as the tests do. A term or
reference that is not there yet is an error: run without --offline, then
commit the cache.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
NAMS_DIR = REPO / "nams"
RESOURCES_DIR = REPO / "resources"
NAM_SCHEMA = REPO / "src/nams_registry/schema/nam_records.yaml"
OAK_CONFIG = REPO / "conf/oak_config.yaml"
TERM_CACHE = REPO / "cache"
REFERENCE_CONFIG = REPO / ".linkml-reference-validator.yaml"

DOI_URL = re.compile(r"^https?://(?:dx\.)?doi\.org/(.+)$", re.IGNORECASE)
PUBMED_URL = re.compile(r"^https?://(?:www\.)?(?:pubmed\.)?ncbi\.nlm\.nih\.gov/(?:pubmed/)?(\d+)/?$")


@dataclass(frozen=True)
class Problem:
    path: Path
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.path.relative_to(REPO)}: {self.where}: {self.message}"


def load(path: Path) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


def link_namo() -> None:
    """Put the NAMO schema in place, as scripts/link_namo.py does."""
    script = REPO / "scripts/link_namo.py"
    spec = importlib.util.spec_from_file_location("link_namo", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main(quiet=True)


# ------------------------------------------------------------------ terms


@cache
def term_validator(offline: bool):
    from linkml.validator import Validator
    from linkml_term_validator.plugins import BindingValidationPlugin, DynamicEnumPlugin

    link_namo()
    options = {"cache_dir": str(TERM_CACHE), "oak_config_path": str(OAK_CONFIG), "offline": offline}
    return Validator(
        schema=str(NAM_SCHEMA),
        validation_plugins=[
            DynamicEnumPlugin(**options),
            BindingValidationPlugin(validate_labels=True, **options),
        ],
    )


def term_problems(path: Path, offline: bool = False) -> list[Problem]:
    """What is wrong with the ontology terms of one NAM record."""
    record = load(path)
    validator = term_validator(offline)
    checks = [("record", record, "NAMRecord")]
    model = record.get("model") or {}
    if model.get("type"):
        bare = {k: v for k, v in model.items() if k != "type"}
        checks.append(("model", bare, model["type"]))
    problems = []
    for where, instance, target in checks:
        for result in validator.validate(instance, target_class=target).results:
            context = "; ".join(str(c) for c in result.context or [])
            message = f"{result.message} ({context})" if context else result.message
            problems.append(Problem(path, where, message))
    return problems


# ------------------------------------------------------------- references


@dataclass(frozen=True)
class Citation:
    where: str
    reference: str
    title: str | None


def reference_id(value: str, doi: str | None = None) -> str:
    """The id the reference validator can look up, for an id as written in a record.

    Resources imported from KG-Registry give a publication's id as a URL and
    its DOI separately; the DOI is the reference.
    """
    if doi:
        return f"doi:{doi}"
    if m := DOI_URL.match(value):
        return f"doi:{m.group(1)}"
    if m := PUBMED_URL.match(value):
        return f"PMID:{m.group(1)}"
    if value.startswith(("http://", "https://")):
        return f"url:{value}"
    return value


def citations(path: Path) -> Iterator[Citation]:
    """Every reference a NAM record or a resource cites."""
    record = load(path)
    model = record.get("model") or {}
    for i, ref in enumerate(model.get("references") or []):
        yield Citation(f"model.references[{i}]", reference_id(ref["id"]), ref.get("title"))
    for section in ("applications", "limitations"):
        for i, statement in enumerate(record.get(section) or []):
            for j, ref in enumerate(statement.get("supporting_references") or []):
                yield Citation(f"{section}[{i}].supporting_references[{j}]", reference_id(ref), None)
    for i, pub in enumerate(record.get("publications") or []):
        yield Citation(f"publications[{i}]", reference_id(pub["id"], pub.get("doi")), pub.get("title"))


@cache
def reference_validator():
    from linkml_reference_validator.cli.shared import load_validation_config
    from linkml_reference_validator.validation.supporting_text_validator import (
        SupportingTextValidator,
    )

    config = load_validation_config(REFERENCE_CONFIG)
    config.cache_dir = REPO / config.cache_dir
    return SupportingTextValidator(config)


def reference_problems(path: Path, offline: bool = False) -> list[Problem]:
    """What is wrong with the references one record cites."""
    validator = reference_validator()
    fetcher = validator.fetcher
    problems = []
    for c in citations(path):
        if offline and not fetcher.get_cache_path(fetcher.normalize_reference_id(c.reference)).exists():
            problems.append(
                Problem(path, c.where, f"{c.reference} is not in references_cache/; run `just validate-references`")
            )
            continue
        if fetcher.fetch(c.reference) is None:
            problems.append(Problem(path, c.where, f"{c.reference} could not be fetched; check the identifier"))
            continue
        if c.title:
            result = validator.validate_title(c.reference, expected_title=c.title, path=c.where)
            if not result.is_valid and not result.skipped:
                problems.append(Problem(path, c.where, result.message or f"title does not match {c.reference}"))
    return problems


# ------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("check", choices=["terms", "references"])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--offline", action="store_true", help="use only the committed caches")
    args = parser.parse_args(argv)

    files = [f.resolve() for f in args.files]
    if not files:
        files = sorted(NAMS_DIR.glob("*.yaml"))
        if args.check == "references":
            files += sorted(RESOURCES_DIR.glob("*.yaml"))
    check = term_problems if args.check == "terms" else reference_problems

    problems = []
    for path in files:
        found = check(path, offline=args.offline)
        problems += found
        print(f"{'FAIL' if found else 'ok  '} {path.relative_to(REPO)}")
    for p in problems:
        print(p, file=sys.stderr)
    print(f"\n{len(files)} file(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
