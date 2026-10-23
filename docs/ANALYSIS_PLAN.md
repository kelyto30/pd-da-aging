# Analysis plan for Aim 2, step 3 onward

Status: version 2, revised 2026-10-23 before any aging or senescence scores were computed (see change log). Any later change is recorded in the change log at the bottom, never made silently.

## Data
16,755 DA neurons (clusters 14–18 of step 2) from 18 donors in GSE178265: 8 control, 6 PD, 4 LBD. Raw counts; per-cell donor, status, sex, age, PMI and FACS sort status.

## Definitions fixed before scoring
1. **DA subtypes.** Subtypes follow Kamath et al. 2022, using the marker genes reported in that paper (taken from its supplementary tables, not typed from memory). Assignment works in three steps:
   1. Re-cluster the DA neurons only: normalise, select highly variable genes, run Harmony by library, then Leiden clustering.
   2. Score each sub-cluster for each Kamath subtype's markers and name it after the subtype with the highest mean marker score.
   3. Check that the SOX6_AGTR1 sub-clusters fall mainly within step 2 cluster 14 and the CALB1 sub-clusters mainly within cluster 18. Report this cross-tabulation.

   The two groups compared are:
   - **Vulnerable:** SOX6_AGTR1.
   - **Resilient:** CALB1-positive subtypes, pooled.

   Other SOX6 subtypes are analysed separately.
2. **Gene sets.** Taken from their original sources and saved with the code, with the download date:
   - **Primary:** SenMayo (Saul et al. 2022).
   - **Secondary:** CDKN1A (p21) and CDKN2A (p16), as single genes (core senescence cell-cycle inhibitors); CellAge senescence genes; a published human brain-aging gene set.
   - **Not used as a readout:** TP53 target gene sets. Kamath et al. already reported them highest in SOX6_AGTR1 neurons, so they would not test a new hypothesis.
   - **Marker removal:** before scoring, genes that are themselves subtype markers are removed from each set, so a score cannot simply re-detect the subtype.
3. **Score.** Per-nucleus gene-set score on log-normalised counts (scanpy `score_genes`, which subtracts expression of matched control genes). AUCell is a sensitivity check. Single genes (CDKN1A, CDKN2A) are analysed as log-normalised expression and, at the donor level, as pseudobulk counts.
4. **Inclusion.** A donor contributes to a subtype comparison only if it has at least 20 neurons of each subtype being compared. If fewer than 5 control donors meet this, the threshold for H1 becomes 10 neurons. This rule is fixed now, before scoring. The number of donors kept is reported for every test.

## Hypotheses and tests
- **H1 (primary).** In control donors, SOX6_AGTR1 neurons have a higher SenMayo score than resilient neurons.
  - **Unit of analysis:** donor. For each donor, take the mean score per subtype and compute the difference (vulnerable minus resilient).
  - **Primary test:** two-sided paired t-test on the per-donor differences (equivalently, a one-sample t-test of the differences against zero). Report the mean difference, its 95% confidence interval, and Cohen's d for paired data.
  - **Significance level:** 0.05.
  - **Supporting analyses:**
    - Paired Wilcoxon signed-rank test. Note that with 5 donors the smallest possible two-sided p is 0.0625, so it is supportive only.
    - Nucleus-level linear mixed model with a donor-specific subtype effect, `score ~ subtype + (1 + subtype | donor)`. If the random slope does not converge, fit `(1 | donor)` and say so.
- **H2 (secondary).** The vulnerable-minus-resilient difference is larger in PD/LBD than in controls.
  - Model on donor-by-subtype means: `score ~ subtype * status + (1 | donor)`, with sex and age as covariates if the model converges.
- **H3 (exploratory).** Among controls, the vulnerable-minus-resilient difference increases with donor age.
  - Spearman correlation. With 8 or fewer control donors this is exploratory and reported as such.
- **Secondary readouts.** H1 and H2 are repeated for CDKN1A, CDKN2A, CellAge and the brain-aging set.
- **Multiple testing.** Benjamini–Hochberg correction across all secondary readouts and tests. H1 (SenMayo, paired t-test) is a single pre-specified test.

## Sensitivity analyses (reported whatever the result)
- PD only (LBD excluded).
- Only FACS-positive (DA-enriched) libraries.
- Minimum neurons per donor of 10 and 50.
- AUCell instead of `score_genes`.
- Leave-one-donor-out for H1.
- **Depth adjustment:** H1 repeated after regressing each nucleus's score on its log total counts and number of detected genes, so differences in cell size or sequencing depth between subtypes cannot explain the result.

## Replication
The same H1 test is repeated in GSE157783 (Smajić et al. 2022), and in GSE184950 if feasible. Exact replication is not expected, since these studies sampled fewer DA neurons. The direction of the effect is the main replication criterion.

## Negative-result policy
A null H1 is reported as a finding. Gene sets, thresholds and tests are not changed after seeing results unless the change is logged below with a reason.

## Change log
| Date | Change | Reason |
| --- | --- | --- |
| 2026-10-23 | Version 2, made **before any scores were computed**. (1) H1 primary test changed from paired Wilcoxon to paired t-test with effect size and 95% CI; Wilcoxon and a random-slope mixed model kept as supporting; fallback threshold of 10 neurons if fewer than 5 controls qualify. (2) Subtype assignment method specified (re-cluster DA neurons, label by Kamath markers, cross-check against step 2 clusters 14 and 18). (3) CDKN1A and CDKN2A added as secondary readouts; TP53 target sets explicitly excluded as a readout. (4) Depth adjustment added as a sensitivity analysis. | Review found that with 5 qualifying control donors the Wilcoxon test cannot reach p < 0.05; the subtype method was unspecified; SenMayo is weighted toward secreted factors that neurons express weakly; and subtypes may differ in sequencing depth. |
