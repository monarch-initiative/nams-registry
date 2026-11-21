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

# Generate the NAM records schema docs, with the NAMO classes at the pinned commit, into docs/nam-records/
[group('model development')]
gen-doc-nam-records: namo
  -rm -rf docs/nam-records/*.md
  uv run gen-doc {{gen_doc_args}} -d docs/nam-records {{source_schema_dir}}/nam_records.yaml

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

# Check each quote in a NAM record is really in its cited reference (imports DisMech's snippet audit)
[group('research')]
[positional-arguments]
check-snippets *args:
  uv run --group research python -m nams_registry.check_snippets "$@"

# Run a deep-research provider on a paper, e.g. `just deep-research --provider mock "query"`
# [positional-arguments] keeps a quoted multi-word query as one argument; with
# just's plain `{{args}}` expansion the shell resplits it on spaces.
[group('research')]
[positional-arguments]
deep-research *args:
  uv run --group research python -m nams_registry.deep_research "$@"

# Search an ontology for a term, e.g. `just search-term sqlite:obo:cl "goblet cell"`
[group('data')]
search-term adapter query:
  uv run runoak -i {{adapter}} search "{{query}}"

# Show a term, e.g. `just term-info sqlite:obo:uberon UBERON:0002048`
[group('data')]
term-info adapter curie:
  uv run runoak -i {{adapter}} info {{curie}}

# Fetch a research group's papers from OpenAlex into templates/research_groups/<slug>.works.yaml (commit it)
[group('research')]
research-group-works slug:
  uv run python scripts/fetch_openalex_works.py {{slug}}

# Print the prompt `just research-group` would send for a group, and stop. Read it before paying for a run.
[group('research')]
research-group-prompt slug:
  uv run --group research python scripts/research_group_vars.py {{slug}} --format prompt

# Goes through `just deep-research`'s wrapper, so DisMech's provider policy applies.
# Writes research/<stem>-deep-research-<provider>.md and its _artifacts/, with every
# reference checked against references_cache/. Extra arguments go to the client,
# e.g. `-- --param max_iterations=8 --param timeout=7200`.
#
# Refuses to run while the template, the group's spec or its paper list has
# uncommitted changes: the report's frontmatter names the template and every
# variable, and a committed template is what lets that be traced to a revision.
# Refuses to overwrite a report, too; change the spec's stem for a second run.
#
# Run deep research on a research group's models, e.g. `just research-group openscientist carreras_puigvert`
[group('research')]
research-group provider slug *args="":
  #!/usr/bin/env bash
  set -euo pipefail
  template=templates/research_group_models.md
  spec=templates/research_groups/{{slug}}.yaml
  works=templates/research_groups/{{slug}}.works.yaml
  dirty=$(git status --porcelain -- "$template" "$spec" "$works" scripts/research_group_vars.py)
  if [ -n "$dirty" ]; then
    echo "Commit these before a run, so the report can be traced to them:" >&2
    echo "$dirty" >&2
    exit 1
  fi
  stem=$(uv run python scripts/research_group_vars.py {{slug}} --format stem)
  output="research/$stem-deep-research-{{provider}}.md"
  if [ -e "$output" ] || [ -e "research/$stem-deep-research-{{provider}}_artifacts" ]; then
    echo "$output already exists. Reports are never overwritten; give the spec a new stem." >&2
    exit 1
  fi
  # The values are multi-line, so they pass through a NUL-separated file:
  # command substitution would drop the separators.
  vars_file=$(mktemp)
  trap 'rm -f "$vars_file"' EXIT
  uv run python scripts/research_group_vars.py {{slug}} --format null > "$vars_file"
  var_args=()
  while IFS= read -r -d '' record; do
    var_args+=(--var "$record")
  done < "$vars_file"
  echo "Research group {{slug}} ({{provider}}) -> $output"
  uv run --group research python -m nams_registry.deep_research \
    --template "$template" \
    "${var_args[@]}" \
    --provider {{provider}} \
    --output "$output" \
    --validate-references --validation-cache-dir references_cache \
    {{args}}
