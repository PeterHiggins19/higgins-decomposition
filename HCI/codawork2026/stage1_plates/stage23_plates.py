#!/usr/bin/env python3
"""
HCI Stage 2/3 — Navigation Plate Extension Generator
=====================================================

Extends the Stage 1 PDF slideshow with Stage 2 (metric cross-examination)
and Stage 3 (triadic structure) plate pages.

Reads stage1_output.json (same input as stage1_plates_raw.py).
Produces a multi-page PDF appending after Stage 1 output.

Output pages:
  Page 1: System Course Plot (full trajectory overview)
  Page 2: Stage 2 — Group Barycenter Distance Matrix
  Page 3: Stage 2 — Helmsman Frequency Chart
  Page 4: Stage 2 — Pairwise Divergence Ranking
  Page 5: Stage 3 — Triadic Area Ranking (top 10)
  Page 6: Stage 3 — Carrier Interaction Matrix
  Page 7: Summary Navigation Table (all metrics, all years)

DISPLAY STANDARD: Maximum text size. Back row readable. Line graphics only.
Monochrome. Scientific. No decoration.

Usage:
  python stage23_plates.py stage1_output.json [output.pdf]

The instrument reads. The expert decides. The loop stays open.
"""

import json
import sys
import os
import math
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import numpy as np


# ── Configuration ─────────────────────────────────────────────────
FIG_W = 16
FIG_H = 10
DPI = 150
FONT_SIZE_TITLE = 18
FONT_SIZE_LABEL = 14
FONT_SIZE_TICK = 12
FONT_SIZE_TABLE = 11
BAR_COLOR = "0.25"
LINE_COLOR = "black"
GRID_COLOR = "0.80"
BG_COLOR = "white"


# ═════════════════════════════════════════════════════════════��════
# SHARED GEOMETRY
# ══════════════════════════════════════════════════════════════════

def closure(x, eps=1e-15):
    x_pos = [max(float(v), eps) for v in x]
    total = sum(x_pos)
    return [v / total for v in x_pos]


def clr(x):
    D = len(x)
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]


def metric_distance(h1, h2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(h1, h2)))


def metric_energy(h):
    return sum(v ** 2 for v in h)


def barycenter(h_list):
    if not h_list:
        return []
    D = len(h_list[0])
    n = len(h_list)
    return [sum(h[j] for h in h_list) / n for j in range(D)]


def metric_angle(h1, h2):
    dot = sum(a * b for a, b in zip(h1, h2))
    m1_sq = sum(a ** 2 for a in h1)
    m2_sq = sum(a ** 2 for a in h2)
    if m1_sq < 1e-300 or m2_sq < 1e-300:
        return 0.0
    cross_sq = max(0.0, m1_sq * m2_sq - dot * dot)
    return math.degrees(math.atan2(math.sqrt(cross_sq), dot))


def dcdi(h1, h2, carriers):
    deltas = [(abs(h2[j] - h1[j]), j) for j in range(len(h1))]
    deltas.sort(reverse=True)
    return carriers[deltas[0][1]], deltas[0][0]


# ══════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════

def load_data(path):
    with open(path) as f:
        data = json.load(f)

    carriers = data["carriers"]
    D = data["D"]
    N = data["N"]
    years = data["years"]
    records = data["records"]

    # Extract CLR vectors
    h_all = [r["clr"] for r in records]
    x_all = [r["composition"] for r in records]

    return {
        "carriers": carriers,
        "D": D,
        "N": N,
        "years": years,
        "records": records,
        "h": h_all,
        "x": x_all,
    }


# ══════════════════════════════════════════════════════════════════
# STAGE 2 COMPUTATIONS
# ══════════════════════════════════════════════════════════════════

def compute_stage2(data):
    """Run Stage 2 analysis on loaded data."""
    h = data["h"]
    carriers = data["carriers"]
    years = data["years"]
    N = data["N"]

    # Per-year metrics (each year = one group)
    year_barycenters = h  # each year is a single point (already barycenter)
    year_energies = [metric_energy(hi) for hi in h]

    # Helmsman per transition
    helmsmen = []
    for i in range(1, N):
        name, delta = dcdi(h[i - 1], h[i], carriers)
        helmsmen.append({"year": years[i], "carrier": name, "delta": delta})

    # Helmsman frequency
    helm_freq = {}
    for hm in helmsmen:
        c = hm["carrier"]
        helm_freq[c] = helm_freq.get(c, 0) + 1

    # Pairwise distance matrix
    dist_matrix = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(metric_distance(h[i], h[j]))
        dist_matrix.append(row)

    # Pairwise ranking (all pairs, sorted by distance)
    pairs = []
    for i, j in combinations(range(N), 2):
        d = dist_matrix[i][j]
        angle = metric_angle(h[i], h[j])
        # Dominant contrast carrier
        carrier_deltas = [(abs(h[i][k] - h[j][k]), k) for k in range(len(h[i]))]
        carrier_deltas.sort(reverse=True)
        dom = carriers[carrier_deltas[0][1]]
        pairs.append({
            "year_a": years[i], "year_b": years[j],
            "distance": d, "angle": angle, "dom_carrier": dom
        })
    pairs.sort(key=lambda p: p["distance"], reverse=True)

    return {
        "year_energies": year_energies,
        "helmsmen": helmsmen,
        "helm_freq": helm_freq,
        "dist_matrix": dist_matrix,
        "pairs_ranked": pairs,
    }


