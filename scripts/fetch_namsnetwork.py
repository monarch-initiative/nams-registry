#!/usr/bin/env python3
"""Fetch the NAMs.network catalogue through its public JSON API.

NAMs.network (https://nams.network/explore) is a single-page app run by QSAR
Lab. Its data comes from a JSON API at https://api.nams.network. Two of the
endpoints the explorer uses need no login:

- ``data_models/nams_table/`` lists the NAMs, 10 per page (``page_size`` and
  ``limit`` are ignored). Each row has the NAM's name, type, endpoint, organ,
  cell types, development status, guideline or strategy, regulations and its
  ``qsar_id``. Query parameters filter the list, e.g. ``?aop=10``.
- ``data_models/get_filters/`` lists every filter facet with its values and
  ids: substances, methods and biomarkers, AOP-Wiki AOPs and Key Events, and
  others.

A NAM's full record, ``data_models/nam/<qsar_id>/``, needs a logged-in
account and is not fetched here. Instead, for the facets that the list rows
don't carry, this script queries the list once per facet value and records
which NAMs it returns. That rebuilds those links from public data only.

Writes, into the output directory:

- ``filters.json``: the facets as the API returns them.
- ``nams.json``: one record per NAM, the list row plus the facet values
  linked to it (under ``linked``).
- ``manifest.json``: the fetch time, the API base, the counts, and any facet
  values whose query failed.

Requests are made one at a time with a pause between them. A full run is
roughly 550 requests, about 10 minutes at the default pause.

    uv run python scripts/fetch_namsnetwork.py
    uv run python scripts/fetch_namsnetwork.py --output tmp/namsnetwork --pause 1.5
    uv run python scripts/fetch_namsnetwork.py --facets aop key_event   # a quick partial run
"""

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.nams.network"
USER_AGENT = "nams-registry (https://github.com/monarch-initiative/nams-registry)"

# Facets whose values are not in the list rows, so their links to NAMs have to
# be rebuilt by filtering. The value of each is the field in a facet entry
# that holds its label. Facets already in each row (nam_type, organ,
# cell_type, endpoint, dev_status, guideline_strategy, regulations) and
# nam_name (one value per NAM) are left out.
LINKED_FACETS = {
    "substance_name": "name",
    "method_biomarker": "name",
    "biological_endpoint": "name",
    "aop": "code",
    "key_event": "code",
    "conv_mat": "name",
}


def get_json(path, query=None, retries=3, pause=1.0):
    """GET a path under the API and return the parsed JSON."""
    url = f"{API}/{path.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            # Retry only what may pass on a later attempt: rate limiting (429)
            # and server errors (5xx).
            retryable = error.code == 429 or error.code >= 500
            if not retryable or attempt == retries:
                raise
        except urllib.error.URLError:
            if attempt == retries:
                raise
        time.sleep(pause * 2**attempt)
    raise AssertionError("unreachable")


def fetch_list(query, pause):
    """Return every row of the NAM list for a query, following the pages."""
    rows, page = [], 1
    while True:
        data = get_json("data_models/nams_table/", {**query, "page": page}, pause=pause)
        rows.extend(data["results"])
        if not data.get("next"):
            return rows, data["count"]
        page += 1
        time.sleep(pause)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", type=Path, default=Path("tmp/namsnetwork"), help="Directory to write into (default: tmp/namsnetwork, which git ignores)")
    parser.add_argument("--pause", type=float, default=1.0, help="Seconds to wait between requests (default: 1.0)")
    parser.add_argument("--facets", nargs="*", choices=sorted(LINKED_FACETS), default=sorted(LINKED_FACETS), help="Facets to rebuild links for (default: all)")
    args = parser.parse_args()

    started = datetime.datetime.now(datetime.timezone.utc)
    args.output.mkdir(parents=True, exist_ok=True)

    filters = get_json("data_models/get_filters/")
    (args.output / "filters.json").write_text(json.dumps(filters, indent=1, ensure_ascii=False))
    time.sleep(args.pause)

    rows, count = fetch_list({}, args.pause)
    if len(rows) != count:
        print(f"warning: the list reports {count} NAMs but {len(rows)} rows were returned", file=sys.stderr)
    nams = {row["qsar_id"]: {**row, "linked": {facet: [] for facet in args.facets}} for row in rows}
    print(f"{len(nams)} NAMs listed", file=sys.stderr)

    failed, unknown = [], set()
    for facet in args.facets:
        label_field = LINKED_FACETS[facet]
        values = [v for v in filters.get(facet, []) if v.get("id")]  # id 0 is the empty value
        for n, value in enumerate(values, 1):
            time.sleep(args.pause)
            try:
                matched, _ = fetch_list({facet: value["id"]}, args.pause)
            except (urllib.error.URLError, json.JSONDecodeError, KeyError) as error:
                failed.append({"facet": facet, "id": value["id"], "error": str(error)})
                continue
            for row in matched:
                nam = nams.get(row["qsar_id"])
                if nam is None:
                    unknown.add(row["qsar_id"])
                    continue
                nam["linked"][facet].append({"id": value["id"], "label": value.get(label_field)})
            print(f"{facet}: {n}/{len(values)}", file=sys.stderr, end="\r")
        print(f"{facet}: {len(values)} values queried" + " " * 10, file=sys.stderr)

    records = sorted(nams.values(), key=lambda r: r["qsar_id"])
    (args.output / "nams.json").write_text(json.dumps(records, indent=1, ensure_ascii=False))
    manifest = {
        "source": "https://nams.network/explore",
        "api": API,
        "fetched_at": started.isoformat(timespec="seconds"),
        "nams_reported": count,
        "nams_fetched": len(records),
        "facets_linked": args.facets,
        "facet_values": {facet: sum(1 for v in filters.get(facet, []) if v.get("id")) for facet in args.facets},
        "nams_with_links": {facet: sum(1 for r in records if r["linked"][facet]) for facet in args.facets},
        "failed_queries": failed,
        "qsar_ids_not_in_list": sorted(unknown),
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print(json.dumps({k: manifest[k] for k in ("nams_fetched", "nams_with_links", "failed_queries")}, indent=1), file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
