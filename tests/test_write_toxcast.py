"""scripts/write_toxcast.py, run on a fixture of real CTX annotations.

tests/data/toxcast/assay_annotations.json is nine endpoint objects from EPA's
CTX API, copied from DisMech's own fixture (tests/data/toxcast/ there, fetched
2026-09-24). hgnc.json and taxa.json hold the HGNC and OLS answers for the
genes and organisms in it, and aops.json what CTX's AOP endpoint returned for
those nine endpoints on 2026-11-17. The records are decoded with the real
conf/toxcast_decoder.yaml.
"""

import importlib.util
import re
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
    assert "not an approved human gene in HGNC" in target["notes"]


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


def test_ratio_endpoint_takes_its_mode_from_the_assay_name(written):
    # aeid 2240 is a "ratio" endpoint of TOX21_TRB_BLA_Antagonist_Followup.
    (target,) = written["tox21-trb-bla-antagonist-followup"]["measured_targets"]
    assert target["measurement"] == "antagonist"


def test_cell_free_assay_names_no_cells(written):
    # aid 651 is cell-free: EPA's cell format says so, so no cells are written.
    source = written["tox21-trb-coa-antagonist-followup"]["source_resources"][0]
    assert "cell_lines" not in source
    assert source["method_type"] == "in chemico"


def test_cells_and_organs_are_decoded(written):
    source = written["tox21-ar-luc-mdakb2-antagonist-0-5nm-r1881"]["source_resources"][
        0
    ]
    assert source["cell_lines"] == ["MDA-kb2"]
    assert source["organs"] == ["Breast"]
    source = written["acea-er"]["source_resources"][0]
    assert source["cell_lines"] == ["T-47D"]  # EPA writes T47D


def test_aop_links_are_read(written):
    source = written["acea-er"]["source_resources"][0]
    assert source["aops"] == ["aop:220"]
    assert source["key_events"] == ["aop.events:1394"]


def test_check_fails_on_a_value_missing_from_the_decoder(tmp_path):
    decoder = yaml.safe_load((ROOT / "conf/toxcast_decoder.yaml").read_text())
    del decoder["cells"]["HEK293T"]
    path = tmp_path / "decoder.yaml"
    path.write_text(yaml.safe_dump(decoder, allow_unicode=True))
    assert run(tmp_path, "--check", "--decoder", str(path)) == 1
    assert run(tmp_path, "--check") == 0


def test_decoder_ids_are_well_formed():
    decoder = yaml.safe_load((ROOT / "conf/toxcast_decoder.yaml").read_text())
    patterns = {
        "uberon": r"^UBERON:\d{7}$",
        "cl": r"^CL:\d{7}$",
        "cellosaurus": r"^CVCL_[0-9A-Z]{4}$",
        "parent": r"^CVCL_[0-9A-Z]{4}$",
    }
    entries = list(decoder["tissue"].values())
    for value in decoder["cells"].values():
        entries += value if isinstance(value, list) else [value]
    for entry in entries:
        for key, pattern in patterns.items():
            if key in entry:
                assert re.match(pattern, entry[key]), entry
