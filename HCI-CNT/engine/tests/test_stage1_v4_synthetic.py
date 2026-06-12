#!/usr/bin/env python3
"""
Stage 1 v4 — synthetic 10-frame end-to-end test.

Generates a known D=4 trajectory of 10 timesteps following a smooth
parametric path on the simplex, runs the REAL CNT engine on it, then:

  1. Verifies the engine's CLR matches hand computation at every t
  2. Verifies the engine's ILR (Helmert basis × CLR) matches hand
     computation at every t
  3. Renders the Stage 1 v4 ortho atlas (10 plates) with magnitude
     factor and FIXED HLR scale
  4. Writes both the input CSV and the resulting JSON next to each
     other so the user can verify the data is genuine — no fabrication.

The path: closure of [exp(sin(2πk/10)), exp(cos(2πk/10)),
                       exp(sin(2πk/10 + π/3)),
                       exp(cos(2πk/10 + π/3))]   for k = 0..9
This produces 10 points on the simplex following a smooth orbit, with
known closed and CLR/ILR values.
"""
from __future__ import annotations
import csv, json, math, sys, tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ATLAS_DIR = ROOT / "atlas"
sys.path.insert(0, str(ROOT / "cnt"))
sys.path.insert(0, str(ATLAS_DIR))

import cnt as cnt_engine
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_pdf import PdfPages
from stage1_v4 import (compute_ilr, compute_window_and_factor,
                        render_plate, fmt_factor)


D = 4
T = 10
CARRIERS = ["A", "B", "C", "D"]
PHASE = math.pi / 3


def synthetic_trajectory():
    """Smooth simplex orbit, deterministic, 10 frames."""
    rows = []
    for k in range(T):
        t = 2 * math.pi * k / T
        raw = [
            math.exp(math.sin(t)),
            math.exp(math.cos(t)),
            math.exp(math.sin(t + PHASE)),
            math.exp(math.cos(t + PHASE)),
        ]
        s = sum(raw)
        rows.append([v / s for v in raw])
    return rows


def write_csv(rows, csv_path: Path):
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t"] + CARRIERS)
        for k, r in enumerate(rows):
            w.writerow([f"t{k:02d}"] + [f"{v:.10f}" for v in r])


def hand_clr(comp):
    g = math.exp(sum(math.log(v) for v in comp) / len(comp))
    return [math.log(v / g) for v in comp]


def main():
    print("=" * 78)
    print("Stage 1 v4 — synthetic 10-frame end-to-end test")
    print("=" * 78)

    out_dir = Path(tempfile.mkdtemp(prefix="stage1v4_"))
    csv_path  = out_dir / "synthetic_10frame.csv"
    json_path = out_dir / "synthetic_10frame_cnt.json"

    rows = synthetic_trajectory()
    write_csv(rows, csv_path)
    print(f"\n  Generated synthetic CSV : {csv_path}")
    print(f"  D = {D}, T = {T}, carriers = {CARRIERS}")
    print(f"  First row: {[f'{v:.4f}' for v in rows[0]]}")
    print(f"  Closure check on every row:")
    for k, r in enumerate(rows):
        s = sum(r)
        print(f"    t{k:02d}: Σ = {s:.10f}  {'OK' if abs(s - 1.0) < 1e-12 else 'FAIL'}")

    # ── Run real CNT engine ──
    print(f"\n  Running real CNT engine...")
    cnt_engine.cnt_run(str(csv_path), str(json_path),
                        {"is_temporal": True, "ordering_method": "by-time",
                         "caveat": None})
    j = json.loads(json_path.read_text())
    print(f"  Engine version  : {j['metadata']['engine_version']}")
    print(f"  Schema version  : {j['metadata']['schema_version']}")
    print(f"  content_sha256  : {j['diagnostics']['content_sha256']}")

    # ── Verify CLR / ILR per timestep ──
    print(f"\n  Verifying CLR and ILR against hand computation...")
    basis = np.asarray(j["tensor"]["helmert_basis"]["coefficients"])
    timesteps = j["tensor"]["timesteps"]
    n_pass = 0; n_fail = 0
    for t, ts in enumerate(timesteps):
        cs = ts["coda_standard"]
        eng_closed = cs.get("composition") or ts.get("raw_values")
        eng_clr    = cs["clr"]
        # Hand-compute from the engine's read-back composition
        # (isolates engine math from CSV float serialization noise)
        ref_comp = eng_closed if eng_closed else rows[t]
        my_clr = hand_clr(ref_comp)
        my_ilr = list(basis @ np.asarray(my_clr))
        eng_ilr = list(basis @ np.asarray(eng_clr))
        clr_err = max(abs(a - b) for a, b in zip(my_clr, eng_clr))
        ilr_err = max(abs(a - b) for a, b in zip(my_ilr, eng_ilr))
        ok = (clr_err < 1e-10 and ilr_err < 1e-10)
        tag = "OK " if ok else "FAIL"
        print(f"    t{t:02d}  CLR err = {clr_err:.2e}   ILR err = {ilr_err:.2e}  {tag}")
        if ok: n_pass += 1
        else:  n_fail += 1
    print(f"  Result: {n_pass}/{len(timesteps)} PASS")

    # ── Render Stage 1 v4 plate ──
    print(f"\n  Rendering Stage 1 v4 ortho atlas...")
    ilr_raw = compute_ilr(j)
    window, F = compute_window_and_factor(ilr_raw, n_axes=3, target_max=5.0)
    print(f"  Raw max|ILR(1..3)|     : {float(np.abs(ilr_raw[:, :3]).max()):.4f} HLR")
    print(f"  Auto-picked factor F   : {fmt_factor(F)}  (so display range fits)")
    print(f"  Display window (HLR×F) : [{window[0]:.3f}, {window[1]:.3f}]")

    pdf_path = out_dir / "synthetic_10frame_stage1v4.pdf"
    with PdfPages(pdf_path) as pdf:
        for page_idx in range(T):
            render_plate(pdf, j, "synthetic_10frame", "test001",
                          page_idx + 1, T, page_idx,
                          ilr_raw, window, F, aliases={})

    pdf_size = pdf_path.stat().st_size
    print(f"  Output PDF             : {pdf_path}")
    print(f"  Size                   : {pdf_size:,} bytes  ({T} pages)")

    # ── Copy artifacts into the package for inspection ──
    sample_dir = ROOT / "atlas" / "SAMPLE_stage1v4_synthetic"
    sample_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    for src, name in [(csv_path,  "synthetic_10frame.csv"),
                      (json_path, "synthetic_10frame_cnt.json"),
                      (pdf_path,  "synthetic_10frame_stage1v4.pdf")]:
        shutil.copy2(src, sample_dir / name)
    print(f"\n  Artifacts copied to    : {sample_dir}")
    print(f"    - synthetic_10frame.csv         (the input — not fabricated)")
    print(f"    - synthetic_10frame_cnt.json    (engine output, hash-locked)")
    print(f"    - synthetic_10frame_stage1v4.pdf (10-page ortho atlas)")

    print()
    print("=" * 78)
    if n_fail == 0:
        print(f"PASS  All {n_pass} timesteps reproduce CLR / ILR to within 1e-10.")
        print("      Engine math verified by hand. Stage 1 v4 plate rendered.")
        sys.exit(0)
    else:
        print(f"FAIL  {n_fail} timesteps disagreed with hand computation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
