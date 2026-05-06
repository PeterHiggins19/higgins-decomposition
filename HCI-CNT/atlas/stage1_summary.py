#!/usr/bin/env python3
"""
HCI-Atlas Stage 1 — closing summary plate.

A single PDF page placed at the end of every Stage 1 atlas. Summarises
the entire trajectory using ONLY Order-1 quantities (per-timestep
first principles + trajectory statistical aggregates), no Order-2+
derivative content.

What's on the page:
  * Title bar:   dataset id, T, D, engine, schema, content SHA
  * Top-left:    Hs trajectory (line plot, 0..1 axis fixed)
  * Top-right:   Aitchison-norm trajectory (centroid distance in HLR)
  * Mid-left:    ILR axes 1, 2, 3 trajectories (overlaid)
  * Mid-right:   closure invariant (max|Σ-1| across all timesteps)
  * Bottom:      per-carrier min/mean/max/std table
  * Footer:      source SHA, content SHA, run id, page n/N

This page closes the Stage 1 first-order output. Anything beyond it
requires Order 2 or higher and lives on Stage 2/3/4 plates per the
output doctrine.
"""
from __future__ import annotations
import math
import numpy as np
import matplotlib.pyplot as plt


PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


def _carrier_palette(n: int) -> list:
    base = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    return [base[i % len(base)] for i in range(n)]


def hs_per_timestep(j: dict) -> list:
    """Higgins scale Hs = H(x) / ln(D) per timestep — Order 1A."""
    timesteps = j["tensor"]["timesteps"]
    D = j["input"]["n_carriers"]
    out = []
    lnD = math.log(D)
    for ts in timesteps:
        cs = ts.get("coda_standard", {}) or {}
        comp = cs.get("composition") or ts.get("raw_values") or []
        if not comp:
            out.append(float("nan")); continue
        H = -sum(v * math.log(max(v, 1e-300)) for v in comp)
        out.append(H / lnD if lnD > 0 else 0.0)
    return out


def aitchison_norm_per_timestep(j: dict) -> list:
    """‖clr(x)‖₂ per timestep — distance from centroid, in HLR. Order 1A."""
    out = []
    for ts in j["tensor"]["timesteps"]:
        cs = ts.get("coda_standard", {}) or {}
        clr = cs.get("clr") or [0.0]
        out.append(math.sqrt(sum(c*c for c in clr)))
    return out


def closure_max_drift(j: dict) -> float:
    """max|Σ closed - 1| across all timesteps — Order 1A invariant."""
    drift = 0.0
    for ts in j["tensor"]["timesteps"]:
        cs = ts.get("coda_standard", {}) or {}
        comp = cs.get("composition") or ts.get("raw_values") or []
        if comp:
            drift = max(drift, abs(sum(comp) - 1.0))
    return drift


def per_carrier_stats(j: dict) -> list:
    """For each carrier, return (min, mean, max, std) over the trajectory."""
    timesteps = j["tensor"]["timesteps"]
    D = j["input"]["n_carriers"]
    closed_matrix = []
    for ts in timesteps:
        cs = ts.get("coda_standard", {}) or {}
        comp = cs.get("composition") or ts.get("raw_values") or []
        if comp and len(comp) == D:
            closed_matrix.append(comp)
    if not closed_matrix:
        return [(0, 0, 0, 0)]*D
    arr = np.asarray(closed_matrix)
    return [(float(arr[:, c].min()),
             float(arr[:, c].mean()),
             float(arr[:, c].max()),
             float(arr[:, c].std()))
            for c in range(D)]


