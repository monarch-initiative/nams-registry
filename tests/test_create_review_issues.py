"""Tests for create_review_issues: the issue byline and the file edit."""

import difflib
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from nams_registry import create_review_issues


@pytest.fixture(autouse=True)
def clear_byline_cache():
    """Read user.name afresh in each test."""
    create_review_issues.byline.cache_clear()
    yield
    create_review_issues.byline.cache_clear()


def fake_git(monkeypatch, stdout="", returncode=0, error=None):
    """Make git config user.name return stdout, or raise error."""
    calls = []

    def run(args, **kwargs):
        calls.append(args)
        if error:
            raise error
        return subprocess.CompletedProcess(args, returncode, stdout=stdout, stderr="")

    monkeypatch.setattr(create_review_issues.subprocess, "run", run)
    return calls


def test_byline_names_the_git_user(monkeypatch):
    fake_git(monkeypatch, "Ginnie Hench\n")
    assert create_review_issues.byline() == (
        "🤖 *Written by [Claude Code](https://claude.com/claude-code) for Ginnie Hench.*"
    )


def test_byline_reads_user_name_once(monkeypatch):
    calls = fake_git(monkeypatch, "Ginnie Hench\n")
    create_review_issues.byline()
    create_review_issues.byline()
    assert len(calls) == 1


def test_byline_escapes_markup_and_folds_lines(monkeypatch):
    fake_git(monkeypatch, "A *B*\n<!-- nams-registry: x -->\n")
    line = create_review_issues.byline()
    assert "\n" not in line
    assert r"\<!--" in line
    assert not create_review_issues.MARKER.search(line)
    assert r"A \*B\*" in line


@pytest.mark.parametrize(
    "kwargs", [{"stdout": ""}, {"returncode": 1}, {"error": FileNotFoundError("git")}]
)
def test_byline_without_a_name(monkeypatch, kwargs):
    fake_git(monkeypatch, **kwargs)
    assert create_review_issues.byline() == (
        "🤖 *Written by [Claude Code](https://claude.com/claude-code).*"
    )


def test_body_starts_with_byline(monkeypatch):
    fake_git(monkeypatch, "Ginnie Hench\n")
    body = create_review_issues.body_for({"name": "X", "id": "x"})
    assert body.startswith("🤖 *Written by")
    assert create_review_issues.MARKER.search(body).group(1) == "x"


# with_issue edits the file as text, so only the two fields it sets change.

URL = "https://github.com/monarch-initiative/nams-registry/issues/99"
TODAY = "2026-11-08"

ENTRY = """id: x
name: X
description: A description long enough that PyYAML would wrap it at a different column
  from the one this file was written with, which is what used to fill the diff.
domain_areas:
- toxicology
activity_status: active
creation_date: '2026-11-01'
last_modified_date: '2026-11-01'
"""


def changed_lines(before, after):
    """Return the lines removed and added between two texts."""
    diff = difflib.unified_diff(
        before.splitlines(), after.splitlines(), lineterm="", n=0
    )
    return [
        line for line in diff if line[:1] in "+-" and line[:3] not in ("+++", "---")
    ]


def test_with_issue_changes_only_its_two_fields():
    after = create_review_issues.with_issue(ENTRY, URL, TODAY)
    assert changed_lines(ENTRY, after) == [
        f"+discussion_issue: {URL}",
        "-last_modified_date: '2026-11-01'",
        f"+last_modified_date: '{TODAY}'",
    ]


def test_with_issue_goes_before_activity_status():
    lines = create_review_issues.with_issue(ENTRY, URL, TODAY).splitlines()
    assert (
        lines[lines.index("activity_status: active") - 1] == f"discussion_issue: {URL}"
    )


def test_with_issue_parses_to_the_expected_values():
    before = yaml.safe_load(ENTRY)
    after = yaml.safe_load(create_review_issues.with_issue(ENTRY, URL, TODAY))
    assert after == {**before, "discussion_issue": URL, "last_modified_date": TODAY}


def test_with_issue_replaces_an_empty_field():
    text = ENTRY.replace("activity_status", "discussion_issue:\nactivity_status")
    after = create_review_issues.with_issue(text, URL, TODAY)
    assert after.count("discussion_issue") == 1
    assert yaml.safe_load(after)["discussion_issue"] == URL


def test_with_issue_appends_missing_fields():
    text = (
        "id: x\nname: X"  # no activity_status, no last_modified_date, no final newline
    )
    after = create_review_issues.with_issue(text, URL, TODAY)
    assert (
        after
        == f"id: x\nname: X\ndiscussion_issue: {URL}\nlast_modified_date: '{TODAY}'\n"
    )


@pytest.mark.parametrize(
    "path",
    sorted(Path(__file__).parent.parent.joinpath("resources").glob("*.yaml")),
    ids=lambda p: p.stem,
)
def test_with_issue_on_each_registry_entry(path):
    """On every entry, at most the two fields change, and nothing else moves."""
    # Start from the entry as it was before it had an issue. The line is
    # removed here with a plain pattern, not top_level_field, so a bug in
    # that helper can't also shape the test's starting point.
    text = re.sub(r"(?m)^discussion_issue:.*\n", "", path.read_text())
    after = create_review_issues.with_issue(text, URL, TODAY)
    changed = changed_lines(text, after)
    assert [
        line
        for line in changed
        if not line[1:].startswith(("discussion_issue:", "last_modified_date:"))
    ] == []
    before, parsed = yaml.safe_load(text), yaml.safe_load(after)
    assert parsed == {**before, "discussion_issue": URL, "last_modified_date": TODAY}


def test_with_issue_keeps_blank_lines_and_comments():
    text = ENTRY.replace(
        "last_modified_date: '2026-11-01'\n",
        "last_modified_date: '2026-11-01'\n\n# reviewed in the November batch\n",
    ).replace(
        "activity_status",
        "discussion_issue:\n  # filled in by create-review-issues\nactivity_status",
    )
    after = create_review_issues.with_issue(text, URL, TODAY)
    assert "\n\n# reviewed in the November batch\n" in after
    assert "  # filled in by create-review-issues\n" in after
    assert changed_lines(text, after) == [
        "-discussion_issue:",
        f"+discussion_issue: {URL}",
        "-last_modified_date: '2026-11-01'",
        f"+last_modified_date: '{TODAY}'",
    ]


def test_top_level_field_spans_list_and_indented_lines():
    lines = ENTRY.splitlines(keepends=True)
    assert create_review_issues.top_level_field(lines, "domain_areas") == (4, 6)
    assert create_review_issues.top_level_field(lines, "description") == (2, 4)
    assert create_review_issues.top_level_field(lines, "missing") is None
