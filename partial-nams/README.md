# Partial NAM records

A partial NAM record is a NAM found in a resource and recorded only in part.
It holds only what the resource gives publicly, in the resource's own terms,
in `partial-nams/<resource>/<id>.yaml`, and validates as a `PartialNAMRecord`
(in `src/nams_registry/schema/nam_records.yaml`).

A NAM is kept as a partial record where a full record in `nams/` can't yet be
written. For NAMs.network, a NAM's full record needs a logged-in account and
the site states no terms for reusing it, so the registry holds only the
public catalogue entry until that is settled.

Partial records are generated, not written by hand. Each resource with partial
records has a script that writes them:

| Folder | Resource | Script |
|---|---|---|
| `namsnetwork/` | [NAMs Network](../resources/namsnetwork.yaml) | `scripts/write_partial_namsnetwork.py`, from the output of `scripts/fetch_namsnetwork.py` |

To write a full record for a NAM, add a NAM record in `nams/` whose
`source_resources` names the partial record's `source_urls`, then rerun the
script: it no longer writes a partial record for a NAM that a full record
names. The tests fail while both exist.

A partial record's `proposed_namo_class` is set only where the resource's data
makes the class clear, and is a starting point, not a decision.
