#!/usr/bin/env python3
"""
HCI Stage 1 — ILR-Helmert Orthogonal Triplet Plate Generator (matplotlib)
==========================================================================

Companion view to stage1_plates_raw.py (the Section Plate / bar+XY reading).
Together they form the **Dual-View Stage 1 Output**:

  View A — Section Plate (CoDa-Standard reading)
    XY = scatter (h_i, h_j) for each carrier pair — plan view
    XZ = bar of pairwise bearings θ_ij — magnitude index
    YZ = bar of CLR coordinate per carrier — magnitude index
    Generator: stage1_plates_raw.py

  View B — ILR-Helmert Orthogonal Triplet Plate (Orthonormal reading)   ← THIS FILE
    Panel 1 = scatter (ilr_1, ilr_2) — first two Helmert ILR axes
    Panel 2 = scatter (ilr_1, ilr_3) — first and third
    Panel 3 = scatter (ilr_2, ilr_3) — second and third
    Trajectory drawn as connected line; ○ = start, ◾ = end
    Cine pages highlight current year with a red ×.

The two views answer different questions:
  · Section Plate answers "what are the magnitudes at this timestep?"
  · Triplet Plate answers "where is the composition in ILR space and where has it moved?"

The Triplet Plate is the Order-1 reference reading per Output Doctrine v1.0.
Each panel has commensurate axes (Euclidean ILR), so all three are genuinely
orthogonal 2D projections of the same point cloud in ℝ³.

Layout (one summary page + N cine pages, one per year):
  ┌──────────────┬──────────────┬──────────────┐
  │  ilr_1 × 2   │  ilr_1 × 3   │  ilr_2 × 3   │   ← three orthogonal panels
  ├──────────────┴──────────────┼──────────────┤
  │  Helmert basis loadings     │  Trajectory  │   ← axis-meaning + metadata
  │  (which carriers contrast)  │  info block  │
  └─────────────────────────────┴──────────────┘

Output: multi-page PDF (1 summary + 1 per year).
Monochrome. Line graphics. Scales to any D ≥ 3.

Usage:
  python ilr_triplet_plate.py stage1_output.json [output.pdf]

Conforms to HUF Publication Standards (HUF-STD-001).
Conforms to HUF Tensor Train I/O Standard (HUF-STD-002).
Implements Order-1 reading per Output Doctrine v1.0.

The instrument reads. The expert decides. The hashes carry the receipts.
The vocabulary holds the line.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# ── Configuration ─────────────────────────────────────────────────
FIG_W = 16
FIG_H = 10
DPI = 150
plt.rcParams['font.family'] = 'monospace'


# ══════════════════════════════════════════════════════════════════
# Helmert basis (D-1) × D for the standard ILR-Helmert pivot
# ══════════════════════════════════════════════════════════════════

def helmert_basis(D: int) -> np.ndarray:
    """Build the (D-1) × D Helmert orthonormal basis.

    Row k (0..D-2) of H projects D-dim CLR onto the k-th ILR axis.
    H[k, j] = +c_k for j <= k, -(k+1)·c_k for j = k+1, 0 otherwise,
    where c_k = sqrt(1 / ((k+1)·(k+2))).
    """
    H = np.zeros((D - 1, D))
    for k in range(D - 1):
        c = math.sqrt(1.0 / ((k + 1) * (k + 2)))
        for j in range(k + 1):
            H[k, j] = c
        H[k, k + 1] = -(k + 1) * c
    return H


def clr_to_ilr(clr_array: np.ndarray, H: np.ndarray) -> np.ndarray:
    """Project CLR coordinates to ILR-Helmert space.

    clr_array: shape (N, D) — N compositions in CLR coordinates
    H:         shape (D-1, D) — Helmert basis
    returns:   shape (N, D-1) — N compositions in ILR coordinates
    """
    clr = np.asarray(clr_array, dtype=float)
    return clr @ H.T


# ══════════════════════════════════════════════════════════════════
# Rendering — summary page + cine pages
# ══════════════════════════════════════════════════════════════════

def _render_summary_page(pdf, ilrs, years, carriers, H, country_code, country_name):
    """One overview page showing all three orthogonal panels with full trajectory."""
    D = len(carriers)
    rng = max(float(abs(ilrs[:, :3]).max()), 0.5) * 1.15

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.suptitle(
        f"ILR-Helmert Orthogonal Triplet — {country_code} {country_name}  ·  Stage 1 Order-1 plate",
        fontsize=18, fontweight='bold', y=0.96,
    )
    fig.text(0.5, 0.93,
             f"Three orthogonal scatter projections of CLR onto the first three Helmert ILR axes"
             f"  ·  N={len(years)} years  ·  D={D} carriers",
             ha='center', fontsize=11, style='italic', color='#555')

    gs = fig.add_gridspec(2, 3, height_ratios=[2.5, 1.2], hspace=0.4, wspace=0.3)

    pairs = [(0, 1, "ilr_1 × ilr_2"),
             (0, 2, "ilr_1 × ilr_3"),
             (1, 2, "ilr_2 × ilr_3")]
    for col, (i, j, label) in enumerate(pairs):
        ax = fig.add_subplot(gs[0, col])
        ax.plot(ilrs[:, i], ilrs[:, j], color='gray', lw=0.6, alpha=0.5, zorder=1)
        ax.scatter(ilrs[0, i], ilrs[0, j], s=120, marker='o', facecolors='white',
                   edgecolors='black', linewidths=1.5, zorder=3, label='start')
        ax.scatter(ilrs[-1, i], ilrs[-1, j], s=120, marker='s', color='black',
                   zorder=3, label='end')
        ax.scatter(ilrs[1:-1, i], ilrs[1:-1, j], s=30, color='black', alpha=0.7, zorder=2)
        ax.axhline(0, color='gray', lw=0.4)
        ax.axvline(0, color='gray', lw=0.4)
        ax.set_xlim(-rng, rng)
        ax.set_ylim(-rng, rng)
        ax.set_aspect('equal')
        ax.set_xlabel(f"ilr_{i+1}")
        ax.set_ylabel(f"ilr_{j+1}")
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)
        if col == 0:
            ax.legend(loc='upper right', fontsize=8)

    # Helmert basis loadings — bottom-left
    ax = fig.add_subplot(gs[1, 0:2])
    ax.axis('off')
    ax.text(0.0, 1.0, "Helmert basis loadings (which carriers each ILR axis contrasts):",
            fontsize=11, fontweight='bold', transform=ax.transAxes, va='top')
    rows = []
    for k in range(min(3, D - 1)):
        pos = [c for j, c in enumerate(carriers) if H[k, j] > 0.001]
        neg = [c for j, c in enumerate(carriers) if H[k, j] < -0.001]
        rows.append(f"  ilr_{k+1}:  ({' + '.join(pos)})  vs  {' '.join(neg)}")
    ax.text(0.0, 0.80, "\n".join(rows), fontsize=10, family='monospace',
            transform=ax.transAxes, va='top')

    # Trajectory info — bottom-right
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    info = f"""Trajectory:
  start year:  {years[0]}
  end year:    {years[-1]}
  N readings:  {len(years)}

