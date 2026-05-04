#!/usr/bin/env python3
"""
HCI Stage 1 — Raw Section Plate Generator (matplotlib)
======================================================

Standalone Python program. No AI. No node. No formatting tricks.
Reads stage1_output.json, produces one matplotlib figure per time
interval showing all 3 orthogonal faces + plate information.

FIXED-SCALE INSTRUMENT DISPLAY
-------------------------------
All axes are fixed across all time frames (like a physical oscilloscope
graticule). Rapid scrolling through the cine-deck shows genuine movement
of compositional state against a constant backdrop.

Scale determination:
  - Bearings (XZ face): [-180, +180] degrees — exact (atan2 bound)
  - CLR (YZ face, XY scatter): pre-scanned from full dataset at load time
  - Hs: [0, 1] — exact by definition

The pre-scan reads all N records once, finds the global CLR range,
then pads by 10% for visual margin. This range is locked for all plates.

Layout (Higgins tensor data field layout v1.0):
  ┌──────────┬──────────┬──────────────────┐
  │  Info    │  Legend  │  Bar: XZ         │
  │  (text)  │  (pairs) │  (bearings)      │
  ├──────────┴──────────┼──────────────────┤
  │  Scatter: XY        │  Bar: YZ         │
  │  (plan view)        │  (CLR)           │
  └─────────────────────┴──────────────────┘

Info + Legend share top-left as two columns — maximum area use.
XY scatter = plan view: plots (h_i, h_j) for each carrier pair.
   The angle from origin to each point IS the bearing theta_{ij}.
XZ bar = all D(D-1)/2 pairwise bearings in degrees.
YZ bar = CLR coordinate per carrier (position in Higgins space).

Output: multi-page PDF (1 page per year) or individual PNGs.

Monochrome. Raw data. No interpretation. Scales to any D.

Usage:
  python stage1_plates_raw.py stage1_output.json [output.pdf]
  python stage1_plates_raw.py stage1_output.json --png output_dir/

The instrument reads. The expert decides. The loop stays open.
"""

import json
import sys
import os
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker


# ── Configuration ─────────────────────────────────────────────────
MONOCHROME = True       # enforce black/white/gray only
FIG_W      = 16         # inches
FIG_H      = 10         # inches
DPI        = 150
FONT_MONO  = "monospace"
BAR_COLOR  = "0.25"     # dark gray
SCATTER_COLOR = "black"
GRID_COLOR = "0.80"     # light gray
BG_COLOR   = "white"
TEXT_COLOR  = "black"


# ══════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════

def load_json(path):
    """Load stage1_output.json. Returns the full dict."""
    with open(path, "r") as f:
        return json.load(f)


# ══════════════════════════════════════════════════════════════════
# FIXED-SCALE PRE-SCAN — determines graticule limits for all plates
# ══════════════════════════════════════════════════════════════════

def compute_fixed_scales(data):
    """
    Pre-scan all records to determine fixed axis limits.

    Returns a dict with:
      bearing_ylim : (min, max) for XZ face — always (-180, 180)
      clr_ylim     : (min, max) for YZ face bars — data-adaptive + 10% pad
      scatter_xlim : (min, max) for XY scatter x-axis
      scatter_ylim : (min, max) for XY scatter y-axis

    The bearing range is exact (atan2 guarantee).
    The CLR range is computed from the full dataset and padded.
    The XY scatter uses CLR range on both axes (same space).

    For ANY compositional dataset:
      - Bearings will NEVER exceed [-180, +180]
      - CLR depends on the composition floor (smallest x_j)
      - Hs is always [0, 1] by construction

    This function is called ONCE at load time. The returned scales
    are passed to every render_plate() call, ensuring the graticule
    is identical across all time frames — like a physical scope.
    """
    D = data["D"]
    records = data["records"]

    # ── Bearings: mathematically exact ────────────────────────────
    bearing_ylim = (-180.0, 180.0)

    # ── CLR: scan all records for global range ────────────────────
    all_clr = []
    for rec in records:
        all_clr.extend(rec["clr"])

    clr_min = min(all_clr)
    clr_max = max(all_clr)

    # Pad by 10% of range for visual margin
    clr_range = clr_max - clr_min
    pad = clr_range * 0.10
    clr_ylim = (clr_min - pad, clr_max + pad)

    # XY scatter uses CLR values on both axes
    scatter_xlim = clr_ylim
    scatter_ylim = clr_ylim

    scales = {
        "bearing_ylim": bearing_ylim,
        "clr_ylim": clr_ylim,
        "scatter_xlim": scatter_xlim,
        "scatter_ylim": scatter_ylim,
        "clr_min_raw": clr_min,
        "clr_max_raw": clr_max,
    }

    return scales


