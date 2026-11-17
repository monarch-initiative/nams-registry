# Schema Directory

This folder contains the LinkML schemas. Each kind of record has its own, and
the two do not import each other.

- `nam_resources.yaml`: the resources in `resources/`. `config.public.mk`
  names it as the project's main schema (`LINKML_SCHEMA_NAME`), so it is the
  one the `just` recipes generate the Python datamodel and `docs/schema/`
  from.
- `nam_records.yaml`: the NAM records in `nams/`. It imports NAMO.
- `namo.yaml`: a link to NAMO's schema, made by `just namo`, which
  `nam_records.yaml` imports. NAMO's schema is kept in the
  [namo repository](https://github.com/monarch-initiative/namo), never
  here, so this file is not committed and is not edited.
