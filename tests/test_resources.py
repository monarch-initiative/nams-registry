"""Registry data test."""

import glob
import os
from pathlib import Path

import pytest
import yaml
from linkml.validator import validate

from nams_registry.datamodel import MAIN_SCHEMA_PATH

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
