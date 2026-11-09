"""Test the registry browser page."""

import json
import re
from pathlib import Path

import yaml

from nams_registry import build_table

ROOT = Path(__file__).parent.parent

STUB = {
    "id": "example-stub",
    "name": "Example stub",
    "resource": "namsnetwork",
    "source_urls": ["https://nams.network/details/1"],
    "accessed_on": "2026-11-09",
    "method_type": "in vitro",
}


def page_data(path):
    """The records embedded in a built page."""
    text = path.read_text()
    return json.loads(re.search(r"const DATA = (.*);\nconst TABS", text).group(1))


def test_page_lists_resources_nams_and_stubs(tmp_path):
    """Every resource, NAM record and stub is on the page, with its kind."""
    stubs = tmp_path / "stubs"
    (stubs / "namsnetwork").mkdir(parents=True)
    (stubs / "namsnetwork" / "example-stub.yaml").write_text(yaml.safe_dump(STUB))
    output = tmp_path / "index.html"
    build_table.main([
        "--resources", str(ROOT / "resources"),
        "--nams", str(ROOT / "nams"),
        "--stubs", str(stubs),
        "--output", str(output),
    ])
    rows = page_data(output)
    kinds = {k: [r for r in rows if r["kind"] == k] for k in ("resource", "nam", "stub")}
    assert len(kinds["resource"]) == len(list((ROOT / "resources").glob("*.yaml")))
    assert len(kinds["nam"]) == len(list((ROOT / "nams").glob("*.yaml")))
    (stub,) = kinds["stub"]
    assert stub["sources"] == ["NAMs Network"]
    assert stub["source_resource_ids"] == ["namsnetwork"]
    assert stub["record_path"] == "stubs/namsnetwork/example-stub.yaml"
    assert all(r["kind_label"] for r in rows)
