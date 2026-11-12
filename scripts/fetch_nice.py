#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright", "pandas", "openpyxl"]
# ///
"""Fetch the NICE data set catalogue, assay list and data set files.

NICE, the NIH Integrated Chemical Environment (https://ice.ntp.niehs.nih.gov/),
is built with Vaadin: the server sends each page's content over a live
browser session, so a plain HTTP request gets only an empty shell. The Data
Sets page (DATASETDESCRIPTION) therefore has to be rendered in a browser.
This script uses Playwright driving an installed Google Chrome. Vaadin keeps
a connection open, so the page never goes network-idle; the script waits for
the load event and then a fixed delay instead.

The other sources need no browser:

- ``api/v1/search`` with no query returns usage text that lists every assay
  name the REST API accepts.
- Each data set's file is at ``downloads/DataonNICE/<file>``, linked from
  the Data Sets table.

Steps, each also available on its own:

- ``catalogue``: render the Data Sets page and parse its table into
  ``datasets.json``: name, chemical, endpoint and record counts, description,
  how the data can be retrieved, download link and version.
- ``assays``: write the API's assay names to ``assays.json``.
- ``download``: download the files linked from ``datasets.json`` into
  ``downloads/``, skipping any larger than ``--max-mb``.
- ``summarize``: for each downloaded spreadsheet, tally the values of its
  assay, species, reference and data type columns into ``summary.json``.

    uv run scripts/fetch_nice.py                      # all four steps
    uv run scripts/fetch_nice.py catalogue assays     # no downloads
    uv run scripts/fetch_nice.py download summarize --max-mb 50
"""

import argparse
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://ice.ntp.niehs.nih.gov/"
USER_AGENT = "nams-registry (https://github.com/monarch-initiative/nams-registry)"
STEPS = ["catalogue", "assays", "download", "summarize"]

# Spreadsheet columns worth tallying: a column is tallied when its name
# contains one of these, ignoring case.
TALLY_COLUMNS = ("assay", "species", "reference", "data type")


def request(url, method="GET"):
    return urllib.request.Request(
        url, method=method, headers={"User-Agent": USER_AGENT}
    )


def render(path, channel, settle_seconds):
    """Open a NICE page in headless Chrome and wait for Vaadin to fill it.

    Returns the Playwright instance, the browser and the page; the caller
    closes the browser and stops Playwright.
    """
    from playwright.sync_api import sync_playwright

    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(channel=channel, headless=True)
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(BASE + path, wait_until="load", timeout=90_000)
        page.wait_for_timeout(settle_seconds * 1000)
    except Exception:
        if browser:
            browser.close()
        playwright.stop()
        raise
    return playwright, browser, page


def parse_count(text, label):
    match = re.search(rf"([\d,]+)\s+{label}", text)
    return int(match.group(1).replace(",", "")) if match else None


def catalogue(out, channel, settle_seconds):
    """Parse the Data Sets table into one record per data set."""
    playwright, browser, page = render("DATASETDESCRIPTION", channel, settle_seconds)
    try:
        rows = page.eval_on_selector_all(
            "table tr",
            """rows => rows.filter(r => r.cells.length >= 4).map(r => ({
                cells: [...r.cells].map(c => c.innerText.trim()),
                links: [...r.querySelectorAll('a[href]')].map(a => [a.innerText.trim(), a.href]),
            }))""",
        )
    finally:
        browser.close()
        playwright.stop()

    datasets = []
    for row in rows:
        name_cell, description, retrieval, version = row["cells"][:4]
        if name_cell == "Toxicity Endpoint":  # the header row
            continue
        downloads = [href for text, href in row["links"] if text == "Download"]
        datasets.append(
            {
                "name": name_cell.splitlines()[0].strip(),
                "chemicals": parse_count(name_cell, "Chemicals"),
                "endpoints": name_cell.splitlines()[2].strip()
                if len(name_cell.splitlines()) > 2
                else None,
                "records": parse_count(name_cell, "Records"),
                "description": re.sub(r"\s*Learn more\.?$", "", description).strip(),
                "retrieval": [
                    line.strip() for line in retrieval.splitlines() if line.strip()
                ],
                "download_url": downloads[0] if downloads else None,
                "version": version,
            }
        )
    if not datasets:
        sys.exit(
            "error: no data sets found on the Data Sets page; the page may not have finished rendering (try --settle 20)"
        )
    (out / "datasets.json").write_text(
        json.dumps(datasets, indent=1, ensure_ascii=False)
    )
    print(f"catalogue: {len(datasets)} data sets", file=sys.stderr)
    return datasets


def assays(out):
    """Write the assay names the REST API lists in its usage text."""
    with urllib.request.urlopen(
        request(BASE + "api/v1/search"), timeout=60
    ) as response:
        text = response.read().decode("utf-8")
    if "Supported assay(s):" not in text:
        sys.exit("error: the API usage text no longer lists supported assays")
    names = sorted(
        set(re.findall(r'"([^"]+)"', text.split("Supported assay(s):", 1)[1]))
    )
    (out / "assays.json").write_text(json.dumps(names, indent=1, ensure_ascii=False))
    print(f"assays: {len(names)} assay names", file=sys.stderr)


