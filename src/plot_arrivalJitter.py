#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
GREEN           = "#65B32E"   # shaping

# Choose plot type: 'violin', 'box', or 'cdf'
PLOT_TYPE = 'cdf'
# Marker frequency: use a fixed interval for markevery
MARKER_EVERY = 30  # place a marker every N points along each CDF line


def read_intervals(csv_path: Path, vector_name: str, unit: str = 'ms') -> np.ndarray:
    """Load reception times and compute inter-receiving intervals."""
    df = pd.read_csv(csv_path)
    row = df[(df["type"] == "vector") & (df["name"] == vector_name)].iloc[0]
    t_s = np.fromiter(map(float, row["vectime"].split()), dtype=float)
    factor = 1e3 if unit == 'ms' else 1e6
    return np.diff(t_s * factor)


def plot_packet_jitter(folder: Path, plot_type: str = 'violin'):
    """
    Plot packet inter-receiving intervals as a violin, box, or CDF plot.
    """
    files = {
        "Baseline":        folder / "baseline_packetJitter.csv",
        "DynamicHL":       folder / "dynamicHL_packetJitter.csv",
        "Sorting":         folder / "sorting_packetJitter.csv",
        "Sorting+Shaping": folder / "shaping_packetJitter.csv",
    }
    vector_name = "packetJitter:vector"

    # load data
    data_ms = {lbl: read_intervals(path, vector_name, unit='ms')
               for lbl, path in files.items()}

    # print quartiles
    print("Variant        Q1 (µs)   Q3 (µs)   IQR (µs)")
    for lbl, arr in data_ms.items():
        arr_us = read_intervals(files[lbl], vector_name, unit='us')
        q1, q3 = np.percentile(arr_us, [25, 75])
        print(f"{lbl:<15}{q1:10.2f}{q3:10.2f}{(q3-q1):10.2f}")

    variants = ["Baseline", "DynamicHL", "Sorting", "Sorting+Shaping"]
    colors = [TUD_BLUE, COMNETS_BLUE, COMNETS_MAGENTA, GREEN]
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'd']

    fig, ax = plt.subplots()

    if plot_type == 'violin':
        df = pd.DataFrame({
            "Variant": np.repeat(variants, [len(data_ms[v]) for v in variants]),
            "Interval (ms)": np.concatenate([data_ms[v] for v in variants])
        })
        sns.violinplot(x="Variant", y="Interval (ms)", data=df,
                       palette=colors, inner="box", ax=ax)
        ax.set_yscale('log')
        ax.set_ylabel("Interval (ms) (log scale)")

    elif plot_type == 'box':
        df = pd.DataFrame({
            "Variant": np.repeat(variants, [len(data_ms[v]) for v in variants]),
            "Interval (ms)": np.concatenate([data_ms[v] for v in variants])
        })
        sns.boxplot(x="Variant", y="Interval (ms)", data=df,
                    palette=colors, ax=ax)
        ax.set_ylabel("Interval (ms)")

    elif plot_type == 'cdf':
        # CDF with both line and marker in single handle
        for lbl, color, ls, mk in zip(variants, colors, linestyles, markers):
            arr = np.sort(data_ms[lbl])
            cdf = np.arange(1, len(arr)+1) / len(arr)
            ax.plot(arr, cdf, label=lbl,
                    color=color, linestyle=ls,
                    marker=mk, markevery=MARKER_EVERY, alpha=0.8)
        # plot markers at the last point of each CDF
        for lbl, color, mk in zip(variants, colors, markers):
            arr = np.sort(data_ms[lbl])
            ax.scatter(arr[-1], 1.0,
                    color=color, marker=mk,
                    s=30,           # size tweak if you like
                    zorder=3)       # draw on top
        ax.set_ylabel('Empirical CDF')
        ax.set_xscale('log')
        ax.set_xlabel('Interval (ms)')
        ax.legend(title='Variant', frameon=True)

    else:
        raise ValueError("Invalid plot_type. Choose 'violin', 'box', or 'cdf'.")

    #ax.set_title("Packet Inter-Arrival Interval Distribution", pad=6, fontsize=16)
    if plot_type in ['violin', 'box']:
        ax.set_xlabel("")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

    out_pdf = folder / f"packetJitter_{plot_type}.pdf"
    fig.savefig(out_pdf, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()
    print(f"✅ Saved figure → {out_pdf}")


if __name__ == "__main__":
    results_dir = Path(
        "/home/howhang/omnetpp-6.1.0-linux-x86_64"
        "/omnetpp-6.1/samples/FRER/simulations/results"
    )
    plot_packet_jitter(results_dir, plot_type=PLOT_TYPE)
