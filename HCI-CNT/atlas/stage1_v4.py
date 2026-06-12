#!/usr/bin/env python3
"""
HCI-Atlas — Stage 1 v4: orthonormal first-order plate with magnitude factor.

Unit basis is HLR (Higgins Log-Ratio = nepers).  The display is FIXED in
HLR units, but if the natural data range is too small (or too large)
for clear pattern separation, an automatic magnitude factor F (a power
of 10 in {... 0.01, 0.1, 1, 10, 100, ...}) is applied so the displayed
axes span a clean readable range, typically [-5, +5] HLR after scaling.

The factor is declared on the title bar and on every axis label so
the reader is never in doubt: e.g. "ILR(1) × 100  [HLR scaled]".

The plate is purely first-order:
  * 3 orthogonal panels of the ILR-Helmert projection (axes 1×2, 1×3, 2×3)
  * Stacked strip of the closed composition
  * Carrier table (name | closed | CLR)
  * Helmert axis loadings (which carriers each ILR axis contrasts)
NO bearings, no ω, no Hs, no helmsman, no ring.

The engine never fabricates data: every value displayed traces back to
the JSON's tensor.timesteps[t].coda_standard.{composition, clr} via a
deterministic transform.
"""
from __future__ import annotations
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


# --------------------------------------------------------------
def pick_magnitude_factor(max_abs: float, target_max: float = 5.0,
                          comfort_lo: float = 0.5,
                          comfort_hi: float = 50.0) -> float:
    """Pick a clean power-of-10 factor F.

    If max_abs is already in the comfortable range [comfort_lo, comfort_hi]
    HLR, return F = 1 (no scaling — display in raw HLR units). Otherwise:
        max_abs < comfort_lo  →  scale up   (F = 10^k, k > 0)
        max_abs > comfort_hi  →  scale down (F = 10^k, k < 0)
    Smallest scaling that brings F * max_abs into [comfort_lo, comfort_hi].
    """
    if max_abs <= 0 or not math.isfinite(max_abs):
        return 1.0
    if comfort_lo <= max_abs <= comfort_hi:
        return 1.0
    log = math.log10(max_abs)
    if max_abs < comfort_lo:
        # ceil(log10(comfort_lo) - log) is the smallest positive k with F·max ≥ comfort_lo
        k = math.ceil(math.log10(comfort_lo) - log)
    else:
        # floor(log10(comfort_hi) - log) is the largest negative k with F·max ≤ comfort_hi
        k = math.floor(math.log10(comfort_hi) - log)
    return 10.0 ** k


def fmt_factor(F: float) -> str:
    """Human-readable factor: 'x1' / 'x10' / 'x100' / 'x0.1' / 'x0.01' …"""
    if F == 1.0: return "x1"
    if F >= 1.0: return f"x{int(F)}"
    return f"x{F:g}"


def _carrier_palette(n: int) -> list:
    base = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    return [base[i % len(base)] for i in range(n)]


def compute_ilr(j: dict) -> np.ndarray:
    """Per-timestep ILR coordinates via the Helmert basis published in the JSON.

    Returns a (T, D-1) array. ILR = Helmert_basis @ CLR.
    """
    basis = np.asarray(j["tensor"]["helmert_basis"]["coefficients"])
    timesteps = j["tensor"]["timesteps"]
    T = len(timesteps)
    D = j["input"]["n_carriers"]
    ilr = np.zeros((T, D - 1))
    for t, ts in enumerate(timesteps):
        cs = ts.get("coda_standard", {}) or {}
        clr = cs.get("clr") or ts.get("clr") or [0.0]*D
        ilr[t] = basis @ np.asarray(clr)
    return ilr


def compute_window_and_factor(ilr: np.ndarray, n_axes: int = 3,
                              target_max: float = 5.0) -> tuple:
    """Across the first n_axes ILR axes, compute the data range and pick a
    clean magnitude factor that brings the displayed range to ~[-target_max,
    +target_max] HLR-scaled."""
    if ilr.size == 0:
        return ((-1, 1), 1.0)
    n = min(n_axes, ilr.shape[1])
    sub = ilr[:, :n]
    max_abs = float(np.abs(sub).max())
    F = pick_magnitude_factor(max_abs, target_max=target_max)
    scaled = sub * F
    lo = float(scaled.min())
    hi = float(scaled.max())
    margin = 0.05 * max(hi - lo, 1.0)
    return ((lo - margin, hi + margin), F)


