#!/usr/bin/env python3
"""Fetch EPA's ToxCast and Tox21 assay annotations through the CTX API.

EPA's CompTox Chemicals Dashboard APIs (CTX) describe every ToxCast and Tox21
assay endpoint: the assay it belongs to, its readout, its intended gene
target, the cells or cell-free system it runs in, and which way a hit reads.
invitrodb, EPA's database behind them, has three levels: an assay (``aid``),
its components (``acid``) and their endpoints (``aeid``). The API returns one
object per endpoint, each carrying the ids of all three, so
scripts/write_toxcast.py can group them back into assays.

Adapted from DisMech's src/dismech/toxcast_assays.py (``just
toxcast-refresh``), which fetches the same annotations for its pathograph
coverage analysis (dismech#12858). This copy saves what the registry needs to
write NAM records and nothing about chemical results.

Writes, into the output directory:

- ``assay_annotations.json``: the API's endpoint objects, as returned.
- ``aops.json``: for each endpoint, what ``bioactivity/aop/search/by-toxcast-aeid``
  returns, the AOP-Wiki Key Events and AOPs EPA links it to. Most are empty.
- ``hgnc.json``: HGNC's approved genes keyed by Entrez id, from HGNC's own
  complete set, so a target's HGNC id is read from HGNC, never built from its
  symbol.
- ``taxa.json``: the NCBI Taxonomy label of each organism the assays name,
  from OLS.
- ``manifest.json``: the fetch time, the sources, the counts, and any request
  that failed.

Needs CTX_API_KEY in the environment; a free key is requested from
ccte_api@epa.gov. Never write the key into a file in the repository. The API
has no version endpoint, so the invitrodb release cannot be recorded; the
fetch date is the provenance. A full run is one annotation request plus one
AOP request per endpoint (about 1,600), roughly 6 minutes at the default
pause.

    uv run python scripts/fetch_toxcast.py
    uv run python scripts/fetch_toxcast.py --no-aops        # skip the per-endpoint AOP requests
    uv run python scripts/fetch_toxcast.py --output tmp/toxcast --pause 0.5
"""

import argparse
import csv
import datetime
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://comptox.epa.gov/ctx-api"
API_KEY_ENV = "CTX_API_KEY"
ANNOTATIONS_PATH = "bioactivity/assay/"
AOPS_PATH = "bioactivity/aop/search/by-toxcast-aeid/{aeid}"
HGNC_URL = (
    "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/"
    "hgnc_complete_set.txt"
)
OLS_TERM = "https://www.ebi.ac.uk/ols4/api/ontologies/ncbitaxon/terms"
USER_AGENT = "nams-registry (https://github.com/monarch-initiative/nams-registry)"

MISSING_KEY = f"""no EPA CTX API key: set {API_KEY_ENV}.
A free individual key is requested by emailing ccte_api@epa.gov with your
name, email and organization. Export it in your shell profile, e.g. ~/.zshrc:
    export {API_KEY_ENV}='...'
and start a new shell. Never write the key into a file in the repository."""


def get(url, headers, retries=3, pause=1.0):
    """GET a URL and return the response body as bytes."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **headers})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code in (401, 403):
                sys.exit(
                    f"{url}: HTTP {error.code}; check {API_KEY_ENV}.\n\n{MISSING_KEY}"
                )
            # Retry only what may pass on a later attempt: rate limiting (429)
            # and server errors (5xx).
            if not (error.code == 429 or error.code >= 500) or attempt == retries:
                raise
        except urllib.error.URLError:
            if attempt == retries:
                raise
        time.sleep(pause * 2**attempt)
    raise AssertionError("unreachable")


def ctx(path, key, pause):
    """GET a CTX API path and return the parsed JSON."""
    body = get(
        f"{API}/{path.lstrip('/')}",
        {"Accept": "application/json", "x-api-key": key},
        pause=pause,
    )
    return json.loads(body)


def fetch_hgnc():
    """HGNC's approved genes, keyed by Entrez id."""
    text = get(HGNC_URL, {}).decode("utf-8")
    genes = {}
    for row in csv.DictReader(io.StringIO(text), delimiter="\t"):
        if row.get("status") == "Approved" and row.get("entrez_id"):
            genes[row["entrez_id"]] = {
                "hgnc_id": row["hgnc_id"].lower(),  # hgnc:5182, the registry's form
                "symbol": row["symbol"],
            }
    return genes


