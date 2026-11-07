"""Tests for the review issue byline."""

import subprocess

import pytest

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
