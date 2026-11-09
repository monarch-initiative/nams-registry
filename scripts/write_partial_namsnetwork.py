#!/usr/bin/env python3
"""Write a partial record for each NAM in the NAMs.network catalogue.

Reads the public catalogue that scripts/fetch_namsnetwork.py writes
(``nams.json``) and writes one PartialNAMRecord (see
src/nams_registry/schema/nam_records.yaml) per NAM into
partial-nams/namsnetwork/.

NAMs.network lists some NAMs more than once, once per endpoint; records whose
names match, ignoring case, spaces and punctuation, are merged into one
partial record. A NAM with a NAM record in nams/, i.e. one whose
source_urls include one of its NAMs.network pages, gets no partial record.
Partial records are rewritten on each run, and those of NAMs no longer listed,
or now named by a NAM record, are removed.

The NAMO class is proposed only when the method type and the NAM's name make
it clear, e.g. "co-culture" in an in vitro NAM's name. NAMO has no class for
in chemico or ex vivo methods.

    uv run python scripts/fetch_namsnetwork.py
    uv run python scripts/write_partial_namsnetwork.py
    uv run python scripts/write_partial_namsnetwork.py --catalogue tmp/namsnetwork/nams.json --accessed-on 2026-11-09
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
        ("CoCulture", r"co-?culture|bi-culture|tri-culture|triple|tetra-culture|quadruple"),
        ("ThreeDCellCulture", r"\b3d\b|spheroid|reconstructed human"),
        ("TwoDCellCulture", r"mono-?culture"),
    ],
    "in silico": [
        ("QSARModel", r"q?sar\b|qspr|structural alert|toxtree|derek"),
        ("PBPKModel", r"\bpb[p]?k\b"),
        ("MLModel", r"machine learning|deep learning|neural network|random forest"),
    ],
}


# Misspellings in the NAMs.network catalogue, corrected in the partial
# records: whole words in any text, and whole values. Kept here, not in the
# partial record files, so
# they survive a rerun. Report new ones to NAMs.network as well.
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
    text = WORD_PATTERN.sub(lambda m: WORD_CORRECTIONS[m.group(1)], " ".join(text.split()))
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


def recorded_pages():
    """The NAMs.network pages that NAM records in nams/ already name."""
    pages = set()
    for path in (ROOT / "nams").glob("*.yaml"):
        record = yaml.safe_load(path.read_text())
        for source in record.get("source_resources", []):
            if source.get("resource") == RESOURCE:
                pages.update(source.get("source_urls", []))
    return pages


def build_partial(rows, accessed_on):
    rows = sorted(rows, key=lambda r: r["qsar_id"])
    name = clean(rows[0]["name"])
    method_type = single(rows, "nam_type")
    linked = lambda facet: lambda r: [v["label"] for v in r["linked"].get(facet, []) if v.get("label")]
    partial = {
        "id": None,  # set by the caller once ids are deduplicated
        "name": name,
        "resource": RESOURCE,
        "source_ids": [str(r["qsar_id"]) for r in rows],
        "source_urls": [PAGE.format(r["qsar_id"]) for r in rows],
        "accessed_on": accessed_on,
        "method_type": method_type,
        "proposed_namo_class": propose_class(method_type, name),
        "development_status": single(rows, "development_status"),
        "endpoints": union(rows, lambda r: [r["endpoint"]]),
        "organs": union(rows, lambda r: [r["organ"]]),
        "cell_lines": union(rows, lambda r: r["cell_types"]),
        "guidelines": union(rows, lambda r: [r["guideline_strategy"]]),
        "regulations": union(rows, lambda r: r["regulations"]),
        "substances": union(rows, linked("substance_name")),
        "methods_biomarkers": union(rows, linked("method_biomarker")),
        "aops": [f"aop:{v}" for v in union(rows, linked("aop"))],
        "key_events": [f"aop.events:{v}" for v in union(rows, linked("key_event"))],
    }
    return {k: v for k, v in partial.items() if k == "id" or v not in (None, [])}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--catalogue", type=Path, default=ROOT / "tmp/namsnetwork/nams.json", help="nams.json from fetch_namsnetwork.py (default: tmp/namsnetwork/nams.json)")
    parser.add_argument("--output", type=Path, default=ROOT / "partial-nams" / RESOURCE, help="Directory to write the partial records into (default: partial-nams/namsnetwork)")
    parser.add_argument("--accessed-on", help="The date the catalogue was fetched (default: the fetched_at date in manifest.json beside the catalogue)")
    args = parser.parse_args()

    accessed_on = args.accessed_on
    if not accessed_on:
        manifest = json.loads((args.catalogue.parent / "manifest.json").read_text())
        accessed_on = manifest["fetched_at"][:10]
    datetime.date.fromisoformat(accessed_on)

    groups = {}
    for row in json.loads(args.catalogue.read_text()):
        groups.setdefault(merge_key(row["name"]), []).append(row)

    recorded = recorded_pages()
    partials, skipped = [], 0
    for rows in groups.values():
        partial = build_partial(rows, accessed_on)
        if recorded.intersection(partial["source_urls"]):
            skipped += 1
            continue
        partials.append(partial)

    # Ids from names; a name that slugs the same as another's gets its first
    # NAMs.network id appended.
    partials.sort(key=lambda s: int(s["source_ids"][0]))
    taken = {}
    for partial in partials:
        record_id = slug(partial["name"])
        if record_id in taken:
            record_id = f"{record_id}-{partial['source_ids'][0]}"
        taken[record_id] = partial
        partial["id"] = record_id

    args.output.mkdir(parents=True, exist_ok=True)
    written = set()
    for partial in partials:
        path = args.output / f"{partial['id']}.yaml"
        path.write_text(yaml.safe_dump(partial, sort_keys=False, allow_unicode=True, width=88))
        written.add(path.name)
    removed = [p for p in args.output.glob("*.yaml") if p.name not in written]
    for path in removed:
        path.unlink()

    classes = {}
    for partial in partials:
        key = partial.get("proposed_namo_class", f"none ({partial['method_type']})")
        classes[key] = classes.get(key, 0) + 1
    print(json.dumps({"partial_records": len(partials), "have_full_record": skipped, "removed": len(removed), "proposed_namo_class": dict(sorted(classes.items(), key=lambda kv: -kv[1]))}, indent=1), file=sys.stderr)


if __name__ == "__main__":
    main()
