#!/usr/bin/env python3
"""Write a NAM record for each ToxCast and Tox21 assay.

Reads what scripts/fetch_toxcast.py saves (``assay_annotations.json`` and the
files beside it) and writes one NAMRecord (see
src/nams_registry/schema/nam_records.yaml) per assay into nams/.

One record per assay, not per endpoint. invitrodb's assay (``aid``) is the
experiment: agonist and antagonist screens are separate assays, e.g.
TOX21_ERa_BLA_Agonist (aid 318) and TOX21_ERa_BLA_Antagonist (aid 319). An
assay's endpoints (``aeid``) are outputs of that one experiment -- detection
channels and their ratio, a cell-viability counter-screen run in the same
wells, a reagent concentration -- so they are readouts on its record, not NAMs
of their own (see CLAUDE.md, "A single NAM can have multiple endpoints").

EPA's values are decoded through conf/toxcast_decoder.yaml, which lists every
value EPA uses in the fields below and what the registry does with it. The
writer only applies that file; a value it does not list is left out and
reported, and ``--check`` exits 1 while any is. What a record holds:

- ``model``: the assay's name and EPA's description of it, with EPA's text
  repaired as the decoder says. No NAMO type: the annotation does not make the
  class clear, and over half the assays are cell-free, for which NAMO has no
  class.
- ``species``: the organism the assay ran in.
- ``measured_targets``: the intended gene targets of the assay's endpoints,
  one per target and measurement, leaving out endpoints the decoder marks as
  not measuring them (viability, background controls). A target is human, with
  HGNC's id and symbol, when HGNC lists the Entrez id EPA gives; it is never
  built from the symbol. Other targets keep EPA's symbol and carry a note.
  EPA's target is what the assay is aimed at, which is not always what it
  reads: H295R steroidogenesis endpoints measure a hormone but name its
  receptor.
- ``source_resources``: ``toxcast`` for every assay, with the assay and
  endpoint ids, the CTX API record of each endpoint, the decoded method type,
  cells and organs, and the AOP-Wiki AOPs and Key Events EPA links to the
  endpoints; ``tox21`` as well for an assay Tox21 ran.

The script owns only the records it writes. A record in nams/ with anything
the script does not write (applications, limitations, another source, ...) has
been curated and is left alone, and an assay that a curated record already
names (by ``aid:`` in a toxcast source_ids) gets no record of its own. The
script's own records are rewritten on each run, so a hand edit to a field it
writes is lost: curate a record by adding to it. Records of assays no longer
returned are removed.

    uv run python scripts/fetch_toxcast.py
    uv run python scripts/write_toxcast.py --check       # exit 1 if the decoder lacks a value
    uv run python scripts/write_toxcast.py --dry-run     # report only, write nothing
    uv run python scripts/write_toxcast.py
"""

import argparse
import datetime
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RESOURCE = "toxcast"
TOX21 = "tox21"
API = "https://comptox.epa.gov/ctx-api"
ENDPOINT_URL = API + "/bioactivity/assay/search/by-aeid/{}"
MAX_ID_LENGTH = 60

#: EPA's identifier for a human gene in ``gene[].organismId``. It is EPA's own,
#: not an NCBI taxon id; DisMech read it off the data (toxcast_assays.py).
HUMAN_GENE_ORGANISM_ID = 1
HUMAN_TAXON = 9606

#: Values EPA uses for "no value".
BLANK = {"", "na", "n/a", "none", "null"}

# The keys a record this script writes can have. A record with any other key
# has been curated, and the script leaves it alone.
RECORD_KEYS = {"model", "species", "measured_targets", "source_resources"}
MODEL_KEYS = {"id", "name", "description", "description_scope"}
TARGET_KEYS = {"name", "gene", "gene_symbol", "measurement", "organism", "notes"}
SOURCE_KEYS = {
    "resource",
    "source_urls",
    "accessed_on",
    "source_ids",
    "method_type",
    "cell_lines",
    "organs",
    "aops",
    "key_events",
}

# Field names of an AOP record from bioactivity/aop/search/by-toxcast-aeid,
# tried in order; any other key ending in "eventNumber" or "aopNumber" is
# taken too, and records with neither are counted in the report.
EVENT_KEYS = ("eventNumber", "keyEventNumber", "eventId")
AOP_KEYS = ("aopNumber", "aopId")


