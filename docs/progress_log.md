# PD dopaminergic vulnerability thesis — project status and handoff

Last updated: 25 November 2026 (Aim 2 step 3 done; next is GitHub upload, then replication)

**Start every new chat here.** Key documents:
- Thesis pipeline (plan, dataset tables, progress log): https://claude.ai/code/artifact/733fc522-8c3e-4d60-a735-159177b7e83d
- Research proposal (formal, for committee): https://claude.ai/artifact/F4cRzWdRXKBC6HDHVodQUK
- My Research Companion (plain-language step-by-step record for presenting): https://claude.ai/artifact/3ZJSg4PzaaSFGayXUv8Qk7
- GitHub (private): https://github.com/kelyto30/pd-da-aging

**Standing request from the user:** after each analysis step, update (1) the Research Companion (new section in the what/why/how/results/meaning pattern, plus its update log and committee Q&A where relevant), (2) the thesis pipeline Progress log, (3) this file, and (4) the GitHub repo.

## The question
Do the dopaminergic (DA) neurons that die in Parkinson's disease (the SOX6_AGTR1 subtype, Kamath et al. 2022) carry a senescence or accelerated-aging program, compared with resilient subtypes (CALB1+), in human substantia nigra? Which of those genes have genetic (Mendelian randomization) support?

Purely computational, public data only. Standalone project (no links to other work).

## Setup
- Computer: MacBook Pro Early 2015, Intel, 8 GB RAM, macOS Monterey 12.7.6, ~100 GB free disk.
- Single-cell steps run in Google Colab (free; CPU runtime, no High-RAM option on this account; Colab now runs Python 3.13). Outputs go to Google Drive > My Drive.
- Notebooks live in Google Drive > Colab Notebooks (outputs, tables and plots saved inside them). Copies are attached to this project.
- The Mac will run Aim 1 (bulk datasets) and Aim 3 in R (Intel R 4.6; RStudio 2024.09.1+394 is the last version certified for Monterey).

## Done
1. Topic, design and novelty check. Ferraro et al. 2022 (Cells) already did the bulk SN meta-analysis with cell-composition correction, so novelty lives in Aim 2 (subtype aging test) and Aim 3 (causal layer).
2. Dataset screening: 20 GEO series verified on GEO pages (table in the thesis doc).
3. Aim 2 step 1 (Colab, 9 Oct): GSE178265 human matrix (41,625 genes x 434,340 cells) reduced to 50,058 cells: 30,058 DA candidates + 20,000 marker-negative cells.
4. Aim 2 step 2 (Colab, 23 Oct):
   - 97 libraries matched to GEO records; caudate removed (2,627 cells).
   - 18 donors: 8 control (ages 49-92), 6 PD, 4 LBD. Donor ID = first 4-digit number in the sample name. No conflicts.
   - QC (>=500 genes, <5% mito): 40,078 cells. Harmony on sample, Leiden 0.5: 19 clusters.
   - Clusters 14-18 = DA neurons (16,755 cells). Cluster 14: highest SOX6 (1.88) and AGTR1 (0.66) = vulnerable subtype. Cluster 18: highest CALB1 (0.68) = resilient. Cluster 8 borderline DA/GABA, excluded.
   - Lesson: the step 1 candidate rule made the original Cell 7 detection table circular; DA identity was confirmed by marker-strength scores (Cell 7b) instead.
