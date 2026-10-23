# Core logic for extracting dopaminergic-neuron candidates from a large
# Matrix Market (.mtx.gz) file without loading the whole matrix into memory.
# The Colab notebook runs these same steps cell by cell.

import gzip
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.io import mmwrite

CHUNK = 20_000_000  # rows of the .mtx file read at a time


def read_header(mtx_path):
    """Return (n_rows, n_cols, n_entries) and the number of lines before the data."""
    skip = 0
    with gzip.open(mtx_path, "rt") as f:
        for line in f:
            skip += 1
            if line.startswith("%"):
                continue
            n_rows, n_cols, n_entries = (int(x) for x in line.split())
            return n_rows, n_cols, n_entries, skip
    raise ValueError("No size line found in the .mtx file")


def iter_chunks(mtx_path, skip):
    """Yield (row, col, value) arrays, 0-based, one chunk at a time."""
    reader = pd.read_csv(
        mtx_path, sep=" ", header=None, skiprows=skip, chunksize=CHUNK,
        names=["r", "c", "v"], dtype={"r": np.int64, "c": np.int64, "v": np.float32},
        compression="gzip", engine="c",
    )
    for chunk in reader:
        yield (chunk["r"].to_numpy() - 1, chunk["c"].to_numpy() - 1, chunk["v"].to_numpy())


def load_names(features_path, barcodes_path):
    feats = pd.read_csv(features_path, sep="\t", header=None, dtype=str)
    bcds = pd.read_csv(barcodes_path, sep="\t", header=None, dtype=str)
    return feats, bcds


def find_gene_column(feats, markers):
    """Pick the features column that contains the marker gene symbols."""
    best, best_hits = 0, -1
    for j in range(feats.shape[1]):
        hits = feats[j].isin(markers).sum()
        if hits > best_hits:
            best, best_hits = j, hits
    return best, best_hits


def orientation(n_rows, n_cols, n_feats, n_bcds):
    """'genes_by_cells' or 'cells_by_genes'."""
    if n_rows == n_feats and n_cols == n_bcds:
        return "genes_by_cells"
    if n_rows == n_bcds and n_cols == n_feats:
        return "cells_by_genes"
    raise ValueError(f"Matrix is {n_rows} x {n_cols}, but there are {n_feats} features and {n_bcds} barcodes")


def pass1_marker_counts(mtx_path, skip, orient, n_cells, marker_idx):
    """Per-cell total counts and per-cell counts for each marker gene."""
    totals = np.zeros(n_cells, dtype=np.float64)
    marker_counts = {g: np.zeros(n_cells, dtype=np.float64) for g in marker_idx}
    idx_to_gene = {i: g for g, i in marker_idx.items()}
    marker_set = np.array(list(idx_to_gene.keys()))
    for r, c, v in iter_chunks(mtx_path, skip):
        genes, cells = (r, c) if orient == "genes_by_cells" else (c, r)
        totals += np.bincount(cells, weights=v, minlength=n_cells)
        hit = np.isin(genes, marker_set)
        for gi, ci, vi in zip(genes[hit], cells[hit], v[hit]):
            marker_counts[idx_to_gene[gi]][ci] += vi
    return totals, marker_counts


def choose_cells(totals, marker_counts, min_umi=500, n_reference=20_000, seed=1):
    """DA candidates = any DA marker detected; reference = random sample of the rest."""
    da_signal = sum(marker_counts.values())
    ok = totals >= min_umi
    da = np.where(ok & (da_signal > 0))[0]
    rest = np.where(ok & (da_signal == 0))[0]
    rng = np.random.default_rng(seed)
    ref = rng.choice(rest, size=min(n_reference, rest.size), replace=False)
    return np.sort(da), np.sort(ref)


def pass2_extract(mtx_path, skip, orient, n_genes, n_cells, keep):
    """Keep only entries for the selected cells; return a genes x kept-cells matrix."""
    new_pos = np.full(n_cells, -1, dtype=np.int64)
    new_pos[keep] = np.arange(keep.size)
    rows, cols, vals = [], [], []
    for r, c, v in iter_chunks(mtx_path, skip):
        genes, cells = (r, c) if orient == "genes_by_cells" else (c, r)
        m = new_pos[cells] >= 0
        rows.append(genes[m].astype(np.int32))
        cols.append(new_pos[cells[m]].astype(np.int32))
        vals.append(v[m])
    rows, cols, vals = np.concatenate(rows), np.concatenate(cols), np.concatenate(vals)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(n_genes, keep.size))


def write_outputs(out_dir, mat, feats, gene_col, barcodes, cell_info):
    import os
    os.makedirs(out_dir, exist_ok=True)
    with gzip.open(f"{out_dir}/matrix.mtx.gz", "wb") as f:
        mmwrite(f, mat.tocoo())
    feats[[gene_col]].to_csv(f"{out_dir}/features.tsv.gz", sep="\t", header=False, index=False)
    pd.Series(barcodes).to_csv(f"{out_dir}/barcodes.tsv.gz", sep="\t", header=False, index=False)
    cell_info.to_csv(f"{out_dir}/cell_info.csv", index=False)
