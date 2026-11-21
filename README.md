<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# nams-registry

This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.

## Documentation Website

[https://monarch-initiative.github.io/nams-registry](https://monarch-initiative.github.io/nams-registry)

The [registry browser](https://monarch-initiative.github.io/nams-registry/resources/)
lists every record in the registry, with a tab each for resources and NAM
records. `just build-table` rebuilds it, and the docs
deployment does so on every push to main.

The site also documents both schemas: the resources schema,
`nam_resources.yaml`, and the NAM records schema, `nam_records.yaml`,
together with the NAMO classes it imports, at the NAMO commit
`pyproject.toml` pins. `just gen-doc` generates both.

## Making changes

A change is made to a record, to the schema, or to both:

- **A record** describes one resource, in `resources/<id>.yaml`. Each
  resource has a review issue, labelled `resource-review`, where it is
  discussed; the registry browser links to it.
- **A NAM record** describes one NAM extracted from those resources, such
  as an organoid system, in `nams/<id>.yaml`. Its `model` is the NAM as an
  unmodified [NAMO](https://github.com/monarch-initiative/namo) model, whose
  `type` names the NAMO class, such as `Organoid`. Around it the record
  holds what NAMO does not: the resources the NAM was found in
  (`source_resources`), what it is used for and its limitations, each with
  the pages it was taken from. A NAM found in a research paper names the
  `scientific-literature` resource, alongside any database or catalogue it
  is also found in, with the paper's DOI link in
  `source_urls` and its citation in the model's `references`; a paper is
  not a resource of its own. Two NAMs compared head to head in one study
  name each other, and the paper, in `compared_with`. A NAM that came
  through DisMech curation records whether DisMech's graph represents it
  in `dismech_status`.
- **The schema**, `src/nams_registry/schema/nam_resources.yaml`, sets
  what every resource record can hold. NAM records have a separate schema,
  `nam_records.yaml`, which imports NAMO; the two schemas do not import
  each other. NAMO's schema is kept only in the
  [namo repository](https://github.com/monarch-initiative/namo), never here:
  `just namo` links it from a local NAMO checkout (`NAMO_DIR`, or `../namo`)
  or, without one, downloads it from GitHub at the NAMO commit set in
  `pyproject.toml` (`[tool.nams-registry.namo]`), or at `NAMO_REF`. The
  tests do this themselves.
  Where a NAM needs a property NAMO lacks, it is added to
  `nam_records.yaml` and proposed to NAMO at the same time (see below).

In practice records and the schema change together, because it is the
content that drives the schema. Reviewing a resource or curating a NAM
usually turns up something the schema has no field for, and the schema
change lands in the same pull request as the records that need it. When
that happens:

- Open an issue labelled `schema-change` first, saying what the records
  need and why. The pull request that makes the change closes it.
- Make the schema change in its own commit, ahead of the record changes
  that use it, since it affects every record of that kind. Include the
  files it regenerates: `just test` regenerates the Python datamodel, and
  `just gen-doc` the copy in `docs/schema/`.
- Refer to the issue the records came from, such as a resource's review
  issue, in the record commits and in the pull request.

A property a NAM record needs but NAMO lacks is added here and proposed to
NAMO at the same time. The goal is for the NAMO schema to cover every
attribute of a NAM, but curation does not wait for NAMO. In order:

1. Add the property to `src/nams_registry/schema/nam_records.yaml`, in its
   own commit as above.
2. Open an issue in
   [monarch-initiative/namo](https://github.com/monarch-initiative/namo/issues)
   proposing the property for the NAMO schema.
3. Cite that issue, as `monarch-initiative/namo#N`, in the property's
   description and in the pull request.
4. Once NAMO has the property and `pyproject.toml` pins a NAMO commit that
   includes it, move the values into each record's `model` and remove the
   property from `nam_records.yaml`.

Only the property moves. The NAM records in `nams/` stay in this registry.

Make each change on a branch, and run `just test` before opening a pull
request.

## Checking terms and references

`just test` also checks, without the network, that:

- each ontology term in a NAM record exists, sits under the root of the
  NAMO enum it is bound to (e.g. a cell type under CL `cell`), and carries
  the ontology's own label, using
  [linkml-term-validator](https://github.com/linkml/linkml-term-validator);
- each reference a NAM record or resource cites resolves, and each title
  given is the reference's own, using
  [linkml-reference-validator](https://github.com/linkml/linkml-reference-validator).

These checks read the lookups kept in `cache/` and `references_cache/`, which
are committed. When you add a term or a reference, run `just validate-terms`
or `just validate-references` (they use the network), then commit what they
add to the caches. `conf/oak_config.yaml` says where each ontology is looked
up. `just search-term`, `just term-info` and `just fetch-reference` help find
and read terms and references.

A reference is cached with its full text where the paper's licence allows it
(`fetch_full_text` in `.linkml-reference-validator.yaml`). Open access is
enforced by the fetcher, not by the curator: a PMC author manuscript is free
to read but not open-access licensed, and is cached as an abstract. The full
text is kept because a NAM that no mechanism graph can hold today may be
linked later, and that linkage will need evidence from the paper's methods
and results rather than its abstract.

## Checking quotes, and reading a paper

A statement in a NAM record can carry the source's own words, as
`applications` / `limitations` > `quotes`, each quote with the one reference it
is from. `just check-snippets` finds every quote in its reference's cached
text and reports the ones that are not there; `--strict` makes that a
failure, which is what a pull request wants.

```bash
just check-snippets                      # every record in nams/
just check-snippets --strict             # exit 1 on an unverified quote

# A real run, keyed on the paper rather than on a DisMech entity:
just deep-research --provider openscientist --input-file prompt.md \
  --output research/<stem>-deep-research-openscientist.md

# A run on a researcher, team or organization, from a committed spec
# (see research/README.md, "Running a research group"):
just research-group-works carreras_puigvert      # its papers, from OpenAlex
just research-group-prompt carreras_puigvert     # read before paying
just research-group openscientist carreras_puigvert

# A cheap end-to-end check that the recipe works; the mock provider is
# off unless its own environment variable enables it:
ENABLE_MOCK_PROVIDER=true just deep-research --provider mock "a test query"
```

A quote whose reference is cached as an abstract only is reported apart, and
`--strict` still fails on it: nothing is established either way, because the
full text may well contain it. The cure is to cache the full text, not to
pass `--allow-abstract-only`.

Both recipes **import DisMech rather than copying it** — the snippet audit
from `dismech.reference_snippet_audit`, and the research provider policy from
`dismech.deep_research_policy`. Nothing is copied into this repository; one
copy of the thing stays in the repository that owns it, as with `just namo`.

DisMech is in the `research` dependency group in `pyproject.toml`, pinned to a
commit and resolved in `uv.lock`. It is a group rather than a project
dependency because only these two recipes need it, so `uv sync` does not
install it by default; the recipes pass `--group research`. Bump the pin by
editing the rev and running `uv lock --upgrade-package dismech`. DisMech
requires Python >=3.12, which is why this project's floor is >=3.12.

The research client itself is the third-party `deep-research-client`, in the
same group; DisMech does not implement one either. DisMech's own
`just research-*` recipes are each keyed on a DisMech entity and none takes a
PMID, which is why a paper with no DisMech anchor is run from here. Read
[research/README.md](research/README.md) before committing a report: a report
is a lead, never a source.

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated documentation of the resources schema
  * nam-records/ - generated documentation of the NAM records schema and
    the NAMO classes it imports (not committed)
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [resources/](resources/) - one file per resource in the registry (edit these)
* [nams/](nams/) - one file per NAM extracted from the resources (edit these)
* [scripts/](scripts/) - scripts that fetch content from resources
  (`fetch_*.py`) and write NAM records from it (`write_*.py`), to be
  listed in the resource's `supporting_scripts`. Also `link_namo.py`,
  which `just namo` runs, and `fetch_openalex_works.py` and
  `research_group_vars.py`, which the `research-group` recipes run.
* [projects/](projects/) - project pages for curation work that spans many
  records, such as the Complement-ARIE disease papers, with their review
  logs
* [research/](research/) - deep-research reports, kept as provenance for
  the records they informed; a report is a lead, never a source (see its
  [README](research/README.md))
* [templates/](templates/) - deep-research prompts, and one spec per
  research group in `research_groups/`; `just research-group` runs them
* [cache/](cache/) - ontology term lookups that `just test` checks NAM
  records against offline; `just validate-terms` adds to it (commit what
  it adds)
* [references_cache/](references_cache/) - the cited references, one file
  each, that `just test` checks citations against offline;
  `just validate-references` and `just fetch-reference` add to it (commit
  what they add)
* [conf/](conf/) - `oak_config.yaml`, which says where each ontology is
  looked up when the term cache is filled
* [src/](src/) - source files (edit these)
  * [nams_registry](src/nams_registry)
    * [schema/](src/nams_registry/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/nams_registry/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/).
To list all pre-defined commands, run `just` or `just --list`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
