# Publication years in the Complement-ARIE Landscape Analysis

Written 2026-11-13 for the registry entries
[`complement-arie-landscape-analysis`](https://github.com/monarch-initiative/nams-registry/blob/main/resources/complement-arie-landscape-analysis.yaml)
([#36](https://github.com/monarch-initiative/nams-registry/issues/36)) and
[`complement-arie-landscape-dashboard`](https://github.com/monarch-initiative/nams-registry/blob/main/resources/complement-arie-landscape-dashboard.yaml)
([#37](https://github.com/monarch-initiative/nams-registry/issues/37)).
It asks when the papers in the Landscape Analysis were published, so that a
review of them can be planned.

Sources:

- The NIH Common Fund
  [Complement-ARIE Landscape Analysis](https://commonfund.nih.gov/sites/commonfund/files/Complement-ARIE-Landscape-Analysis-29-Feb-2024-508.pdf)
  report, dated 29 February 2024. Its methods are on pages A-6 to A-12.
- The "Q&A-Question Details" download from the report's
  [Tableau Public dashboard](https://public.tableau.com/app/profile/complement.arie/viz/Complement-ARIELandscapeAnalysis_17029296896540/ExploreQuestions),
  parsed with dismech's `just complement-arie-parse`. The download and the
  parser are described in dismech's
  [landscape analysis report](https://github.com/monarch-initiative/dismech/blob/main/docs/reports/complement-arie-landscape-analysis-2026-10-30.md).
- PubMed, for checking years and publication types.

## Summary

- **The corpus is a recent snapshot, not a history of NAMs.** Of the 2,737
  papers with answers, 2,447 (89%) were published in 2023 and 10 in 2024. Only
  3 were published before 2018.
- **That is how the corpus was searched.** The Landscape Analysis searched
  reviews from 2018 onwards, and all papers only from 2023 onwards. A wider
  search was judged too large for the project.
- **Almost every paper from 2018–2022 is a review.** 267 of the 276 with a
  PMID are indexed as reviews in PubMed. Papers from 2023–2024 are mostly
  primary research.
- **The years in the download are correct.** All 40 papers in a random check
  had the same year in PubMed.
- **Publication year will not divide the review into useful parts.** Splitting
  by question, or by the kind of paper, will.

## Publication years for each question

The download gives a year for each paper but no month or day, so the ranges
below are in years. Counts are papers with an answer to the question, out of
the 2,737 papers with answers. The years come from the paper's citation key
(for example "Smith et al. 2023").

| Question | Papers answered | Years | Before 2020 | 2020–2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Method Details Described | 2,682 | 2004–2024 | 90 | 182 | 2,400 | 10 |
| Method Technical Challenges Described | 2,477 | 2004–2024 | 85 | 161 | 2,222 | 9 |
| Method: New Technology or Refinement of Existing Approach | 2,416 | 2004–2024 | 79 | 159 | 2,169 | 9 |
| Tissue Types Examined | 2,152 | 2004–2024 | 66 | 145 | 1,934 | 7 |
| Remaining Challenges after Method Development | 2,130 | 2004–2024 | 78 | 162 | 1,882 | 8 |
| Cell Types Examined | 1,961 | 2004–2024 | 59 | 135 | 1,761 | 6 |
| Human Physiology Elements Considered | 1,847 | 2004–2024 | 53 | 132 | 1,657 | 5 |
| Disease(s) Examined | 1,572 | 2017–2024 | 49 | 126 | 1,392 | 5 |
| Method Limitations | 1,498 | 2004–2024 | 51 | 121 | 1,321 | 5 |
| Cellular Endpoints Measured | 1,472 | 2004–2024 | 45 | 88 | 1,333 | 6 |
| Method Validation Methods Described | 1,391 | 2004–2024 | 29 | 54 | 1,302 | 6 |
| Research Funding Details | 1,303 | 2018–2024 | 24 | 85 | 1,190 | 4 |
| Population Modeled | 553 | 2018–2024 | 12 | 59 | 480 | 2 |
| Model Metabolic Capacity Addressed | 373 | 2018–2023 | 15 | 30 | 328 | 0 |
| Economic Considerations Discussed | 174 | 2018–2024 | 4 | 16 | 151 | 3 |
| Ethical Considerations Discussed | 119 | 2018–2023 | 3 | 8 | 108 | 0 |
| Method Regulatory Use Discussed | 96 | 2018–2023 | 4 | 9 | 83 | 0 |
| Population Diversity and Variability Incorporated | 48 | 2018–2023 | 3 | 9 | 36 | 0 |
| Workforce Considerations Discussed | 11 | 2020–2023 | 0 | 3 | 8 | 0 |

The ranges look wider than the corpus is. Most begin in 2004 because of two
papers, and only three papers are older than 2018:

| Paper | PMID | Year | What it is |
|---|---|---|---|
| Auld et al., *Receptor Binding Assays for HTS and Drug Discovery* | [22553864](https://pubmed.ncbi.nlm.nih.gov/22553864/) | 2004 | A chapter of the NCBI *Assay Guidance Manual* |
| Riss et al., *Apoptosis Marker Assays for HTS* | [34339159](https://pubmed.ncbi.nlm.nih.gov/34339159/) | 2004 | A chapter of the NCBI *Assay Guidance Manual* |
| Du et al., *Progress in Mathematical Modeling of Gastrointestinal Slow Wave Abnormalities* | [29379448](https://pubmed.ncbi.nlm.nih.gov/29379448/) | 2017 | A review |

Across all 2,737 papers, the years are 2004 (2), 2017 (1), 2018 (42), 2019
(48), 2020 (55), 2021 (61), 2022 (71), 2023 (2,447) and 2024 (10).

## Why the corpus is mostly from 2023

The Landscape Analysis ran two literature searches, and each had a date limit.

**The initial search** looked for reviews in PubMed, run on 10 October 2023
and returning 31,237 hits (page A-6):

> We also limited the scope of the years (2018 to Present) and to reviews (as
> indexed by PubMed) only.

**The broad search** added Web of Science and Scopus and included all kinds of
paper, run on 23 October 2023 and returning 67,718 hits after duplicates were
removed (pages A-9 and A-10):

> did not limit to reviews only, but we looked at only the most recently
> published papers (2023 – 2024 references published early).

The report gives the reason for the cutoff:

> Expanding to 2018 – Present would have resulted in about 450k references,
> which was deemed beyond the project's scope given the focus on obtaining the
> most current perspective of NAMs in the scientific literature.

The years in the download match these two windows:

- **2018–2022 (277 papers):** found by the initial search, which took reviews
  only. 267 of the 276 with a PMID are indexed as reviews in PubMed.
- **2023–2024 (2,457 papers):** found mostly by the broad search. 768 of the
  2,148 with a PMID are indexed as reviews, so most are primary research. The
  2024 papers were published online early, before the search ran.
- **2004 and 2017 (3 papers):** outside both windows. The report also added
  261 "seed studies" chosen by the project team (page A-11), and these three
  papers may be among them. That has not been checked.

Both searches ran in October 2023, so nothing published after that is
included.

## Checking the years

The year in each citation key was compared with PubMed for 40 papers chosen at
random: 25 from 2023 and 15 from other years. All 40 matched PubMed's
publication date or electronic publication date.

## What this means for reviewing the papers

- **Read the corpus as NAMs literature from 2023, plus five years of reviews.**
  It cannot show how NAMs developed over time, and it holds no papers
  published after October 2023.
- **Papers from before 2023 are almost all reviews.** A review can point to
  several methods at once, while a 2023 paper usually describes one method.
  The two may be worth reviewing in different ways.
- **Divide the review by question, not by year.** Year splits the corpus into
  2023 and a small remainder. The questions split it more usefully. For
  example, "Disease(s) Examined" (1,572 papers) is the closest to the
  experimental models DisMech records.
- **Methods developed after October 2023 need another source.** For NAMs
  published since then, the registry's other resources will be needed.

## How the counts were made

1. Download "Q&A-Question Details" from the dashboard's "Explore Questions"
   view, as described in dismech's
   [`data/complement-arie/MANIFEST.yaml`](https://github.com/monarch-initiative/dismech/blob/main/data/complement-arie/MANIFEST.yaml).
2. Run dismech's parser, which writes `papers.tsv` and `answers.jsonl`.
3. For each question, take the answers that are not `NA`, look up each
   paper's `year` in `papers.tsv`, and count. Papers that group several
   papers under one key (`merged_key=1`) and papers with no answers
   (`no_content=1`) are left out, as in dismech's report.
4. For review status, look up each PMID's publication types with PubMed's
   E-utilities `esummary` and count those that include "Review".
