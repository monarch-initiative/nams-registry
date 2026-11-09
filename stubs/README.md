# NAM stubs

A stub is a NAM found in a resource and not yet curated. It holds only what
the resource gives, in the resource's own terms, in
`stubs/<resource>/<id>.yaml`, and validates as a `NAMStub` (in
`src/nams_registry/schema/nam_records.yaml`).

Stubs are generated, not written by hand. Each resource with stubs has a
script that writes them:

| Folder | Resource | Script |
|---|---|---|
| `namsnetwork/` | [NAMs Network](../resources/namsnetwork.yaml) | `scripts/stub_namsnetwork.py`, from the output of `scripts/fetch_namsnetwork.py` |

To curate a NAM, write a NAM record for it in `nams/` whose
`source_resources` names the stub's `source_urls`, then rerun the script:
it no longer writes a stub for a NAM that a record names. The tests fail
while both exist.

A stub's `proposed_namo_class` is set only where the resource's data makes
the class clear, and is a starting point, not a decision.
