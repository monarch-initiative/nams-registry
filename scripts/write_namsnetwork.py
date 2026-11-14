#!/usr/bin/env python3
"""Write a NAM record for each NAM in the NAMs.network catalogue.

Reads the public catalogue that scripts/fetch_namsnetwork.py writes
(``nams.json``) and writes one NAMRecord (see
src/nams_registry/schema/nam_records.yaml) per NAM into nams/. Each record
holds only what the public catalogue gives, on its namsnetwork source
record, and sets vendor_holds_more_details, because a NAM's full record on
NAMs.network needs a logged-in account.

NAMs.network lists some NAMs more than once, once per endpoint; records whose
names match, ignoring case, spaces and punctuation, are merged into one
record. The script owns only the records it writes: a record in nams/ that
holds anything more (a description, species, another source, ...) has been
curated, and is left alone, and no record is written for its NAMs.network
pages. The script's own records are rewritten on each run, and those of NAMs
no longer listed, or now named by a curated record, are removed.

The model's NAMO class is set only when the method type and the NAM's name
make it clear, e.g. "co-culture" in an in vitro NAM's name; otherwise the
model has no type. NAMO has no class for in chemico or ex vivo methods.

    uv run python scripts/fetch_namsnetwork.py
    uv run python scripts/write_namsnetwork.py
    uv run python scripts/write_namsnetwork.py --catalogue tmp/namsnetwork/nams.json --accessed-on 2026-11-09
"""

import argparse
import datetime
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RESOURCE = "namsnetwork"
PAGE = "https://nams.network/details/{}"
MAX_ID_LENGTH = 60

# Name patterns that make the NAMO class clear, by method type, checked in
# order: the first match wins.
CLASS_PATTERNS = {
    "in vitro": [
        ("Organoid", r"organoid|bronchosphere|alveolosphere|tracheosphere"),
        ("OrganOnChip", r"on[- ]a[- ]chip|organ[- ]on|lung[- ]on|\bchip\b"),
        (
            "CoCulture",
            r"co-?culture|bi-culture|tri-culture|triple|tetra-culture|quadruple",
        ),
        ("ThreeDCellCulture", r"\b3d\b|spheroid|reconstructed human"),
        ("TwoDCellCulture", r"mono-?culture"),
    ],
    "in silico": [
        ("QSARModel", r"q?sar\b|qspr|structural alert|toxtree|derek"),
        ("PBPKModel", r"\bpb[p]?k\b"),
        ("MLModel", r"machine learning|deep learning|neural network|random forest"),
    ],
}


# Misspellings in the NAMs.network catalogue, corrected in the records:
# whole words in any text, and whole values. Kept here, not in the record
# files, so they survive a rerun. Report new ones to NAMs.network as well.
WORD_CORRECTIONS = {
    "hormons": "hormone",
    "particlen": "particle",
    "relsease": "release",
    "stategy": "strategy",
}
VALUE_CORRECTIONS = {
    # Regulation (EU) 2015/2283 on novel foods, which the catalogue mostly
    # writes correctly; these spellings have no title or link in its records.
    "(EC) 2015/2283": "(EU) 2015/2283",
    "(EU) 2283/2015": "(EU) 2015/2283",
}
WORD_PATTERN = re.compile(r"\b(" + "|".join(WORD_CORRECTIONS) + r")\b")


def clean(text):
    """Collapse whitespace, including non-breaking spaces, and correct known misspellings."""
    if not text:
        return text
    text = WORD_PATTERN.sub(
        lambda m: WORD_CORRECTIONS[m.group(1)], " ".join(text.split())
    )
    return VALUE_CORRECTIONS.get(text, text)


def merge_key(name):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", name).lower())


def slug(name):
    # Trademark signs, including "TM" written out: EpiDermTM, EpiDerm TM.
    name = re.sub(r"[™®©]|(?<=[a-z])TM\b|\bTM\b", "", name)
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if len(text) > MAX_ID_LENGTH:
        text = text[:MAX_ID_LENGTH].rsplit("-", 1)[0]
    return text


def propose_class(method_type, name):
    for namo_class, pattern in CLASS_PATTERNS.get(method_type, []):
        if re.search(pattern, name, re.I):
            return namo_class
    return None


def union(rows, get):
    """The values across rows, in first-seen order, without repeats."""
    seen = {}
    for row in rows:
        for value in get(row):
            value = clean(value)
            if value:
                seen.setdefault(value, None)
    return list(seen)


def single(rows, field):
    values = union(rows, lambda r: [r[field]])
    if len(values) > 1:
        raise ValueError(f"{rows[0]['name']!r}: records disagree on {field}: {values}")
    return values[0] if values else None


# The keys a record this script writes can have. A record with any other key
# has been curated, and the script leaves it alone.
RECORD_KEYS = {"model", "source_resources", "vendor_holds_more_details"}
MODEL_KEYS = {"id", "type", "name"}
SOURCE_KEYS = {
    "resource",
    "source_urls",
    "accessed_on",
    "source_ids",
    "method_type",
    "development_status",
    "endpoints",
    "organs",
    "cell_lines",
    "guidelines",
    "regulations",
    "substances",
    "methods_biomarkers",
    "aops",
    "key_events",
}


