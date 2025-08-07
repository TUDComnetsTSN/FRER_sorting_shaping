#!/usr/bin/env python3
from matplotlib import font_manager
font_manager.fontManager.addfont(
    '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
import seaborn as sns
# ───── STYLE ────────────────────────────────────────────────────────────────
sns.set_style("whitegrid")
mpl.rc('font',   family='serif', serif=['Times New Roman'])
mpl.rc('axes',   titlesize=14,  labelsize=14, grid=True)
mpl.rc('xtick',  labelsize=14)
mpl.rc('ytick',  labelsize=14)
mpl.rc('legend', fontsize=12)
mpl.rc('figure', figsize=(7.16, 3.5))
mpl.rc('grid',   color='0.8', linestyle='-')

# ───── COLORS ───────────────────────────────────────────────────────────────
TUD_BLUE        = "#00305d"   # baseline
COMNETS_BLUE    = "#2C94CC"   # dynamic
COMNETS_MAGENTA = "#E20074"   # sorting


def print_dhl_ratios(results_dir: Path):
    jitters = list(range(11))
    rows = []
    for j in jitters:
        csv   = results_dir / f"dynamicHL_J{j}_seqNum.csv"
        seq   = read_seqnums(csv)
        ooo, dup = compute_ratios(seq)
        rows.append({
            "Jitter (ms)":     j,
            "OoO Ratio (%)":  round(ooo, 2),
            "Dup Ratio (%)":  round(dup, 2),
        })
    df = pd.DataFrame(rows)
    # Print a neat table
    print("\nDHL OoO and Dup ratios by jitter:\n")
    print(df.to_string(index=False))

def darken_hex(hex_color, amount=0.2):
    """Blend `hex_color` with black by `amount` (0–1)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    r, g, b = [int(c * (1 - amount)) for c in (r, g, b)]
    return f"#{r:02x}{g:02x}{b:02x}"

DARK_BLUE = darken_hex(COMNETS_BLUE, amount=0.2)

# ───── DATA HELPERS ─────────────────────────────────────────────────────────
def read_seqnums(csv_path: Path):
    df  = pd.read_csv(csv_path)
    row = df[(df["type"]=="vector") & (df["name"]=="seqNum:vector")].iloc[0]
    return np.fromiter(map(float, row["vecvalue"].split()), dtype=int)

def compute_ratios(seq: np.ndarray):
    diffs = seq[1:] - seq[:-1]
    ooo   = np.sum(diffs != 1) / len(diffs) * 100
    dup   = (len(seq) - len(np.unique(seq))) / len(seq) * 100
    return ooo, dup

# ───── PLOTTING ────────────────────────────────────────────────────────────
def plot_jitter_vs_ratios(results_dir: Path):
    jitters  = list(range(11))

    # dynamicHL values
    dyn_ooo_vals = []
    dyn_dup_vals = []
    for j in jitters:
        csv = results_dir / f"dynamicHL_J{j}_seqNum.csv"
        seq = read_seqnums(csv)
        ooo, dup = compute_ratios(seq)
        dyn_ooo_vals.append(ooo)
        dyn_dup_vals.append(dup)

    # baseline values (constant across jitters)
    base_seq = read_seqnums(results_dir / "baseline_seqNum.csv")
    base_ooo, base_dup = compute_ratios(base_seq)
    base_ooo_vals = [base_ooo] * len(jitters)
    base_dup_vals = [base_dup] * len(jitters)

    # sorting values (constant across jitters)
    sort_seq = read_seqnums(results_dir / "sorting_seqNum.csv")
    sort_ooo, sort_dup = compute_ratios(sort_seq)
    sort_ooo_vals = [sort_ooo] * len(jitters)
    sort_dup_vals = [sort_dup] * len(jitters)

    fig, ax = plt.subplots()
    # Baseline: circle marker, solid for OOO, dashed for Dup
    ax.plot(jitters, base_ooo_vals,
            marker='o', linestyle='-', color=TUD_BLUE,
            label='Baseline OoO.')
    ax.plot(jitters, base_dup_vals,
            marker='o', linestyle='--', color=TUD_BLUE,
            label='Baseline Dup.')

    # dynamicHL: square marker
    ax.plot(jitters, dyn_ooo_vals,
            marker='s', linestyle='-', color=DARK_BLUE,
            label='DHL OoO.')
    ax.plot(jitters, dyn_dup_vals,
            marker='s', linestyle='--', color=COMNETS_BLUE,
            label='DHL Dup.')

    # sorting: triangle marker
    ax.plot(jitters, sort_ooo_vals,
            marker='^', linestyle='-', color=COMNETS_MAGENTA,
            label='Sorting OoO.')
    ax.plot(jitters, sort_dup_vals,
            marker='^', linestyle='--', color=COMNETS_MAGENTA,
            label='Sorting Dup.')

    ax.set_xlabel("Jitter (ms)")
    ax.set_ylabel("Ratio (%)")
    ax.set_xticks(jitters)
    #ax.legend(ncol=3, loc="lower left", borderaxespad=1.0, markerscale=1, frameon=True, fontsize='medium', handlelength=2)
    ax.legend(
        loc='lower center',             # anchor point is bottom-center of legend box
        bbox_to_anchor=(0, 1, 1, 0.1),  # (x0, y0, width, height) in axes fraction
        ncol=3,                         # three columns, one per curve pair
        mode='expand',                  # stretch the legend box to fill bbox width
        frameon=True,
    )

    plt.tight_layout()
    out_pdf = results_dir / "jitter_ratios.pdf"
    fig.savefig(out_pdf, format="pdf", dpi=300, bbox_inches="tight")
    print(f"✅ Saved high-quality PDF → {out_pdf}")

    plt.show()

if __name__ == "__main__":
    results_dir = Path("/home/howhang/omnetpp-6.1.0-linux-x86_64/omnetpp-6.1/samples/FRER/simulations/results")
    plot_jitter_vs_ratios(results_dir)
    print_dhl_ratios(results_dir)