def clean(text):
    """Collapse whitespace; None for a blank or "NA" value."""
    if text is None:
        return None
    text = " ".join(str(text).split())
    return None if text.lower() in BLANK else text


def slug(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if len(text) > MAX_ID_LENGTH:
        text = text[:MAX_ID_LENGTH].rsplit("-", 1)[0]
    return text


def union(values):
    """The non-blank values, in first-seen order, without repeats."""
    seen = {}
    for value in values:
        value = clean(value)
        if value:
            seen.setdefault(value, None)
    return list(seen)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def is_viability(row):
    return bool(row.get("cellViabilityAssay"))


def gene_symbol(gene):
    return clean(gene.get("geneSymbol")) or clean(gene.get("officialSymbol"))


def aop_numbers(records):
    """The Key Event and AOP numbers in an endpoint's AOP records, and how many records had neither."""
    events, aops, unparsed = [], [], 0
    for record in as_list(records):
        if not isinstance(record, dict):
            unparsed += 1
            continue
        found = False
        for key, value in record.items():
            number = str(value).strip()
            if not number.isdigit():
                continue
            if key in EVENT_KEYS or key.lower().endswith("eventnumber"):
                events.append(str(int(number)))
                found = True
            elif key in AOP_KEYS or key.lower().endswith("aopnumber"):
                aops.append(str(int(number)))
                found = True
        unparsed += not found
    return events, aops, unparsed


MODE_IN_NAME = re.compile(r"(?i)(?:^|_)(agonist|antagonist)(?:_|$)")


class Decoder:
    """conf/toxcast_decoder.yaml: EPA's values, and what the registry does with each.

    Every lookup goes through here, and a value the decoder does not list is
    recorded in ``missing`` by field rather than guessed at.
    """

    def __init__(self, path):
        tables = yaml.safe_load(Path(path).read_text())
        self.repairs = tables.get("text_repairs") or {}
        self.tables = {
            field: {clean(k): v for k, v in (tables.get(field) or {}).items()}
            for field in (
                "method_type",
                "cell_format",
                "tissue",
                "cells",
                "function_type",
            )
        }
        self.missing = {field: Counter() for field in self.tables}
        self.organism_ids = {
            int(k): v for k, v in (tables.get("organism_id") or {}).items()
        }

    def taxon(self, row):
        """The assay's NCBI taxon id, corrected where the decoder says EPA's is wrong.

        A correction applies only while EPA's organism name is the one the
        decoder expects, so a later fix upstream is not overridden blindly.
        """
        taxon = row.get("organismId")
        if not taxon:
            return None
        fix = self.organism_ids.get(int(taxon))
        if fix and clean(row.get("organism")) == fix.get("organism"):
            return fix["taxon"]
        return int(taxon)

    def repair(self, value):
        """Apply the text repairs to every string in a parsed JSON value."""
        if isinstance(value, str):
            for bad, good in self.repairs.items():
                value = value.replace(bad, good)
            return value
        if isinstance(value, list):
            return [self.repair(v) for v in value]
        if isinstance(value, dict):
            return {k: self.repair(v) for k, v in value.items()}
        return value

    def lookup(self, field, value):
        """The decoder's entry for a value; None, and recorded as missing, if it has none."""
        value = clean(value)
        if value is None:
            return None
        table = self.tables[field]
        if value not in table:
            self.missing[field][value] += 1
            return None
        return table[value]

    def method_type(self, row):
        return self.lookup("method_type", row.get("assayFormatType"))

    def cells(self, row):
        """The cells an endpoint's test system is made of, as decoder entries.

        Empty when the assay is cell-free: a cell line EPA names there only
        produced the protein.
        """
        if self.lookup("cell_format", row.get("cellFormat")) != "test_system":
            return []
        return as_list(self.lookup("cells", row.get("cellShortName")))

    def organs(self, row):
        """The organs for an endpoint: a cell's own organ where the decoder gives
        one, otherwise EPA's tissue when it is an organ."""
        cells = self.cells(row)
        if len(cells) == 1 and "organ" in cells[0]:
            organ = cells[0]["organ"]
            return [organ] if organ else []
        entry = self.lookup("tissue", row.get("tissue"))
        return [entry["organ"]] if entry and entry.get("organ") else []

    def measurement(self, row):
        """(writes targets, measurement) for an endpoint, from its function type."""
        entry = self.lookup("function_type", row.get("assayFunctionType"))
        if entry is None:
            return True, None
        if entry.get("targets") is False:
            return False, None
        if entry.get("mode_from_name"):
            match = MODE_IN_NAME.search(row.get("assayName") or "")
            return True, match.group(1).lower() if match else None
        return True, entry.get("measurement")


class Inputs:
    """What fetch_toxcast.py saved, read from one directory."""

    def __init__(self, directory, decoder):
        directory = Path(directory)
        self.decoder = decoder
        self.endpoints = decoder.repair(
            json.loads((directory / "assay_annotations.json").read_text())
        )
        aops = directory / "aops.json"
        self.aops = json.loads(aops.read_text()) if aops.exists() else None
        self.hgnc = json.loads((directory / "hgnc.json").read_text())
        self.taxa = json.loads((directory / "taxa.json").read_text())
        manifest = directory / "manifest.json"
        self.manifest = json.loads(manifest.read_text()) if manifest.exists() else {}

    def assays(self):
        """The endpoints grouped by assay id, each group sorted by endpoint id."""
        groups = {}
        for row in self.endpoints:
            groups.setdefault(int(row["aid"]), []).append(row)
        return {
            aid: sorted(rows, key=lambda r: int(r["aeid"]))
            for aid, rows in sorted(groups.items())
        }

    def organism(self, taxon_id):
        label = self.taxa.get(str(int(taxon_id)))
        return {"id": f"NCBITaxon:{int(taxon_id)}", "name": label} if label else None


def measured_targets(rows, inputs, report):
    """One target per gene and function type, from the non-viability endpoints."""
    targets = {}
    for row in rows:
        if is_viability(row):
            continue
        writes_targets, measurement = inputs.decoder.measurement(row)
        if not writes_targets:
            continue
        for gene in as_list(row.get("gene")):
            if not isinstance(gene, dict):
                continue
            symbol = gene_symbol(gene)
            if not symbol:
                report["targets_without_symbol"] += 1
                continue
            key = (symbol, measurement)
            if key in targets:
                continue
            target = {"name": symbol}
            entrez = gene.get("entrezGeneId")
            entrez = str(int(entrez)) if isinstance(entrez, (int, float)) else None
            # An Entrez id names one gene in one species, and HGNC lists only
            # human genes, so HGNC listing the id is what makes a target human.
            # EPA's own gene organismId is not used: the API returns it null.
            hgnc = inputs.hgnc.get(entrez) if entrez else None
            if hgnc:
                target["gene"] = hgnc["hgnc_id"]
                target["gene_symbol"] = hgnc["symbol"]
                report["human_targets_resolved"] += 1
                if hgnc["symbol"] != symbol:
                    report["symbol_differs_from_hgnc"].add(
                        f"{symbol} -> {hgnc['symbol']}"
                    )
            elif gene.get("organismId") == HUMAN_GENE_ORGANISM_ID:
                report["human_targets_unresolved"].add(symbol)
                target["notes"] = (
                    f"EPA lists a human gene, Entrez {entrez or 'id not given'}, "
                    "that is not an approved gene in HGNC, so no HGNC id."
                )
            else:
                report["targets_not_in_hgnc"] += 1
                target["notes"] = (
                    f"Entrez {entrez or 'id not given'} is not an approved human gene "
                    "in HGNC, so no HGNC id."
                )
            if measurement:
                target["measurement"] = measurement
            if "gene" in target:
                human = inputs.organism(HUMAN_TAXON)
                if human:
                    target["organism"] = human
            # Keys in the schema's order.
            targets[key] = {
                k: target[k]
                for k in (
                    "name",
                    "gene",
                    "gene_symbol",
                    "measurement",
                    "organism",
                    "notes",
                )
                if k in target
            }
    return sorted(
        targets.values(), key=lambda t: (t["name"].upper(), t.get("measurement") or "")
    )


def build_record(aid, rows, inputs, accessed_on, report):
    decoder = inputs.decoder
    name = union(r.get("assayName") for r in rows)
    name = name[0] if name else f"ToxCast assay {aid}"
    description = union(r.get("assayDesc") for r in rows)
    model = {"id": None, "name": name}  # id set by the caller once ids are deduplicated
    if description:
        model["description"] = description[0]
        model["description_scope"] = "METHOD"

    record = {"model": model}
    species = []
    for taxon_id in union(str(decoder.taxon(r) or "") for r in rows):
        organism = inputs.organism(taxon_id)
        if organism:
            species.append(organism)
        else:
            report["taxa_without_label"].add(taxon_id)
    if species:
        record["species"] = species
    targets = measured_targets(rows, inputs, report)
    if targets:
        record["measured_targets"] = targets

    events, aops = [], []
    if inputs.aops is not None:
        for row in rows:
            found = inputs.aops.get(str(row["aeid"]))
            if found:
                report["endpoints_with_aop_records"] += 1
            e, a, unparsed = aop_numbers(found)
            events += e
            aops += a
            report["aop_records_unparsed"] += unparsed
            if unparsed and not report["aop_record_example"]:
                report["aop_record_example"] = as_list(found)[0]

    source = {
        "resource": RESOURCE,
        "source_urls": [ENDPOINT_URL.format(r["aeid"]) for r in rows],
        "accessed_on": accessed_on,
        "source_ids": [f"aid:{aid}"] + [f"aeid:{r['aeid']}" for r in rows],
        "method_type": "; ".join(union(decoder.method_type(r) for r in rows)) or None,
        "cell_lines": union(c["name"] for r in rows for c in decoder.cells(r)),
        "organs": union(o for r in rows for o in decoder.organs(r)),
        "aops": [f"aop:{n}" for n in union(aops)],
        "key_events": [f"aop.events:{n}" for n in union(events)],
    }
    sources = [{k: v for k, v in source.items() if v not in (None, [])}]
    if any(clean(r.get("assaySourceName")) == "TOX21" for r in rows):
        sources.append(
            {
                "resource": TOX21,
                "accessed_on": accessed_on,
                "source_ids": [f"aid:{aid}"],
            }
        )
    record["source_resources"] = sources
    return record


def is_generated(record):
    """Whether a record in nams/ is one this script writes, not a curated one."""
    sources = record.get("source_resources") or []
    resources = [s.get("resource") for s in sources]
    return (
        set(record) <= RECORD_KEYS
        and set(record.get("model") or {}) <= MODEL_KEYS
        and all(set(t) <= TARGET_KEYS for t in record.get("measured_targets") or [])
        and RESOURCE in resources
        and set(resources) <= {RESOURCE, TOX21}
        and all(set(s) <= SOURCE_KEYS for s in sources)
    )


def read_nams(nams_dir):
    """The records in nams/, split into this script's and curated ones, by path."""
    generated, curated = {}, {}
    for path in sorted(nams_dir.glob("*.yaml")):
        record = yaml.safe_load(path.read_text())
        (generated if is_generated(record) else curated)[path] = record
    return generated, curated


def curated_aids(curated):
    """The ToxCast assay ids that curated NAM records name."""
    aids = set()
    for record in curated.values():
        for source in record.get("source_resources", []):
            if source.get("resource") == RESOURCE:
                for source_id in source.get("source_ids", []):
                    if str(source_id).startswith("aid:"):
                        aids.add(int(str(source_id)[4:]))
    return aids


def possible_overlaps(assays, curated):
    """Curated records whose id names a cell line or tissue system a ToxCast assay ran in.

    A lead for a person to check, not a match: a curated record of the H295R
    steroidogenesis assay is the same method as ToxCast's CEETOX_H295R assays,
    while a HepG2 spheroid record is not the same as a HepG2 reporter assay.
    """
    cells = {}
    for aid, rows in assays.items():
        for cell in union(r.get("cellShortName") for r in rows):
            key = re.sub(r"[^a-z0-9]", "", cell.lower())
            if len(key) >= 4:
                cells.setdefault(key, set()).add(aid)
    leads = {}
    for path in curated:
        compact = path.stem.replace("-", "")
        for key, aids in cells.items():
            if key in compact:
                leads.setdefault(path.stem, {}).update({key: len(aids)})
    return leads


def summarise(assays, records, report, leads, skipped, changes):
    counts = Counter()
    for rows in assays.values():
        counts["endpoints"] += len(rows)
    lines = [
        f"endpoints                    : {counts['endpoints']}",
        f"assays (records)             : {len(assays)}",
        f"  named by a curated record  : {len(skipped)}"
        + (f" ({', '.join(f'aid:{a}' for a in sorted(skipped))})" if skipped else ""),
        "",
        "assays by source             : "
        + ", ".join(
            f"{k} {v}"
            for k, v in Counter(
                clean(rows[0].get("assaySourceName")) or "blank"
                for rows in assays.values()
            ).most_common()
        ),
        "assays by format             : "
        + ", ".join(
            f"{k} {v}"
            for k, v in Counter(
                clean(rows[0].get("assayFormatType")) or "blank"
                for rows in assays.values()
            ).most_common()
        ),
        "assays by cell format        : "
        + ", ".join(
            f"{k} {v}"
            for k, v in Counter(
                clean(rows[0].get("cellFormat")) or "blank" for rows in assays.values()
            ).most_common()
        ),
        "",
    ]
    endpoints_per_assay = Counter(len(rows) for rows in assays.values())
    lines.append(
        "endpoints per assay          : "
        + ", ".join(f"{n}: {c} assays" for n, c in sorted(endpoints_per_assay.items()))
    )
    viability_only = [
        aid for aid, rows in assays.items() if all(is_viability(r) for r in rows)
    ]
    lines.append(f"viability-only assays        : {len(viability_only)}")

    followups = {
        aid: rows
        for aid, rows in assays.items()
        if "followup" in (rows[0].get("assayName") or "").lower()
    }
    names = {
        (rows[0].get("assayName") or "").lower(): aid for aid, rows in assays.items()
    }
    with_base = sum(
        1
        for rows in followups.values()
        if re.sub(r"_?followup", "", (rows[0].get("assayName") or "").lower()) in names
    )
    lines.append(
        f"follow-up assays             : {len(followups)} ({with_base} with a same-named original assay)"
    )
    lines.append("")

    multi = sorted(
        (
            (
                len({t["name"].upper() for t in r.get("measured_targets", [])}),
                r["model"]["name"],
                aid,
            )
            for aid, r in records.items()
        ),
        reverse=True,
    )
    multi = [m for m in multi if m[0] > 1]
    lines.append(f"assays with >1 target        : {len(multi)}")
    for n, name, aid in multi[:20]:
        lines.append(f"    {n:4d} targets  aid:{aid}  {name}")
    if len(multi) > 20:
        lines.append(f"    ... and {len(multi) - 20} more")
    lines += [
        "",
        f"human targets with HGNC id   : {report['human_targets_resolved']}",
        f"human targets not in HGNC    : {len(report['human_targets_unresolved'])}"
        + (
            f" ({', '.join(sorted(report['human_targets_unresolved']))})"
            if report["human_targets_unresolved"]
            else ""
        ),
        f"EPA symbol differs from HGNC : {len(report['symbol_differs_from_hgnc'])}"
        + (
            f" ({', '.join(sorted(report['symbol_differs_from_hgnc']))})"
            if report["symbol_differs_from_hgnc"]
            else ""
        ),
        f"targets not in HGNC          : {report['targets_not_in_hgnc']}",
        f"gene objects with no symbol  : {report['targets_without_symbol']}",
        f"taxa with no label           : {len(report['taxa_without_label'])}"
        + (
            f" ({', '.join(sorted(report['taxa_without_label']))})"
            if report["taxa_without_label"]
            else ""
        ),
        "",
    ]
    if report["aops_fetched"]:
        lines.append(
            f"endpoints with AOP records   : {report['endpoints_with_aop_records']}"
        )
        lines.append(
            f"assays with Key Events       : {sum(1 for r in records.values() if r['source_resources'][0].get('key_events'))}"
        )
        lines.append(f"AOP records not understood   : {report['aop_records_unparsed']}")
        if report["aop_record_example"]:
            lines.append(
                f"    example: {json.dumps(report['aop_record_example'])[:300]}"
            )
    else:
        lines.append("AOP records                  : not fetched (aops.json absent)")
    lines.append("")
    lines.append(
        f"possible overlaps with curated records, by cell line in the record id: {len(leads)}"
    )
    for stem, keys in sorted(leads.items()):
        lines.append(
            f"    {stem}: "
            + ", ".join(f"{k} ({n} assays)" for k, n in sorted(keys.items()))
        )
    lines.append("")
    lines.append(
        "records                      : "
        + ", ".join(f"{k} {v}" for k, v in changes.items())
    )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "tmp/toxcast",
        help="Directory fetch_toxcast.py wrote (default: tmp/toxcast)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "nams",
        help="Directory of NAM records to write into (default: nams)",
    )
    parser.add_argument(
        "--accessed-on",
        help="The date the annotations were fetched (default: the fetched_at date in manifest.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be written, and write nothing",
    )
    parser.add_argument(
        "--decoder",
        type=Path,
        default=ROOT / "conf/toxcast_decoder.yaml",
        help="The decoder tables (default: conf/toxcast_decoder.yaml)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Write nothing, and exit 1 if any EPA value is missing from the decoder",
    )
    args = parser.parse_args(argv)
    if args.check:
        args.dry_run = True

    decoder = Decoder(args.decoder)
    inputs = Inputs(args.input, decoder)
    accessed_on = args.accessed_on or inputs.manifest.get("fetched_at", "")[:10]
    if not accessed_on:
        sys.exit(
            "no fetch date: pass --accessed-on, or keep manifest.json beside the annotations"
        )
    datetime.date.fromisoformat(accessed_on)

    report = {
        "human_targets_resolved": 0,
        "human_targets_unresolved": set(),
        "symbol_differs_from_hgnc": set(),
        "targets_not_in_hgnc": 0,
        "targets_without_symbol": 0,
        "taxa_without_label": set(),
        "aops_fetched": inputs.aops is not None,
        "endpoints_with_aop_records": 0,
        "aop_records_unparsed": 0,
        "aop_record_example": None,
    }

    args.output.mkdir(parents=True, exist_ok=True)
    generated, curated = read_nams(args.output)
    skipped = curated_aids(curated)
    assays = inputs.assays()
    records = {
        aid: build_record(aid, rows, inputs, accessed_on, report)
        for aid, rows in assays.items()
        if aid not in skipped
    }

    # Ids from names; a name that slugs the same as another's, or as a
    # curated record's id, gets its assay id appended.
    taken = {path.stem for path in curated}
    for aid, record in records.items():
        record_id = slug(record["model"]["name"]) or f"toxcast-assay-{aid}"
        if record_id in taken:
            record_id = f"{record_id}-aid{aid}"
        taken.add(record_id)
        record["model"]["id"] = record_id

    changes = Counter()
    written = set()
    for record in records.values():
        path = args.output / f"{record['model']['id']}.yaml"
        text = yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=88)
        if not path.exists():
            changes["new"] += 1
        elif path.read_text() != text:
            changes["changed"] += 1
        else:
            changes["unchanged"] += 1
        if not args.dry_run:
            path.write_text(text)
        written.add(path)
    removed = [path for path in generated if path not in written]
    changes["removed"] = len(removed)
    if not args.dry_run:
        for path in removed:
            path.unlink()

    leads = possible_overlaps(assays, curated)
    print(summarise(assays, records, report, leads, skipped, changes), file=sys.stderr)
    missing = {f: c for f, c in decoder.missing.items() if c}
    print(
        f"\nvalues not in the decoder    : {sum(len(c) for c in missing.values())}",
        file=sys.stderr,
    )
    for field, values in missing.items():
        for value, n in values.most_common():
            print(f"    {field}: {value!r} ({n} uses, left out)", file=sys.stderr)
    if args.dry_run:
        print("\ndry run: nothing written", file=sys.stderr)
    return 1 if args.check and missing else 0


if __name__ == "__main__":
    sys.exit(main())