def fetch_taxon_label(taxon_id, pause):
    """The NCBI Taxonomy label of a taxon id, from OLS, or None."""
    query = urllib.parse.urlencode({"obo_id": f"NCBITaxon:{taxon_id}"})
    data = json.loads(
        get(f"{OLS_TERM}?{query}", {"Accept": "application/json"}, pause=pause)
    )
    terms = data.get("_embedded", {}).get("terms", [])
    return terms[0].get("label") if terms else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tmp/toxcast",
        help="Directory to write into (default: tmp/toxcast, which git ignores)",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=0.2,
        help="Seconds to wait between AOP requests (default: 0.2)",
    )
    parser.add_argument(
        "--no-aops",
        action="store_true",
        help="Skip the per-endpoint AOP requests",
    )
    args = parser.parse_args()

    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        sys.exit(MISSING_KEY)

    started = datetime.datetime.now(datetime.timezone.utc)
    args.output.mkdir(parents=True, exist_ok=True)

    endpoints = ctx(ANNOTATIONS_PATH, key, args.pause)
    if not isinstance(endpoints, list):
        sys.exit(f"{ANNOTATIONS_PATH}: expected a list, got {type(endpoints).__name__}")
    (args.output / "assay_annotations.json").write_text(
        json.dumps(endpoints, indent=1, ensure_ascii=False)
    )
    aids = {e.get("aid") for e in endpoints}
    print(f"{len(endpoints)} endpoints in {len(aids)} assays", file=sys.stderr)

    failed = []
    aops = {}
    if not args.no_aops:
        for n, endpoint in enumerate(endpoints, 1):
            aeid = endpoint["aeid"]
            time.sleep(args.pause)
            try:
                aops[str(aeid)] = ctx(AOPS_PATH.format(aeid=aeid), key, args.pause)
            except (urllib.error.URLError, json.JSONDecodeError) as error:
                failed.append({"request": "aop", "aeid": aeid, "error": str(error)})
            print(f"aop: {n}/{len(endpoints)}", file=sys.stderr, end="\r")
        print(f"aop: {len(endpoints)} endpoints queried" + " " * 10, file=sys.stderr)
        (args.output / "aops.json").write_text(
            json.dumps(aops, indent=1, ensure_ascii=False)
        )

    hgnc = fetch_hgnc()
    (args.output / "hgnc.json").write_text(json.dumps(hgnc, indent=1))

    # The assays' own organisms, and human for the human gene targets.
    taxon_ids = {e.get("organismId") for e in endpoints if e.get("organismId")} | {9606}
    taxa = {}
    for taxon_id in sorted(taxon_ids):
        try:
            label = fetch_taxon_label(int(taxon_id), args.pause)
        except (urllib.error.URLError, json.JSONDecodeError, ValueError) as error:
            failed.append({"request": "taxon", "id": taxon_id, "error": str(error)})
            continue
        if label:
            taxa[str(int(taxon_id))] = label
        else:
            failed.append({"request": "taxon", "id": taxon_id, "error": "not in OLS"})
    (args.output / "taxa.json").write_text(json.dumps(taxa, indent=1, sort_keys=True))

    manifest = {
        "source": "EPA CompTox Chemicals Dashboard APIs (CTX), bioactivity domain",
        "api": API,
        "annotations_path": ANNOTATIONS_PATH,
        "aops_path": None if args.no_aops else AOPS_PATH,
        "hgnc": HGNC_URL,
        "taxa_source": OLS_TERM,
        "fetched_at": started.isoformat(timespec="seconds"),
        "release": "not recorded: the CTX API has no version endpoint",
        "endpoints": len(endpoints),
        "assays": len(aids),
        "endpoints_with_aop_records": sum(1 for v in aops.values() if v),
        "hgnc_genes": len(hgnc),
        "taxa": len(taxa),
        "failed_requests": failed,
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(
        json.dumps(
            {
                k: manifest[k]
                for k in (
                    "endpoints",
                    "assays",
                    "endpoints_with_aop_records",
                    "failed_requests",
                )
            },
            indent=1,
        ),
        file=sys.stderr,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
