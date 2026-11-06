<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# nams-registry

This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.

## Documentation Website

[https://monarch-initiative.github.io/nams-registry](https://monarch-initiative.github.io/nams-registry)

The [resource table](https://monarch-initiative.github.io/nams-registry/resources/)
lists every resource in the registry.

## Making changes

There are two kinds of change, each with its own kind of issue. Make
each change on a branch and open a pull request that refers to the issue.

- **Updating a record.** A change to one resource, such as setting its
  NAMs relevance or priority, is made in that resource's file,
  `resources/<id>.yaml`. Each resource has a review issue, labelled
  `resource-review`, where it is discussed; the resource table links to it.
- **Changing the schema.** A change to what the registry records, such as
  adding a record count, is made in
  `src/nams_registry/schema/nams_registry.yaml`. Discuss it first in an
  issue labelled `schema-change`, since it affects every resource. Once
  the schema change is merged, filling in the new field for a resource is
  a record update.

Run `just test` before opening a pull request.

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
