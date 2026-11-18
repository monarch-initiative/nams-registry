# Toxicology NAMs special issue

The *Toxicology* special issue "New approach methodologies: from conceptual
development to regulatory application" (2023-2024). Its twenty-five papers were
screened in DisMech, which keeps the screening log and a rationale per paper in
[`projects/NAMS_SPECIAL_ISSUE.md`](https://github.com/monarch-initiative/dismech/blob/main/projects/NAMS_SPECIAL_ISSUE.md)
and the open questions in
[`NAMS_SPECIAL_ISSUE/open-questions.md`](https://github.com/monarch-initiative/dismech/blob/main/projects/NAMS_SPECIAL_ISSUE/open-questions.md)
there. This page is only the registry's side: which of those papers have records
here, and where the ones that do not fit `nams/` are parked.

Most of the issue's papers reached the registry through DisMech curation, one
pull request per paper, and their records carry `dismech_status` with the
DisMech issue and pull request that handled them.

## The papers with no DisMech anchor

Five papers were screened out of DisMech because their output is a prediction, a
classification or a dose metric, so there is no mechanism node to attach a model
to. That decision is DisMech's and it is correct for DisMech; it says nothing
about the registry, whose criteria are strictly broader. The registry settled
that on 2026-11-13 (see
[COMPLEMENT_ARIE_DISEASE_PAPERS.md](COMPLEMENT_ARIE_DISEASE_PAPERS.md)): a
missing DisMech anchor decides *where* a NAM goes, never whether it is kept.

The question of whether the registry takes them is
[dismech#16882](https://github.com/monarch-initiative/dismech/issues/16882).
These records are the answer to it.

| Paper | NAM | Record |
|---|---|---|
| PMID:37993082 | Read-across-derived LDA QSAR for Ames mutagenicity | [`ames-mutagenicity-read-across-lda-qsar-in-silico`](../nams/ames-mutagenicity-read-across-lda-qsar-in-silico.yaml) |
| PMID:37993082 | Classical LDA QSAR for Ames mutagenicity, the comparator built in the same study | [`ames-mutagenicity-lda-qsar-in-silico`](../nams/ames-mutagenicity-lda-qsar-in-silico.yaml) |
| PMID:38043774 | HTTr in MCF7 cells for transcriptional points of departure | [`breast-monolayer-mcf7-httr-cell-line`](../nams/breast-monolayer-mcf7-httr-cell-line.yaml) |
| PMID:38056590 | Random Forest classifier for nanoparticle-induced cell death | [`nanoparticle-cytotoxicity-random-forest-in-silico`](../nams/nanoparticle-cytotoxicity-random-forest-in-silico.yaml) |
| PMID:38705560 | q-RASAR PLS model for subchronic oral NOAEL in rats | [`subchronic-oral-noael-q-rasar-pls-in-silico`](../nams/subchronic-oral-noael-q-rasar-pls-in-silico.yaml) |
| PMID:38719068 | Workflow for true dose considerations in in vitro testing | deferred, see below |

### Granularity

PMID:37993082 gets two records because the paper builds two models and
characterises both: the classical LDA QSAR model's descriptor class, its
descriptor count and its relative predictivity are all reported, so it is a NAM
in its own right and not just a baseline. The two name each other in
`compared_with`.

Three other comparators got no record, for the same reason in each case — the
abstract ranks them without characterising them:

- the four machine-learning classifiers PMID:38056590 trained alongside Random
  Forest (Decision Tree, Support Vector Machine, Naive Bayes, Artificial Neural
  Network);
- the corresponding QSAR model PMID:38705560 reports its q-RASAR model as
  superseding, with no performance values of its own;
- the tPOD calculation methods in PMID:38043774 (tcplfit2, BMDExpress, PLIER),
  which are analyses of one system's readout rather than systems of their own.

All of these are recorded in the prose of the record they belong to. If a later
paper characterises one of them properly, that is the case to revisit this on.

### Deferred records

`NAMS_SPECIAL_ISSUE/deferred-records/<id>.yaml` holds a record that cannot go
into `nams/` yet, following the `NAMRecord` shape as far as the schema allows,
with a comment at the top saying what does not fit and which issue will settle
it. These files are not validated. Once the schema can hold a record, it is
checked, moved into `nams/`, and this page is updated.

One record is deferred:

- [`in-vitro-true-dose-workflow-ngra`](NAMS_SPECIAL_ISSUE/deferred-records/in-vitro-true-dose-workflow-ngra.yaml)
  (PMID:38719068). It is a dosimetry decision workflow, not a model system, and
  NAMO's `ModelSystem` hierarchy has no class for one. Pending
  [namo#55](https://github.com/monarch-initiative/namo/issues/55) and
  [#90](https://github.com/monarch-initiative/nams-registry/issues/90). DisMech
  tracks where a dosimetry bridge belongs as
  [dismech#16887](https://github.com/monarch-initiative/dismech/issues/16887).

The Complement-ARIE round keeps its own `deferred-records/` folder under its own
project page. Both exist for the same reason and could be merged into one
location if a third round needs it.

## Access

All five papers are abstract-only for the registry's purposes. Four have no
PubMed Central copy. PMID:38043774 has one, PMC11917498, but it is an author
manuscript rather than an open-access article, so no full text is quoted or
cached. Every statement in these records comes from the abstract, and each
record says so in its last limitation.

## Still open for the registry

Two further papers from this issue raise the same question these five did and
have no records yet: PMID:38104655, a deep-learning framework that generates
candidate hazardous structures, and PMID:38857863, a next-generation risk
assessment for occupational safety built on an exposure and bioactivity ratio
across a NAM battery. Both are registry candidates on the criteria applied here.
PMID:37924932, a QSAR case study for mercury, is aquatic ecotoxicology reporting
a data gap rather than a working model, and DisMech recorded it as out of scope
for both repositories.

(Started 2026-11-18.)
