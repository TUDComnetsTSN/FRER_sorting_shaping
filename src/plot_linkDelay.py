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
plt.rc("figure",    figsize=(8, 4))  # wider for legend placement

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

    # create main and twin axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # second y-axis for latency

    # 1) Link delay on right axis
    scatter = ax2.scatter(
        t_delay, delay_ms,
        s=20, color=GRAY,
        label="Link delay (ms)"
    )
    ax2.set_ylabel("Latency (ms)", fontsize=14)

    # 2) Baseline on left axis
    ax1.axhline(
        5,
        color=TUD_BLUE, linestyle=linestyles[0],
        linewidth=1.5,
        label="Baseline"
    )

    # helper for sparse markers & lines
    def sparse_step(x, y, color, ls, marker, label):
        markevery = max(1, len(x) // 10)
        line, = ax1.plot(
            x, y,
            drawstyle='steps-post',
            color=color,
            linestyle=ls,
            marker=marker,
            markevery=markevery,
            linewidth=1.5,
            label=label
        )
        return line

    # 3) Dynamic history length
    line_dyn = sparse_step(
        t_hist, hist_dyn,
        COMNETS_BLUE, linestyles[1], markers[1],
        "DHL"
    )

    # 4) Sorting buffer length
    line_sort = sparse_step(
        t_sort, buff_sort,
        COMNETS_MAGENTA, linestyles[2], markers[2],
        "Sorting"
    )

    # 5) Sorting + Shaping buffer length
    line_shape = sparse_step(
        t_shape, buff_shape,
        GREEN, linestyles[3], markers[3],
        "Sorting+Shaping"
    )

    # axes & ticks
    ax1.set_xlabel("Time (ms)", fontsize=14)
    ax1.set_ylabel("Size", fontsize=14)
    #ax1.set_title(
    #    "Link Delay, History Length, Sorting Buffers over Time",
    #    pad=6
    #)

    # same scale for both y-axes
    ax1.set_ylim(0, 40)
    ax2.set_ylim(0, 40)

    # x-axis ticks
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.tick_params(which="minor", length=3)

    # Combine legend handles from both axes
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles = handles2 + handles1
    labels  = labels2 + labels1

    # Add legend inside figure
    ax1.legend(
        handles, labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1),# (x=2% from left, y=98% from bottom of axes)
        ncol=3, # max 3 items per row → yields 2 rows
        frameon=True,
        fontsize=12
    )

    # adjust layout for legend space
    fig.subplots_adjust(top=0.85)

    # save PDF
    out_pdf = folder / "combined_delay_hist.pdf"
    fig.savefig(
        out_pdf,
        format="pdf",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    print(f"✅ Saved combined plot → {out_pdf}")


if __name__ == "__main__":
    src_folder = Path(
        "/home/howhang/omnetpp-6.1.0-linux-x86_64"
        "/omnetpp-6.1/samples/FRER/simulations/results"
    )
    plot_combined(src_folder)
