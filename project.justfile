## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Import KG-Registry resources in the nams collection into resources/
[group('data')]
import-kg-registry *args:
  uv run python -m nams_registry.import_kg_registry {{args}}

# Validate every resource file in resources/
[group('data')]
validate-resources:
  uv run linkml-validate -s {{source_schema_path}} -C Resource resources/*.yaml

# Validate every NAM file in nams/, the record and its NAMO model
[group('data')]
validate-nams:
  uv run pytest -q tests/test_resources.py -k nam_file_is_valid

# Link the NAMO schema from a local checkout (NAMO_DIR or ../namo), or download the ref in pyproject.toml
[group('model development')]
namo:
  uv run python scripts/link_namo.py

# Build the registry browser (resources and NAM records), docs/resources/index.html
[group('data')]
build-table:
  uv run python -m nams_registry.build_table

# Open a GitHub review issue for each resource without one, and record its URL
[group('data')]
create-review-issues *args:
  uv run python -m nams_registry.create_review_issues {{args}}

# Check NAM records' ontology terms against their NAMO enums (looks up and caches new terms; commit cache/)
[group('data')]
validate-terms *files:
  uv run python -m nams_registry.check_records terms {{files}}

# Check each reference resolves and each title given is its own (fetches new ones; commit references_cache/)
[group('data')]
validate-references *files:
  uv run python -m nams_registry.check_records references {{files}}

# Fetch a reference into references_cache/ and show it, e.g. `just fetch-reference doi:10.1038/nm.3201`
[group('data')]
fetch-reference ref:
  uv run linkml-reference-validator lookup {{ref}} --config .linkml-reference-validator.yaml

# Search an ontology for a term, e.g. `just search-term sqlite:obo:cl "goblet cell"`
[group('data')]
search-term adapter query:
  uv run runoak -i {{adapter}} search "{{query}}"

# Show a term, e.g. `just term-info sqlite:obo:uberon UBERON:0002048`
[group('data')]
term-info adapter curie:
  uv run runoak -i {{adapter}} info {{curie}}