# ══════════════════════════════════════════════════════════════════
# STAGE 3 COMPUTATIONS
# ══════════════════════════════════════════════════════════════════

def compute_stage3(data):
    """Run Stage 3 analysis — triadic and carrier interactions."""
    h = data["h"]
    carriers = data["carriers"]
    years = data["years"]
    N = data["N"]
    D = data["D"]

    # Triadic analysis (top triads by area)
    triads = []
    for i, j, k in combinations(range(N), 3):
        d_ij = metric_distance(h[i], h[j])
        d_jk = metric_distance(h[j], h[k])
        d_ki = metric_distance(h[k], h[i])
        s = (d_ij + d_jk + d_ki) / 2.0
        area_sq = s * (s - d_ij) * (s - d_jk) * (s - d_ki)
        area = math.sqrt(max(0.0, area_sq))
        imbalance = max(d_ij, d_jk, d_ki) / max(min(d_ij, d_jk, d_ki), 1e-300)
        triads.append({
            "years": (years[i], years[j], years[k]),
            "area": area, "imbalance": imbalance
        })
    triads.sort(key=lambda t: t["area"], reverse=True)

    # Carrier interaction matrix — correlation of CLR trajectories
    # Each carrier has a time-series of CLR values
    carrier_series = [[h[t][c] for t in range(N)] for c in range(D)]
    interaction_matrix = []
    for ci in range(D):
        row = []
        for cj in range(D):
            # Pearson correlation between carrier CLR trajectories
            xi = carrier_series[ci]
            xj = carrier_series[cj]
            mx = sum(xi) / N
            my = sum(xj) / N
            cov = sum((xi[t] - mx) * (xj[t] - my) for t in range(N)) / N
            sx = math.sqrt(sum((xi[t] - mx) ** 2 for t in range(N)) / N)
            sy = math.sqrt(sum((xj[t] - my) ** 2 for t in range(N)) / N)
            if sx < 1e-300 or sy < 1e-300:
                row.append(0.0)
            else:
                row.append(cov / (sx * sy))
        interaction_matrix.append(row)

    return {
        "triads_ranked": triads[:20],  # top 20
        "interaction_matrix": interaction_matrix,
    }


# ══════════════════════════════════════════════════════════════════
# PLATE GENERATION
# ══════════════════════════════════════════════════════════════════

