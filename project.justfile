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
