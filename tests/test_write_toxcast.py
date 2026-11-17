"""scripts/write_toxcast.py, run on a fixture of real CTX annotations.

tests/data/toxcast/assay_annotations.json is nine endpoint objects from EPA's
CTX API, copied from DisMech's own fixture (tests/data/toxcast/ there, fetched
2026-09-24). hgnc.json and taxa.json hold the HGNC and OLS answers for the
genes and organisms in it. There is no aops.json: what the AOP endpoint
returns has not been captured in a fixture yet.
"""

import importlib.util
from pathlib import Path

import pytest
import yaml
from linkml.validator import validate

from nams_registry.datamodel import NAM_SCHEMA_PATH

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).parent / "data" / "toxcast"

spec = importlib.util.spec_from_file_location(
    "write_toxcast", ROOT / "scripts/write_toxcast.py"
)
write_toxcast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(write_toxcast)


def run(output, *extra):
    return write_toxcast.main(
        ["--input", str(FIXTURE), "--output", str(output), *extra]
    )


@pytest.fixture
def written(tmp_path):
    run(tmp_path)
    return {p.stem: yaml.safe_load(p.read_text()) for p in tmp_path.glob("*.yaml")}


def test_one_record_per_assay(written):
    # Nine endpoints from nine assays; agonist and antagonist are two assays.
    assert len(written) == 9
    assert "tox21-era-bla-agonist" in written
    assert "tox21-era-bla-antagonist" in written


def test_records_validate(written):
    for stem, record in written.items():
        report = validate(record, str(NAM_SCHEMA_PATH), "NAMRecord")
        assert not report.results, (stem, [r.message for r in report.results])


def test_human_target_resolved_through_hgnc(written):
    (target,) = written["tox21-trb-coa-antagonist-followup"]["measured_targets"]
    assert target["gene"] == "hgnc:11799"
    assert target["gene_symbol"] == "THRB"


def test_non_human_target_has_no_hgnc_id(written):
    (target,) = written["nvs-nr-mera"]["measured_targets"]
    assert target["name"] == "Esr1"
    assert "gene" not in target
    assert "Not a human gene" in target["notes"]


def test_viability_endpoint_names_no_target(written):
    # aid 319's only endpoint here is its cell-viability counter-screen.
    assert "measured_targets" not in written["tox21-era-bla-antagonist"]


def test_tox21_assays_also_name_tox21(written):
    resources = [
        s["resource"] for s in written["tox21-era-bla-agonist"]["source_resources"]
    ]
    assert resources == ["toxcast", "tox21"]
    resources = [s["resource"] for s in written["acea-er"]["source_resources"]]
    assert resources == ["toxcast"]


def test_dry_run_writes_nothing(tmp_path):
    run(tmp_path, "--dry-run")
    assert not list(tmp_path.glob("*.yaml"))


def test_rerun_keeps_curated_records(tmp_path):
    run(tmp_path)
    curated = tmp_path / "acea-er.yaml"
    curated.write_text(
        curated.read_text() + "applications:\n- description: Hand-added use.\n"
    )
    before = curated.read_text()
    run(tmp_path)
    assert curated.read_text() == before
    assert len(list(tmp_path.glob("*.yaml"))) == 9