Display:
  fixed scale ±{rng:.2f} ILR
  Order 1 (first principles)
  per Output Doctrine v1.0

Symbology:
  ○  start  ·  ◾  end
  ·  intermediate years"""
    ax.text(0.0, 1.0, info, fontsize=10, family='monospace',
            transform=ax.transAxes, va='top')

    pdf.savefig(fig)
    plt.close(fig)


def _render_cine_page(pdf, ilrs, years, t, country_code, country_name):
    """One cine page per timestep — past trajectory drawn solid, current year highlighted."""
    rng = max(float(abs(ilrs[:, :3]).max()), 0.5) * 1.15

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.suptitle(f"ILR Triplet — {country_code} {country_name}  ·  year {years[t]}"
                 f"  ({t+1}/{len(years)})",
                 fontsize=16, fontweight='bold')
    gs = fig.add_gridspec(1, 3, wspace=0.3)

    pairs = [(0, 1, "ilr_1 × ilr_2"),
             (0, 2, "ilr_1 × ilr_3"),
             (1, 2, "ilr_2 × ilr_3")]
    for col, (i, j, label) in enumerate(pairs):
        ax = fig.add_subplot(gs[0, col])
        # full trajectory in light gray
        ax.plot(ilrs[:, i], ilrs[:, j], color='gray', lw=0.5, alpha=0.4)
        ax.scatter(ilrs[:, i], ilrs[:, j], s=20, color='gray', alpha=0.4)
        # past trajectory up to current t in dark
        ax.plot(ilrs[:t+1, i], ilrs[:t+1, j], color='black', lw=1.2, alpha=0.7)
        # current year marker
        ax.scatter(ilrs[t, i], ilrs[t, j], s=200, color='red', marker='X',
                   zorder=5, edgecolors='black', linewidths=1.5)
        ax.axhline(0, color='gray', lw=0.4)
        ax.axvline(0, color='gray', lw=0.4)
        ax.set_xlim(-rng, rng)
        ax.set_ylim(-rng, rng)
        ax.set_aspect('equal')
        ax.set_xlabel(f"ilr_{i+1}")
        ax.set_ylabel(f"ilr_{j+1}")
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)

    fig.text(0.5, 0.02,
             f"X = current year ({years[t]})  ·  black = past trajectory  ·"
             f"  gray = future  ·  ilr range ±{rng:.2f}",
             ha='center', fontsize=10, style='italic', color='#555')
    pdf.savefig(fig)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════
# Driver
# ══════════════════════════════════════════════════════════════════

def render_triplet_plates(stage1_json_path: str | Path, out_pdf_path: str | Path) -> int:
    """Generate the ILR-Helmert Orthogonal Triplet Plate PDF.

    Args:
        stage1_json_path: Path to stage1_output.json (from stage1_engine.py).
        out_pdf_path: Output PDF path.

    Returns:
        Number of pages written (1 summary + N cine pages).
    """
    data = json.loads(Path(stage1_json_path).read_text(encoding='utf-8'))
    records = data['records']
    carriers = data['carriers']
    D = data['D']
    years = data['years']

    H = helmert_basis(D)
    clr_arr = np.array([r['clr'] for r in records])
    ilrs = clr_to_ilr(clr_arr, H)

    country_code = data.get('dataset', '???')[:3].upper()
    country_name = data.get('dataset', country_code).replace('ember_', '').replace('_', ' ')

    with PdfPages(str(out_pdf_path)) as pdf:
        _render_summary_page(pdf, ilrs, years, carriers, H, country_code, country_name)
        for t in range(len(years)):
            _render_cine_page(pdf, ilrs, years, t, country_code, country_name)

    return 1 + len(years)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ilr_triplet_plate.py stage1_output.json [output.pdf]",
              file=sys.stderr)
        sys.exit(1)
    in_json = sys.argv[1]
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else "ilr_triplet_plate.pdf"
    n_pages = render_triplet_plates(in_json, out_pdf)
    print(f"  ILR Triplet plate written: {out_pdf}  ({n_pages} pages — 1 summary + {n_pages-1} cine)")


if __name__ == "__main__":
    main()
