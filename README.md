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
  which `just namo` runs.
* [projects/](projects/) - project pages for curation work that spans many
  records, such as the Complement-ARIE disease papers, with their review
  logs
* [research/](research/) - deep-research reports, kept as provenance for
  the records they informed; a report is a lead, never a source (see its
  [README](research/README.md))
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
