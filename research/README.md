# Deep research

Reports written by [deep-research-client](https://pypi.org/project/deep-research-client/),
kept here as provenance for the resource records they informed.

```
research/<stem>-deep-research-<provider>.md              the report
research/<stem>-deep-research-<provider>_artifacts/      the provider's own output files
research/<stem>-deep-research-<provider>.errata.md       corrections found after the run
```

The `<stem>` is `<first author><year>-<short topic>`. A report is filed under the name
of whoever wrote the thing it is about, because that is what someone looking for it
will know. Do not use an article id from the tail of a DOI: `kfae159` identifies this
paper perfectly and means nothing to a reader.

A report names its own `_artifacts/` directory in its frontmatter and body, so renaming
one means renaming the directory and updating those paths together. That is the single
mechanical edit a report may receive — see the rules below.

## What a report is for

A report is a lead, never a source. It is one model's reading of a paper, and it is
wrong often enough that nothing in it may be copied into a resource record on its
authority alone.

To use a report:

1. Read it, including the `reference_validation` block in its frontmatter. A
   `confabulation_rate` of 0 means the citations it gave resolve — it does not mean
   the claims around them are right.
2. For each fact worth keeping, read the primary source. For a report about a single
   paper, that means the paper itself and its supplementary material.
3. Write the fact into the resource record from the source, not from the report.
4. Say in the pull request which report informed the record, and name the provider and
   model (both are in the report's frontmatter).

## Where a report lives

A report lives in the repository that holds the records it informs. Most of the
registry's papers are processed through
[DisMech](https://github.com/monarch-initiative/dismech), so most reports are not
here:

- **Run on a DisMech entity** — a disease entry, a module, a comorbidity, a drug or
  model within a disease. DisMech's `just research-*` recipes write the report into
  DisMech's own `research/` and it is committed there. A registry record informed by
  one names it by URL; it is not copied here.
- **Run on a paper** — no DisMech entity, so no DisMech recipe applies. The report
  belongs here, with the records it informs.

Nothing moves a report between the two repositories. DisMech's recipes write only to
DisMech's `research/`, and none of them mentions this registry.

Two consequences worth knowing before sending a paper to DisMech:

- **Every DisMech recipe is keyed on a DisMech entity, and none takes a PMID or DOI.**
  `just research-disorder` requires `kb/disorders/<name>.yaml` to exist and stops if it
  does not. A paper with no DisMech anchor cannot be run through them, so step 4 of
  [the Complement-ARIE project](../projects/COMPLEMENT_ARIE_DISEASE_PAPERS.md) is at
  present a direct `deep-research-client` call with a prompt written for the paper.
- **A report produced that way carries no `template_file`** in its frontmatter, because
  no template file produced it. Record the prompt in the pull request instead.

## Rules

- **Reports are committed.** They are provenance, and a provider run costs real money
  and real time.
- **Never edit a report's content or its provider frontmatter.** They record what was
  produced and what produced it, and an edited report no longer does. Corrections go in
  a sibling `.errata.md`, however obviously wrong the report is.
- **The one permitted edit is a report's own `_artifacts/` paths**, when the report is
  renamed and those paths would otherwise dangle. It changes no claim and no provenance
  fact. Record it in the `.errata.md` with the before and after checksums, so the file
  can still be shown to be the provider's output.
- A report informs a resource record; it is never cited by one. Resource `publications`
  cite the paper, not the report.

## Checking a report

A report is a lead, so some of its claims get checked against the primary source, and
a check worth doing twice is worth committing. When checking one meant running
something, that goes in a directory named for the report's stem and what it derives --
`cable2025-ipp-panel/` beside `cable2025-nam-...-openscientist.md` -- holding the
scripts, their committed output, and a README saying what the numbers are and what
they do not settle.

- **The errata states the finding; the directory shows the work.** A reader who only
  wants the correction reads the errata. A reader who doubts it re-runs the scripts.
- **Commit the output, not the inputs.** A publisher's supplementary file is
  re-downloadable; pin its checksum and gitignore the file. Output that is committed
  turns a later re-run into a diff, which is the point.
- **A derivation directory is not a report** and is not subject to the no-editing
  rule. It is ordinary repository content: fix it, improve it, delete it when the
  claim it supports is gone.
- **It records what it could not settle.** A disagreement between a paper and its own
  supplement is not resolvable by reading the supplement harder, and a directory that
  quietly picks one number is worse than no directory.

## Reports

| Report | Subject | Informs |
|---|---|---|
| `cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist.md` | Cable et al. 2025, *Advancing systemic toxicity risk assessment: evaluation of a NAM-based toolbox approach*, Toxicol Sci 204(1):79-95 ([10.1093/toxsci/kfae159](https://doi.org/10.1093/toxsci/kfae159), PMID:39693112) | four NAM records and four resources, in [#101](https://github.com/monarch-initiative/nams-registry/pull/101). Checked by [`cable2025-ipp-panel/`](cable2025-ipp-panel/README.md) |
