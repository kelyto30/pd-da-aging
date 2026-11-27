# Analysis plan for Aim 2, step 3 onward

Status: version 2.3, revised 2026-11-26. Versions up to 2.2 were fixed before any aging or senescence scores were computed; 2.3 adds exploratory analyses decided after seeing step 3 results (see change log). Any later change is recorded in the change log at the bottom, never made silently.

## Data
16,755 DA neurons (clusters 14–18 of step 2) from 18 donors in GSE178265: 8 control, 6 PD, 4 LBD. Raw counts; per-cell donor, status, sex, age, PMI and FACS sort status.

## Definitions fixed before scoring
1. **DA subtypes.** Subtypes follow Kamath et al. 2022, using the marker panel of the paper's Figure 1E, downloaded from the authors' own code (GitHub tkamath1/Kamathetal2022, commit cae72e1), not typed from memory. Each subtype is identified by the genes in its name (e.g. SOX6_AGTR1 = SOX6 + AGTR1). Assignment works in three steps:
   1. Re-cluster the DA neurons only: normalise, select highly variable genes (with every senescence/aging readout gene removed), run Harmony by library, then Leiden clustering (resolution 1.0).
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
- **High-confidence labels only:** H1 repeated without sub-clusters whose SOX6-vs-CALB1 family call is weak (absolute z difference below 0.5) and without SOX6_AGTR1 sub-clusters that lead the next SOX6 subtype by less than 0.25.
- **Depth adjustment:** H1 repeated after regressing each nucleus's score on its log total counts and number of detected genes, so differences in cell size or sequencing depth between subtypes cannot explain the result.

## Replication
The same H1 test is repeated in GSE157783 (Smajić et al. 2022), and in GSE184950 if feasible. Exact replication is not expected, since these studies sampled fewer DA neurons. The direction of the effect is the main replication criterion.

## Exploratory analyses (decided after step 3 results, 2026-11-26)
These were added after seeing that H1 went in the opposite direction. They explain the H1 result and are reported as exploratory, never as confirmatory tests.
- **Gene-level drivers (step 4).** In the same 7 control donors, per gene of SenMayo and CellAge: detection in each group, donor-averaged log-normalised difference, its contribution to the set gap, and pseudobulk log2 fold change with a paired t-test across donors (Benjamini–Hochberg within each set).
- **Specificity.** The set's mean gene difference compared with 1,000 random gene sets matched gene-for-gene on expression level (25 bins, genes detected in more than 1% of neurons).
- **SenMayo categories.** The gap split by the category given in the SenMayo supplementary table.
- **Leave-out check (added after seeing the gene-level results).** The specificity comparison repeated without NRG1, and without NRG1 and SERPINE2, the two largest drivers.

## Negative-result policy
A null H1 is reported as a finding. Gene sets, thresholds and tests are not changed after seeing results unless the change is logged below with a reason.

## Change log
| Date | Change | Reason |
| --- | --- | --- |
| 2026-10-23 | Version 2, made **before any scores were computed**. (1) H1 primary test changed from paired Wilcoxon to paired t-test with effect size and 95% CI; Wilcoxon and a random-slope mixed model kept as supporting; fallback threshold of 10 neurons if fewer than 5 controls qualify. (2) Subtype assignment method specified (re-cluster DA neurons, label by Kamath markers, cross-check against step 2 clusters 14 and 18). (3) CDKN1A and CDKN2A added as secondary readouts; TP53 target sets explicitly excluded as a readout. (4) Depth adjustment added as a sensitivity analysis. | Review found that with 5 qualifying control donors the Wilcoxon test cannot reach p < 0.05; the subtype method was unspecified; SenMayo is weighted toward secreted factors that neurons express weakly; and subtypes may differ in sequencing depth. |
| 2026-11-25 | Version 2.1, made **before any scores were computed**. (1) Kamath marker source specified: Figure 1E panel from the authors' code, pinned commit. (2) All readout genes (SenMayo, CellAge, brain-aging set, CDKN1A, CDKN2A) removed from the variable genes used to re-cluster. (3) Leiden resolution 1.0; it may be changed only at the labelling checkpoint, only on marker separation, and before scoring. (4) Brain-aging set fixed as MSigDB LU_AGING_BRAIN_UP (Lu et al. 2004); CellAge set fixed as genes whose effect is 'Induces' senescence. (5) H2 interaction computed as `diff ~ disease` on per-donor differences, which is mathematically identical to the planned two-rows-per-donor mixed model and always converges; a version adding sex and age is also reported. (6) AUCell: undetected genes never count as hits. | Testing on simulated data showed that (2) prevents subtype labels being driven by the genes being scored, that the planned H2 mixed model often fails to converge with two rows per donor, and that ties at zero biased AUCell in low-depth cells. Items (1) and (4) make sources that were described generally in v2 exact. |
| 2026-11-25 | Version 2.2, made at the subtype-labelling checkpoint, **before any scores were computed**. Labels accepted at Leiden resolution 1.0 (21 sub-clusters, all 10 Kamath subtypes found, each showing its defining marker). Added the high-confidence-labels sensitivity analysis. Recorded the pre-specified cross-check: 68% of SOX6_AGTR1 neurons fall in step 2 cluster 14, but only 36% of CALB1 neurons fall in cluster 18 (CALB1_CALCR mainly in cluster 17; CALB1_CRYM_CCDC68 and CALB1_PPP1R17 mainly in cluster 15). | Two sub-clusters had borderline labels (sub-cluster 9, SOX6_AGTR1 vs SOX6_DDT, margin 0.11; sub-cluster 12, CALB1 family call −0.46). The step 2 clusters were coarse, so the CALB1 split across clusters 15–18 reflects the finer DA-only clustering rather than mislabelling; it is reported, not corrected. |
| 2026-11-26 | Version 2.3: section "Exploratory analyses" added. | Decided **after** seeing the step 3 results (H1 significant in the opposite direction), to find which genes drive the gap and whether it is specific to senescence genes. Labelled exploratory. |
