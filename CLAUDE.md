# Working in nams-registry

Notes for an agent working in this repository. [README.md](README.md) says how
records and the schema are laid out and what `just` recipes exist;
[CONTRIBUTING.md](CONTRIBUTING.md) covers GitHub, LinkML and modeling practice.
This file holds what neither of those records: the judgment calls this registry
has settled, and the habits that keep a session from breaking things.

## Curation conventions

These were settled while curating papers from the Complement-ARIE Landscape
Analysis (see
[projects/COMPLEMENT_ARIE_DISEASE_PAPERS.md](projects/COMPLEMENT_ARIE_DISEASE_PAPERS.md)),
and they apply beyond that round.

**One NAM record per distinct biological system.** A paper describing an
organoid, a lesioned mouse and the chimera made by grafting one into the other
yields three records. Assays, stains, reporter lines and behavioural batteries
are not records: they are readouts on a record, or entries in `applications`.
If a variant of a protocol differs enough that it looks like its own system,
say so rather than deciding silently — the granularity rule is meant to be
revisited with a case in hand.

**Do not rule a model out of a mechanism before reading the evidence.** A
disease can be modelled in more than one way, and several models on one
mechanism node is the point, not a duplication to avoid. A system built from
healthy donor lines can still carry mechanism evidence; a model that only
replaces a cell population can still speak to the causal chain. State what the
evidence supports, and put what it does not into `limitations`, `divergences`
and `fidelity` — not into a decision to leave the model out.

**Screening records what a paper shows; it does not filter papers out.** Every
method kind belongs in the registry: in vitro, in silico, in chemico,
bioanalytical, clinical, epidemiological, animal, ecotoxicological. A paper is
set aside only when no method or model can be identified at all, and the reason
is written down along with whether the decision rested on the abstract alone,
so it can be revisited. Whether a paper has a DisMech anchor decides *where*
its NAMs go, never whether it is kept.

**Save rather than lose.** A record the schema cannot yet hold is still
written, and parked where it will not fail validation (currently
`projects/COMPLEMENT_ARIE_DISEASE_PAPERS/deferred-records/`, pending
[#90](https://github.com/monarch-initiative/nams-registry/issues/90)). Do not
discard curation work because the field for it does not exist yet; open the
schema issue and keep the record.

**A record from a paper names two resources.** `scientific-literature`, and the
resource the paper was found through — each with the paper's DOI, and the
discovery resource carrying `accessed_on`:

```yaml
source_resources:
- resource: scientific-literature
  source_urls:
  - https://doi.org/10.7150/thno.80271
- resource: complement-arie-landscape-dashboard
  source_urls:
  - https://doi.org/10.7150/thno.80271
  accessed_on: '2026-11-13'
```

A paper is not a resource of its own.

**A record describes either a method or one study's use of it, and the schema
cannot yet say which.** The EPA MEA assay record describes a protocol; a
patient-derived organoid record describes one study's system. Provenance does
not settle it — reviews are publications that yield method descriptions. Until
[namo#52](https://github.com/monarch-initiative/namo/issues/52) and
[#86](https://github.com/monarch-initiative/nams-registry/issues/86) resolve
this, write the record plainly and do not invent a local flag for it.

**Prefer proposing a missing field in NAMO over adding it here.** The registry's
own NAM fields are stopgaps; the goal is NAMO covering the attributes of a NAM.

## Working habits

- **Never commit to `main`.** Branch, then open a pull request when asked. A
  request to save work means a commit on a pushed branch, not a pull request.
- **Run `just test` before pushing**, not bare `pytest` — CI's `just test`
  checks the examples that pytest skips. `just validate-resources` too when
  records changed.
- **Do not run `pre-commit run --all-files`.** The fixing hooks rewrite files
  across the repository. Survey with read-only runs, or in a throwaway
  worktree.
- **Update a branch with `git rebase --onto origin/main`** and force-push with
  `--force-with-lease`. Do not merge `main` into a branch.
- **Never push to someone else's branch.** Open your own and link to theirs.
- **Write "partial record", not "stub"**, for the files in `partial-nams/` and
  for a gap in an external resource such as AOP-Wiki or NAMs.network. "Stub"
  means something else in DisMech.
- **Do not name colleagues in public issues.** Attribute team feedback
  anonymously; no `@` mentions.
- **Write issue and PR numbers as links**, never a bare `#N`.

## Writing for GitHub

Every issue, comment and pull request body an agent writes opens with:

```
🤖 *Written by [Claude Code](https://claude.com/claude-code) for Ginnie Hench.*
```

Pull request descriptions also end with the generated-with-Claude-Code line,
and commit messages end with the `Co-Authored-By` trailer.
