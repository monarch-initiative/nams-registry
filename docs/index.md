# nams-registry

The registry records a landscape analysis of New Approach Methodologies
(NAMs). It holds two kinds of record:

- **Resources**: the sources reviewed for NAMs, such as vendor catalogues,
  databases and the scientific literature, one file per resource in
  `resources/`. Each records what the source holds, how relevant it is, and
  how its NAMs can be extracted.
- **NAM records**: the NAMs found in those resources, one file per NAM in
  `nams/`. Each record holds the NAM as a [NAMO](https://github.com/monarch-initiative/namo)
  model, and around it what the registry adds: the resources the NAM was
  found in, what it is used for, and its limitations.

[Browse the records](resources/index.html) to see both, with a tab for each.

## Schemas

Each kind of record has its own schema:

- [Resources](elements/index.md), from `nam_resources.yaml`. Start with
  [Resource](elements/Resource.md).
- [NAM records and NAMO](nam-records/index.md), from `nam_records.yaml`,
  which imports NAMO. Start with [NAMRecord](nam-records/NAMRecord.md). The
  registry's own classes are NAMRecord, SourceRecord, NAMStatement,
  Comparison, DismechStatus and Product. Every other class on those pages,
  from [ModelSystem](nam-records/ModelSystem.md) down, is NAMO's, at the
  NAMO commit `pyproject.toml` pins, so the pages match what the records are
  validated against.
