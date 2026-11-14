"""Registry data test."""

import glob
import os
from pathlib import Path

import pytest
import yaml
from linkml.validator import Validator, validate
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml_runtime.utils.schemaview import SchemaView

from nams_registry.datamodel import MAIN_SCHEMA_PATH, NAM_SCHEMA_PATH

RESOURCES_DIR = Path(__file__).parent.parent / "resources"

RESOURCE_FILES = sorted(glob.glob(os.path.join(RESOURCES_DIR, "*.yaml")))


@pytest.mark.parametrize("filepath", RESOURCE_FILES, ids=lambda p: Path(p).stem)
def test_resource_file_is_valid(filepath):
    """Test that every resource file validates as a Resource."""
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    report = validate(instance, str(MAIN_SCHEMA_PATH), "Resource")
    assert not report.results, [r.message for r in report.results]


@pytest.mark.parametrize("filepath", RESOURCE_FILES, ids=lambda p: Path(p).stem)
def test_resource_file_name_matches_id(filepath):
    """Test that each file is named after the id it contains."""
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    assert instance["id"] == Path(filepath).stem


@pytest.fixture(scope="session")
def resources():
    """Every resource entry, keyed by file name."""
    entries = {}
    for filepath in RESOURCE_FILES:
        with open(filepath) as fh:
            entries[Path(filepath).stem] = yaml.safe_load(fh)
    return entries


@pytest.mark.parametrize("filepath", RESOURCE_FILES, ids=lambda p: Path(p).stem)
def test_part_of_names_an_organization(filepath, resources):
    """Test that each part_of id is a registry entry of type Organization."""
    instance = resources[Path(filepath).stem]
    for parent in instance.get("part_of", []):
        assert parent in resources, (
            f"part_of lists '{parent}', which is not the id of any registry entry"
        )
        resource_type = resources[parent].get("resource_type")
        assert resource_type == "Organization", (
            f"part_of lists '{parent}', whose resource_type is {resource_type}, "
            "not Organization"
        )


NAMS_DIR = Path(__file__).parent.parent / "nams"

NAM_FILES = sorted(glob.glob(os.path.join(NAMS_DIR, "*.yaml")))

RESOURCE_IDS = {Path(p).stem for p in RESOURCE_FILES}

# The NAMO classes a NAM record's model can be.
_VIEW = SchemaView(str(NAM_SCHEMA_PATH))
CONCRETE_MODEL_CLASSES = {
    c for c in _VIEW.class_descendants("ModelSystem") if not _VIEW.get_class(c).abstract
}


def test_publication_matches_namo_reference():
    """Test that a resource's Publication has the same fields as NAMO's
    Reference, which NAM records cite papers with, so the two stay in step."""

    def fields(schema_path, class_name):
        view = SchemaView(str(schema_path))
        return {
            s.name: (s.range, bool(s.required), bool(s.multivalued), bool(s.identifier))
            for s in view.class_induced_slots(class_name)
        }

    assert fields(MAIN_SCHEMA_PATH, "Publication") == fields(
        NAM_SCHEMA_PATH, "Reference"
    )


@pytest.fixture(scope="module")
def nam_validator():
    """One validator for every NAM file, since loading the schema per file is
    slow with hundreds of records."""
    return Validator(
        str(NAM_SCHEMA_PATH),
        validation_plugins=[JsonschemaValidationPlugin(closed=True)],
    )


@pytest.mark.parametrize("filepath", NAM_FILES, ids=lambda p: Path(p).stem)
def test_nam_file_is_valid(filepath, nam_validator):
    """Test that every NAM file validates as a NAMRecord.

    A model with a type is also validated on its own, as the NAMO class its
    type names, because a bad model makes the NAMRecord check report only
    that the model matches no NAMO class, not which field is wrong. A model
    whose NAMO class isn't clear from its source has no type.
    """
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    model_type = instance.get("model", {}).get("type")
    if model_type is not None:
        assert model_type in CONCRETE_MODEL_CLASSES, (
            f"model type {model_type!r} is not a concrete NAMO ModelSystem class"
        )
        report = nam_validator.validate(instance["model"], model_type)
        assert not report.results, [r.message for r in report.results]
    report = nam_validator.validate(instance, "NAMRecord")
    assert not report.results, [r.message for r in report.results]


@pytest.mark.parametrize("filepath", NAM_FILES, ids=lambda p: Path(p).stem)
def test_nam_file_name_matches_id(filepath):
    """Test that each NAM file is named after its model's id."""
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    assert instance["model"]["id"] == Path(filepath).stem


@pytest.mark.parametrize("filepath", NAM_FILES, ids=lambda p: Path(p).stem)
def test_nam_source_resources_exist(filepath):
    """Test that every resource a NAM names is a file in resources/."""
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    missing = [
        s["resource"]
        for s in instance["source_resources"]
        if s["resource"] not in RESOURCE_IDS
    ]
    assert not missing, f"unknown resources: {missing}"


def load_nam(nam_id):
    with open(NAMS_DIR / f"{nam_id}.yaml") as fh:
        return yaml.safe_load(fh)


@pytest.mark.parametrize("filepath", NAM_FILES, ids=lambda p: Path(p).stem)
def test_nam_comparisons_are_paired(filepath):
    """Test that each record a NAM is compared with is another file in nams/,
    and that it names this NAM back with the same paper."""
    own_id = Path(filepath).stem
    nam_ids = {Path(p).stem for p in NAM_FILES}
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    wrong = []
    for comparison in instance.get("compared_with", []):
        other = comparison["nam"]
        if other == own_id:
            wrong.append("compared with itself")
        elif other not in nam_ids:
            wrong.append(f"{other} is not a record in nams/")
        elif {"nam": own_id, "reference": comparison["reference"]} not in (
            load_nam(other).get("compared_with", [])
        ):
            wrong.append(
                f"{other} does not name {own_id} back with {comparison['reference']}"
            )
    assert not wrong, wrong


def test_namsnetwork_pages_have_one_record():
    """Test that no two NAM records name the same NAMs.network page, since
    each page is one NAM.

    scripts/write_namsnetwork.py writes no record for a page that a curated
    record names, so a rerun resolves a clash with one of its records.
    """
    owners = {}
    for path in NAM_FILES:
        with open(path) as fh:
            for source in yaml.safe_load(fh).get("source_resources", []):
                if source["resource"] == "namsnetwork":
                    for url in source.get("source_urls", []):
                        owners.setdefault(url, []).append(Path(path).name)
    shared = {url: names for url, names in owners.items() if len(names) > 1}
    assert not shared, shared