def advertised_size(url):
    """Return the Content-Length a HEAD request reports, or None if it can't be had."""
    try:
        with urllib.request.urlopen(request(url, "HEAD"), timeout=60) as response:
            length = response.headers.get("Content-Length")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None
    return int(length) if length and length.isdigit() else None


def fetch_capped(url, path, limit):
    """Stream url to path, stopping once more than limit bytes arrive.

    Returns the number of bytes written, or None if the limit was passed, in
    which case the partial file is removed.
    """
    partial = path.with_name(path.name + ".part")
    written = 0
    with (
        urllib.request.urlopen(request(url), timeout=600) as response,
        partial.open("wb") as handle,
    ):
        while chunk := response.read(1 << 20):
            written += len(chunk)
            if written > limit:
                break
            handle.write(chunk)
    if written > limit:
        partial.unlink()
        return None
    partial.replace(path)
    return written


def download(out, max_mb, pause):
    """Download each data set file no larger than max_mb.

    The size a HEAD request reports is checked first, so a large file is
    skipped without downloading any of it. The limit is also enforced while
    downloading, for a server that reports no size.
    """
    datasets = json.loads((out / "datasets.json").read_text())
    target = out / "downloads"
    target.mkdir(exist_ok=True)
    limit = int(max_mb * 1_000_000)
    skipped = []
    for dataset in datasets:
        url = dataset["download_url"]
        if not url:
            continue
        name = Path(urllib.parse.urlparse(url).path).name
        if not name:
            print(f"download: skipped {url} (no file name in the URL)", file=sys.stderr)
            continue
        size = advertised_size(url)
        if size is not None and size > limit:
            skipped.append({"file": name, "megabytes": round(size / 1_000_000, 1)})
            continue
        written = fetch_capped(url, target / name, limit)
        if written is None:
            skipped.append({"file": name, "megabytes": None})
            continue
        print(f"download: {name} ({written / 1_000_000:.1f} MB)", file=sys.stderr)
        time.sleep(pause)
    for item in skipped:
        size = (
            f"{item['megabytes']} MB"
            if item["megabytes"] is not None
            else "size not reported"
        )
        print(
            f"download: skipped {item['file']} ({size}, over --max-mb)", file=sys.stderr
        )
    return skipped


def summarize(out):
    """Tally the assay, species, reference and data type columns of each spreadsheet."""
    import pandas as pd

    summary = {}
    for path in sorted((out / "downloads").glob("*.xlsx")):
        sheets = {}
        for sheet, frame in pd.read_excel(path, sheet_name=None).items():
            columns = {}
            for column in frame.columns:
                if any(key in str(column).lower() for key in TALLY_COLUMNS):
                    counts = frame[column].dropna().astype(str).value_counts()
                    columns[str(column)] = {
                        "distinct": len(counts),
                        "top": counts.head(50).to_dict(),
                    }
            sheets[sheet] = {
                "rows": len(frame),
                "columns": [str(c) for c in frame.columns],
                "tallies": columns,
            }
        summary[path.name] = sheets
        print(f"summarize: {path.name}", file=sys.stderr)
    (out / "summary.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False, default=int)
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "steps",
        nargs="*",
        metavar="step",
        help=f"Steps to run: {', '.join(STEPS)} (default: all, in that order)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/nice"),
        help="Directory to write into (default: tmp/nice, which git ignores)",
    )
    parser.add_argument(
        "--max-mb",
        type=float,
        default=20,
        help="Skip data set files larger than this (default: 20; the cHTS file is about 190 MB)",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=1.0,
        help="Seconds to wait between downloads (default: 1.0)",
    )
    parser.add_argument(
        "--settle",
        type=int,
        default=10,
        help="Seconds to wait after the page loads for Vaadin to fill it (default: 10)",
    )
    parser.add_argument(
        "--channel",
        default="chrome",
        help="Playwright browser channel (default: chrome, the installed Google Chrome)",
    )
    args = parser.parse_args()
    unknown = sorted(set(args.steps) - set(STEPS))
    if unknown:
        parser.error(
            f"unknown step(s): {', '.join(unknown)}; choose from {', '.join(STEPS)}"
        )
    # Run the chosen steps in pipeline order, whatever order they were given in.
    args.steps = [step for step in STEPS if step in args.steps] if args.steps else STEPS

    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "fetched": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "base": BASE,
        "steps": args.steps,
    }
    if "catalogue" in args.steps:
        manifest["datasets"] = len(catalogue(args.output, args.channel, args.settle))
    if "assays" in args.steps:
        assays(args.output)
    if "download" in args.steps:
        manifest["skipped_downloads"] = download(args.output, args.max_mb, args.pause)
    if "summarize" in args.steps:
        summarize(args.output)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
