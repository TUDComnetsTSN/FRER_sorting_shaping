#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# 1) seaborn style & matplotlib rcParams
sns.set_style("whitegrid")
plt.rc("font",      family="serif", serif=["DejaVu Serif"])
plt.rc("axes",      titlesize=14,  labelsize=14)
plt.rc("xtick",     labelsize=14)
plt.rc("ytick",     labelsize=14)
plt.rc("legend",    fontsize=12)
plt.rc("figure",    figsize=(7.16, 3.5))  # two-column width × a bit taller

# custom colors
TUD_BLUE        = "#00305d"   # baseline
COMNETS_BLUE    = "#2C94CC"   # dynamic
COMNETS_MAGENTA = "#E20074"   # sorting

def read_vector(csv_path: Path, vector_name: str):
    """Load a single vector series from a CSV and return (time_ms, values)."""
    df = pd.read_csv(csv_path)
    row = df[(df["type"]=="vector") & (df["name"]==vector_name)].iloc[0]
    t_s    = np.fromiter(map(float, row["vectime"].split()),  dtype=float)
    values = np.fromiter(map(float, row["vecvalue"].split()), dtype=float)
    return t_s * 1e3, values  # time in ms

def plot_seqnum_comparison(folder: Path):
    # file paths
    baseline_csv = folder / "baseline_seqNum.csv"
    dynamic_csv  = folder / "dynamicHL_seqNum.csv"
    sorting_csv  = folder / "sorting_seqNum.csv"
    vector_name  = "seqNum:vector"

    # unpack all series
    t_base, base_vals   = read_vector(baseline_csv, vector_name)
    t_dyn,  dyn_vals    = read_vector(dynamic_csv,  vector_name)
    t_sort, sort_vals   = read_vector(sorting_csv,  vector_name)

    # create figure
    fig, ax = plt.subplots()

    # baseline as step
    ax.step(t_base, base_vals,
            where="post",
            color=TUD_BLUE,
            linewidth=1.5,
            label="Baseline")

    # dynamic as step
    ax.step(t_dyn, dyn_vals,
            where="post",
            color=COMNETS_BLUE,
            linewidth=1.5,
            label="DynamicHL")

    # sorting as step
    ax.step(t_sort, sort_vals,
            where="post",
            color=COMNETS_MAGENTA,
            linewidth=1.5,
            label="Sorting")

    # labels & title
    ax.set_title("Sequence Number over Time", pad=6, fontsize=16)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Sequence Number")

    # ticks
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.tick_params(which="minor", length=3)

    # legend
    ax.legend(loc="upper left", frameon=False)

    # save PDF into results folder
    out_pdf = folder / "seqNum_step_comparison.pdf"
    fig.savefig(out_pdf, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()
    print(f"✅ Saved figure → {out_pdf}")

if __name__ == "__main__":
    results_dir = Path(
        "/home/howhang/omnetpp-6.1.0-linux-x86_64"
        "/omnetpp-6.1/samples/FRER/simulations/results"
    )
    plot_seqnum_comparison(results_dir)
