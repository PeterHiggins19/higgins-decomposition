#!/usr/bin/env python3
"""
HUF-CNT — Standard calibration test set generator.

Builds a 27-point compositional dataset whose ILR coordinates land
exactly on a 3×3×3 grid at (a, b, c) for a, b, c in {-0.7, 0, +0.7}
HLR. Every plate of the resulting Stage 1 v4 atlas should show a
clean 3×3 grid of dots in each orthogonal panel (with z-stacking
producing exactly 3 dots at each visible position in the side views).

Inverse map ILR → CLR → composition:
    For a target ILR vector y in R^(D-1), the corresponding CLR is
        c = V^T · y                   (V is the (D-1, D) Helmert basis)
    The composition is then
        x_j = exp(c_j) / Σ_k exp(c_k)
    which restores the simplex point that projects to y under ILR.

D=4 is the natural choice (ILR is 3-D, matches the 3-panel display).

Outputs (written next to this script):
    STANDARD_CALIBRATION_27pt.csv          -- the input data
    STANDARD_CALIBRATION_27pt_targets.json -- target ILR coordinates
    STANDARD_CALIBRATION_27pt_cnt.json     -- engine output (after cnt run)
    STANDARD_CALIBRATION_27pt_stage1v4.pdf -- 27-page Stage 1 v4 atlas

Re-running this script reproduces the same artifacts byte-for-byte.
"""
from __future__ import annotations
import csv, json, math, sys, tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ATLAS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "cnt"))
sys.path.insert(0, str(ATLAS_DIR))


D = 4
CARRIERS = ["A", "B", "C", "D"]
GRID = (-0.7, 0.0, +0.7)


# ── Helmert basis for D=4 (matches cnt.py construction) ────────
def helmert_basis(D: int) -> np.ndarray:
    """Build the Helmert orthonormal basis as a (D-1, D) matrix."""
    V = np.zeros((D - 1, D))
    for k in range(D - 1):
        s = 1.0 / math.sqrt((k + 1) * (k + 2))
        for j in range(k + 1):
            V[k, j] = s
        V[k, k + 1] = -(k + 1) * s
    return V


def ilr_to_composition(y: np.ndarray, V: np.ndarray) -> list:
    """Inverse: given target ILR y in R^(D-1), return composition x in S^(D-1).

    Steps:  c = V^T · y    (sum-zero CLR)
            x_j = exp(c_j) / Σ exp(c_k)
    """
    c = V.T @ y                     # CLR (sum-zero)
    e = np.exp(c)
    return (e / e.sum()).tolist()


def label_for(a: float, b: float, c: float) -> str:
    def tag(x):
        return "n" if x < 0 else ("p" if x > 0 else "z")
    return f"p_{tag(a)}{tag(b)}{tag(c)}"


def generate_targets() -> list:
    """27 grid points (a, b, c) for a, b, c in GRID."""
    pts = []
    for a in GRID:
        for b in GRID:
            for c in GRID:
                pts.append((a, b, c))
    return pts


def write_csv(rows: list, csv_path: Path):
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label"] + CARRIERS)
        for label, comp in rows:
            w.writerow([label] + [f"{v:.10f}" for v in comp])


