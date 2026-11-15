# Cable et al. 2025: the IPP panel, read from the paper's own workbook

The errata beside
[`cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist.md`](../cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist.errata.md)
says the in vitro pharmacological profiling panel holds 76 assay wells over 64
distinct targets, against the 63 the report and the paper's own main text give.
This directory is where that number comes from. Everything here is a check on
the report, not an output of it.

Paper: Cable S, Baltazar MT, Bunglawala F, et al. "Advancing systemic toxicity
risk assessment: evaluation of a NAM-based toolbox approach." *Toxicological
Sciences* 204(1):79-95 (2025).
doi:[10.1093/toxsci/kfae159](https://doi.org/10.1093/toxsci/kfae159),
PMID 39693112, PMC11879040. Open access.

## Running it

```bash
cd research/cable2025-ipp-panel
./scripts/fetch_inputs.sh                               # once; verifies pinned checksums
uv run --with openpyxl python -I scripts/extract_ipp_panel.py \
    inputs/toxsci-24-0360-File009.xlsx \
    --tsv outputs/ipp_panel_targets.tsv \
    --md  outputs/ipp_panel_targets.md
```

It prints `assay wells: 76`, `distinct targets: 64`, `test chemicals: 38` and
rewrites the two files in `outputs/`, which are committed. A run that changes
them is telling you something: either the workbook moved or the parse did.

## The scripts

**`fetch_inputs.sh`** downloads the paper's two supplementary files into
`inputs/` and verifies each against a pinned sha256. Read its header before
trusting a download — the Europe PMC endpoint fails *by succeeding*, answering
HTTP 200 with a 292-byte XML error body, so the checksum rather than the status
code is what establishes you have the paper's bytes.

**`inspect_xlsx_sheets.py`** prints a workbook's sheet names, dimensions and
header rows. Not part of the extraction: it is how you find out that the panel
lives in a sheet called `S3b. IPP screening %`. Supplementary workbooks
almost never document their own layout, so this is the first thing to run
against a new one.

**`extract_ipp_panel.py`** reads sheet S3b and writes one row per assay well.
Each assay name follows the vendor convention
`<target name>, <SYMBOL> (<species>) (<mode>)`, so the gene symbol is read from
that position rather than found by scanning for capital letters. The sheet's two
`*`-prefixed footnote rows are excluded.

## What the extraction does not settle

The paper's main text builds its 63 as 44 targets from Bowes et al. 2012 plus 19
added for developmental toxicity. The workbook carries 64 symbols. Tubulin is
the one panel member fitting neither stated provenance, which makes
44 + 19 + tubulin = 64 the likeliest reconciliation — and the paper does not say
so, so the errata leaves it open and so should anything built on this. Twelve
nuclear receptors run as agonist and antagonist pairs, which is what separates
76 wells from 64 targets.

## What used to be here

A second step mapped these targets onto DisMech's `kb/`, classifying each as
bound, mentioned in prose, or absent. It was dropped: the targets went into the
registry instead, as `measured_targets` on
[`nams/in-vitro-pharmacological-profiling-panel.yaml`](../../nams/in-vitro-pharmacological-profiling-panel.yaml),
and nothing here needs a DisMech checkout any more.

Three traps that step hit are worth recording, because the next cross-reference
of a panel against a knowledge base will hit them too:

- One row per well is not one row per target. The twelve agonist/antagonist
  pairs have to be collapsed on symbol first.
- The sheet's `ER1` and `GABRA1A` are HGNC's `ESR1` and `GABRA1`. Searching the
  sheet's own spelling reports a gap that is not there.
- Absent means the *symbol* is absent, not the biology. DisMech discusses
  acetylcholinesterase in 34 files without ever binding `ACHE`.

## Inputs are not committed

`inputs/*.xlsx` and `inputs/*.docx` are gitignored — a megabyte of publisher
files that `fetch_inputs.sh` re-fetches against pinned checksums.
[`inputs/README.md`](inputs/README.md) carries the provenance, the checksums and
the sheet inventory, and is committed.
