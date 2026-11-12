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


PARTIAL_DIR = Path(__file__).parent.parent / "partial-nams"

PARTIAL_FILES = sorted(glob.glob(os.path.join(PARTIAL_DIR, "*", "*.yaml")))


def load_partials():
    partials = {}
    for path in PARTIAL_FILES:
        with open(path) as fh:
            partials[Path(path)] = yaml.safe_load(fh)
    return partials


def test_partial_files_are_valid():
    """Test that every partial record in partial-nams/<resource>/ validates
    as a PartialNAMRecord.

    The partial records are checked together, with one validator, because there are
    hundreds of them and loading the schema once per file is slow.
    """
    validator = Validator(
        str(NAM_SCHEMA_PATH),
        validation_plugins=[JsonschemaValidationPlugin(closed=True)],
    )
    failures = {}
    for path, partial in load_partials().items():
        report = validator.validate(partial, "PartialNAMRecord")
        if report.results:
            failures[path.name] = [r.message for r in report.results]
    assert not failures, failures


def test_partial_files_are_named_and_placed():
    """Test that each partial record is named after its id, in its resource's folder,
    and that the resource is a file in resources/."""
    wrong = []
    for path, partial in load_partials().items():
        if partial["id"] != path.stem:
            wrong.append(f"{path.name}: id is {partial['id']}")
        if partial["resource"] != path.parent.name:
            wrong.append(
                f"{path.name}: resource {partial['resource']} but in {path.parent.name}/"
            )
        if partial["resource"] not in RESOURCE_IDS:
            wrong.append(f"{path.name}: unknown resource {partial['resource']}")
    assert not wrong, wrong


def test_partial_proposed_classes_are_namo_classes():
    """Test that a partial record's proposed NAMO class is one a model can have."""
    view = SchemaView(str(NAM_SCHEMA_PATH))
    concrete = {c for c in MODEL_CLASSES if not view.get_class(c).abstract}
    wrong = {
        path.name: partial["proposed_namo_class"]
        for path, partial in load_partials().items()
        if partial.get("proposed_namo_class") not in (None, *concrete)
    }
    assert not wrong, wrong


def test_full_records_have_no_partial():
    """Test that no partial record names a source page a NAM record in
    nams/ names, since a NAM has one or the other.

    Rerunning the resource's script drops the partial record of a NAM that
    a NAM record names.
    """
    recorded = set()
    for path in NAM_FILES:
        with open(path) as fh:
            for source in yaml.safe_load(fh).get("source_resources", []):
                recorded.update(source.get("source_urls", []))
    both = {
        path.name: sorted(recorded.intersection(partial.get("source_urls", [])))
        for path, partial in load_partials().items()
        if recorded.intersection(partial.get("source_urls", []))
    }
    assert not both, both
