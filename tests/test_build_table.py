"""Test the registry browser page."""

import json
import re
from pathlib import Path

from nams_registry import build_table

ROOT = Path(__file__).parent.parent


def page_data(path):
    """The records embedded in a built page."""
    text = path.read_text()
    return json.loads(re.search(r"const DATA = (.*);\nconst TABS", text).group(1))


def test_page_lists_resources_and_nams(tmp_path):
    """Every resource and NAM record is on the page, with its kind."""
    output = tmp_path / "index.html"
    build_table.main(
        [
            "--resources",
            str(ROOT / "resources"),
            "--nams",
            str(ROOT / "nams"),
            "--output",
            str(output),
        ]
    )
    rows = page_data(output)
    kinds = {k: [r for r in rows if r["kind"] == k] for k in ("resource", "nam")}
    assert len(kinds["resource"]) == len(list((ROOT / "resources").glob("*.yaml")))
    assert len(kinds["nam"]) == len(list((ROOT / "nams").glob("*.yaml")))
    assert len(rows) == len(kinds["resource"]) + len(kinds["nam"])
    assert all(r["kind_label"] for r in rows)


def test_page_marks_nams_whose_source_holds_more(tmp_path):
    """A NAM record whose resource holds more than it gives publicly is marked,
    and its rows carry the resource's own terms."""
    output = tmp_path / "index.html"
    build_table.main(
        [
            "--resources",
            str(ROOT / "resources"),
            "--nams",
            str(ROOT / "nams"),
            "--output",
            str(output),
        ]
    )
    marked = [
        r
        for r in page_data(output)
        if r["kind"] == "nam" and r["vendor_holds_more_details"]
    ]
    assert marked
    assert all(r["source_resource_ids"] == ["namsnetwork"] for r in marked)
    assert any(r["cell_lines"] for r in marked)
