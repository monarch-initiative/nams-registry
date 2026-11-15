#!/usr/bin/env python3
"""Print the sheet names, dimensions and first rows of an .xlsx workbook.

A supplementary workbook from a paper rarely documents its own layout, so this
is the first thing to run against one: it says which sheets exist and what the
header rows look like, which is enough to decide which sheet answers a question.

    uv run --with openpyxl python -I scripts/inspect_xlsx_sheets.py WORKBOOK.xlsx
    uv run --with openpyxl python -I scripts/inspect_xlsx_sheets.py WORKBOOK.xlsx --rows 10

A downloaded workbook is untrusted data. Run this with python -I, from a
directory that is not the one holding the download, and pass the path as an
argument -- never cd into the download directory and run an interpreter there.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import load_workbook

CELL_WIDTH = 28


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path, help="path to the .xlsx file")
    parser.add_argument(
        "--rows", type=int, default=4, help="header rows to show per sheet (default 4)"
    )
    parser.add_argument(
        "--cols", type=int, default=9, help="columns to show per row (default 9)"
    )
    args = parser.parse_args()

    workbook = load_workbook(args.workbook, read_only=True, data_only=True)
    print(f"WORKBOOK: {args.workbook.name}")
    print(f"SHEETS ({len(workbook.sheetnames)}): {workbook.sheetnames}")

    for name in workbook.sheetnames:
        sheet = workbook[name]
        print(f"\n--- {name} ({sheet.max_row} x {sheet.max_column}) ---")
        for index, row in enumerate(sheet.iter_rows(values_only=True)):
            if index >= args.rows:
                break
            cells = [
                "" if cell is None else str(cell)[:CELL_WIDTH]
                for cell in row[: args.cols]
            ]
            print(cells)


if __name__ == "__main__":
    main()
