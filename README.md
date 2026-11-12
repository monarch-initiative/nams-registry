<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# nams-registry

This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.

## Documentation Website

[https://monarch-initiative.github.io/nams-registry](https://monarch-initiative.github.io/nams-registry)

The [registry browser](https://monarch-initiative.github.io/nams-registry/resources/)
lists every record in the registry, with a tab each for resources, NAM
records and partial NAM records. `just build-table` rebuilds it, and the docs
deployment does so on every push to main.

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
  `scientific-literature` resource, with the paper's DOI link in
  `source_urls` and its citation in the model's `references`; a paper is
  not a resource of its own. Two NAMs compared head to head in one study
  name each other, and the paper, in `compared_with`. A NAM that came
  through DisMech curation records whether DisMech's graph represents it
  in `dismech_status`.
- **The schema**, `src/nams_registry/schema/nams_registry.yaml`, sets
  what every record can hold. NAM records have a separate schema,
  `nam_records.yaml`, which imports NAMO; the two schemas do not import
  each other. NAMO's schema is kept only in the
  [namo repository](https://github.com/monarch-initiative/namo), never here:
  `just namo` links it from a local NAMO checkout (`NAMO_DIR`, or `../namo`)
  or, without one, downloads it from GitHub at the NAMO commit set in
  `pyproject.toml` (`[tool.nams-registry.namo]`), or at `NAMO_REF`. The
  tests do this themselves.
  Where a NAM needs something NAMO lacks, prefer proposing it in NAMO over
  adding it here.

In practice the two tend to change together, because it is the content
that drives the schema. Reviewing a resource often turns up something
the registry has no field for, and the new field is added in the same
pull request as the record that needs it. When that happens:

- Make the schema change in its own commit, ahead of the record changes
  that use it, since it affects every resource. Include the files it
  regenerates: `just test` regenerates the Python datamodel, and
  `just gen-doc` the copy in `docs/schema/`.
- Refer to the resource's review issue in the record commits and in the
  pull request.

A schema change that needs discussion before anyone builds on it, or
that no single resource prompted, can have its own issue, labelled
`schema-change`.

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
and read terms and references. The setup follows
[mechmaker](https://github.com/monarch-initiative/mechmaker)'s.

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [resources/](resources/) - one file per resource in the registry (edit these)
* [nams/](nams/) - one file per NAM extracted from the resources (edit these)
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
