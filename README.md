<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# nams-registry

This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.

## Documentation Website

[https://monarch-initiative.github.io/nams-registry](https://monarch-initiative.github.io/nams-registry)

The [resource table](https://monarch-initiative.github.io/nams-registry/resources/)
lists every resource in the registry.

## Making changes

A change is made to a record, to the schema, or to both:

- **A record** describes one resource, in `resources/<id>.yaml`. Each
  resource has a review issue, labelled `resource-review`, where it is
  discussed; the resource table links to it.
- **The schema**, `src/nams_registry/schema/nams_registry.yaml`, sets
  what every record can hold.

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

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [resources/](resources/) - one file per resource in the registry (edit these)
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
