"""Tests for the KG-Registry import."""

from nams_registry.import_kg_registry import convert_publication


def test_publication_id_becomes_doi_curie():
    """Test that a doi.org URL id becomes a doi: CURIE, the year an integer,
    and that the doi and preferred fields are dropped."""
    publication = {
        "id": "https://doi.org/10.1093/nar/gkw928",
        "title": "A paper",
        "year": "2017",
        "doi": "10.1093/nar/gkw928",
        "preferred": True,
    }
    assert convert_publication(publication) == {
        "id": "doi:10.1093/nar/gkw928",
        "title": "A paper",
        "year": 2017,
    }


def test_publication_pubmed_id_becomes_its_doi():
    """Test that a PubMed URL id is replaced by the publication's DOI."""
    publication = {
        "id": "https://pubmed.ncbi.nlm.nih.gov/36271792/",
        "title": "A paper",
        "doi": "10.1093/nar/gkac942",
    }
    assert convert_publication(publication)["id"] == "doi:10.1093/nar/gkac942"


def test_publication_without_doi_keeps_its_id():
    """Test that a publication with no DOI keeps its id, e.g. a report's URL."""
    url = "https://example.org/report.pdf"
    assert convert_publication({"id": url, "title": "A report"})["id"] == url