def page1_course_plot(pdf, data):
    """System Course Plot — full CLR trajectory in plan view."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)

    h = data["h"]
    years = data["years"]
    carriers = data["carriers"]
    D = data["D"]

    # Plot trajectory of first two CLR dimensions
    x_vals = [hi[0] for hi in h]
    y_vals = [hi[1] for hi in h]

    ax.plot(x_vals, y_vals, "-", color=LINE_COLOR, linewidth=1.5, zorder=2)
    ax.scatter(x_vals, y_vals, color=LINE_COLOR, s=30, zorder=3)

    # Label every 5th year
    for i, yr in enumerate(years):
        if i % 5 == 0 or i == len(years) - 1:
            ax.annotate(str(yr), (x_vals[i], y_vals[i]),
                        fontsize=FONT_SIZE_TICK, ha="left", va="bottom",
                        xytext=(4, 4), textcoords="offset points")

    # Mark start and end
    ax.scatter([x_vals[0]], [y_vals[0]], color="black", s=100, marker="s", zorder=4)
    ax.scatter([x_vals[-1]], [y_vals[-1]], color="black", s=100, marker="D", zorder=4)

    ax.axhline(0, color=GRID_COLOR, linewidth=0.8, zorder=1)
    ax.axvline(0, color=GRID_COLOR, linewidth=0.8, zorder=1)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)

    ax.set_xlabel(f"CLR({carriers[0]}) [HLR]", fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel(f"CLR({carriers[1]}) [HLR]", fontsize=FONT_SIZE_LABEL)
    ax.set_title("SYSTEM COURSE PLOT — XY Plan View (CLR Space)", fontsize=FONT_SIZE_TITLE, fontweight="bold")
    ax.tick_params(labelsize=FONT_SIZE_TICK)
    ax.set_aspect("equal")

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page2_distance_matrix(pdf, data, s2):
    """Stage 2 — Distance matrix heatmap."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)

    N = data["N"]
    years = data["years"]
    dm = np.array(s2["dist_matrix"])

    im = ax.imshow(dm, cmap="Greys", aspect="auto")
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels([str(y) for y in years], fontsize=FONT_SIZE_TICK - 2, rotation=45, ha="right")
    ax.set_yticklabels([str(y) for y in years], fontsize=FONT_SIZE_TICK - 2)
    ax.set_title("STAGE 2 — Aitchison Distance Matrix (all year pairs)", fontsize=FONT_SIZE_TITLE, fontweight="bold")
    ax.set_xlabel("Year", fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel("Year", fontsize=FONT_SIZE_LABEL)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("d_A (HLR)", fontsize=FONT_SIZE_LABEL)

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page3_helmsman(pdf, data, s2):
    """Stage 2 — Helmsman frequency chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)

    carriers = data["carriers"]
    helm_freq = s2["helm_freq"]
    helmsmen = s2["helmsmen"]
    years = data["years"]

    # Left: frequency bar chart
    sorted_carriers = sorted(helm_freq.keys(), key=lambda c: helm_freq[c], reverse=True)
    counts = [helm_freq[c] for c in sorted_carriers]
    y_pos = range(len(sorted_carriers))
    ax1.barh(y_pos, counts, color=BAR_COLOR)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sorted_carriers, fontsize=FONT_SIZE_LABEL)
    ax1.set_xlabel("Helmsman Count (times dominant)", fontsize=FONT_SIZE_LABEL)
    ax1.set_title("HELMSMAN FREQUENCY", fontsize=FONT_SIZE_TITLE, fontweight="bold")
    ax1.tick_params(labelsize=FONT_SIZE_TICK)
    ax1.grid(True, axis="x", color=GRID_COLOR, linewidth=0.5)

    # Right: helmsman timeline
    helm_years = [hm["year"] for hm in helmsmen]
    helm_deltas = [hm["delta"] for hm in helmsmen]
    helm_names = [hm["carrier"] for hm in helmsmen]

    ax2.bar(range(len(helm_years)), helm_deltas, color=BAR_COLOR)
    ax2.set_xticks(range(len(helm_years)))
    ax2.set_xticklabels([str(y) for y in helm_years], fontsize=FONT_SIZE_TICK - 2, rotation=45, ha="right")
    ax2.set_ylabel("|delta h| (HLR)", fontsize=FONT_SIZE_LABEL)
    ax2.set_title("HELMSMAN DISPLACEMENT PER YEAR", fontsize=FONT_SIZE_TITLE, fontweight="bold")
    ax2.tick_params(labelsize=FONT_SIZE_TICK)
    ax2.grid(True, axis="y", color=GRID_COLOR, linewidth=0.5)

    # Annotate top 5
    sorted_idx = sorted(range(len(helm_deltas)), key=lambda i: helm_deltas[i], reverse=True)
    for rank, idx in enumerate(sorted_idx[:5]):
        ax2.annotate(helm_names[idx], (idx, helm_deltas[idx]),
                     fontsize=FONT_SIZE_TICK - 1, ha="center", va="bottom",
                     xytext=(0, 3), textcoords="offset points")

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page4_pairwise_ranking(pdf, data, s2):
    """Stage 2 — Pairwise divergence ranking (top 15)."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis("off")

    pairs = s2["pairs_ranked"][:15]

    # Table
    col_labels = ["Rank", "Year A", "Year B", "d_A (HLR)", "Angle (deg)", "Dominant Carrier"]
    table_data = []
    for i, p in enumerate(pairs):
        table_data.append([
            f"{i + 1}",
            str(p["year_a"]),
            str(p["year_b"]),
            f"{p['distance']:.4f}",
            f"{p['angle']:.1f}",
            p["dom_carrier"]
        ])

    table = ax.table(cellText=table_data, colLabels=col_labels,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(FONT_SIZE_TABLE)
    table.scale(1.0, 1.8)

    # Style header
    for j in range(len(col_labels)):
        table[0, j].set_facecolor("0.85")
        table[0, j].set_text_props(fontweight="bold")

    ax.set_title("STAGE 2 — Pairwise Divergence Ranking (Top 15)",
                 fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page5_triadic(pdf, data, s3):
    """Stage 3 — Triadic area ranking (top 10)."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis("off")

    triads = s3["triads_ranked"][:10]

    col_labels = ["Rank", "Year A", "Year B", "Year C", "Area (HLR^2)", "Imbalance"]
    table_data = []
    for i, t in enumerate(triads):
        table_data.append([
            f"{i + 1}",
            str(t["years"][0]),
            str(t["years"][1]),
            str(t["years"][2]),
            f"{t['area']:.4f}",
            f"{t['imbalance']:.2f}"
        ])

    table = ax.table(cellText=table_data, colLabels=col_labels,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(FONT_SIZE_TABLE)
    table.scale(1.0, 1.8)

    for j in range(len(col_labels)):
        table[0, j].set_facecolor("0.85")
        table[0, j].set_text_props(fontweight="bold")

    ax.set_title("STAGE 3 — Triadic Metric Triangle Area Ranking (Top 10)",
                 fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page6_carrier_interaction(pdf, data, s3):
    """Stage 3 — Carrier CLR trajectory correlation matrix."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)

    carriers = data["carriers"]
    D = data["D"]
    mat = np.array(s3["interaction_matrix"])

    im = ax.imshow(mat, cmap="RdGy", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(D))
    ax.set_yticks(range(D))
    ax.set_xticklabels(carriers, fontsize=FONT_SIZE_TICK, rotation=45, ha="right")
    ax.set_yticklabels(carriers, fontsize=FONT_SIZE_TICK)

    # Annotate cells with values
    for i in range(D):
        for j in range(D):
            val = mat[i, j]
            color = "white" if abs(val) > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=FONT_SIZE_TICK - 1, color=color)

    ax.set_title("STAGE 3 — Carrier CLR Trajectory Correlation",
                 fontsize=FONT_SIZE_TITLE, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Pearson r", fontsize=FONT_SIZE_LABEL)

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


def page7_summary_table(pdf, data, s2):
    """Summary Navigation Table — all metrics, all years."""
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis("off")

    records = data["records"]
    years = data["years"]

    col_labels = ["Year", "Hs", "Ring", "E_metric", "omega(deg)", "d_A", "Helmsman", "kappa_max"]
    table_data = []
    for i, r in enumerate(records):
        helm = r.get("helmsman") or "---"
        omega = r.get("angular_velocity_deg", 0.0)
        d_a = r.get("d_aitchison", 0.0)
        hs = r.get("hs", 0.0)
        ring = r.get("ring", "---")
        energy = r.get("metric_energy", 0.0)
        # max steering sensitivity
        ss = r.get("steering_sensitivity", {})
        kappa_max = max(ss.values()) if ss else 0.0
        table_data.append([
            str(years[i]),
            f"{hs:.4f}",
            ring,
            f"{energy:.1f}",
            f"{omega:.2f}",
            f"{d_a:.4f}",
            helm,
            f"{kappa_max:.0f}"
        ])

    table = ax.table(cellText=table_data, colLabels=col_labels,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(FONT_SIZE_TABLE - 1)
    table.scale(1.0, 1.4)

    for j in range(len(col_labels)):
        table[0, j].set_facecolor("0.85")
        table[0, j].set_text_props(fontweight="bold")

    ax.set_title("NAVIGATION SUMMARY — All Stage 1 Metrics by Year",
                 fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)

    fig.tight_layout()
    pdf.savefig(fig, dpi=DPI)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python stage23_plates.py stage1_output.json [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "stage23_plates.pdf"

    print(f"Loading: {input_path}")
    data = load_data(input_path)
    print(f"  {data['D']} carriers, {data['N']} years ({data['years'][0]}-{data['years'][-1]})")

    print("Computing Stage 2...")
    s2 = compute_stage2(data)
    print(f"  Helmsman freq: {s2['helm_freq']}")
    print(f"  Max pair distance: {s2['pairs_ranked'][0]['distance']:.4f}")

    print("Computing Stage 3...")
    s3 = compute_stage3(data)
    print(f"  Top triad area: {s3['triads_ranked'][0]['area']:.4f}")

    print(f"Generating PDF: {output_path}")
    with PdfPages(output_path) as pdf:
        page1_course_plot(pdf, data)
        print("  Page 1: System Course Plot")
        page2_distance_matrix(pdf, data, s2)
        print("  Page 2: Distance Matrix")
        page3_helmsman(pdf, data, s2)
        print("  Page 3: Helmsman Analysis")
        page4_pairwise_ranking(pdf, data, s2)
        print("  Page 4: Pairwise Divergence Ranking")
        page5_triadic(pdf, data, s3)
        print("  Page 5: Triadic Area Ranking")
        page6_carrier_interaction(pdf, data, s3)
        print("  Page 6: Carrier Interaction Matrix")
        page7_summary_table(pdf, data, s2)
        print("  Page 7: Navigation Summary Table")

    print(f"\nDone: {output_path} (7 pages)")
    print("The instrument reads. The expert decides. The loop stays open.")


if __name__ == "__main__":
    main()
