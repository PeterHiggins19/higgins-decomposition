#!/usr/bin/env python3
"""
HCI-Atlas — complete Stage 1 driver (locked Order-1 standard).

Reads any conforming CNT JSON and emits the closed Stage 1 atlas:
    T per-timestep plates (atlas/stage1_v4.py)
  + 1 trajectory-summary plate (atlas/stage1_summary.py)

Total pages = T + 1.

This is the canonical Stage 1 PDF for the v1.1 doctrine.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_pdf import PdfPages

ATLAS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ATLAS_DIR))
from stage1_v4 import (compute_ilr, compute_window_and_factor,
                        render_plate, fmt_factor)
from stage1_summary import render_summary_plate
try:
    from alias_map import load_aliases
except ImportError:
    def load_aliases(*a, **kw): return {}


def render(input_json, output_pdf, max_plates=None, run_id=None):
    inp = Path(input_json); out = Path(output_pdf)
    j = json.loads(inp.read_text())
    dataset_id = inp.stem.replace("_cnt", "")
    T = j["input"]["n_records"]
    is_codawork = ("codawork2026" in str(inp).replace("\\", "/"))
    if max_plates is None:
        max_plates = T if is_codawork else min(T, 50)
    if max_plates >= T:
        frames = list(range(T)); regime = "FULL"
    else:
        K = max(2, max_plates)
        frames = sorted(set(int(round(i*(T-1)/(K-1))) for i in range(K)))
        regime = "DECIMATED"

    ilr = compute_ilr(j)
    window, F = compute_window_and_factor(ilr, n_axes=3, target_max=5.0)

    mc = ATLAS_DIR.parent / "mission_command" / "master_control.json"
    aliases = load_aliases(mc, dataset_id)

    out.parent.mkdir(parents=True, exist_ok=True)
    n_pages = len(frames) + 1   # +1 for summary plate
    with PdfPages(out) as pdf:
        for pi, fi in enumerate(frames, 1):
            render_plate(pdf, j, dataset_id, run_id,
                          pi, n_pages, fi, ilr, window, F, aliases)
        # Closing summary plate
        render_summary_plate(pdf, j, dataset_id, run_id,
                              n_pages, n_pages, ilr, aliases)

    return {"dataset_id": dataset_id, "T_total": T, "n_pages": n_pages,
            "regime": regime, "is_codawork": is_codawork,
            "factor": F, "window": window,
            "output": str(out)}


def main():
    ap = argparse.ArgumentParser(description="Complete Stage 1 atlas (Order-1 doctrine)")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--max-plates", type=int, default=None)
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args()
    out = args.output or str(Path(args.input).with_suffix("")) + "_stage1_complete.pdf"
    print("HCI-Atlas Stage 1 — complete (T plates + summary)")
    print(f"Input  : {args.input}")
    print(f"Output : {out}")
    meta = render(args.input, out, args.max_plates, args.run_id)
    print()
    print(f"Dataset      : {meta['dataset_id']}")
    print(f"T total      : {meta['T_total']}")
    print(f"Regime       : {meta['regime']}"
          f" ({'codawork2026 FULL default' if meta['is_codawork'] else 'standard'})")
    print(f"Factor F     : {fmt_factor(meta['factor'])}")
    print(f"Window       : [{meta['window'][0]:.3f}, {meta['window'][1]:.3f}] HLR (× factor)")
    print(f"Total pages  : {meta['n_pages']} (T per-timestep + 1 summary)")
    print(f"Output       : {meta['output']}")


if __name__ == "__main__":
    main()
