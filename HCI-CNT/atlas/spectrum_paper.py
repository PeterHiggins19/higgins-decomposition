#!/usr/bin/env python3
"""
HCI-Atlas — Spectrum Paper Plate (paper-only, all carriers + World together).

A complete static PDF version of the Hs Spectrum Analyzer dashboard. Shows
all carriers across all selected datasets on one set of common-axes panels:

    1. Complexity spectrum    — Aitchison norm trajectory per dataset
    2. Velocity spectrum      — angular velocity ω(t) per dataset
    3. Peak structural change — max ω per dataset (bar)
    4. Drift detection        — Hs slope (linear fit) per dataset (bar)
    5. Carrier composition    — per-carrier mean share over the trajectory
                                (one row per dataset, stacked bar)
    6. Year-by-year trajectory — Hs(t) panel per dataset, common y-scale

Every panel is FIXED-SCALE (common across datasets); every page carries
the doctrine order tag. This is Order 2 (cross-trajectory aggregates of
Order-1 quantities), and Order 3 only where ω is read.
"""
from __future__ import annotations
import json
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


def _carrier_palette(n: int) -> list:
    base = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    return [base[i % len(base)] for i in range(n)]


def _dataset_palette(n: int) -> list:
    """Distinct colours for stacked dataset trajectories."""
    base = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#17becf", "#bcbd22"]
    return [base[i % len(base)] for i in range(n)]


def collect(j: dict) -> dict:
    """Pull all spectrum quantities out of one CNT JSON."""
    inp = j["input"]
    timesteps = j["tensor"]["timesteps"]
    T = len(timesteps)
    D = inp["n_carriers"]
    carriers = list(inp["carriers"])
    labels = list(inp["labels"])

    # Trajectory aggregates (Order 1 readings → Order 2 trajectory series)
    hs       = np.array([ts["coda_standard"]["shannon_entropy"] for ts in timesteps])
    norm     = np.array([ts["coda_standard"]["aitchison_norm"]  for ts in timesteps])
    closed   = np.array([ts["coda_standard"]["composition"]      for ts in timesteps])

    # ω angular velocity (Order 3 read; one ω per inter-step).
    # Stage 1's metric ledger publishes per-step ω in degrees; we read it here
    # rather than recomputing from bearing_tensor pairs (the JSON's pairs
    # array carries θ only, not ω).
    ml = j["stages"]["stage1"]["higgins_extensions"]["metric_ledger"]
    omega_deg_full = np.array([m.get("omega_deg", 0.0) for m in ml])
    # First entry is t=0 (no preceding step). Drop it for inter-step view.
    omega = np.deg2rad(omega_deg_full[1:]) if omega_deg_full.size > 1 else np.array([])

    # Linear drift in Hs over time index
    if T >= 2:
        x = np.arange(T)
        slope_hs   = float(np.polyfit(x, hs,   1)[0])
        slope_norm = float(np.polyfit(x, norm, 1)[0])
    else:
        slope_hs = slope_norm = 0.0

    return dict(
        carriers=carriers, labels=labels, T=T, D=D,
        hs=hs, norm=norm, closed=closed,
        omega=omega,
        slope_hs=slope_hs, slope_norm=slope_norm,
        peak_omega=float(omega.max()) if omega.size else 0.0,
        peak_norm=float(norm.max()) if norm.size else 0.0,
    )


