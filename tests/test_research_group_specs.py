"""Every research-group spec must fill every placeholder its template has.

`just research-group` renders templates/research_group_models.md from a spec in
templates/research_groups/<slug>.yaml and the paper list beside it,
<slug>.works.yaml. A field missing from either is a hole in the prompt, and
deep-research-client either refuses the run or, worse, a provider is sent a
prompt with a gap in it. A run costs real time and credit, so these tests make
the mistake fail offline in milliseconds instead.

They do not import deep-research-client, which is in the `research` dependency
group that `just test` does not install; the contract under test is the
template's, not the renderer's.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re

import pytest
import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "research_group_models.md"
USE_CASES = REPO / "templates" / "research_groups"
SCRIPT = REPO / "scripts" / "research_group_vars.py"
FETCH = REPO / "scripts" / "fetch_openalex_works.py"

# deep-research-client's f-string templates treat every {word} as a variable.
PLACEHOLDER = re.compile(r"\{(\w+)\}")


def load(path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    """Import a script with cwd at the repo root, which its paths assume."""
    monkeypatch.chdir(REPO)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def template_placeholders() -> set[str]:
    return set(PLACEHOLDER.findall(TEMPLATE.read_text(encoding="utf-8")))


def spec_paths() -> list[pathlib.Path]:
    return sorted(
        p for p in USE_CASES.glob("*.yaml") if not p.name.endswith(".works.yaml")
    )


def test_the_template_and_the_script_agree_on_the_variables(monkeypatch) -> None:
    module = load(SCRIPT, monkeypatch)
    assert set(module.HAND_WRITTEN) | set(module.GENERATED) == template_placeholders()


def test_at_least_one_spec_is_committed() -> None:
    """A passing sweep over zero specs would prove nothing."""
    assert spec_paths(), f"no specs found in {USE_CASES}"


@pytest.mark.parametrize("path", spec_paths(), ids=lambda p: p.stem)
def test_spec_has_its_paper_list(path: pathlib.Path) -> None:
    works = path.with_name(f"{path.stem}.works.yaml")
    assert works.is_file(), f"run `just research-group-works {path.stem}`"


@pytest.mark.parametrize("path", spec_paths(), ids=lambda p: p.stem)
def test_spec_renders_with_no_placeholder_left(path, monkeypatch) -> None:
    module = load(SCRIPT, monkeypatch)
    values = module.variables(module.use_case(path.stem), module.works(path.stem))
    rendered = TEMPLATE.read_text(encoding="utf-8")
    for name, value in values.items():
        rendered = rendered.replace("{" + name + "}", value)
    leftover = sorted(set(PLACEHOLDER.findall(rendered)))
    assert not leftover, f"{path.name} leaves unsubstituted: {', '.join(leftover)}"


@pytest.mark.parametrize("path", spec_paths(), ids=lambda p: p.stem)
def test_paper_list_was_generated_from_this_spec(path, monkeypatch) -> None:
    """A spec whose openalex block changed must have its paper list re-fetched."""
    fetch = load(FETCH, monkeypatch)
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    works = yaml.safe_load(path.with_name(f"{path.stem}.works.yaml").read_text())
    assert works["openalex_filter"] == fetch.build_filter(spec["openalex"]), (
        f"re-run `just research-group-works {path.stem}`"
    )
    assert works.get("openalex_search") == spec["openalex"].get("search")


def test_unknown_slug_is_refused_and_names_the_available_ones(monkeypatch) -> None:
    module = load(SCRIPT, monkeypatch)
    with pytest.raises(SystemExit) as excinfo:
        module.use_case("no_such_group")
    message = str(excinfo.value)
    assert "no_such_group" in message
    for path in spec_paths():
        assert path.stem in message


def test_spec_missing_a_field_is_refused(monkeypatch, tmp_path) -> None:
    module = load(SCRIPT, monkeypatch)
    (tmp_path / "incomplete.yaml").write_text(
        "stem: someone2026-topic\ngroup_name: Someone\ngroup_kind: team\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "USE_CASES", tmp_path)
    with pytest.raises(SystemExit) as excinfo:
        module.use_case("incomplete")
    for field in ("group_description", "focus", "date_range", "data_analysis"):
        assert field in str(excinfo.value)


def _work(**overrides) -> dict:
    work = {
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1/A",
        "ids": {},
        "display_name": "A paper",
        "publication_year": 2025,
        "type": "article",
        "primary_location": {"source": {"display_name": "A Journal"}},
        "cited_by_count": 0,
        "is_retracted": False,
    }
    return {**work, **overrides}


def test_selection_drops_supplements_and_keeps_the_published_version(
    monkeypatch,
) -> None:
    fetch = load(FETCH, monkeypatch)
    works = [
        _work(id="https://openalex.org/W1", type="preprint", display_name="A Paper"),
        _work(id="https://openalex.org/W2", display_name="A paper"),
        _work(
            id="https://openalex.org/W3",
            type="other",
            display_name="Figure S1 from A paper",
            primary_location=None,
        ),
        _work(id="https://openalex.org/W4", type="supplementary-materials"),
        _work(id="https://openalex.org/W5", type="dataset", display_name="Images"),
        _work(
            id="https://openalex.org/W6",
            doi="https://doi.org/10.1/excluded",
            display_name="Unrelated",
        ),
    ]
    papers, datasets, dropped = fetch.select(works, {"10.1/excluded"})
    assert [p["openalex"] for p in papers] == ["W2"]
    assert [d["openalex"] for d in datasets] == ["W5"]
    assert dropped == {
        "duplicate title (preprint or repository copy)": 1,
        "supplementary item typed other": 1,
        "supplementary-materials": 1,
        "excluded in spec": 1,
    }
