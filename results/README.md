# Results

Figures and small tables produced by the notebooks in `notebooks/`. Large outputs (`.h5ad` files and per-neuron score tables) stay in Google Drive.

| Folder | From | Contents |
| --- | --- | --- |
| `step2/` | `step2_clean_and_confirm_DA.ipynb` | UMAP of all substantia nigra nuclei (Leiden clusters, TH, SLC6A3, DA candidates vs reference sample); cell-type marker dot plot per cluster; cluster cell-type scores; the 97 libraries matched to GEO metadata. Step 1 produced no figures. |
| `step3/` | `step3_subtypes_and_senescence.ipynb` | Kamath subtype marker dot plot and UMAP; H1 paired-donor plot; H2/H3 plot; subtype labels and cross-check; donor-level pairs for every readout; H1/H2/H3 results; sensitivity analyses; gene lists with sources and download date; software versions. |
| `step4/` | `step4_gene_drivers.ipynb` (exploratory) | Per-gene results for SenMayo and CellAge; SenMayo by category; comparison with expression-matched random gene sets (with leave-out checks); figures of the gene drivers and random-set distributions; software versions. |