5. Set-up before step 3 (23 Oct):
   - GitHub kelyto30/pd-da-aging: commit 24ec439 (steps 1-2 notebooks, src, README, LICENSE, .gitignore, docs) + analysis plan v2 commit. Uploads are MANUAL (Claude's GitHub link is to a different account); tell the user exactly which files changed and where to put them.
   - Analysis plan v2 (docs/ANALYSIS_PLAN.md, also in this project) written and revised BEFORE any scoring.
   - Both .h5ad files backed up on the Mac: Documents/MY PERSONAL PROJECTS/pd-da-aging/data (ignored by git).
   - Research proposal and Research Companion created (links above).
6. Aim 2 step 3 (Colab, 25 Nov; notebook step3_subtypes_and_senescence.ipynb, in this project):
   - Notebook tested first on simulated data (labels 100% correct, planted effect found, 0/3 false positives under the null).
   - Analysis plan v2.1 and v2.2, both BEFORE scoring: readout genes excluded from clustering HVGs; H2 as diff ~ disease on per-donor differences (identical to the planned model; always converges) plus a sex+age-adjusted version; AUCell counts detected genes only; Kamath markers = Fig 1E panel from authors' code (commit cae72e1); brain-aging set = LU_AGING_BRAIN_UP; CellAge = "Induces"; high-confidence-labels sensitivity check (drop |SOX6_minus_CALB1| < 0.5 and SOX6_AGTR1 margin < 0.25).
   - Colab fixes: numba thread error (set sc.settings.n_jobs = NUMBA_NUM_THREADS); Cell 5 resets X from raw counts (leftover uns['log1p'] from step 2).
   - Gene lists (downloaded 25 Nov): Kamath 17/17 in data; SenMayo 125 (105 used; GEM removed as a marker; 124/125 match MSigDB SAUL_SEN_MAYO); CellAge induces 370 (359); LU_AGING_BRAIN_UP 264 (249); CDKN1A detected in 1.9% and CDKN2A in 0.5% of neurons.
   - Subtypes: 21 sub-clusters (resolution 1.0), all 10 Kamath subtypes. SOX6_AGTR1 6,444 (vulnerable); CALB1 pooled 6,243 (resilient); other SOX6 4,068. Cross-check: 68% of SOX6_AGTR1 in step 2 cluster 14; only 36% of CALB1 in cluster 18 (reported, not corrected). Low-confidence sub-clusters: 2, 9, 11, 12.
   - **H1 (primary): opposite to prediction.** 7 of 8 controls qualified (>=108 neurons per group). SenMayo vulnerable minus resilient = -0.0217 (95% CI -0.0239 to -0.0195), paired t p = 3.1e-7, dz -9.2, Wilcoxon p = 0.016 (all 7 negative), random-slope MixedLM p < 1e-30.
   - Sensitivity, all same direction: min 10/50 identical; FACS-positive -0.0216; depth-adjusted -0.0193; AUCell -0.0070 (p = 0.0004); high-confidence -0.0234; leave-one-out -0.0211 to -0.0221. Vulnerable neurons have more UMIs (median 28,063 vs 26,096) and fewer genes (6,227 vs 6,580).
   - Secondary (controls, BH q): CellAge -0.008 (p 0.003, q 0.07); CDKN1A pseudobulk -0.13 (p 0.045, q 0.21); CDKN1A per-neuron p 0.05; CDKN2A and LU_AGING_BRAIN_UP null.
   - H2: 7 control vs 4 disease donors qualified; no interaction (SenMayo p 0.64; adjusted p 0.90). PD-only p = 0.004 with only 2 PD donors: unreliable.
   - H3 (exploratory): SenMayo rho 0.09 (p 0.85); LU_AGING_BRAIN_UP rho -0.85 (p 0.016, q 0.19); CDKN1A pseudobulk rho -0.79 (p 0.033, q 0.21).
   - Interpretation: baseline senescence program does not explain SOX6_AGTR1 vulnerability; small, robust difference in the opposite direction; SenMayo leans on secreted/immune genes neurons barely express, so identity effects are possible; not evidence of protection.
   - Research Companion (Step 3 section, update log, 5 new committee Q&As, next steps) and thesis pipeline progress log updated 25 Nov.

## Files in Google Drive (My Drive)
| File | Contents |
| --- | --- |
| GSE178265_DA_neurons.h5ad | 16,755 DA neurons x 29,685 genes, raw counts; obs has donor, status (Ctrl/PD/LBD), disease, sex, age, pmi, facs, sample, DA_cluster |
| GSE178265_celltype_reference.h5ad | 40,078 SN cells with cell_type labels, raw counts (for Aim 1 deconvolution) |
| GSE178265_cluster_identities.csv | Cell-type scores per cluster |
| GSE178265_samples_with_GEO.csv | 97 libraries with GEO metadata |
| GSE178265_all_cells_clusters.csv | Per-cell cluster labels and QC |
| GSE178265_DA_extract.zip | Step 1 output (raw, 955 MB) |
| pd-da-aging_step3/ | GSE178265_DA_neurons_step3.h5ad (265 MB; subtype, group, subcluster and all scores in obs); figures/ (4 PNGs); tables/ (16 CSVs incl. H1_result_SenMayo, H1_sensitivity, all_readouts_H1_H2_H3, subcluster_subtype_labels); gene_sets/gene_sets_2026-11-25.json; software_versions.txt |

## Decisions
- Main comparison: PD + LBD together (as Kamath); PD alone as sensitivity.
- Statistics count donors, not libraries; minimum neurons per donor (some donors have <50 DA neurons, e.g. 1963: 20, 3298: 32).
- Primary test is within-donor (AGTR1 vs resilient subtypes in the same person).
- FACS sort status (Positive/Negative) recorded as a technical covariate.
- Gene lists (Kamath subtype markers, SenMayo, CellAge) must be taken from their original sources, not typed from memory.
- Analysis plan (now v2.2): see docs/ANALYSIS_PLAN.md and claude/ANALYSIS_PLAN.md; change log records every change and that all were made before scoring.
- Any analysis decided after seeing step 3 results (e.g. gene-level drivers) must be labelled exploratory / post hoc.

## Next
1. User uploads to GitHub: notebooks/step3_subtypes_and_senescence.ipynb, docs/ANALYSIS_PLAN.md (v2.2), docs/progress_log.md (if kept in repo).
2. User shares the step 3 result with the advisor.
3. Aim 2 replication in GSE157783 (Smajic et al. 2022): same H1 test; direction is the criterion. Check how many DA neurons and control donors it has first.
4. Exploratory (post hoc): which SenMayo/CellAge genes drive the vulnerable-minus-resilient difference.

## Remaining after that
- Aim 2: GSE184950 if feasible; backup scoring of GSE20141 (laser-captured SNpc).
- Aim 1 (Mac, R): 11 bulk SN cohorts, per-cohort limma, random-effects meta-analysis, deconvolution with our reference, aging/senescence overlap, Braak staging (GSE49036, GSE42966), held-out RNA-seq validation (GSE114517).
- Aim 3: MR + colocalisation (PD GWAS + eQTLGen/GTEx), blood classifier (GSE99039 train; GSE6613, GSE72267 test), CMap/LINCS drug repurposing.
- Admin: advisor/committee approval of this project (share proposal + analysis plan); IRB not-human-subjects check.
- Writing: chapters and papers.
