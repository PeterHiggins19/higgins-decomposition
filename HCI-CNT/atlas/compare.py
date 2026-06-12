#!/usr/bin/env python3
"""
HUF-CNT Atlas — Comparison atlas (v1.1 feature D).

Renders a single PDF where each analytical plate shows N datasets
overlaid on shared axes. Demonstrates cross-dataset findings visually:
"France and Japan share the period-2 attractor signature" becomes one
bearing rose with two traces, not two PDFs to mentally overlay.

Usage:
    python atlas/compare.py JSON1 JSON2 [JSON3 ...] -o out.pdf
    python atlas/compare.py \
      experiments/codawork2026/ember_jpn/ember_jpn_cnt.json \
      experiments/codawork2026/ember_fra/ember_fra_cnt.json \
      experiments/codawork2026/ember_deu/ember_deu_cnt.json \
      -o /tmp/three_country_compare.pdf
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


PAGE_SIZE = (11.0, 8.5)
PDF_DPI = 150

# Distinct, accessible colour palette for up to ~10 datasets
COMPARE_COLOURS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#17becf", "#bcbd22", "#7f7f7f",
]


def load_dataset(path: str) -> dict:
    p = Path(path)
    j = json.loads(p.read_text())
    return {
        "id":       p.stem.replace("_cnt", ""),
        "json":     j,
        "ir":       j["depth"]["higgins_extensions"]["impulse_response"],
        "summ":     j["depth"]["higgins_extensions"]["summary"],
        "ca":       j["depth"]["higgins_extensions"]["curvature_attractor"],
        "tower_e":  j["depth"]["higgins_extensions"]["energy_tower"],
        "tower_c":  j["depth"]["higgins_extensions"]["curvature_tower"],
        "metric_ledger": j["stages"]["stage1"]["higgins_extensions"]["metric_ledger"],
        "locks":    j["diagnostics"]["higgins_extensions"]["lock_events"],
        "T":        j["input"]["n_records"],
        "D":        j["input"]["n_carriers"],
        "carriers": j["input"]["carriers"],
        "engine":   j["metadata"]["engine_version"],
        "schema":   j["metadata"]["schema_version"],
        "content_sha": j["diagnostics"]["content_sha256"],
    }


def render_cover(pdf: PdfPages, datasets: list):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.text(0.5, 0.92, "HCI-ATLAS", fontsize=24, fontweight="bold",
             ha="center", color="#1f4e79")
    fig.text(0.5, 0.88, "Comparison atlas", fontsize=12, style="italic",
             ha="center", color="#444444")
    fig.text(0.5, 0.83, f"{len(datasets)} datasets on shared axes",
             fontsize=14, fontweight="bold", ha="center", color="#222222")

    fig.text(0.10, 0.74, "Datasets", fontsize=12, fontweight="bold")
    for i, d in enumerate(datasets):
        y = 0.70 - i * 0.05
        c = COMPARE_COLOURS[i % len(COMPARE_COLOURS)]
        fig.text(0.10, y, "■", fontsize=16, color=c)
        fig.text(0.13, y, d["id"], fontsize=11, fontweight="bold")
        fig.text(0.32, y, f"T={d['T']}, D={d['D']}", fontsize=10, color="#555")
        fig.text(0.46, y, f"IR: {d['ir'].get('classification', '?')}",
                 fontsize=10, color=c)
        amp = d["ir"].get("amplitude_A")
        if amp is not None:
            fig.text(0.70, y, f"A = {amp:.4f}", fontsize=10, color="#222")
        fig.text(0.86, y, d["content_sha"][:12] + "...", fontsize=8,
                 family="monospace", color="#888")

    # Common axes are the cross-dataset comparison promise — declare them
    fig.text(0.10, 0.20,
             "Common axes (fixed across every comparison atlas):",
             fontsize=10, fontweight="bold")
    rows = [
        "  Bearing θ      0–360°",
        "  Amplitude A    0–1 (Higgins scale)",
        "  Damping ζ      0–2",
        "  EITT variation 0–100%",
    ]
    for i, row in enumerate(rows):
        fig.text(0.10, 0.17 - i * 0.025, row, fontsize=9, family="monospace")

    fig.text(0.5, 0.04,
             "The instrument reads.  The expert decides.  "
             "The comparison is on the same axes.",
             ha="center", style="italic", color="#888", fontsize=9)
    pdf.savefig(fig); plt.close(fig)


def render_ir_card_compare(pdf: PdfPages, datasets: list):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.suptitle("Plate 1 — IR class + amplitude A on a common 0..1 bar",
                 fontsize=12, fontweight="bold")
    ax = fig.add_axes([0.18, 0.20, 0.72, 0.65])
    for i, d in enumerate(datasets):
        c = COMPARE_COLOURS[i % len(COMPARE_COLOURS)]
        amp = (d["ir"].get("amplitude_A") or 0.0)
        ax.barh(i, amp, color=c, height=0.65,
                label=f"{d['id']}  ({d['ir'].get('classification', '?')})")
        ax.text(min(amp + 0.02, 0.98), i, f"A={amp:.4f}",
                va="center", fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_yticks(range(len(datasets)))
    ax.set_yticklabels([d["id"] for d in datasets], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Amplitude A  (Higgins scale, common 0..1)")
    ax.axvline(0.1, ls="--", color="#888", lw=0.6)
    ax.axvline(0.7, ls="--", color="#888", lw=0.6)
    ax.text(0.1, len(datasets) - 0.3, "0.1", fontsize=7, color="#888", ha="center")
    ax.text(0.7, len(datasets) - 0.3, "0.7", fontsize=7, color="#888", ha="center")
    ax.grid(True, axis="x", alpha=0.3)
    pdf.savefig(fig); plt.close(fig)


def render_bearing_rose_compare(pdf: PdfPages, datasets: list):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.suptitle("Plate 2 — Angular velocity rose (overlaid)",
                 fontsize=12, fontweight="bold")
    ax = fig.add_axes([0.30, 0.10, 0.55, 0.75], projection="polar")
    n_bins = 24
    width = 2 * np.pi / n_bins
    for i, d in enumerate(datasets):
        c = COMPARE_COLOURS[i % len(COMPARE_COLOURS)]
        omegas = [r.get("omega_deg", 0.0) for r in d["metric_ledger"]
                  if r.get("omega_deg") is not None]
        if not omegas:
            continue
        omegas_rad = np.deg2rad(np.array(omegas) % 360)
        counts, _ = np.histogram(omegas_rad, bins=n_bins, range=(0, 2 * np.pi))
        # Normalised counts so different T compare on shape, not magnitude
        if counts.max() > 0:
            counts_n = counts / counts.max()
        else:
            counts_n = counts
        centres = np.linspace(0, 2 * np.pi, n_bins, endpoint=False) + width / 2
        ax.plot(np.append(centres, centres[0]), np.append(counts_n, counts_n[0]),
                color=c, lw=1.5, label=d["id"])
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_ylim(0, 1.1)
    ax.set_rticks([0.25, 0.5, 0.75, 1.0])
    ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.0), fontsize=9)
    fig.text(0.5, 0.04,
             "Counts normalised per dataset to compare shape, not raw frequency.",
             ha="center", fontsize=9, color="#666", style="italic")
    pdf.savefig(fig); plt.close(fig)


def render_helmsman_compare(pdf: PdfPages, datasets: list):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    fig.suptitle("Plate 3 — Energy and curvature tower depth (per dataset)",
                 fontsize=12, fontweight="bold")
    ax = fig.add_axes([0.18, 0.20, 0.72, 0.65])
    n = len(datasets)
    bar_h = 0.35
    for i, d in enumerate(datasets):
        c = COMPARE_COLOURS[i % len(COMPARE_COLOURS)]
        ed = d["summ"].get("energy_depth", 0)
        cd = d["summ"].get("curvature_depth", 0)
        ax.barh(i - bar_h/2, ed, color=c, height=bar_h, alpha=0.6,
                label="energy depth" if i == 0 else None)
        ax.barh(i + bar_h/2, cd, color=c, height=bar_h, alpha=1.0,
                label="curvature depth" if i == 0 else None,
                hatch="//")
        ax.text(ed + 0.5, i - bar_h/2, str(ed), va="center", fontsize=8)
        ax.text(cd + 0.5, i + bar_h/2, str(cd), va="center", fontsize=8)
    ax.set_yticks(range(n))
    ax.set_yticklabels([d["id"] for d in datasets], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Levels")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, axis="x", alpha=0.3)
    pdf.savefig(fig); plt.close(fig)


def render_compare(input_jsons: list, output_pdf: str) -> dict:
    datasets = [load_dataset(p) for p in input_jsons]
    out = Path(output_pdf)
    out.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(out) as pdf:
        render_cover            (pdf, datasets)
        render_ir_card_compare  (pdf, datasets)
        render_bearing_rose_compare(pdf, datasets)
        render_helmsman_compare (pdf, datasets)
        d = pdf.infodict()
        d["Title"]    = f"HCI-Atlas Comparison ({len(datasets)} datasets)"
        d["Author"]   = "HUF-CNT System"
        d["Subject"]  = "Compositional Plate Atlas — comparison"
        d["CreationDate"] = datetime.now(timezone.utc)

    return {
        "datasets":     [d["id"] for d in datasets],
        "n_datasets":   len(datasets),
        "output_pdf":   str(out),
        "generated":    datetime.now(timezone.utc).isoformat(),
    }


def main():
    ap = argparse.ArgumentParser(description="HCI-Atlas comparison atlas")
    ap.add_argument("inputs", nargs="+", help="2 or more CNT JSON paths")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    if len(args.inputs) < 2:
        raise SystemExit("comparison atlas requires >= 2 inputs")
    print(f"Building comparison atlas of {len(args.inputs)} datasets...")
    meta = render_compare(args.inputs, args.output)
    print(f"  Datasets: {meta['datasets']}")
    print(f"  Output:   {meta['output_pdf']}")


if __name__ == "__main__":
    main()
