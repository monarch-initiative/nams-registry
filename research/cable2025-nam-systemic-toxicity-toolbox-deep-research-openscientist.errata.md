# Errata: `cable2025-nam-systemic-toxicity-toolbox-deep-research-openscientist.md`

Errors found by checking the report against the paper's full text and supplementary
material (Europe PMC `PMC11879040`, DOI [10.1093/toxsci/kfae159](https://doi.org/10.1093/toxsci/kfae159)).
No claim in the report has been altered, as `README.md` requires.

## Rename

The report was produced under the stem `kfae159-deep-research-openscientist`, after the
article id in the paper's DOI. It was renamed to be legible, which meant renaming its
`_artifacts/` directory and updating the four paths naming that directory inside the
report — two in its frontmatter `artifacts` block, two in its closing artifact links.

That is the only edit the file has received, and nothing else in it differs by a byte:

```
sha256 as produced  a0c25cc2aea0a4f30b92f2a618dbaeb2e32f5b550cb9b65f7ee7bc9dbc347441
sha256 as committed ec2a1925d412b94ae9b94396b0c19b3455988cd670c04111a678427da1ea8745
```

To check that claim, rewrite each file's artifact-directory prefix to a common string
and compare; the two are then identical.

## The "22/24" conservatism ratio does not appear in the paper

The report states, in its summary and again in its findings list, that the NAM point of
departure was more conservative than the in vivo point of departure in **22/24**
comparisons. No such ratio is in the paper, and neither number is right.

What the paper says:

> Like other studies that have compared NAM PoDs with traditional PoDs, we found that
> for nearly all chemicals the minimum NAM PoD was more conservative, i.e. lower, than
> the minimum traditional PoD. Exceptions to this were for aspartame and for
> fenbuconazole, where the difference between the traditional PoD and the NAM PoD was
> under 5-fold.

The comparison set is 25 chemicals, not 24 — "a set out earlier could only be found for
25 of the test chemicals (see Table S5)" — and the paper names exactly two exceptions.
So the figure implied is **23/25**, and the paper deliberately expresses it as "nearly
all" rather than as a ratio.

Do not reuse 22/24. If a record needs this result, quote the sentence above.

## The IPP panel holds 64 distinct targets, not 63

The report's §4.2 heads its panel "The 63 targets (tested as 76 assay wells…)", taking
the figure from the paper's own main text, which builds it as 44 targets from Bowes
et al. 2012 plus 19 added for developmental toxicity.

Sheet `S3b. IPP screening %` of the supplementary workbook carries **76 assay wells
across 64 distinct target symbols**, screened against 38 test chemicals. The well
count is right; the target count is one short. Twelve nuclear receptors are run as
agonist and antagonist pairs, which is what separates 76 from 64.

The report's own §4.2 list is internally inconsistent in the same way: enumerated, its
six groups contain 64 symbols under a heading that says 63.

This is a discrepancy between the paper and its own supplement, not a reading error in
the report, so it cannot be resolved from the files here. Tubulin is the one panel
member that fits neither of the paper's two stated provenances, which makes 44 + 19 +
tubulin = 64 the likeliest reconciliation, but the paper does not say so and this
should not be written into a record as though it did.

If a record needs the panel size, say 76 assay wells over 64 targets and cite the
workbook sheet, or quote the paper's "63" and attribute it to the main text. Do not
present them as the same claim.

The counts above come from reading the sheet with a short `openpyxl` script, held
outside this repository along with its output. It parses each assay name on the
vendor's `<target name>, <SYMBOL> (<species>) (<mode>)` convention rather than
pattern-matching for symbols, and ignores the two rows beginning `*` that are the
sheet's own footnotes. Anyone re-deriving these numbers needs the workbook
(`toxsci-24-0360-File009.xlsx`, from the publisher) and those two rules.

## Checked and found correct

- **"The same protectiveness and utility are reached by IPP + HTTr BIFROST Global
  alone"** is the paper's own statement in its discussion, and Table 3 carries a
  two-platform row with the same 96% protectiveness / 29% utility as the full toolbox.
- **The panel's two unavailable assays** are NR3C2 and RARG, both marked `**` in the
  sheet, matching the main text. The third dropped assay the main text names, AhR, is
  absent from the sheet entirely rather than marked.
