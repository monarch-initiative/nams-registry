# Research group models template

## The group under study

- **Name:** {group_name}
- **Kind:** {group_kind}
- **Period covered:** {date_range}

{group_description}

**Focus for this run:** {focus}

## Goal

Produce a structured, evidence-cited account of the biological and computational
models (the methods, test systems and platforms) that this group develops and uses,
the mechanisms and phenotypes it has characterised with them, and the contexts of use
and domains it works in. The account is the starting point for curating method
records in a registry of New Approach Methodologies (NAMs) and for finding
biological mechanisms that could be written up as Adverse Outcome Pathways (AOPs).

Every kind of method counts: in vitro, in silico, in chemico, bioanalytical, clinical,
epidemiological, animal and ecotoxicological. Do not leave out a method because it
seems minor or conventional. Report it and say what it was used for.

## The group's publications

These were retrieved from OpenAlex for this group and pruned by a curator. Treat
them as the core corpus, not as a limit: search for further papers by the group,
especially the papers that first set up a platform the later work relies on, and
say which ones you added.

{anchor_papers}

## 1. Methods and models

Give each distinct system its own entry. Where a paper describes variants of one
protocol, say whether each is a variant of one system or a system in its own right,
and why. Assays, stains, reporters and analysis pipelines run *on* a system are its
readouts, not systems of their own; list them under the system.

For each system, report the fields a registry record needs:

- **name**, and **model type**: one of TwoDCellCulture, ThreeDCellCulture, CoCulture,
  Organoid, OrganOnChip, CellLineModel, AnimalModel, QSARModel, PBPKModel, MLModel,
  MolecularModel, or "other: …" when none fits;
- **description**: what the system is and what it reads out;
- **biological material**: cell types, cell lines, species, and cell source
  (pluripotent stem cells, adult tissue, tumor tissue, immortalized cell lines,
  primary cells);
- **culture or run conditions**: format, exposure route and duration, imaging or
  computation set-up;
- **readouts**: staining panel or assay, feature extraction and analysis pipeline;
- **perturbations**: compound libraries, environmental chemicals, mixtures, genetic
  perturbations, infection;
- **applications**: what the group used it to do, one entry per distinct use;
- **validation**: reference compounds, benchmarks, orthogonal assays;
- **limitations**: what it cannot show, in the authors' own terms where they state
  them;
- **origin**: whether the group developed the system or applied an existing one;
- **references**: PMID or DOI for each paper that uses it.

## 2. Mechanisms and phenotypes

List the mechanisms, pathways, cellular processes and phenotypes the group's systems
have been used to detect or distinguish. For each, state the evidence (paper, system,
readout, effect size where given) and how specific the signature was to that
mechanism as opposed to general cytotoxicity or cell loss. Suggest ontology terms
(GO biological process, Cell Ontology, CHEBI) where they are obvious, labelled as
suggestions.

## 3. Candidate mechanistic chains (possible new AOPs)

A central aim is to find mechanisms in this work that could be written up as AOPs
but may not yet exist as AOPs. Work from the evidence outward:

1. First, from the papers and any data you analyse, and **without consulting
   AOP-Wiki or fitting to existing AOPs**, lay out each causal chain the evidence
   supports: the initiating molecular interaction where known, the intermediate
   cellular events the readouts capture, and the downstream outcomes at cell, tissue
   or organism level. For each link, give the evidence (dose-response, temporal
   order, rescue or knockout, reference compounds) and how strong it is. Gaps and
   uncertain links are findings too; do not fill them with steps the evidence does
   not show.
2. Only after that, check AOP-Wiki (aopwiki.org) to see which events and
   relationships in each chain already exist there, giving Key Event, Key Event
   Relationship and AOP IDs where they match. Treat AOP-Wiki as a coverage check,
   not as the right answer: where the evidence diverges from an existing AOP, report
   the divergence instead of resolving it toward AOP-Wiki.
3. Flag the chains, events and relationships that appear to be absent from AOP-Wiki
   as candidate new AOPs or Key Events, and say what further evidence each would need.

## 4. Contexts of use and domains

Classify the work by domain (for example drug discovery and repurposing, mechanism
of action deconvolution, toxicology and chemical safety, environmental monitoring,
infectious disease, oncology, neurodegeneration) and by decision context (hazard
identification, prioritisation or screening, mode-of-action support, benchmarking).
Note where the group positions its methods as NAMs for regulatory or safety use, and
any links to AOPs or Key Events that the papers themselves make.

## 5. Data

These datasets are attributed to the group in OpenAlex. Search for others it has
released or used (for example in the Cell Painting Gallery, the Image Data Resource,
Zenodo, Figshare, the SciLifeLab Data Repository, GEO, PRIDE or BioStudies).

{known_datasets}

For each dataset, record its accession, size, systems and perturbations, and which
paper it supports. Do not invent accessions; if a dataset cannot be found, say so.

{data_analysis_instructions}

## Output

Cite every factual claim with a PMID or DOI. Quote sentences only when they are
copied exactly from the source, and say whether a quote comes from the abstract or
the full text. Never invent an identifier or a quote.

End the report with these tables:

1. **Systems**: name, model type, biological material and species, cell source,
   readouts, perturbations, applications, validation, limitations, origin
   (developed or applied), references.
2. **Per-paper pairings**, one row for each pairing of a system with a mechanism in
   one paper: paper (PMID or DOI), system, mechanism (in the paper's own terms),
   relationship (RECAPITULATES, PARTIALLY_RECAPITULATES, FAILS_TO_RECAPITULATE,
   PERTURBS, MEASURES or RESCUES), fidelity (HIGH, MODERATE, LOW or UNKNOWN, with
   the reason), model_scale (MOLECULAR, CELLULAR, TISSUE or ORGANISM, the scale the
   system actually observes), readouts with direction (INCREASED, DECREASED,
   UNCHANGED, RESTORED, ABOLISHED or ALTERED), and a verbatim quote. A
   FAILS_TO_RECAPITULATE row is as valuable as a positive one.
3. **Mechanisms and phenotypes**: mechanism, systems, evidence, specificity,
   references.
4. **Candidate mechanistic chains**: chain (event → event), evidence for each link,
   matching AOP-Wiki IDs if any, and status (present in AOP-Wiki, partly present, or
   apparently new).
5. **Contexts of use**: domain, decision context, systems, references.
6. **Datasets**: accession, repository, systems, perturbations, paper, and whether
   you analysed it.

Finish with a short section on gaps: mechanisms, domains or validations the group's
methods have not yet covered.
