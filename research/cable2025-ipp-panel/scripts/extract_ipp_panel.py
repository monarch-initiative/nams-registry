#!/usr/bin/env python3
"""Extract the in vitro pharmacological profiling (IPP) panel from Cable et al. 2025.

Source: the supplementary workbook of

    Cable S, Baltazar MT, Bunglawala F, et al. Advancing systemic toxicity risk
    assessment: evaluation of a NAM-based toolbox approach. Toxicol Sci
    204(1):79-95 (2025). doi:10.1093/toxsci/kfae159

Sheet "S3b. IPP screening %" holds one row per assay well. Each assay name
follows the vendor convention

    <long target name>, <SYMBOL> (<species>) (<mode>)

so the gene symbol is read from between the last comma and the species marker
rather than guessed. Rows beginning with "*" or "**" are the sheet's own
footnotes, not assays.

    uv run --with openpyxl python -I scripts/extract_ipp_panel.py WORKBOOK.xlsx \
        --tsv outputs/ipp_panel_targets.tsv --md outputs/ipp_panel_targets.md

A downloaded workbook is untrusted data. Run this with python -I from a
directory other than the one holding the download, and pass the path as an
argument.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook

SHEET_PREFIX = "S3b"
# "Histamine H1 receptor, HRH1 (h)  (antagonist radioligand)" -> HRH1, h, antagonist...
# Also handles a missing comma ("Kappa-type opioid receptor  OPRK1 (h) ...") and
# no space before the paren ("PTGS1(h)").
ASSAY_RE = re.compile(
    r"^(?P<name>.*?)[,\s]\s*(?P<symbol>[A-Z][A-Z0-9-]{1,9})\s*\((?P<species>[hr])\)"
    r"(?P<rest>.*)$"
)
MODE_RE = re.compile(r"\((?P<mode>agonist|antagonist)[^)]*\)", re.IGNORECASE)
UNAVAILABLE_MARK = "**"


def parse_assay(raw: str) -> dict[str, str]:
    """Split one assay name into target name, symbol, species and assay mode."""
    text = " ".join(raw.split())
    match = ASSAY_RE.match(text)
    if not match:
        # Species-only names such as "Tubulin (r)" carry no symbol field.
        bare = re.match(r"^(?P<name>.*?)\s*\((?P<species>[hr])\)(?P<rest>.*)$", text)
        if bare:
            name = bare.group("name").strip().rstrip(",")
            return {
                "assay_name": raw,
                "target_name": name,
                "symbol": name.upper(),
                "species": bare.group("species"),
                "mode": "",
                "unavailable": str(UNAVAILABLE_MARK in text).lower(),
            }
        return {
            "assay_name": raw,
            "target_name": text,
            "symbol": "",
            "species": "",
            "mode": "",
            "unavailable": str(UNAVAILABLE_MARK in text).lower(),
        }

    mode_match = MODE_RE.search(match.group("rest"))
    return {
        "assay_name": raw,
        "target_name": match.group("name").strip().rstrip(","),
        "symbol": match.group("symbol"),
        "species": match.group("species"),
        "mode": mode_match.group("mode").lower() if mode_match else "",
        "unavailable": str(UNAVAILABLE_MARK in match.group("rest")).lower(),
    }


def load_rows(workbook_path: Path) -> tuple[list[dict[str, str]], int]:
    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    sheet_names = [n for n in workbook.sheetnames if n.strip().startswith(SHEET_PREFIX)]
    if not sheet_names:
        raise SystemExit(f"no sheet starting with {SHEET_PREFIX!r} in {workbook_path}")
    sheet = workbook[sheet_names[0]]

    raw_rows = list(sheet.iter_rows(values_only=True))
    header = raw_rows[0]
    # Columns past RESPONSE/READOUT are one test chemical each.
    chemical_columns = sum(1 for cell in header[3:] if cell)

    records: list[dict[str, str]] = []
    for row in raw_rows[1:]:
        name = row[0]
        if not name or str(name).strip().startswith("*"):
            continue  # footnote row, not an assay
        record = parse_assay(str(name))
        record["ligand_or_control"] = (
            "" if row[1] is None else " ".join(str(row[1]).split())
        )
        record["readout"] = "" if row[2] is None else str(row[2]).strip()
        records.append(record)
    return records, chemical_columns


FAMILY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Monoamine transporter", ("SLC6A2", "SLC6A3", "SLC6A4")),
    (
        "Ion channel",
        ("CACNA1C", "KCNQ1", "SCN5A", "KCNH2", "GRIN1", "GABRA1A", "CHRNA4"),
    ),
    (
        "Enzyme",
        ("ACHE", "PDE3A", "PDE4D", "PTGS1", "PTGS2", "LCK", "ACE2", "CA2", "MAOA"),
    ),
    (
        "Nuclear receptor",
        (
            "AR",
            "NR3C1",
            "NR1I3",
            "PPARA",
            "PPARD",
            "PPARG",
            "NR1I2",
            "PGR",
            "VDR",
            "ER1",
            "ESR2",
            "RARA",
            "RARG",
            "RXRA",
            "RXRB",
            "THRA",
            "THRB",
            "NR3C2",
        ),
    ),
    ("Cytoskeleton", ("TUBULIN",)),
]


def family_of(symbol: str) -> str:
    for family, members in FAMILY_RULES:
        if symbol in members:
            return family
    return "GPCR / other receptor"


def write_tsv(path: Path, records: list[dict[str, str]]) -> None:
    columns = [
        "symbol",
        "target_name",
        "family",
        "species",
        "mode",
        "readout",
        "ligand_or_control",
        "assay_unavailable",
        "assay_name",
    ]
    lines = ["\t".join(columns)]
    for record in sorted(
        records, key=lambda r: (family_of(r["symbol"]), r["symbol"], r["mode"])
    ):
        lines.append(
            "\t".join(
                [
                    record["symbol"],
                    record["target_name"],
                    family_of(record["symbol"]),
                    record["species"],
                    record["mode"],
                    record["readout"],
                    record["ligand_or_control"],
                    record["unavailable"],
                    " ".join(record["assay_name"].split()),
                ]
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_md(path: Path, records: list[dict[str, str]], chemical_columns: int) -> None:
    symbols = [r["symbol"] for r in records if r["symbol"]]
    counts = Counter(symbols)
    by_family: dict[str, set[str]] = defaultdict(set)
    for symbol in symbols:
        by_family[family_of(symbol)].add(symbol)

    unavailable = sorted({r["symbol"] for r in records if r["unavailable"] == "true"})
    paired = sorted(s for s, n in counts.items() if n > 1)
    readouts = Counter(r["readout"] for r in records if r["readout"])

    out = [
        "# IPP panel targets (Cable et al. 2025)",
        "",
        "Extracted from sheet `S3b. IPP screening %` of the supplementary workbook of",
        "doi:10.1093/toxsci/kfae159 by `scripts/extract_ipp_panel.py`. Regenerate rather",
        "than edit.",
        "",
        "## Counts",
        "",
        f"- assay wells: **{len(records)}**",
        f"- distinct targets: **{len(counts)}**",
        f"- test chemicals screened (columns): **{chemical_columns}**",
        f"- targets run as agonist + antagonist pairs: **{len(paired)}**",
        f"- assays marked unavailable by end of study: **{len(unavailable)}**"
        + (f" ({', '.join(unavailable)})" if unavailable else ""),
        "",
        "Readouts:",
        "",
    ]
    out += [f"- {readout}: {n} wells" for readout, n in readouts.most_common()]
    out += ["", "## Targets by family", ""]
    for family, members in sorted(by_family.items()):
        out += [f"### {family} ({len(members)})", "", ", ".join(sorted(members)), ""]
    out += [
        "## Wells",
        "",
        "| Symbol | Target | Family | Mode | Readout |",
        "|---|---|---|---|---|",
    ]
    for record in sorted(
        records, key=lambda r: (family_of(r["symbol"]), r["symbol"], r["mode"])
    ):
        out.append(
            f"| {record['symbol']} | {record['target_name']} | {family_of(record['symbol'])} "
            f"| {record['mode'] or '-'} | {record['readout'] or '-'} |"
        )
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--tsv", type=Path, required=True)
    parser.add_argument("--md", type=Path, required=True)
    args = parser.parse_args()

    records, chemical_columns = load_rows(args.workbook)
    write_tsv(args.tsv, records)
    write_md(args.md, records, chemical_columns)

    counts = Counter(r["symbol"] for r in records if r["symbol"])
    print(f"assay wells      : {len(records)}")
    print(f"distinct targets : {len(counts)}")
    print(f"test chemicals   : {chemical_columns}")
    unresolved = [r["assay_name"] for r in records if not r["symbol"]]
    if unresolved:
        print(f"UNPARSED SYMBOLS : {len(unresolved)}")
        for name in unresolved:
            print(f"  {name}")
    print(f"wrote {args.tsv}")
    print(f"wrote {args.md}")


if __name__ == "__main__":
    main()