def helmert_loadings(j: dict, axis: int) -> list:
    basis = np.asarray(j["tensor"]["helmert_basis"]["coefficients"])
    return basis[axis].tolist()


# --------------------------------------------------------------
def _draw_panel(ax, ilr_scaled, frame_idx, ax_x, ax_y, window, title, F):
    xs = ilr_scaled[:, ax_x]
    ys = ilr_scaled[:, ax_y]
    ax.plot(xs, ys, "-", color="#cccccc", lw=0.6, alpha=0.6, zorder=1)
    other_x = [xs[i] for i in range(len(xs)) if i != frame_idx]
    other_y = [ys[i] for i in range(len(ys)) if i != frame_idx]
    ax.scatter(other_x, other_y, s=10, color="#aaaaaa", alpha=0.6, zorder=2)
    ax.scatter([xs[frame_idx]], [ys[frame_idx]], s=140, color="#d62728",
               edgecolor="black", linewidth=0.9, zorder=5)
    lo, hi = window
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_aspect('equal', adjustable='box')
    ax.axhline(0, color="#555", lw=0.5, zorder=0)
    ax.axvline(0, color="#555", lw=0.5, zorder=0)
    ax.set_xlabel(f"ILR axis {ax_x+1}  ({fmt_factor(F)} HLR)", fontsize=8)
    ax.set_ylabel(f"ILR axis {ax_y+1}  ({fmt_factor(F)} HLR)", fontsize=8)
    ax.set_title(title, fontsize=10, color="#1f4e79")
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(labelsize=7)


def _draw_strip(ax, closed, carriers, palette, aliases):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    cum = 0.0
    for ci, val in enumerate(closed):
        c = palette[ci]
        ax.barh([0.5], [val], left=[cum], height=0.6, color=c,
                edgecolor="white", linewidth=1.0)
        cname = aliases.get(carriers[ci], carriers[ci])
        if val >= 0.05:
            ax.text(cum + val/2, 0.5, f"{cname[:10]}\n{val*100:.1f}%",
                    ha="center", va="center", fontsize=7,
                    color="white", fontweight="bold")
        cum += val
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=7)
    ax.set_yticks([])
    ax.set_title("Closed composition  (closure invariant)", fontsize=9,
                 color="#1f4e79", loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)


def _format_loadings(loads, carriers, aliases, n_show=3):
    items = sorted([(carriers[i], loads[i]) for i in range(len(carriers))],
                   key=lambda x: -abs(x[1]))
    parts = []
    for c, w in items[:n_show]:
        disp = aliases.get(c, c)[:9]
        parts.append(f"{disp:>9}{w:+.3f}")
    return "  ".join(parts)


