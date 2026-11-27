# Aging and senescence programs in vulnerable dopaminergic neurons in Parkinson's disease

PhD thesis project (computational, public data only).

**Question.** Do the substantia nigra dopaminergic (DA) neurons that are selectively lost in Parkinson's disease (the SOX6_AGTR1 subtype; Kamath et al., *Nat Neurosci* 2022) carry a senescence or accelerated-aging transcriptional program compared with resilient subtypes, and which of these genes have genetic support for a causal role?

## Structure

| Folder | Contents |
| --- | --- |
| `notebooks/` | Google Colab notebooks, run in order (step1, step2, ...) |
| `src/` | Helper code used by the notebooks |
| `docs/` | Analysis plan and progress log |
| `results/` | Figures and small result tables for each step (see `results/README.md`; large outputs are kept in Google Drive) |

## Analysis steps

| Step | Notebook | What it does | Status |
| --- | --- | --- | --- |
| 1 | `step1_extract_DA_neurons.ipynb` | Streams the GSE178265 human matrix (41,625 genes x 434,340 nuclei) and keeps DA-marker-positive nuclei (TH plus SLC6A3 or SLC18A2; 30,058) plus 20,000 random marker-negative nuclei | Done 2026-10-09 |
| 2 | `step2_clean_and_confirm_DA.ipynb` | Matches libraries to GEO metadata; removes caudate; QC (>=500 genes, <5% mitochondrial); Harmony (by library) + Leiden; confirms DA clusters by marker-strength scores; saves 16,755 DA neurons (18 donors) and a labelled reference of 40,078 SN nuclei | Done 2026-10-23 |
| 3 | `step3_subtypes_and_senescence.ipynb` | Downloads gene lists from their sources (Kamath Fig 1E panel, SenMayo, CellAge, MSigDB LU_AGING_BRAIN_UP); re-clusters the DA neurons with readout genes excluded and labels the 10 Kamath subtypes; scores senescence/aging; H1 (within-donor, controls), H2 (disease), H3 (age), secondary readouts and pre-specified sensitivity analyses | Done 2026-11-25 |
| 4 | `step4_gene_drivers.ipynb` | Exploratory (decided after step 3): gene-by-gene breakdown of the SenMayo and CellAge gaps, comparison with expression-matched random gene sets, SenMayo categories | Done 2026-11-27 |
| 5a | `step5a_replication_feasibility.ipynb` | Replication feasibility in GSE184950: streams each sample from GEO, counts dopamine-neuron candidates per donor and keeps them | Done 2026-11-27 |
| 5b | `step5b_replication.ipynb` | H1 replication in GSE184950 control donors (protocol in `docs/ANALYSIS_PLAN.md`), with label transfer from GSE178265, sensitivity checks and the step 4 driver genes | Stopped at the labelling checkpoint 2026-11-27: subtypes not resolvable in GSE184950 (no scores computed) |
| 5c | `step5c_siletti_feasibility.ipynb` | Replication feasibility in the Siletti et al. 2023 human brain atlas (CELLxGENE): dopamine neurons per healthy donor | Done 2026-11-27: 3 donors, 159 to 310 candidates each |
| 5d | `step5d_siletti_replication.ipynb` | H1 replication in the Siletti atlas (same protocol and labelling checkpoint as step 5b) | Done 2026-11-27: replicated in direction (3 of 3 donors; mean difference −0.0217, p = 0.053) |

Cells added during the step 2 run (4b, 4c, 7b, 8b) are included in the notebook. Cell 7 in step 2 is kept for the record but is not used for the DA call: because step 1 selected candidates on the same markers, its detection fractions are circular. DA identity was assigned from Cell 7b (mean log-normalised marker expression per cluster).

## Data

All input data are public. Nothing is redistributed here.

| Dataset | Source | Used for |
| --- | --- | --- |
| GSE178265 (Kamath et al. 2022) | NCBI GEO, processed human matrix `GSE178265_Homo_matrix.mtx.gz` with `_features` and `_bcd` files; sample metadata from the GEO series matrix files | Aim 2 |

Additional bulk and blood datasets (Aims 1 and 3) are listed in `docs/progress_log.md`.

## Software

Run on Google Colab (Python 3). Package versions: see `docs/software_versions.txt`.

## Use of AI assistance

Analysis code was drafted with AI assistance (Anthropic Claude) and run, checked and interpreted by the author. This will be disclosed in publications according to each journal's policy.

## Citation

Please cite the original data: Kamath T, et al. Single-cell genomic profiling of human dopamine neurons identifies a population that selectively degenerates in Parkinson's disease. *Nat Neurosci* 2022;25(5):588-595.