def is_generated(record):
    """Whether a record in nams/ is one this script writes, not a curated one."""
    sources = record.get("source_resources") or []
    return (
        set(record) <= RECORD_KEYS
        and set(record.get("model") or {}) <= MODEL_KEYS
        and len(sources) == 1
        and sources[0].get("resource") == RESOURCE
        and set(sources[0]) <= SOURCE_KEYS
    )


def read_nams(nams_dir):
    """The records in nams/, split into this script's and curated ones, by path."""
    generated, curated = {}, {}
    for path in sorted(nams_dir.glob("*.yaml")):
        record = yaml.safe_load(path.read_text())
        (generated if is_generated(record) else curated)[path] = record
    return generated, curated


def recorded_pages(curated):
    """The NAMs.network pages that curated NAM records name."""
    pages = set()
    for record in curated.values():
        for source in record.get("source_resources", []):
            if source.get("resource") == RESOURCE:
                pages.update(source.get("source_urls", []))
    return pages


def linked_labels(facet, row):
    """The labels of the facet values linked to a catalogue row."""
    return [v["label"] for v in row["linked"].get(facet, []) if v.get("label")]


def build_record(rows, accessed_on):
    rows = sorted(rows, key=lambda r: r["qsar_id"])
    name = clean(rows[0]["name"])
    method_type = single(rows, "nam_type")

    def linked(facet):
        return union(rows, lambda r: linked_labels(facet, r))

    model = {
        "id": None,  # set by the caller once ids are deduplicated
        "type": propose_class(method_type, name),
        "name": name,
    }
    source = {
        "resource": RESOURCE,
        "source_urls": [PAGE.format(r["qsar_id"]) for r in rows],
        "accessed_on": accessed_on,
        "source_ids": [str(r["qsar_id"]) for r in rows],
        "method_type": method_type,
        "development_status": single(rows, "development_status"),
        "endpoints": union(rows, lambda r: [r["endpoint"]]),
        "organs": union(rows, lambda r: [r["organ"]]),
        "cell_lines": union(rows, lambda r: r["cell_types"]),
        "guidelines": union(rows, lambda r: [r["guideline_strategy"]]),
        "regulations": union(rows, lambda r: r["regulations"]),
        "substances": linked("substance_name"),
        "methods_biomarkers": linked("method_biomarker"),
        "aops": [f"aop:{v}" for v in linked("aop")],
        "key_events": [f"aop.events:{v}" for v in linked("key_event")],
    }
    return {
        "model": {k: v for k, v in model.items() if k == "id" or v is not None},
        "vendor_holds_more_details": True,
        "source_resources": [{k: v for k, v in source.items() if v not in (None, [])}],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=ROOT / "tmp/namsnetwork/nams.json",
        help="nams.json from fetch_namsnetwork.py (default: tmp/namsnetwork/nams.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "nams",
        help="Directory of NAM records to write into (default: nams)",
    )
    parser.add_argument(
        "--accessed-on",
        help="The date the catalogue was fetched (default: the fetched_at date in manifest.json beside the catalogue)",
    )
    args = parser.parse_args()

    accessed_on = args.accessed_on
    if not accessed_on:
        manifest = json.loads((args.catalogue.parent / "manifest.json").read_text())
        accessed_on = manifest["fetched_at"][:10]
    datetime.date.fromisoformat(accessed_on)

    groups = {}
    for row in json.loads(args.catalogue.read_text()):
        groups.setdefault(merge_key(row["name"]), []).append(row)

    args.output.mkdir(parents=True, exist_ok=True)
    generated, curated = read_nams(args.output)
    recorded = recorded_pages(curated)
    records, skipped = [], 0
    for rows in groups.values():
        record = build_record(rows, accessed_on)
        if recorded.intersection(record["source_resources"][0]["source_urls"]):
            skipped += 1
            continue
        records.append(record)

    # Ids from names; a name that slugs the same as another's, or as a
    # curated record's id, gets its first NAMs.network id appended.
    def first_id(record):
        return record["source_resources"][0]["source_ids"][0]

    records.sort(key=lambda r: int(first_id(r)))
    taken = {path.stem for path in curated}
    for record in records:
        record_id = slug(record["model"]["name"])
        if record_id in taken:
            record_id = f"{record_id}-{first_id(record)}"
        taken.add(record_id)
        record["model"]["id"] = record_id

    written = set()
    for record in records:
        path = args.output / f"{record['model']['id']}.yaml"
        path.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=88)
        )
        written.add(path)
    removed = [path for path in generated if path not in written]
    for path in removed:
        path.unlink()

    classes = {}
    for record in records:
        key = record["model"].get(
            "type", f"none ({record['source_resources'][0]['method_type']})"
        )
        classes[key] = classes.get(key, 0) + 1
    print(
        json.dumps(
            {
                "records": len(records),
                "have_curated_record": skipped,
                "removed": len(removed),
                "namo_class": dict(sorted(classes.items(), key=lambda kv: -kv[1])),
            },
            indent=1,
        ),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
