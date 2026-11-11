---
reference_id: DOI:10.3389/ftox.2023.1275980
extractor_version: 1
title: "The ToxCast pipeline: updates to curve-fitting approaches and database structure"
authors:
- M. Feshuk
- L. Kolaczkowski
- K. Dunham
- S. E. Davidson-Fritz
- K. E. Carstens
- J. Brown
- R. S. Judson
- K. Paul Friedman
journal: Frontiers in Toxicology
year: '2023'
doi: 10.3389/ftox.2023.1275980
content_type: abstract_only
is_preprint: false
---

# The ToxCast pipeline: updates to curve-fitting approaches and database structure
**Authors:** M. Feshuk, L. Kolaczkowski, K. Dunham, S. E. Davidson-Fritz, K. E. Carstens, J. Brown, R. S. Judson, K. Paul Friedman
**Journal:** Frontiers in Toxicology (2023)
**DOI:** [10.3389/ftox.2023.1275980](https://doi.org/10.3389/ftox.2023.1275980)

## Content

Introduction: The US Environmental Protection Agency Toxicity Forecaster (ToxCast) program makes in vitro medium- and high-throughput screening assay data publicly available for prioritization and hazard characterization of thousands of chemicals. The assays employ a variety of technologies to evaluate the effects of chemical exposure on diverse biological targets, from distinct proteins to more complex cellular processes like mitochondrial toxicity, nuclear receptor signaling, immune responses, and developmental toxicity. The ToxCast data pipeline (tcpl) is an open-source R package that stores, manages, curve-fits, and visualizes ToxCast data and populates the linked MySQL Database, invitrodb.

Methods: Herein we describe major updates to tcpl and invitrodb to accommodate a new curve-fitting approach. The original tcpl curve-fitting models (constant, Hill, and gain-loss models) have been expanded to include Polynomial 1 (Linear), Polynomial 2 (Quadratic), Power, Exponential 2, Exponential 3, Exponential 4, and Exponential 5 based on BMDExpress and encoded by the R package dependency, tcplfit2. Inclusion of these models impacted invitrodb (beta version v4.0) and tcpl v3 in several ways: (1) long-format storage of generic modeling parameters to permit additional curve-fitting models; (2) updated logic for winning model selection; (3) continuous hit calling logic; and (4) removal of redundant endpoints as a result of bidirectional fitting.

Results and discussion: Overall, the hit call and potency estimates were largely consistent between invitrodb v3.5 and 4.0. Tcpl and invitrodb provide a standard for consistent and reproducible curve-fitting and data management for diverse, targeted in vitro assay data with readily available documentation, thus enabling sharing and use of these data in myriad toxicology applications. The software and database updates described herein promote comparability across multiple tiers of data within the US Environmental Protection Agency CompTox Blueprint.