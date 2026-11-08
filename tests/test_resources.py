"""Registry data test."""

import glob
import os
from pathlib import Path

import pytest
import yaml
from linkml.validator import validate
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
MODEL_CLASSES = set(SchemaView(str(NAM_SCHEMA_PATH)).class_descendants("ModelSystem"))


@pytest.mark.parametrize("filepath", NAM_FILES, ids=lambda p: Path(p).stem)
def test_nam_file_is_valid(filepath):
    """Test that every NAM file validates as a NAMRecord.

    The model is also validated on its own, as the NAMO class its type names,
    because a bad model makes the NAMRecord check report only that the model
    matches no NAMO class, not which field is wrong.
    """
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    model_type = instance.get("model", {}).get("type")
    assert model_type in MODEL_CLASSES, (
        f"model type {model_type!r} is not a NAMO ModelSystem class"
    )
    report = validate(instance["model"], str(NAM_SCHEMA_PATH), model_type)
    assert not report.results, [r.message for r in report.results]
    report = validate(instance, str(NAM_SCHEMA_PATH), "NAMRecord")
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
