# PD dopaminergic vulnerability thesis — project status and handoff

Last updated: 23 October 2026 (proposal and companion created; GitHub repo created at kelyto30/pd-da-aging)

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
- Single-cell steps run in Google Colab (free, ~12 GB RAM). Outputs go to Google Drive > My Drive.
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

## Files in Google Drive (My Drive)
| File | Contents |
| --- | --- |
| GSE178265_DA_neurons.h5ad | 16,755 DA neurons x 29,685 genes, raw counts; obs has donor, status (Ctrl/PD/LBD), disease, sex, age, pmi, facs, sample, DA_cluster |
| GSE178265_celltype_reference.h5ad | 40,078 SN cells with cell_type labels, raw counts (for Aim 1 deconvolution) |
| GSE178265_cluster_identities.csv | Cell-type scores per cluster |
| GSE178265_samples_with_GEO.csv | 97 libraries with GEO metadata |
| GSE178265_all_cells_clusters.csv | Per-cell cluster labels and QC |
| GSE178265_DA_extract.zip | Step 1 output (raw, 955 MB) |

## Decisions
- Main comparison: PD + LBD together (as Kamath); PD alone as sensitivity.
- Statistics count donors, not libraries; minimum neurons per donor (some donors have <50 DA neurons, e.g. 1963: 20, 3298: 32).
- Primary test is within-donor (AGTR1 vs resilient subtypes in the same person).
- FACS sort status (Positive/Negative) recorded as a technical covariate.
- Gene lists (Kamath subtype markers, SenMayo, CellAge) must be taken from their original sources, not typed from memory.

## Next
Aim 2 step 3 (Colab): label DA subtypes, score aging/senescence per neuron, within-donor comparison, age association in controls, save figures as image files to Drive.

## Remaining after that
- Aim 2: replication in GSE157783 (and GSE184950 if feasible); backup scoring of GSE20141 (laser-captured SNpc).
- Aim 1 (Mac, R): 11 bulk SN cohorts, per-cohort limma, random-effects meta-analysis, deconvolution with our reference, aging/senescence overlap, Braak staging (GSE49036, GSE42966), held-out RNA-seq validation (GSE114517).
- Aim 3: MR + colocalisation (PD GWAS + eQTLGen/GTEx), blood classifier (GSE99039 train; GSE6613, GSE72267 test), CMap/LINCS drug repurposing.
- Admin: advisor/committee approval of this project; IRB exemption check; GitHub repo.
- Writing: chapters and papers.
