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
plt.rc("figure",    figsize=(7.16, 3.5))  # a little taller for 3 curves

# custom colors
TUD_BLUE       = "#00305d"   # baseline historyLength
COMNETS_BLUE   = "#2C94CC"   # link delay
COMNETS_MAGENTA= "#E20074"   # dynamic historyLength
GRAY = "#555555"  # gray

def unpack_vector(csv_path: Path, vector_name: str):
    df = pd.read_csv(csv_path)
    row = df[(df["type"]=="vector") & (df["name"]==vector_name)].iloc[0]
    t_s  = np.fromiter(map(float, row["vectime"].split()),  dtype=float)
    v     = np.fromiter(map(float, row["vecvalue"].split()), dtype=float)
    return t_s * 1e3, v  # time in ms, value as-is

def plot_combined(folder: Path):
    # file paths
    delay_csv = folder / "baseline_linkDelay.csv"
    dyn_csv   = folder / "dynamicHL_historyLength.csv"
    sort_csv   = folder / "sorting_reorderBuffLength.csv"

    # unpack both vectors
    t_delay, delay_ms     = unpack_vector(delay_csv, "linkDelay:vector")
    t_hist,  hist_dyn     = unpack_vector(dyn_csv,   "historyLength:vector")
    t_sort,  buff_sort     = unpack_vector(sort_csv,   "reorderBuffLength:vector")

    # make plot
    fig, ax = plt.subplots()

    # 3a) Link delay as blue circles
    sns.scatterplot(x=t_delay, y=delay_ms,
                    ax=ax, s=20, color=GRAY,
                    label="Link delay (ms)", edgecolor="none")

    # 3b) Baseline history length = 5, horizontal line
    ax.axhline(5, color=TUD_BLUE, linestyle="--", linewidth=1.0,
               label="Baseline historyLength")

    # 3c) Dynamic history length as magenta step plot
    ax.step(t_hist, hist_dyn,
            where="post",
            color=COMNETS_BLUE,
            linewidth=1.5,
            label="Dynamic historyLength")

    # 3d) Sorting buffer length as magenta step plot
    ax.step(t_sort, buff_sort,
            where="post",
            color=COMNETS_MAGENTA,
            linewidth=1.5,
            label="Sorting buffer length")

    # axes & ticks
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Value")
    ax.set_title("Link Delay, History Length, and Sorting Buffer over Time", pad=6, fontsize=14)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.tick_params(which="minor", length=3)

    # legend
    ax.legend(loc="upper left", frameon=False)

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
