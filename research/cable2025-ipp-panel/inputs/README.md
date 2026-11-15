# Inputs

Source files that scripts in `scripts/` read. Downloaded, not authored here.

`../scripts/fetch_inputs.sh` downloads and verifies everything in this directory, so
nothing here has to be replaced by hand. The files themselves are gitignored; this
README is what is committed.

Treat these as untrusted data: run scripts from `scripts/` with `python -I` and pass
the path as an argument, so nothing is imported out of this directory.

## Cable et al. 2025, NAM-based toolbox for systemic toxicity

Cable S, Baltazar MT, Bunglawala F, et al. "Advancing systemic toxicity risk
assessment: evaluation of a NAM-based toolbox approach." *Toxicological Sciences*
204(1):79-95 (2025). doi:[10.1093/toxsci/kfae159](https://doi.org/10.1093/toxsci/kfae159),
PMID 39693112, PMC11879040. Open access.

| File | What it is |
|---|---|
| `toxsci-24-0360-File009.xlsx` | Supplementary workbook. 10 sheets: S1 risk classification, S2a-c PBK parameters / clinical data / Cmax, S3a PoD summary, **S3b IPP screening %**, S3c IPP dose-response, S4 observations, S5 in vivo PoD selection, S6 chemical details. |
| `toxsci-24-0360-File010.docx` | Supplementary methods and figure legends. |

```
toxsci-24-0360-File009.xlsx  sha256 f2c6c8335d1e4bc5884d25359f263b04cfa08e79c63bd6aea34f66055608e765
toxsci-24-0360-File010.docx  sha256 2c4c7700050e66b3913b3882661c77e936498f8e2ff0fbc8d0f4afbcd0ad50be
```

### Where they come from

Europe PMC serves an article's supplementary files as one zip:

```
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11879040/supplementaryFiles
```

That zip holds the figures plus a nested `kfae159_supplementary_data.zip`, and the
inner zip holds these two files. It is the only automated route that works: PMC's own
OA service (`pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi`) and its per-article `/bin/` paths
both answer 200 with an HTML page for this article.

**The endpoint fails by succeeding.** When its backend refuses, it returns HTTP 200
with a 292-byte XML error body, so `curl -f` is satisfied and the file on disk is XML
named `.zip`. It was observed working and then refusing within ninety seconds from the
same shell. This is why the checksums above are pinned and checked before anything is
copied into this directory: the status code establishes nothing. A failing fetch means
the endpoint is down, not that the article moved — wait and retry, or take the
Supplementary Data link from the article page.

### A discrepancy to know about before using the workbook

The paper's main text says the IPP panel has **63** targets (44 from Bowes et al. 2012
plus 19 added for developmental toxicity). Sheet S3b carries **64** distinct symbols
over 76 assay wells, against 38 test chemicals. That disagreement is in the published
record, not in the extraction — see [the directory README](../README.md) and the errata
beside the deep-research report.