# ══════════════════════════════════════════════════════════════════
# PLATE RENDERING — ONE FIGURE PER TIME INTERVAL
# ══════════════════════════════════════════════════════════════════

def render_plate(data, t, scales, fig=None):
    """
    Render one section plate for time index t with FIXED scales.

    Layout: Higgins tensor data field layout v1.0
      ┌──────────┬──────────┬──────────────────┐
      │  Info    │  Legend  │  XZ Bearings bar │
      ├──────────┴──────────┼──────────────────┤
      │  XY Scatter         │  YZ CLR bar      │
      └─────────────────────┴──────────────────┘

    Parameters
    ----------
    data   : dict   — full stage1_output.json contents
    t      : int    — time index (0-based)
    scales : dict   — fixed axis limits from compute_fixed_scales()
    fig    : Figure — optional existing figure to draw on

    Returns
    -------
    fig : matplotlib Figure
    """
    rec      = data["records"][t]
    carriers = data["carriers"]
    D        = data["D"]
    N        = data["N"]
    year     = rec["year"]
    clr      = rec["clr"]
    bearings = rec["bearings_deg"]
    hs       = rec["hs"]
    ring     = rec["ring"]
    omega    = rec["angular_velocity_deg"]
    d_a      = rec["d_aitchison"]
    helm     = rec["helmsman"]
    helm_d   = rec["helmsman_delta"]
    e_metric = rec["metric_energy"]
    kappa    = rec["condition_number"]
    steer    = rec["steering_sensitivity"]

    n_pairs  = D * (D - 1) // 2

    if fig is None:
        fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI,
                         facecolor=BG_COLOR)
    fig.clf()

    # ── Grid layout: 2 rows × 3 columns ─────────────────────────
    # Matches Higgins tensor data field layout v1.0 (Visio spec):
    #   [0,0] Info    [0,1] Legend   [0,2] XZ bar
    #   [1,0:2] XY scatter           [1,2] YZ bar
    # Width ratios from Visio: Info 1.82, Legend 1.76, Charts 2.91
    gs = fig.add_gridspec(2, 3,
                          width_ratios=[1.82, 1.76, 2.91],
                          height_ratios=[1, 1],
                          hspace=0.28, wspace=0.22,
                          left=0.06, right=0.97,
                          top=0.93, bottom=0.07)

    # ── Super-title ──────────────────────────────────────────────
    fig.suptitle(
        f"SECTION PLATE  t={t}  |  Year {year}  |  "
        f"D={D}  N={N}  pairs={n_pairs}",
        fontsize=14, fontfamily=FONT_MONO, fontweight="bold",
        color=TEXT_COLOR
    )

    # ─────────────────────────────────────────────────────────────
    # [0,0] TOP-LEFT: Plate Information Field
    # ─────────────────────────────────────────────────────────────
    ax_info = fig.add_subplot(gs[0, 0])
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis("off")

    info_lines = [
        f"CBS / CNT Stage 1",
        f"FIXED SCALE",
        f"",
        f"Dataset : {data.get('dataset', '—')}",
        f"Year    : {year}",
        f"t       : {t} / {N-1}",
        f"D       : {D}  carriers",
        f"Pairs   : {n_pairs}  channels",
        f"",
        f"Hs      = {hs:.6f}",
        f"Ring    = {ring}",
        f"E_metric= {e_metric:.4f}",
        f"kappa   = {kappa:.2f}",
        f"omega   = {omega:.4f} deg",
        f"d_A     = {d_a:.6f}",
        f"Helm    = {helm if helm else '---'}",
        f"Helm d  = {helm_d:+.6f}" if helm else "Helm d  = ---",
        f"",
        f"XZ [{scales['bearing_ylim'][0]:.0f},{scales['bearing_ylim'][1]:.0f}]",
        f"CLR[{scales['clr_ylim'][0]:.1f},{scales['clr_ylim'][1]:.1f}]",
        f"Hs [0, 1]",
    ]

    info_text = "\n".join(info_lines)
    ax_info.text(0.05, 0.97, info_text,
                 transform=ax_info.transAxes,
                 fontsize=8.5, fontfamily=FONT_MONO,
                 verticalalignment="top",
                 color=TEXT_COLOR,
                 bbox=dict(boxstyle="square,pad=0.3",
                           facecolor="0.95", edgecolor="0.5",
                           linewidth=1))

    # ─────────────────────────────────────────────────────────────
    # [0,1] TOP-CENTER: Pair Index Legend
    # ─────────────────────────────────────────────────────────────
    ax_legend = fig.add_subplot(gs[0, 1])
    ax_legend.set_xlim(0, 1)
    ax_legend.set_ylim(0, 1)
    ax_legend.axis("off")

    pair_labels = list(bearings.keys())
    legend_lines = []
    for idx, label in enumerate(pair_labels):
        legend_lines.append(f"{idx:2d}={label}")

    # Split into 2 columns for this panel width
    cols = 2
    rows_per_col = math.ceil(len(legend_lines) / cols)
    legend_cols = []
    for c in range(cols):
        start = c * rows_per_col
        end = min(start + rows_per_col, len(legend_lines))
        legend_cols.append(legend_lines[start:end])

    # Pad columns to equal length
    max_rows = max(len(col) for col in legend_cols)
    for col in legend_cols:
        while len(col) < max_rows:
            col.append("")

    # Build legend text
    legend_text_lines = ["PAIR INDEX:"]
    for r in range(max_rows):
        row_parts = []
        for c in range(cols):
            row_parts.append(f"{legend_cols[c][r]:<24s}")
        legend_text_lines.append("".join(row_parts))

    legend_text = "\n".join(legend_text_lines)
    ax_legend.text(0.05, 0.97, legend_text,
                   transform=ax_legend.transAxes,
                   fontsize=7, fontfamily=FONT_MONO,
                   verticalalignment="top",
                   color="0.2",
                   bbox=dict(boxstyle="square,pad=0.3",
                             facecolor="0.97", edgecolor="0.6",
                             linewidth=0.8))

    # ─────────────────────────────────────────────────────────────
    # [0,2] TOP-RIGHT: XZ Face — Bar graph of ALL bearings (deg)
    # ─────────────────────────────────────────────────────────────
    ax_xz = fig.add_subplot(gs[0, 2])

    pair_labels = list(bearings.keys())
    pair_values = [bearings[k] for k in pair_labels]
    pair_indices = list(range(len(pair_labels)))

    ax_xz.bar(pair_indices, pair_values, color=BAR_COLOR,
              edgecolor="black", linewidth=0.5, width=0.8)

    ax_xz.set_title("XZ : Bearings (deg)  [-180, +180]",
                     fontsize=9, fontfamily=FONT_MONO, fontweight="bold",
                     color=TEXT_COLOR)
    ax_xz.set_xlabel("Pair index", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_xz.set_ylabel("theta (deg)", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_xz.axhline(0, color="black", linewidth=0.8)
    ax_xz.set_xlim(-0.6, len(pair_indices) - 0.4)
    ax_xz.set_ylim(scales["bearing_ylim"])  # FIXED
    ax_xz.grid(axis="y", color=GRID_COLOR, linewidth=0.5)
    ax_xz.tick_params(labelsize=6)

    if n_pairs <= 28:
        ax_xz.set_xticks(pair_indices)
        ax_xz.set_xticklabels(pair_indices, fontsize=5.5,
                               fontfamily=FONT_MONO)

    # ─────────────────────────────────────────────────────────────
    # [1,0:2] BOTTOM-LEFT: XY Face — Scatter (plan view)
    # Spans Info + Legend columns for maximum area
    # ─────────────────────────────────────────────────────────────
    ax_xy = fig.add_subplot(gs[1, 0:2])

    scatter_x = []
    scatter_y = []
    scatter_labels = []

    pair_idx = 0
    for i in range(D):
        for j in range(i + 1, D):
            scatter_x.append(clr[i])
            scatter_y.append(clr[j])
            scatter_labels.append(f"{pair_idx}")
            pair_idx += 1

    ax_xy.scatter(scatter_x, scatter_y, s=30, c=SCATTER_COLOR,
                  marker="o", zorder=3, edgecolors="none")

    ax_xy.axhline(0, color="0.5", linewidth=0.5, linestyle="--")
    ax_xy.axvline(0, color="0.5", linewidth=0.5, linestyle="--")

    for k in range(len(scatter_x)):
        ax_xy.annotate(scatter_labels[k],
                        (scatter_x[k], scatter_y[k]),
                        fontsize=5.5, fontfamily=FONT_MONO,
                        textcoords="offset points",
                        xytext=(3, 3), color="0.3")

    clr_lo = scales["clr_ylim"][0]
    clr_hi = scales["clr_ylim"][1]
    ax_xy.set_title(f"XY : Plan View  [{clr_lo:.1f}, {clr_hi:.1f}]",
                     fontsize=9, fontfamily=FONT_MONO,
                     fontweight="bold", color=TEXT_COLOR)
    ax_xy.set_xlabel("h_i (CLR carrier i)", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_xy.set_ylabel("h_j (CLR carrier j)", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_xy.set_xlim(scales["scatter_xlim"])  # FIXED
    ax_xy.set_ylim(scales["scatter_ylim"])  # FIXED
    ax_xy.grid(True, color=GRID_COLOR, linewidth=0.5)
    ax_xy.tick_params(labelsize=7)

    # ─────────────────────────────────────────────────────────────
    # [1,2] BOTTOM-RIGHT: YZ Face — Bar graph of CLR per carrier
    # ─────────────────────────────────────────────────────────────
    ax_yz = fig.add_subplot(gs[1, 2])

    carrier_indices = list(range(D))
    short_names = [c[:8] for c in carriers]

    ax_yz.bar(carrier_indices, clr, color=BAR_COLOR,
              edgecolor="black", linewidth=0.5, width=0.7)

    ax_yz.set_title(f"YZ : CLR  [{clr_lo:.1f}, {clr_hi:.1f}]",
                     fontsize=9, fontfamily=FONT_MONO,
                     fontweight="bold", color=TEXT_COLOR)
    ax_yz.set_xlabel("Carrier", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_yz.set_ylabel("h_j (CLR)", fontsize=7,
                      fontfamily=FONT_MONO, color=TEXT_COLOR)
    ax_yz.axhline(0, color="black", linewidth=0.8)
    ax_yz.set_ylim(scales["clr_ylim"])  # FIXED
    ax_yz.set_xticks(carrier_indices)
    ax_yz.set_xticklabels(short_names, fontsize=6.5, rotation=45,
                           ha="right", fontfamily=FONT_MONO)
    ax_yz.grid(axis="y", color=GRID_COLOR, linewidth=0.5)
    ax_yz.tick_params(labelsize=6)

    return fig


# ══════════════════════════════════════════════════════════════════
# OUTPUT — PDF (multi-page) or PNG (one file per year)
# ══════════════════════════════════════════════════════════════════

def generate_pdf(data, output_path):
    """Generate multi-page PDF with one plate per time interval."""
    N = data["N"]

    # Pre-scan: compute fixed scales for all plates
    scales = compute_fixed_scales(data)
    print(f"  Fixed scales computed:")
    print(f"    Bearings : [{scales['bearing_ylim'][0]:.0f}, {scales['bearing_ylim'][1]:.0f}] deg (exact)")
    print(f"    CLR      : [{scales['clr_ylim'][0]:.2f}, {scales['clr_ylim'][1]:.2f}] (data-adaptive)")
    print(f"    CLR raw  : [{scales['clr_min_raw']:.4f}, {scales['clr_max_raw']:.4f}]")
    print()

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI,
                     facecolor=BG_COLOR)

    with PdfPages(output_path) as pdf:
        for t in range(N):
            render_plate(data, t, scales, fig)
            pdf.savefig(fig, facecolor=BG_COLOR)
            year = data["records"][t]["year"]
            print(f"  Plate t={t:3d}  Year={year}  -> page {t+1}")

    plt.close(fig)
    print(f"\nPDF written: {output_path}")
    print(f"Pages: {N}")


def generate_pngs(data, output_dir):
    """Generate one PNG per time interval."""
    os.makedirs(output_dir, exist_ok=True)
    N = data["N"]

    # Pre-scan: compute fixed scales for all plates
    scales = compute_fixed_scales(data)
    print(f"  Fixed scales computed:")
    print(f"    Bearings : [{scales['bearing_ylim'][0]:.0f}, {scales['bearing_ylim'][1]:.0f}] deg (exact)")
    print(f"    CLR      : [{scales['clr_ylim'][0]:.2f}, {scales['clr_ylim'][1]:.2f}] (data-adaptive)")
    print()

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI,
                     facecolor=BG_COLOR)

    for t in range(N):
        render_plate(data, t, scales, fig)
        year = data["records"][t]["year"]
        path = os.path.join(output_dir, f"plate_t{t:03d}_{year}.png")
        fig.savefig(path, facecolor=BG_COLOR, dpi=DPI)
        print(f"  Plate t={t:3d}  Year={year}  -> {path}")

    plt.close(fig)
    print(f"\nPNGs written to: {output_dir}")
    print(f"Files: {N}")


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python stage1_plates_raw.py <input.json> [output.pdf]")
        print("  python stage1_plates_raw.py <input.json> --png <output_dir>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)

    data = load_json(json_path)
    print(f"Loaded: {json_path}")
    print(f"  Instrument : {data['instrument']}")
    print(f"  Engine     : {data['engine']}")
    print(f"  D={data['D']}  N={data['N']}")
    print(f"  Carriers   : {', '.join(data['carriers'])}")
    print()

    # Determine output mode
    if len(sys.argv) >= 3 and sys.argv[2] == "--png":
        out_dir = sys.argv[3] if len(sys.argv) > 3 else "plates_png"
        generate_pngs(data, out_dir)
    else:
        out_path = sys.argv[2] if len(sys.argv) > 2 else "stage1_plates.pdf"
        generate_pdf(data, out_path)


if __name__ == "__main__":
    main()
