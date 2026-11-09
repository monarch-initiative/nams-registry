"""Test the registry browser page."""

import json
import re
from pathlib import Path

import yaml

from nams_registry import build_table

ROOT = Path(__file__).parent.parent

PARTIAL = {
    "id": "example-partial",
    "name": "Example partial record",
    "resource": "namsnetwork",
    "source_urls": ["https://nams.network/details/1"],
    "accessed_on": "2026-11-09",
    "method_type": "in vitro",
}


def page_data(path):
    """The records embedded in a built page."""
    text = path.read_text()
    return json.loads(re.search(r"const DATA = (.*);\nconst TABS", text).group(1))


def test_page_lists_resources_nams_and_partials(tmp_path):
    """Every resource, NAM record and partial NAM record is on the page, with its kind."""
    partials = tmp_path / "partial-nams"
    (partials / "namsnetwork").mkdir(parents=True)
    (partials / "namsnetwork" / "example-partial.yaml").write_text(yaml.safe_dump(PARTIAL))
    output = tmp_path / "index.html"
    build_table.main([
        "--resources", str(ROOT / "resources"),
        "--nams", str(ROOT / "nams"),
        "--partial-nams", str(partials),
        "--output", str(output),
    ])
    rows = page_data(output)
    kinds = {k: [r for r in rows if r["kind"] == k] for k in ("resource", "nam", "partial")}
    assert len(kinds["resource"]) == len(list((ROOT / "resources").glob("*.yaml")))
    assert len(kinds["nam"]) == len(list((ROOT / "nams").glob("*.yaml")))
    (partial,) = kinds["partial"]
    assert partial["sources"] == ["NAMs Network"]
    assert partial["source_resource_ids"] == ["namsnetwork"]
    assert partial["record_path"] == "partial-nams/namsnetwork/example-partial.yaml"
    assert all(r["kind_label"] for r in rows)