def main():
    print("HUF-CNT — Standard 27-point calibration set generator")
    print(f"  D = {D}, grid = {GRID}, T = {len(GRID)**3} points")

    V = helmert_basis(D)
    targets = generate_targets()

    rows = []
    target_records = []
    for (a, b, c) in targets:
        y = np.array([a, b, c])
        comp = ilr_to_composition(y, V)
        label = label_for(a, b, c)
        rows.append((label, comp))
        # Verify the round-trip: ILR(comp) should equal (a, b, c)
        clr_check = np.log(np.asarray(comp))
        clr_check = clr_check - clr_check.mean()  # centred
        ilr_check = V @ clr_check
        round_trip_err = float(np.max(np.abs(ilr_check - y)))
        target_records.append({
            "label":          label,
            "target_ilr":     [a, b, c],
            "composition":    comp,
            "round_trip_err": round_trip_err,
        })

    # ── Sanity check round-trip ──
    max_err = max(t["round_trip_err"] for t in target_records)
    print(f"  Round-trip ILR target → composition → ILR: max err = {max_err:.2e}")
    assert max_err < 1e-12, f"round-trip error too large: {max_err}"
    print(f"  Round-trip verified to better than 1e-12 ✓")

    # ── Write CSV + targets JSON ──
    csv_path     = ATLAS_DIR / "STANDARD_CALIBRATION_27pt.csv"
    targets_path = ATLAS_DIR / "STANDARD_CALIBRATION_27pt_targets.json"
    write_csv(rows, csv_path)
    targets_path.write_text(json.dumps({
        "_meta": {
            "type":        "HUF_CNT_CALIBRATION_TARGETS",
            "schema":      "1.0",
            "D":           D,
            "carriers":    CARRIERS,
            "grid":        list(GRID),
            "n_points":    len(target_records),
            "description": "27-point ILR calibration grid at "
                           "(a,b,c) for a,b,c in {-0.7, 0, +0.7} HLR",
        },
        "points": target_records,
    }, indent=2))
    print(f"  Wrote: {csv_path}")
    print(f"  Wrote: {targets_path}")

    # ── Run the real CNT engine on the calibration CSV ──
    import cnt as cnt_engine
    out_json = ATLAS_DIR / "STANDARD_CALIBRATION_27pt_cnt.json"
    cnt_engine.cnt_run(str(csv_path), str(out_json),
                       {"is_temporal": False, "ordering_method": "by-label",
                        "caveat": "Calibration grid; non-temporal."})
    j = json.loads(out_json.read_text())
    print(f"  Engine version  : {j['metadata']['engine_version']}")
    print(f"  content_sha256  : {j['diagnostics']['content_sha256']}")
    print(f"  Wrote: {out_json}")

    # ── Verify engine ILR matches our targets ──
    print(f"\n  Verifying engine ILR matches calibration targets...")
    n_ok = 0; n_fail = 0; max_drift = 0.0
    for t_rec, ts in zip(target_records, j["tensor"]["timesteps"]):
        cs = ts["coda_standard"]
        eng_clr = cs["clr"]
        eng_ilr = list(V @ np.asarray(eng_clr))
        target = t_rec["target_ilr"]
        err = max(abs(a - b) for a, b in zip(eng_ilr, target))
        max_drift = max(max_drift, err)
        if err < 1e-8:
            n_ok += 1
        else:
            n_fail += 1
    print(f"    {n_ok}/{len(target_records)} match within 1e-8")
    print(f"    max drift target → engine ILR: {max_drift:.2e}")
    if n_fail:
        print(f"    FAIL: {n_fail} points drifted beyond 1e-8")
        sys.exit(1)

    # ── Render Stage 1 v4 plate ──
    print(f"\n  Rendering Stage 1 v4 calibration atlas...")
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.backends.backend_pdf import PdfPages
    from stage1_v4 import (compute_ilr, compute_window_and_factor,
                            render_plate, fmt_factor)

    ilr_raw = compute_ilr(j)
    window, F = compute_window_and_factor(ilr_raw, n_axes=3, target_max=5.0)
    print(f"    Raw max|ILR(1..3)|     : {float(np.abs(ilr_raw[:, :3]).max()):.4f} HLR")
    print(f"    Auto-picked factor F   : {fmt_factor(F)}")
    print(f"    Display window         : [{window[0]:.3f}, {window[1]:.3f}]")

    pdf_path = ATLAS_DIR / "STANDARD_CALIBRATION_27pt_stage1v4.pdf"
    T = len(target_records)
    with PdfPages(pdf_path) as pdf:
        for k in range(T):
            render_plate(pdf, j, "calibration_27pt", "calib",
                          k + 1, T, k, ilr_raw, window, F, aliases={})
    print(f"    Wrote: {pdf_path}  ({pdf_path.stat().st_size:,} bytes)")

    print()
    print("=" * 70)
    print("STANDARD CALIBRATION ARTIFACTS")
    print("=" * 70)
    for p in [csv_path, targets_path, out_json, pdf_path]:
        print(f"  {p.name:<48}  {p.stat().st_size:>10,} bytes")
    print()
    print("PASS  Calibration grid round-trips through the real CNT engine to")
    print(f"      within {max_drift:.1e} HLR. Display this PDF and you should")
    print(f"      see exactly a 3x3 dot pattern in each orthogonal panel.")


if __name__ == "__main__":
    main()