def render_summary_plate(pdf, j: dict, dataset_id: str,
                          run_id: str | None,
                          page_num: int, total_pages: int,
                          ilr: np.ndarray,
                          aliases: dict | None = None):
    aliases = aliases or {}
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)

    md = j["metadata"]
    inp = j["input"]
    di = j["diagnostics"]
    carriers = inp["carriers"]
    labels = inp["labels"]
    T = inp["n_records"]
    D = inp["n_carriers"]
    palette = _carrier_palette(D)

    # ── Title ─────────────────────────────────────────────────
    fig.text(0.5, 0.965,
             f"STAGE 1 SUMMARY  |  {dataset_id}  |  D={D}  T={T}  |  "
             f"Order 1 (first-principles closure)",
             ha="center", fontsize=11, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.943,
             f"Engine {md['engine_version']}  |  Schema {md['schema_version']}  |  "
             f"Generated {md.get('generated', '?')[:19]}",
             ha="center", fontsize=9, color="#444")

    # ── Hs trajectory (top-left) ──────────────────────────────
    hs = hs_per_timestep(j)
    ax_hs = fig.add_axes([0.06, 0.55, 0.42, 0.32])
    x = list(range(T))
    ax_hs.plot(x, hs, "o-", color="#1f4e79", lw=1.2, markersize=4)
    ax_hs.set_xlim(-0.5, T - 0.5)
    ax_hs.set_ylim(0, 1.05)
    ax_hs.set_xlabel("timestep index", fontsize=8)
    ax_hs.set_ylabel("Hs (Higgins scale)", fontsize=8)
    ax_hs.set_title("Hs trajectory — single-composition entropy / ln(D)",
                    fontsize=10, color="#1f4e79", loc="left")
    ax_hs.grid(True, alpha=0.3)
    ax_hs.tick_params(labelsize=7)
    if T <= 30:
        ax_hs.set_xticks(x)
        if T <= 12:
            ax_hs.set_xticklabels(labels, rotation=45, ha="right", fontsize=6)
    ax_hs.text(0.02, 0.98,
               f"Hs:  min {min(hs):.4f}  mean {sum(hs)/T:.4f}  max {max(hs):.4f}",
               transform=ax_hs.transAxes, fontsize=7, family="monospace",
               va="top", color="#222")

    # ── Aitchison-norm trajectory (top-right) ─────────────────
    norms = aitchison_norm_per_timestep(j)
    ax_a = fig.add_axes([0.55, 0.55, 0.42, 0.32])
    ax_a.plot(x, norms, "s-", color="#d62728", lw=1.2, markersize=4)
    ax_a.set_xlim(-0.5, T - 0.5)
    ax_a.set_xlabel("timestep index", fontsize=8)
    ax_a.set_ylabel("‖clr(x)‖₂  (HLR)", fontsize=8)
    ax_a.set_title("Aitchison norm — distance from centroid (HLR)",
                   fontsize=10, color="#1f4e79", loc="left")
    ax_a.grid(True, alpha=0.3)
    ax_a.tick_params(labelsize=7)
    if T <= 30:
        ax_a.set_xticks(x)
    ax_a.text(0.02, 0.98,
              f"Norm:  min {min(norms):.4f}  mean {sum(norms)/T:.4f}  max {max(norms):.4f} HLR",
              transform=ax_a.transAxes, fontsize=7, family="monospace",
              va="top", color="#222")

    # ── ILR-axis trajectories (mid-left) ─────────────────────
    ax_i = fig.add_axes([0.06, 0.18, 0.42, 0.30])
    n_axes_show = min(3, ilr.shape[1])
    colors = ["#2ca02c", "#1f77b4", "#ff7f0e"]
    for k in range(n_axes_show):
        ax_i.plot(x, ilr[:, k], "-o", color=colors[k], lw=1.0, markersize=3,
                  label=f"ILR({k+1})")
    ax_i.axhline(0, color="#888", lw=0.6, ls="--")
    ax_i.set_xlim(-0.5, T - 0.5)
    ax_i.set_xlabel("timestep index", fontsize=8)
    ax_i.set_ylabel("ILR coordinate (HLR)", fontsize=8)
    ax_i.set_title("ILR axes 1–3 trajectories (Helmert basis)",
                   fontsize=10, color="#1f4e79", loc="left")
    ax_i.grid(True, alpha=0.3)
    ax_i.legend(loc="upper right", fontsize=7)
    ax_i.tick_params(labelsize=7)

    # ── Closure invariant summary (mid-right) ────────────────
    ax_inv = fig.add_axes([0.55, 0.18, 0.42, 0.30])
    ax_inv.axis("off")
    ax_inv.text(0.0, 0.97, "Order-1 invariants (whole trajectory)",
                fontsize=10, fontweight="bold", color="#1f4e79")
    drift = closure_max_drift(j)
    drift_ok = drift < 1e-10
    rows = [
        f"closure invariant     :  max |Σ closed − 1| = {drift:.2e}",
        f"closure status        :  {'OK ✓' if drift_ok else 'FAIL'}",
        "",
        f"Hs range              :  [{min(hs):.4f}, {max(hs):.4f}]",
        f"Aitchison norm range  :  [{min(norms):.4f}, {max(norms):.4f}] HLR",
        f"ILR(1) range          :  [{ilr[:,0].min():+.4f}, {ilr[:,0].max():+.4f}]",
        f"ILR(2) range          :  [{ilr[:,1].min():+.4f}, {ilr[:,1].max():+.4f}]"
        if ilr.shape[1] > 1 else "",
        f"ILR(3) range          :  [{ilr[:,2].min():+.4f}, {ilr[:,2].max():+.4f}]"
        if ilr.shape[1] > 2 else "",
        "",
        f"Source file           :  {inp.get('source_file', '?')}",
        f"Source SHA-256        :  {inp.get('source_file_sha256', '?')[:32]}...",
        f"Closed-data SHA-256   :  {inp.get('closed_data_sha256', '?')[:32]}...",
        f"Content SHA-256       :  {di.get('content_sha256', '?')[:32]}...",
        f"Ordering              :  temporal={inp['ordering']['is_temporal']}, "
        f"method={inp['ordering']['ordering_method']}",
        f"Zero replacement δ    :  {inp.get('zero_replacement', {}).get('delta', '?')}",
    ]
    for i, line in enumerate(rows):
        ax_inv.text(0.0, 0.91 - i * 0.05, line, fontsize=8,
                    family="monospace", color="#222")

    # ── Per-carrier stats table (bottom) ─────────────────────
    ax_t = fig.add_axes([0.06, 0.04, 0.91, 0.10])
    ax_t.axis("off"); ax_t.set_xlim(0, 1); ax_t.set_ylim(0, 1)
    stats = per_carrier_stats(j)
    ax_t.text(0.0, 0.95, "Per-carrier closed-value summary (Order 1B aggregates)",
              fontsize=9, fontweight="bold", color="#1f4e79")
    ax_t.text(0.0, 0.78,
              f"{'#':>3}  {'carrier':<16}{'min':>10}{'mean':>10}{'max':>10}"
              f"{'std':>10}",
              fontsize=7, family="monospace", color="#444",
              fontweight="bold")
    n_show = min(D, 12)
    col_x = 0.0
    for ci in range(n_show):
        cname = aliases.get(carriers[ci], carriers[ci])[:14]
        mn, mu, mx, sd = stats[ci]
        # Two-column layout if D > 6
        if D > 6 and ci >= 6:
            col_x = 0.50
            row_i = ci - 6
        else:
            col_x = 0.0
            row_i = ci
        y = 0.62 - row_i * 0.10
        ax_t.add_patch(plt.Rectangle((col_x, y - 0.02), 0.018, 0.06,
                                     facecolor=palette[ci],
                                     transform=ax_t.transAxes,
                                     clip_on=False))
        ax_t.text(col_x + 0.025, y, f"{ci:>2}  {cname:<14}",
                  fontsize=7, family="monospace", color="#222")
        ax_t.text(col_x + 0.20, y, f"{mn:.4f}",
                  fontsize=7, family="monospace", color="#222")
        ax_t.text(col_x + 0.28, y, f"{mu:.4f}",
                  fontsize=7, family="monospace", color="#222")
        ax_t.text(col_x + 0.36, y, f"{mx:.4f}",
                  fontsize=7, family="monospace", color="#222")
        ax_t.text(col_x + 0.44, y, f"{sd:.4f}",
                  fontsize=7, family="monospace", color="#222")

    # ── Footer ─────────────────────────────────────────────────
    fig.text(0.5, 0.01,
             f"source SHA: {inp.get('source_file_sha256', '?')[:12]}...  |  "
             f"content SHA: {di.get('content_sha256', '?')[:12]}...  |  "
             f"run: {run_id or 'unsaved'}  |  "
             f"page {page_num}/{total_pages}  |  "
             f"STAGE 1 CLOSED",
             ha="center", fontsize=7, family="monospace", color="#666")

    pdf.savefig(fig)
    plt.close(fig)