def render_plate(pdf, j, dataset_id, run_id, page_num, total_pages,
                  frame_idx, ilr_raw, window, F, aliases):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)

    inp = j["input"]
    md  = j["metadata"]
    di  = j["diagnostics"]
    carriers = inp["carriers"]
    labels   = inp["labels"]
    T        = inp["n_records"]
    D        = inp["n_carriers"]
    palette  = _carrier_palette(D)

    label = labels[frame_idx] if frame_idx < len(labels) else f"t={frame_idx}"

    timestep = j["tensor"]["timesteps"][frame_idx]
    cs = timestep.get("coda_standard", {}) or {}
    closed = cs.get("composition") or timestep.get("raw_values") or []
    if not closed or len(closed) != D:
        closed = [1.0/D]*D
    clr = cs.get("clr") or [0.0]*D

    ilr_scaled = ilr_raw * F

    # Title
    fig.text(0.5, 0.965,
             f"STAGE 1 v4  |  t={frame_idx}  |  {label}  |  D={D}  T={T}  |  "
             f"level 1 first-principles",
             ha="center", fontsize=11, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.943,
             f"{dataset_id}  |  ILR via Helmert basis (orthonormal, HLR units)  |  "
             f"display factor {fmt_factor(F)}  |  Engine {md['engine_version']}",
             ha="center", fontsize=9, color="#444")

    # Panels
    ax_xy = fig.add_axes([0.04, 0.51, 0.30, 0.388])
    _draw_panel(ax_xy, ilr_scaled, frame_idx, 0, 1, window,
                "XY : ILR(1) × ILR(2)", F)

    ax_xz = fig.add_axes([0.36, 0.51, 0.30, 0.388])
    _draw_panel(ax_xz, ilr_scaled, frame_idx, 0, 2, window,
                "XZ : ILR(1) × ILR(3)", F)

    ax_yz = fig.add_axes([0.04, 0.06, 0.30, 0.388])
    _draw_panel(ax_yz, ilr_scaled, frame_idx, 1, 2, window,
                "YZ : ILR(2) × ILR(3)", F)

    # Carrier table + Helmert loadings
    ax_tbl = fig.add_axes([0.68, 0.06, 0.30, 0.83])
    ax_tbl.axis("off"); ax_tbl.set_xlim(0, 1); ax_tbl.set_ylim(0, 1)
    ax_tbl.text(0.0, 0.97, "Closed composition (first principles)",
                fontsize=10, fontweight="bold", color="#1f4e79")
    ax_tbl.text(0.0, 0.92,
                f"{'carrier':<14}{'closed':>11}{'CLR':>10}",
                fontsize=8, family="monospace", color="#444",
                fontweight="bold")
    for ci, cname in enumerate(carriers):
        y = 0.88 - ci * 0.045
        if y < 0.32:
            ax_tbl.text(0.0, y, f"... + {len(carriers)-ci} more",
                        fontsize=7, color="#888", style="italic"); break
        disp = aliases.get(cname, cname)[:14]
        ax_tbl.add_patch(plt.Rectangle((0.0, y - 0.018), 0.022, 0.025,
                                       facecolor=palette[ci],
                                       transform=ax_tbl.transAxes,
                                       clip_on=False))
        ax_tbl.text(0.04, y, disp, fontsize=8, family="monospace", color="#222")
        ax_tbl.text(0.62, y, f"{closed[ci]:.4f}",
                    fontsize=8, family="monospace", color="#222", ha="right")
        ax_tbl.text(0.95, y, f"{clr[ci]:+.3f}",
                    fontsize=8, family="monospace", color="#222", ha="right")

    s = sum(closed)
    ok = abs(s - 1.0) < 1e-10
    ax_tbl.text(0.0, 0.30, f"closure: Σ = {s:.6f}  {'OK' if ok else 'FAIL'}",
                fontsize=8, family="monospace",
                color="#2ca02c" if ok else "#d62728")
    ax_tbl.text(0.0, 0.26,
                f"display factor: {fmt_factor(F)}  (raw HLR x {F:g})",
                fontsize=8, family="monospace", color="#1f4e79",
                fontweight="bold")
    ax_tbl.text(0.0, 0.22,
                "Helmert basis loadings (top 3 carriers per axis)",
                fontsize=9, fontweight="bold", color="#1f4e79")
    for ai, lbl in enumerate(("ILR(1)", "ILR(2)", "ILR(3)")):
        if ai >= D - 1: break
    for ai, lbl in enumerate(("ILR(1)", "ILR(2)", "ILR(3)")):
        if ai >= D - 1: break
        loads = helmert_loadings(j, ai)
        ax_tbl.text(0.0, 0.18 - ai * 0.045,
                    f"{lbl}: {_format_loadings(loads, carriers, aliases)}",
                    fontsize=7, family="monospace", color="#222")

    # Strip
    ax_strip = fig.add_axes([0.36, 0.16, 0.30, 0.08])
    _draw_strip(ax_strip, closed, carriers, palette, aliases)

    # Footer
    src_sha = inp.get('source_file_sha256', '?')
    csha    = di.get('content_sha256', '?')
    fig.text(0.5, 0.02,
             f"source SHA: {src_sha[:12]}...  |  "
             f"content SHA: {csha[:12]}...  |  "
             f"run: {run_id or 'unsaved'}  |  page {page_num}/{total_pages}",
             ha="center", fontsize=7, family="monospace", color="#666")

    pdf.savefig(fig)
    plt.close(fig)