def render_spectrum_paper(out_pdf: str, datasets: list,
                          title: str = "EMBER Carriers + World — Spectrum (Paper)"):
    """Render one combined spectrum PDF.

    datasets : list of (dataset_id, j_dict)
    """
    n = len(datasets)
    ds_palette = _dataset_palette(n)
    ctxs = [(did, collect(j)) for did, j in datasets]

    # Common scales — FIXED across datasets ─────────────────────
    all_hs    = np.concatenate([c["hs"]     for _, c in ctxs])
    all_norm  = np.concatenate([c["norm"]   for _, c in ctxs])
    all_omega = np.concatenate([c["omega"]  for _, c in ctxs])
    hs_lo, hs_hi = float(all_hs.min()) - 0.02, float(all_hs.max()) + 0.02
    nm_lo, nm_hi = 0.0, float(all_norm.max()) * 1.05
    om_lo, om_hi = 0.0, float(all_omega.max()) * 1.05 if all_omega.size else (0.0, 1.0)

    # Years: take the union of int-castable labels
    def to_int(s):
        try:    return int(s)
        except: return None
    all_years = []
    for _, c in ctxs:
        ys = [to_int(l) for l in c["labels"]]
        if all(y is not None for y in ys):
            all_years.extend(ys)
    if all_years:
        x_lo, x_hi = min(all_years), max(all_years)
    else:
        x_lo, x_hi = 0, max(c["T"] for _, c in ctxs) - 1

    pdf = PdfPages(out_pdf)

    # ───────── Page 1: Cover + spectrum legend ─────────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.92, title, ha="center", fontsize=16,
             fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.88,
             "Order 2 — cross-trajectory aggregates of Order-1 readings   |   "
             "FIXED SCALE   |   one combined book, all datasets",
             ha="center", fontsize=9, color="#444")

    # Legend block listing all datasets
    fig.text(0.08, 0.80, "Datasets (color = trajectory):",
             fontsize=11, fontweight="bold", color="#1f4e79")
    for i, (did, c) in enumerate(ctxs):
        col = ds_palette[i]
        y = 0.76 - i * 0.04
        fig.add_artist(plt.Rectangle((0.08, y - 0.012), 0.025, 0.022,
                                     facecolor=col, edgecolor="black",
                                     linewidth=0.5,
                                     transform=fig.transFigure))
        fig.text(0.115, y, f"{did:<28}  T={c['T']}  D={c['D']}  "
                          f"carriers: {', '.join(c['carriers'][:4])}"
                          f"{' …' if c['D']>4 else ''}",
                 fontsize=9, family="monospace", color="#222")

    # Doctrine note
    fig.text(0.08, 0.30,
             "Panels in this report\n"
             "  P2. Complexity spectrum         — Aitchison norm trajectory\n"
             "  P3. Velocity spectrum           — mean |ω| per inter-step  (Order 3 read)\n"
             "  P4. Peak structural change      — max |ω|        (bar)\n"
             "  P5. Hs drift detection          — linear slope of Hs(t)  (bar)\n"
             "  P6. Mean carrier composition    — per-carrier mean share\n"
             "  P7. Hs(t) trajectories          — full year-by-year curves",
             fontsize=10, family="monospace", color="#222")
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 2: Complexity (Aitchison norm) ───────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95, "P2  Complexity spectrum  —  Aitchison norm  ‖clr(x)‖",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925, "Order 2  |  FIXED SCALE across all datasets",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.08, 0.10, 0.84, 0.78])
    for i, (did, c) in enumerate(ctxs):
        ys = [to_int(l) for l in c["labels"]]
        xs = ys if all(y is not None for y in ys) else list(range(c["T"]))
        ax.plot(xs, c["norm"], "-o", lw=1.4, ms=3.5,
                color=ds_palette[i], label=did)
    ax.set_xlim(x_lo - 0.5, x_hi + 0.5)
    ax.set_ylim(nm_lo, nm_hi)
    ax.set_xlabel("year"); ax.set_ylabel("Aitchison norm  ‖clr(x_t)‖")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8, ncol=2, framealpha=0.85)
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 3: Velocity (mean |ω|) ────────────────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95, "P3  Velocity spectrum  —  mean |ω| (rad / step)",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925,
             "Order 3 read  (bearing differences)  |  FIXED SCALE  |  one ω per inter-step",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.08, 0.10, 0.84, 0.78])
    for i, (did, c) in enumerate(ctxs):
        ys = [to_int(l) for l in c["labels"]][1:]  # ω is between t and t+1
        xs = ys if all(y is not None for y in ys) else list(range(1, c["T"]))
        ax.plot(xs, c["omega"], "-o", lw=1.3, ms=3.0,
                color=ds_palette[i], label=did)
    ax.set_xlim(x_lo - 0.5, x_hi + 0.5)
    ax.set_ylim(om_lo, om_hi)
    ax.set_xlabel("year (between t-1 and t)")
    ax.set_ylabel("mean |ω|   (radians / step)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8, ncol=2, framealpha=0.85)
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 4: Peak ω bar ─────────────────────────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95, "P4  Peak structural change  —  max |ω|",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925,
             "Order 2 aggregate of Order 3 read  |  FIXED SCALE",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.10, 0.12, 0.80, 0.76])
    names  = [did for did, _ in ctxs]
    values = [c["peak_omega"] for _, c in ctxs]
    bars = ax.bar(range(n), values, color=ds_palette, edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("max |ω|  (radians / step)")
    ax.set_ylim(0, om_hi)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width()/2, v, f"{v:.3f}",
                ha="center", va="bottom", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 5: Hs drift bars ──────────────────────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95, "P5  Drift detection  —  linear slope of Hs(t) per dataset",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925,
             "Order 2 aggregate  |  positive = increasing entropy / mixing,  "
             "negative = concentrating",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.10, 0.12, 0.80, 0.76])
    slopes = [c["slope_hs"] for _, c in ctxs]
    colors = [ds_palette[i] for i in range(n)]
    bars = ax.bar(range(n), slopes, color=colors, edgecolor="black", linewidth=0.4)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("d Hs / d step   (linear fit)")
    for b, v in zip(bars, slopes):
        sgn = "+" if v >= 0 else "−"
        ax.text(b.get_x() + b.get_width()/2, v,
                f"{sgn}{abs(v):.4f}",
                ha="center",
                va="bottom" if v >= 0 else "top",
                fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 6: Mean carrier composition (heatmap) ──────
    # rows = datasets, cols = carriers ; share = mean over trajectory
    # Carriers may differ across datasets; so use the ember 8 ordering when present
    canonical = ["Bioenergy", "Coal", "Gas", "Hydro", "Nuclear",
                 "Other Fossil", "Solar", "Wind"]
    common = canonical
    if not all(set(common) == set(c["carriers"]) for _, c in ctxs):
        # fall back: union ordered by appearance
        seen = []
        for _, c in ctxs:
            for cn in c["carriers"]:
                if cn not in seen:
                    seen.append(cn)
        common = seen
    M = np.zeros((n, len(common)))
    for i, (_, c) in enumerate(ctxs):
        idx = {cn: k for k, cn in enumerate(c["carriers"])}
        means = c["closed"].mean(axis=0)
        for k, cn in enumerate(common):
            if cn in idx:
                M[i, k] = means[idx[cn]]

    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95,
             "P6  Mean carrier composition  —  per dataset, per carrier",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925, "Order 2 aggregate  |  rows sum to 1.0  |  fixed colourbar 0 → max",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.18, 0.12, 0.74, 0.76])
    im = ax.imshow(M, aspect="auto", cmap="viridis",
                   vmin=0, vmax=float(M.max()) if M.size else 1.0)
    ax.set_yticks(range(n)); ax.set_yticklabels(names, fontsize=9)
    ax.set_xticks(range(len(common)))
    ax.set_xticklabels(common, rotation=30, ha="right", fontsize=9)
    for i in range(n):
        for k in range(len(common)):
            v = M[i, k]
            if v > 0:
                col = "white" if v < 0.4*float(M.max() or 1) else "black"
                ax.text(k, i, f"{v*100:.0f}%",
                        ha="center", va="center", fontsize=7, color=col)
    cb = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.set_label("mean share")
    pdf.savefig(fig); plt.close(fig)

    # ───────── Page 7: Hs(t) per dataset on common axes ────────
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.95,
             "P7  Hs(t) trajectories  —  Shannon entropy of the closed composition",
             ha="center", fontsize=12, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.925, "Order 1 reading per timestep  |  FIXED y-axis  |  all datasets overlaid",
             ha="center", fontsize=9, color="#666")
    ax = fig.add_axes([0.08, 0.10, 0.84, 0.78])
    for i, (did, c) in enumerate(ctxs):
        ys = [to_int(l) for l in c["labels"]]
        xs = ys if all(y is not None for y in ys) else list(range(c["T"]))
        ax.plot(xs, c["hs"], "-o", lw=1.4, ms=3.5,
                color=ds_palette[i], label=did)
    ax.set_xlim(x_lo - 0.5, x_hi + 0.5)
    ax.set_ylim(hs_lo, hs_hi)
    ax.set_xlabel("year"); ax.set_ylabel("Hs(t)  (nats)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8, ncol=2, framealpha=0.85)
    pdf.savefig(fig); plt.close(fig)

    pdf.close()
    return out_pdf


def _load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


# ─────────────────────────── CLI ────────────────────────────
if __name__ == "__main__":
    import sys
    base = "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/HUF-CNT-System/experiments/codawork2026"
    countries = [
        ("EMBER chn", f"{base}/ember_chn/ember_chn_cnt.json"),
        ("EMBER deu", f"{base}/ember_deu/ember_deu_cnt.json"),
        ("EMBER fra", f"{base}/ember_fra/ember_fra_cnt.json"),
        ("EMBER gbr", f"{base}/ember_gbr/ember_gbr_cnt.json"),
        ("EMBER ind", f"{base}/ember_ind/ember_ind_cnt.json"),
        ("EMBER jpn", f"{base}/ember_jpn/ember_jpn_cnt.json"),
        ("EMBER usa", f"{base}/ember_usa/ember_usa_cnt.json"),
        ("EMBER wld", f"{base}/ember_wld/ember_wld_cnt.json"),
    ]
    datasets = [(name, _load(p)) for name, p in countries]
    out = sys.argv[1] if len(sys.argv) > 1 else \
          "/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/HUF-CNT-System/atlas/codawork2026_ember/spectrum_paper_ember.pdf"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render_spectrum_paper(out, datasets,
                          title="EMBER Electricity (8 countries + World) — Spectrum (Paper)")
    print(f"wrote {out}")
