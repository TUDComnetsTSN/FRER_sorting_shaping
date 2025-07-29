#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# seaborn & matplotlib style
sns.set_style("whitegrid")
plt.rc("font",      family="serif", serif=["DejaVu Serif"])
plt.rc("axes",      titlesize=14,  labelsize=14)
plt.rc("xtick",     labelsize=14)
plt.rc("ytick",     labelsize=14)
plt.rc("legend",    fontsize=12)
plt.rc("figure",    figsize=(7.16, 3.5))

# custom colors
TUD_BLUE         = "#00305d"   # Baseline
COMNETS_BLUE     = "#2C94CC"   # DynamicHL
COMNETS_MAGENTA  = "#E20074"   # Sorting

def read_seqnums(csv_path: Path, vector_name: str):
    """Read seqNum vector from CSV and return numpy array of ints."""
    df = pd.read_csv(csv_path)
    row = df[(df["type"]=="vector") & (df["name"]==vector_name)].iloc[0]
    seq = np.fromiter(map(float, row["vecvalue"].split()), dtype=int)
    return seq

def compute_ratios(seq: np.ndarray):
    """Compute out-of-order and duplicate ratios (in %)."""
    # Out-of-order: adjacent jumps ≠ +1
    diffs = seq[1:] - seq[:-1]
    total_pairs = len(diffs)
    ooo_count = np.sum(diffs != 1)

    # Duplicate: any repeated sequence number across the whole series
    total = len(seq)
    unique = len(np.unique(seq))
    dup_count = total - unique

    return {
        "Out-of-order (%)":  ooo_count / total_pairs * 100,
        "Duplicate (%)":     dup_count    / total       * 100
    }

def plot_bar_ratios(folder: Path):
    # file paths
    baseline_csv = folder / "baseline_seqNum.csv"
    dynamic_csv  = folder / "dynamicHL_seqNum.csv"
    sorting_csv  = folder / "sorting_seqNum.csv"
    vector_name  = "seqNum:vector"

    # read sequences
    seq_base = read_seqnums(baseline_csv, vector_name)
    seq_dyn  = read_seqnums(dynamic_csv,  vector_name)
    seq_sort = read_seqnums(sorting_csv,  vector_name)

    # compute ratios
    ratios_base = compute_ratios(seq_base)
    ratios_dyn  = compute_ratios(seq_dyn)
    ratios_sort = compute_ratios(seq_sort)

    # prepare DataFrame for seaborn
    df = pd.DataFrame([
        {"Scenario": "Baseline",   "Metric": m, "Ratio": r}
        for m, r in ratios_base.items()
    ] + [
        {"Scenario": "DynamicHL",  "Metric": m, "Ratio": r}
        for m, r in ratios_dyn.items()
    ] + [
        {"Scenario": "Sorting",    "Metric": m, "Ratio": r}
        for m, r in ratios_sort.items()
    ])

    # plot grouped bar chart
    fig, ax = plt.subplots()
    sns.barplot(
        data=df,
        x="Metric", y="Ratio", hue="Scenario",
        palette={
            "Baseline":   TUD_BLUE,
            "DynamicHL":  COMNETS_BLUE,
            "Sorting":    COMNETS_MAGENTA
        },
        ax=ax
    )

    # labels & title
    ax.set_xlabel("Metric")
    ax.set_ylabel("Ratio (%)")
    #ax.set_title("Out-of-Order and Duplicate Ratios", pad=6, fontsize=16)

    # ticks & legend
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.legend(loc="upper right", frameon=False)

    # for each BarContainer (one per hue), label its bars
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.0f%%",   # integer percent
            padding=0       # space in points between bar top and label
        )

    # save PDF in results folder
    out_pdf = folder / "seqNum_ratios.pdf"
    fig.savefig(out_pdf, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()
    print(f"✅ Saved → {out_pdf}")

if __name__ == "__main__":
    results_dir = Path(
        "/home/howhang/omnetpp-6.1.0-linux-x86_64"
        "/omnetpp-6.1/samples/FRER/simulations/results"
    )
    plot_bar_ratios(results_dir)
