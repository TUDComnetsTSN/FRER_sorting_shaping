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
plt.rc("figure",    figsize=(8, 4))  # wider for legend outside

# custom colors and styles
TUD_BLUE        = "#00305d"   # baseline
COMNETS_BLUE    = "#2C94CC"   # dynamic
COMNETS_MAGENTA = "#E20074"   # sorting
GREEN           = "#65B32E"   # shaping

# styles
linestyles = ['-', '--', '-.', ':']
markers    = ['o', 's', '^', 'd']

# gray scatter for link delay
GRAY = "#555555"

def unpack_vector(csv_path: Path, vector_name: str):
    df = pd.read_csv(csv_path)
    row = df[(df["type"] == "vector") & (df["name"] == vector_name)].iloc[0]
    t_s = np.fromiter(map(float, row["vectime"].split()), dtype=float)
    v   = np.fromiter(map(float, row["vecvalue"].split()), dtype=float)
    return t_s * 1e3, v  # time in ms, value as-is


def plot_combined(folder: Path):
    # file paths
    delay_csv = folder / "baseline_linkDelay.csv"
    dyn_csv   = folder / "dynamicHL_historyLength.csv"
    sort_csv  = folder / "sorting_reorderBuffLength.csv"
    shape_csv = folder / "shaping_reorderBuffLength.csv"

    # unpack vectors
    t_delay, delay_ms   = unpack_vector(delay_csv, "linkDelay:vector")
    t_hist,  hist_dyn   = unpack_vector(dyn_csv,   "historyLength:vector")
    t_sort,  buff_sort  = unpack_vector(sort_csv,  "reorderBuffLength:vector")
    t_shape, buff_shape = unpack_vector(shape_csv, "reorderBuffLength:vector")

    # create plot
    fig, ax = plt.subplots()

    # 1) link delay as gray circles
    sns.scatterplot(x=t_delay, y=delay_ms,
                    ax=ax, s=20, color=GRAY,
                    label="Link delay (ms)", edgecolor="none")

    # 2) baseline history length
    ax.axhline(5,
               color=TUD_BLUE, linestyle=linestyles[0],
               linewidth=1.5, label="Baseline")

    # helper for sparse markers
    def sparse_step(x, y, color, ls, marker, label):
        markevery = max(1, len(x) // 10)
        ax.plot(x, y,
                drawstyle='steps-post',
                color=color,
                linestyle=ls,
                marker=marker,
                markevery=markevery,
                linewidth=1.5,
                label=label)

    # 3) dynamic history length
    sparse_step(t_hist, hist_dyn,
                COMNETS_BLUE, linestyles[1], markers[1],
                "DynamicHL")

    # 4) sorting buffer length
    sparse_step(t_sort, buff_sort,
                COMNETS_MAGENTA, linestyles[2], markers[2],
                "Sorting")

    # 5) shaping buffer length
    sparse_step(t_shape, buff_shape,
                GREEN, linestyles[3], markers[3],
                "Sorting+Shaping")

    # axes & ticks
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Value")
    ax.set_title("Link Delay, History Length, Sorting Buffers over Time", pad=6)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.tick_params(which="minor", length=3)

    # legend outside to avoid overlap
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    fig.subplots_adjust(right=0.75)

    # save PDF
    out_pdf = folder / "combined_delay_hist.pdf"
    fig.savefig(out_pdf, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()
    print(f"✅ Saved combined plot → {out_pdf}")


if __name__ == "__main__":
    src_folder = Path(
        "/home/howhang/omnetpp-6.1.0-linux-x86_64"
        "/omnetpp-6.1/samples/FRER/simulations/results"
    )
    plot_combined(src_folder)
