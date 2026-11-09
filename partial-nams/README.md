# Partial NAM records

A partial NAM record is a NAM found in a resource and recorded only in part.
It holds only what the resource gives publicly, in the resource's own terms,
in `partial-nams/<resource>/<id>.yaml`, and validates as a `PartialNAMRecord`
(in `src/nams_registry/schema/nam_records.yaml`).

A NAM is kept as a partial record where the registry can't hold the
resource's full records. For NAMs.network, a NAM's full record needs a
logged-in account and the site states no terms for reusing it, so the
registry holds only the public catalogue entry.

Partial describes what the registry can hold from a resource, not how far a
NAM has been curated. A partial record is not a draft, and not a queue of NAMs
waiting to be curated.

Partial records are generated, not written by hand. Each resource with partial
records has a script that writes them:

| Folder | Resource | Script |
|---|---|---|
| `namsnetwork/` | [NAMs Network](../resources/namsnetwork.yaml) | `scripts/write_partial_namsnetwork.py`, from the output of `scripts/fetch_namsnetwork.py` |

A NAM has either a partial record or a NAM record in `nams/`, not both. If a
NAM record's `source_resources` names a partial record's `source_urls`, the
script no longer writes that partial record when rerun, and the tests fail
while both exist.

A partial record's `proposed_namo_class` is set only where the resource's data
makes the class clear, and is a starting point, not a decision.
