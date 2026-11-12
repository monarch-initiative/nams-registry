"""Ontology terms and references in the records, checked from the committed caches.

These run offline, from cache/ and references_cache/. A term or reference
that is new since the caches were last filled fails here: run
`just validate-terms` or `just validate-references`, which look it up, then
commit the cache.
"""

import glob
import os
from pathlib import Path

import pytest

from nams_registry.check_records import reference_problems, term_problems

REPO = Path(__file__).parent.parent
NAM_FILES = sorted(glob.glob(os.path.join(REPO, "nams", "*.yaml")))
RESOURCE_FILES = sorted(glob.glob(os.path.join(REPO, "resources", "*.yaml")))

# Records whose terms are right but which a NAMO binding rejects, until NAMO
# changes. strict: the test fails once the record passes, so this is removed.
NAMO_BINDING_GAPS = {
    "blood-vessel-organoid-pluripotent-stem-cell": (
        "Organoid.organ_modeled binds OrganEnum, and blood microvessel "
        "(UBERON:8410081) is not under UBERON organ"
    ),
}


def nam_params():
    for path in NAM_FILES:
        stem = Path(path).stem
        marks = []
        if stem in NAMO_BINDING_GAPS:
            marks.append(pytest.mark.xfail(reason=NAMO_BINDING_GAPS[stem], strict=True))
        yield pytest.param(path, id=stem, marks=marks)


@pytest.mark.parametrize("filepath", nam_params())
def test_nam_terms(filepath):
    """Each term exists, sits under its NAMO enum's root, and has its ontology label."""
    problems = term_problems(Path(filepath), offline=True)
    assert not problems, "\n".join(str(p) for p in problems)


@pytest.mark.parametrize(
    "filepath", NAM_FILES + RESOURCE_FILES, ids=lambda p: Path(p).stem
)
def test_references(filepath):
    """Each reference resolves, and each title given is the reference's own."""
    problems = reference_problems(Path(filepath), offline=True)
    assert not problems, "\n".join(str(p) for p in problems)
