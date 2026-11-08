"""Data test."""

import os
import glob
import pytest
from pathlib import Path

import yaml
import nams_registry.datamodel.nams_registry
from linkml.validator import validate
from linkml_runtime.loaders import yaml_loader
from nams_registry.datamodel import MAIN_SCHEMA_PATH, NAM_SCHEMA_PATH

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_VALID, "*.yaml"))
INVALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_INVALID, "*.yaml"))


def schema_for(target_class_name):
    """The registry schema, or the NAM records schema for its classes."""
    if hasattr(nams_registry.datamodel.nams_registry, target_class_name):
        return MAIN_SCHEMA_PATH
    return NAM_SCHEMA_PATH


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Test loading of all valid data files.

    NAM records have no generated Python classes, so they are validated
    against the NAM records schema instead.
    """
    target_class_name = Path(filepath).stem.split("-")[0]
    if schema_for(target_class_name) == NAM_SCHEMA_PATH:
        with open(filepath) as fh:
            instance = yaml.safe_load(fh)
        report = validate(instance, str(NAM_SCHEMA_PATH), target_class_name)
        assert not report.results, [r.message for r in report.results]
        return
    tgt_class = getattr(
        nams_registry.datamodel.nams_registry,
        target_class_name,
    )
    obj = yaml_loader.load(filepath, target_class=tgt_class)
    assert obj


@pytest.mark.parametrize("filepath", INVALID_EXAMPLE_FILES)
def test_invalid_data_files(filepath):
    """Test that every invalid data file fails validation."""
    target_class_name = Path(filepath).stem.split("-")[0]
    with open(filepath) as fh:
        instance = yaml.safe_load(fh)
    report = validate(instance, str(schema_for(target_class_name)), target_class_name)
    assert report.results, f"{filepath} should not validate"
