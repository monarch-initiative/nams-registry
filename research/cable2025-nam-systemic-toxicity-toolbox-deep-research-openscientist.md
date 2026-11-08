---
provider: openscientist
model: openscientist-autonomous
cached: false
start_time: '2026-11-07T15:14:22.201973'
end_time: '2026-11-07T15:35:52.469301'
duration_seconds: 1290.27
provider_config:
  timeout: 3600
  max_retries: 3
  parameters:
    allowed_domains: []
    max_iterations: 5
    use_hypotheses: false
    investigation_mode: autonomous
    poll_interval: 30
    timeout: 3600
    save_artifacts: true
    artifact_max_bytes: 5242880
reference_validation:
  total_references: 3
  verified: 3
  not_found: 0
  unverifiable: 0
  confabulation_rate: 0.0
  relevance_assessed: 3
  on_topic: 0
  validator_version: 0.5.1
artifact_count: 2
artifact_sources:
  openscientist_artifacts_zip: 2
artifacts:
- filename: final_report.html
  path: cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist_artifacts/final_report.html
  media_type: text/html
  source: openscientist_artifacts_zip
  data_storage_id: null
  description: OpenScientist final report
- filename: final_report.pdf
  path: cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist_artifacts/final_report.pdf
  media_type: application/pdf
  source: openscientist_artifacts_zip
  data_storage_id: null
  description: OpenScientist final report
---

## Question

Review this paper:

Cable S, Baltazar MT, Bunglawala F, et al. "Advancing systemic toxicity risk assessment: Evaluation of a NAM-based toolbox approach." Toxicological Sciences (2024). DOI: 10.1093/toxsci/kfae159 (https://doi.org/10.1093/toxsci/kfae159)

Base the review on this paper itself (its main text and supplementary material). Where you cite other sources, say so and keep them distinct from what this paper reports.

Tasks:
1. Extract specific methods and models used for systemic toxicity risk assessment.
2. Identify recommendations for how methods and models should be combined.
3. Extract associations between specific biological entities and processes measured, along with the methods associated with each biological entity or process.

## Output

# Review: "Advancing systemic toxicity risk assessment: Evaluation of a NAM-based toolbox approach"

**Paper reviewed:** Cable S, Baltazar MT, Bunglawala F, Carmichael P, Contreas L, Dent M, Houghton J, Kukic P, Malcomber S, Nicol B, Przybylak K, Punt A, Reynolds G, Reynolds J, Scott S, Tang D, Middleton A. *Toxicological Sciences* 204(1):79–95 (2024/2025). DOI: 10.1093/toxsci/kfae159 (PMID 39693112; PMC11879040). Open access.

**Scope of this review:** All content below is extracted from *this paper's* main text and its description of supplementary tables (notably Table S3b, Table 1, Table 4), unless explicitly flagged as an *external/cited source*. Where the paper attributes a method to earlier work (e.g. Middleton et al. 2022, Hatherell et al. 2020, Moxon et al. 2020, Reynolds et al. 2020), that is noted so the reader can distinguish what this paper newly did from what it reused.

---

## 1. Summary (answer to the research question)

The paper evaluates a "systemic-safety toolbox" — a New Approach Methodology (NAM) workflow for conducting **animal-free systemic toxicity risk assessment** of consumer-product chemicals. The toolbox pairs **two modules**: (i) an **exposure module** of physiologically based kinetic (PBK) models that predict internal exposure (plasma **Cmax**), and (ii) a **bioactivity module** of three complementary in vitro/in chemico platforms that give broad, largely mechanism-agnostic coverage of toxicity modes of action. Their outputs are integrated into a **bioactivity:exposure ratio (BER)** — an analogue of a margin of internal exposure — which is compared to PBK-level-specific thresholds to classify an exposure scenario as "low risk" or "uncertain risk." Across 38 new chemicals and 70 consumer exposure scenarios, the workflow was **protective of human health in >90%** of high-risk scenarios and was **more conservative than in vivo PoDs in 22/24** comparable cases. The authors recommend using the toolbox as **Tier 1 of a tiered, iterative NGRA framework**, combining specific and nonspecific assays and never in isolation.

---

## 2. Task 1 — Specific methods and models used

### 2.1 Exposure module (internal dose)
- **PBK modeling software:** **GastroPlus 9.8** (Simulations Plus, Lancaster, CA), simulating **oral, dermal, and IV** routes. Output metric = **maximum total plasma concentration (Cmax)**.
- **PBK input parameters:** logP (octanol–water partition), water solubility, fraction unbound in plasma (f_up), blood:plasma ratio (Rbp), hepatic intrinsic clearance (Cl_int), MDCK permeability (P_app), pKa, and intestinal absorption / skin penetration as applicable.
- **Tiered PBK parameterization** (framework from Moxon et al. 2020):
  - **L1 – in silico only:** parameters from **ADMET Predictor** (in silico).
  - **L2 – in silico + in vitro:** ≥1 parameter from in vitro measurement.
  - **L3 – in silico + in vitro + clinical:** model calibrated to human clinical data (from distinct scenarios; L3 Cmax is still a prediction, not a measurement).
- **Reverse dosimetry** used to convert in vitro PoDs to administered-equivalent doses for comparison against in vivo PoDs.
- **In silico acute-tox predictor (recommended for Tier 0 problem formulation):** **CATMoS / CatMOS** (Collaborative Acute Toxicity Modelling Suite; Mansouri et al. 2021 — *external cited tool*).

### 2.2 Bioactivity module (three platforms)
1. **In vitro Pharmacological Profiling (IPP)** — **63 targets** with known safety liabilities, tested in **binding, enzymatic, coactivator-recruitment, and luciferase** assays (full list: Table S3b). 44 targets linked to in vivo adverse drug reactions (Bowes et al. 2012); **19 added** for developmental-toxicity coverage. Two-stage PoD: (a) **screening** at a fixed 10 or 100 µM (2 replicates); (b) targets with >50% inhibition/stimulation followed up with **concentration–response** → **EC50 / IC50 / AC50**. (Three targets dropped as unavailable: mineralocorticoid receptor NR3C2, RARγ, and the AhR assay.)
2. **High-Throughput Transcriptomics (HTTr)** — **TempO-Seq** (BioSpyder lysis kit; BioClavis sequencing), **version 2 human whole-transcriptome panel**, in **HepG2, HepaRG, and MCF7** cells; 24 h, **7 concentrations**. Analysis with **BMDExpress2** (probe-level benchmark concentrations BMD/BMDL/BMDU, **benchmark response = 10%**; **Reactome** pathway enrichment → mean pathway BMDL) **and BIFROST** (Bayesian "global PoD" = minimum effect concentration across all genes).
3. **Cell Stress Panel (CSP)** — expanded panel (Hatherell et al. 2020; Middleton et al. 2022) in **HepG2**, 24 h, **8 concentrations**, 3 biological + 2 technical replicates. PoD = **CSP global PoD via BIFROST**. Measures stress biomarkers including **AhR activation, oxidative stress/GSH, and metabolism-related gene transcription**.
- **Concentration-range setting:** cytotoxicity via **cellular ATP** and **LDH release** in HepG2, HepaRG, MCF7; max dose = min(solubility limit, cytotoxic concentration).

### 2.3 Integration, decision, and performance
- **PoD estimation tools:** BMDExpress2 and BIFROST.
- **BER = (minimum PoD across platforms) / Cmax.** One BER per PBK level.
- **Decision thresholds** (Table 1; from a Bayesian model of PBK prediction error over 8 benchmark scenarios, Middleton 2022): **L1 = 110, L2 = 11, L3 = 2.5.** BER above threshold → "low risk"; below → "uncertain risk" (escalate).
- **Performance metrics:** **protectiveness** = H_U/(H_U+H_L) (high-risk scenarios correctly flagged as uncertain) and **utility** = L_L/(L_L+L_U) (low-risk scenarios correctly called low-risk).
- **Benchmarking:** NAM PoD vs. traditional in vivo PoD (typically subchronic 90-day repeat-dose studies, or human data), using reverse dosimetry.

---

## 3. Task 2 — Recommendations for how methods/models should be combined

1. **Take the minimum PoD across all bioactivity platforms** (IPP IC50/AC50; CSP BIFROST global PoD; HTTr per-cell-line minimum pathway BMDL and HTTr per-cell-line BIFROST global PoD) to form the most conservative overall PoD, then compute BER = minPoD/Cmax and apply the **PBK-level-specific threshold**.
2. **Minimal effective combination:** the full four-component toolbox gives the most conservative PoD (**96% protectiveness / 29% utility** at the highest available PBK level), but the **identical 96%/29% is achievable from IPP + HTTr-BIFROST global PoD** alone (Table 3). Protectiveness is dominated by the broad **HTTr BIFROST global PoD** — combinations lacking it drop to ~61–74% protectiveness (while gaining utility to 54–62%); the HTTr-BMD minimum-pathway PoD adds conservatism without ever lowering protectiveness.
3. **Combine specific (targeted) and nonspecific (broad) evidence.** Broad HTTr/CSP platforms make protective decisions agnostic of mode of action in most cases; targeted IPP assays cover specific molecular liabilities. The **warfarin** case shows the risk when a *specific* target (VKORC1) is absent: toolbox PoDs (13.6–259 µM) far exceeded Cmax (0.6–6 µM), misclassifying it as low risk, whereas a VKORC1 assay (literature IC50 24.7 nM–4 µM) would give BER ≪ 1 and flag uncertain risk.
4. **Embed in a tiered, iterative NGRA framework (Fig. 1), never in isolation.** Tier 0 problem formulation uses historical data + in silico tools (e.g., **CATMoS** acute-tox predictions) to judge whether the toolbox is appropriate; Tier 1 is the toolbox/BER; **"uncertain risk" escalates to Tier 2** higher-tier, case-by-case models. A disagreement between an in silico acute-tox alert and the NAM output should trigger a mode-of-action evaluation and bespoke assays.
5. **Stay within the defined context of use:** systemic toxicity only. Genotoxicity, carcinogenicity, developmental/reproductive toxicity, and sensitization are explicitly **out of scope** and must be addressed by other methods (e.g., trimellitic anhydride's respiratory-sensitization risk).
6. **Strengthen the exposure module:** redefine **L2 to require a minimal ADME set** — hepatic intrinsic clearance, fraction unbound, blood:plasma ratio, plus route-specific absorption (dermal/intestinal) — because early-tier decisions will increasingly rely on in vitro (L2) rather than clinical (L3) data. (Would require recalculating BER thresholds.)
7. **Improve utility by distinguishing adaptive bioactivity from adversity** — annotate biomarkers (e.g., GSH, metabolism genes may be non-adverse) and resolve gene-level vs pathway-level transcriptomic PoD debates. Low utility was often driven by HTTr BIFROST PoDs.

---

## 4. Task 3 — Biological entity/process ↔ method associations

| Biological entity / process | Method / platform (as reported) |
|---|---|
| 63 pharmacological safety targets (GPCRs, ion channels, enzymes, nuclear receptors, transporters; 44 ADR targets of Bowes 2012 + 19 developmental-tox targets) — full list in §4.2 below | **IPP** — binding, enzymatic, coactivator-recruitment, luciferase assays → EC50/IC50/AC50 |
| Carbonic anhydrase II (topiramate secondary target) | **IPP** (detected; drove BER < L2 threshold) |
| Genome-wide transcriptional response; **Reactome** pathway perturbation | **HTTr** — TempO-Seq v2 in HepG2/HepaRG/MCF7 → BMDExpress2 (pathway BMDL) + BIFROST (global PoD) |
| Aryl hydrocarbon receptor (AhR) activation | **Cell Stress Panel** (endpoint; replaced the discontinued IPP AhR assay) |
| Oxidative stress / glutathione (GSH); metabolism-related gene transcription | **Cell Stress Panel** (HepG2) |
| Cytotoxicity (ATP depletion, LDH release) — for range-finding | HepG2 / HepaRG / MCF7 cytotoxicity assays |
| Internal exposure / ADME (logP, solubility, f_up, Rbp, Cl_int, MDCK P_app, pKa, absorption) → plasma Cmax | **PBK model (GastroPlus)** + **ADMET Predictor** (in silico parameters) |
| Acute toxic potency (Tier 0 alert) | **CATMoS** in silico suite (*external cited tool*) |

### 4.1 Per-chemical mode-of-action detection (Table 4)

The paper's Table 4 maps each high-risk chemical's known MoA to whether the toolbox detected it:

**MoA detected → protective** (targets present in the IPP panel unless noted):
cetirizine → **histamine H1 receptor**; dexamethasone → **glucocorticoid receptor**; fenbuconazole & ketoconazole → **aromatase (steroid/ergosterol biosynthesis)**; ibuprofen, paracetamol & furosemide(secondary) → **COX-1/COX-2**; metoclopramide → **dopamine D2 receptor**; verapamil → **calcium channel**.

**MoA NOT detected but BER still protective** (nonspecific HTTr bioactivity rescued the decision):
azathioprine → purine-mimic DNA-synthesis inhibition (metabolism-limited); benzocaine → **methaemoglobin formation**; chlorpyrifos → **acetylcholinesterase** (metabolism-driven); cyclophosphamide → DNA damage (metabolism-driven); digoxin → **Na⁺/K⁺-ATPase**; glibenclamide → **K_ATP channel**; hydralazine → **Ca²⁺ flux**; metformin → gluconeogenesis (energy markers respond only at conc > exposure); topiramate → **GABA-receptor subunit**; furosemide(primary) → **Na-K-Cl transporter**.

**Not protective** (MoA missed *and* misclassified low-risk): trimellitic anhydride → serum-IgE/respiratory sensitization (out of scope); warfarin → **VKORC1**/anticoagulation.

### 4.2 Full IPP target panel (verbatim from supplementary Table S3b)

The 63 targets (tested as 76 assay wells; nuclear receptors run as agonist + antagonist pairs) group as:
- **Aminergic / neurotransmitter GPCRs:** 5-HT receptors HTR1A, HTR1B, HTR2A, HTR2B, HTR3A; adrenergic ADRA1A, ADRA2A, ADRB1, ADRB2; dopamine DRD1, DRD2; muscarinic CHRM1, CHRM2, CHRM3; nicotinic CHRNA4; histamine HRH1, HRH2; opioid OPRK1, OPRM1, OPRD1; adenosine ADORA2A; cannabinoid CNR1, CNR2; cholecystokinin CCKAR; endothelin EDNRA; vasopressin AVPR1A; angiotensin AGTR1.
- **Monoamine transporters:** SLC6A2 (NET), SLC6A3 (DAT), SLC6A4 (SERT).
- **Ion channels:** CACNA1C (L-type Ca²⁺, DHP site), KCNQ1, SCN5A (Naᵥ1.5, site 2), KCNH2/**hERG** ([³H]-dofetilide), GRIN1 (NMDA), GABRA1A (GABA-A α1 benzodiazepine site).
- **Enzymes:** ACHE, PDE3A, PDE4D, PTGS1 (COX-1), PTGS2 (COX-2), LCK, ACE2, CA2 (carbonic anhydrase II), MAOA.
- **Nuclear receptors (coactivator recruitment; agonist & antagonist):** AR, NR3C1 (GR), NR1I3 (CAR), PPARA, PPARD, PPARG, NR1I2 (PXR), PGR, VDR, ESR1, ESR2, RARA, RARG\*, RXRA, RXRB, THRA, THRB, NR3C2 (MR)\*.
- **Other:** Tubulin.
- *\*NR3C2 (MR) and RARG marked "assay unavailable by the end of the study" — matches the main-text note.*

This confirms why classic receptor pharmacology is detected (H1, GR, D2, COX-1/2, L-type Ca channel, aromatase via steroid pathway) whereas **Na⁺/K⁺-ATPase, K_ATP, Na-K-Cl cotransporter, and VKORC1 are genuinely absent** from the panel. Note the nuance: GABA-A α1 (GABRA1A) *is* in the panel, yet topiramate's subunit-specific effect was still not detected.

**Documented coverage gaps (entity NOT measured by any toolbox assay):**
- **VKORC1 / vitamin-K epoxide reductase** — warfarin's specific mechanism (toolbox not protective here).
- **GABA-receptor subunit** — topiramate's primary target (subunit absent from IPP).
- **Methaemoglobin formation** — benzocaine (no biomarker in any assay).
- **Ion-flux / ion-movement targets** — hydralazine, glibenclamide (relevant targets absent).
- **DNA-reactive metabolites** — cyclophosphamide, azathioprine (require metabolic competency; not in CSP biomarkers — but still highly active in HTTr, giving protective BERs).
- **Mineralocorticoid receptor NR3C2 and RARγ** — removed (assays no longer available).
- **Immune markers (serum IgE), respiratory sensitization** — trimellitic anhydride (out of systemic-toxicity scope).

---

## 4b. Quantitative performance and benchmarking (added Iteration 2)

**Benchmark set & coverage:** 38 chemicals, **70 scenarios (46 high-risk, 24 low-risk)**; routes = **49 oral, 13 dermal, 6 IV, 2 inhalation**; use classes = 21 medicinal, 9 cosmetic, 5 agricultural, 3 food, 1 occupational. 2 chemicals L1-only (1,2-octanediol, panthenol); 47 PBK models calibrated to clinical data (L3) but only 3 of these were low-risk.

**Protectiveness / utility by PBK level:**
- **L1** (threshold 110): 93% protectiveness, 8% utility
- **L2** (threshold 11; most likely future scenario): **43/46** high-risk flagged uncertain = **93% protectiveness**; 6/22 low-risk correct = **27% utility**
- **L3** (threshold 2.5): **98% protectiveness** (warfarin upper therapeutic dose reclassified)
- Only **trimellitic anhydride** and **warfarin** were high-risk scenarios misclassified as low-risk.

**NAM vs traditional in vivo (same early-tier logic):** In vivo PoDs (subchronic/chronic NOAEL/NOEL) available for only **25** chemicals. Minimum NAM PoD was more conservative (lower) than traditional in nearly all cases (exceptions **aspartame, fenbuconazole**, <5-fold). **Pearson r = 0.8** (plasma-concentration basis) and **0.57** after reverse-dosimetry to external dose. On the shared subset with an assumed **MoS > 100** threshold: traditional data → **97% protectiveness / 42% utility**; toolbox → **96% / 32%**. (No in vivo NOAEL existed for warfarin given rodent potency.) Note: this comparison does not apply the interspecies/assessment factors normally used with animal data.

**Chemical-space characterization methods:** unbiased two-step stratified sampling from ~2,500 structures (to avoid the pilot's selection bias); physicochemical range MW 100.12–780.9 g/mol, predicted S logP −2.32 to 5.99; **ToxPrint chemotypes via ChemoTyper** (Yang et al. 2015 — *external method*) — 572/729 chemotypes represented across sets (181 in the 38 test chemicals), top chemotypes `ring:aromatic_benzene` and `bond:C=O_carbonyl_generic`; **CPCat** cosmetics list used as a human-exposure reference set. On-target = on-toxicity examples: **digoxin** (Na⁺/K⁺-ATPase→cardiotoxicity), **warfarin** (VKORC1/coagulation), **ibuprofen** (COX-1/COX-2→gastric effects).

## 5. Supported vs refuted claims (as evaluated by the paper)

**Supported by the paper's data:**
- The NAM toolbox is protective in **>90%** of high-risk scenarios and comparable in conservatism to in vivo data (**NAM PoD more conservative in 22/24** comparisons).
- Protective decisions are generally possible **without identifying the mechanism of action** (9/10 undetected-MoA high-risk scenarios still protective).
- A **reduced platform set (IPP + HTTr-BIFROST)** matches full-toolbox protectiveness/utility.

**Limitations the paper itself raises (refuted "stand-alone sufficiency"):**
- **Low utility:** many low-risk scenarios flagged "uncertain risk" because the workflow does not yet distinguish adaptive from adverse bioactivity.
- **Specific-mechanism blind spots:** warfarin misclassified (missing VKORC1 assay); the toolbox is **not sufficient in isolation**.
- **Metabolic competency** limited (metabolite-driven toxicity under-detected in CSP).
- **L3 performance skewed** (few low-risk scenarios had clinical data); conclusions on human-kinetic impact on utility cannot be drawn.
- **Chemical space** not fully covered; more chemicals of shared MoA/structure needed to make class-level conclusions.

---

## 6. Provenance and limitations of this review
This review is built from the paper's **Europe PMC full text** (main text + the four embedded Tables 1–4) **and its actual supplementary workbook** (`toxsci-24-0360-File009.xlsx`, containing sheets S1 risk classification, S2a–c PBK parameters/clinical data/Cmax, S3a PoD summary, **S3b IPP screening %** — the source of the verbatim 63-target panel in §4.2, S3c IPP dose-response/PoD, S4 observations, S5 in-vivo PoD selection, S6 chemical details). Numerical thresholds, cell lines, concentrations, platform permutations, per-chemical MoA detection, and the BER/PoD logic are quoted directly from the paper and its supplement.

**What could NOT be sourced from this paper:** the individual **CSP biomarker roster** is not enumerated in this paper or its supplement — it resides in the cited methods papers (Hatherell et al. 2020; Middleton et al. 2022, *external sources*). This paper names only selected CSP endpoints in its main text (AhR activation, GSH/oxidative stress, metabolism-related gene transcription). External tools/sources referenced above (Bowes et al. 2012 ADR panel; ChemoTyper/ToxPrint, Yang 2015; CPCat; CATMoS, Mansouri 2021; Moxon et al. 2020 PBK tiering) are flagged as such and kept distinct from this paper's own reporting.

---

*Prepared as a methods/recommendation/entity-association extraction of Cable et al. (2024), Toxicological Sciences.*


## Artifacts

- [OpenScientist final report](cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist_artifacts/final_report.html)
- [OpenScientist final report](cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist_artifacts/final_report.pdf)

## Reference Validation

Checked with `linkml-reference-validator` 0.5.1.

| Outcome | Count |
| --- | --- |
| References checked | 3 |
| Resolved | 3 |
| Unresolved (possible confabulation) | 0 |
| Unverifiable | 0 |
| References weighed for topical relevance | 3 |
| On topic | 0 |
| Off topic | 0 |

All extracted references resolved successfully.