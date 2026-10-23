# Analysis plan for Aim 2, step 3 onward

Status: DRAFT for author and advisor review. Written 2026-10-23, before any aging or senescence scores were computed. Once approved, changes are recorded in the change log at the bottom, never made silently.

## Data
16,755 DA neurons (clusters 14–18 of step 2) from 18 donors in GSE178265: 8 control, 6 PD, 4 LBD. Raw counts; per-cell donor, status, sex, age, PMI and FACS sort status.

## Definitions fixed before scoring
1. **DA subtypes.** Neurons are assigned to the DA subtypes of Kamath et al. 2022 using the marker genes reported in that paper (taken from its supplementary tables, not typed from memory). The two groups compared are:
   - **Vulnerable:** SOX6_AGTR1.
   - **Resilient:** CALB1-positive subtypes, pooled.
   Other SOX6 subtypes are analysed separately.
2. **Gene sets.** Taken from their original sources and saved with the code, with the download date:
   - Primary: SenMayo (Saul et al. 2022).
   - Secondary: CellAge senescence genes; a published human brain-aging gene set.
   - Before scoring, genes that are themselves subtype markers are removed from each set, so the scores cannot simply re-detect the subtype.
3. **Score.** Per-nucleus gene-set score on log-normalised counts (scanpy `score_genes`, which subtracts expression of matched control genes). AUCell is a sensitivity check.
4. **Inclusion.** A donor contributes to a subtype comparison only if it has at least 20 neurons of each subtype being compared. The number of donors kept is reported for every test.

## Hypotheses and tests
- **H1 (primary).** In control donors, SOX6_AGTR1 neurons have a higher SenMayo score than resilient neurons.
  - Unit of analysis: donor. For each donor, take the mean score per subtype.
  - Test: paired Wilcoxon signed-rank across control donors (two-sided).
  - Reported alongside: a linear mixed model at the nucleus level, `score ~ subtype + (1 | donor)`.
  - Significance level 0.05.
- **H2 (secondary).** The vulnerable-minus-resilient difference is larger in PD/LBD than in controls.
  - Mixed model on donor-by-subtype means, `score ~ subtype * status + (1 | donor)`, with sex and age as covariates if the model converges.
- **H3 (exploratory).** Among controls, the vulnerable-minus-resilient difference increases with donor age.
  - Spearman correlation. With only 8 control donors this is exploratory and reported as such.
- **Multiple testing.** Benjamini–Hochberg correction across all secondary gene sets and tests. H1 is a single pre-specified test.

## Sensitivity analyses (reported whatever the result)
- PD only (LBD excluded).
- Only FACS-positive (DA-enriched) libraries.
- Minimum neurons per donor of 10 and 50.
- AUCell instead of `score_genes`.
- Leave-one-donor-out for H1.

## Replication
The same H1 test is repeated in GSE157783 (Smajić et al. 2022), and in GSE184950 if feasible. Exact replication is not expected, since these studies sampled fewer DA neurons. The direction of the effect is the main replication criterion.

## Negative-result policy
A null H1 is reported as a finding. Gene sets, thresholds and tests are not changed after seeing results unless the change is logged below with a reason.

## Change log
| Date | Change | Reason |
| --- | --- | --- |
| | | |
