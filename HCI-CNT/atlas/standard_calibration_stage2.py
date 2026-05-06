#!/usr/bin/env python3
"""
Stage 2 calibration fixture — two synthetic trajectories whose
navigation metrics are mathematically known.

Trajectory A: a 6-point straight line in CLR space.
              Predicted course_directness = 1.0 exactly.

Trajectory B: a 7-point closed loop (returns to start).
              Predicted V_net = 0, course_directness = 0 exactly.

Both run through the real CNT engine. Verifies that
stage2_locked.compute_navigation gives the predicted directness
to within IEEE floor.
"""
from __future__ import annotations
import csv, json, math, sys, tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cnt"))
sys.path.insert(0, str(ROOT / "atlas"))
import cnt as cnt_engine
from stage2_locked import collect


D = 4
CARRIERS = ["A", "B", "C", "D"]


def helmert(D):
    V = np.zeros((D-1, D))
    for k in range(D-1):
        s = 1.0 / math.sqrt((k+1)*(k+2))
        for j in range(k+1): V[k, j] = s
        V[k, k+1] = -(k+1) * s
    return V


def comp_from_clr(clr):
    """Inverse of CLR: x_j = exp(clr_j) / Σ exp(clr_k). clr must sum to 0."""
    e = np.exp(clr)
    return list(e / e.sum())


def write_csv(rows, path):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t"] + CARRIERS)
        for k, r in enumerate(rows):
            w.writerow([f"t{k:02d}"] + [f"{v:.10f}" for v in r])


def run_engine(csv_path):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = Path(tf.name)
    cnt_engine.cnt_run(str(csv_path), str(out),
                        {"is_temporal": True, "ordering_method": "by-time",
                         "caveat": None})
    return json.loads(out.read_text())


def trajectory_A_straight(T=6):
    """Linear path from (-1, -0.5, +0.5, +1) to (+1, +0.5, -0.5, -1) in CLR.

    h(t) = h_start + (t/(T-1)) * (h_final - h_start)
    Each h is a 4-vector summing to 0 (CLR constraint).
    """
    h_start = np.array([-1.0, -0.5, +0.5, +1.0])
    h_final = np.array([+1.0, +0.5, -0.5, -1.0])
    rows = []
    for t in range(T):
        alpha = t / (T - 1)
        clr = h_start + alpha * (h_final - h_start)
        rows.append(comp_from_clr(clr))
    return rows


def trajectory_B_loop(T=7):
    """Closed loop: a circle in (CLR1, CLR2) returning to start.

    h(t) = (cos(2π·t/(T-1)), sin(2π·t/(T-1)), 0, 0) — but adjusted
    to sum to 0 by setting CLR3 = -CLR1, CLR4 = -CLR2 so the
    sum-zero constraint holds.
    """
    rows = []
    for t in range(T):
        theta = 2 * math.pi * t / (T - 1)
        c1 = math.cos(theta); s1 = math.sin(theta)
        clr = np.array([c1, s1, -c1, -s1])      # sum = 0
        rows.append(comp_from_clr(clr))
    return rows


def navigation_directness(j):
    """Compute course_directness from a CNT JSON the same way Stage 2 does."""
    ctx = collect(j)
    h_s = ctx["clr_mat"][0]; h_f = ctx["clr_mat"][-1]
    V_net = h_f - h_s
    net_d = float(np.sqrt(np.sum(V_net**2)))
    path_len = float(ctx["d_step"].sum())
    return net_d / path_len if path_len > 0 else 0.0, net_d, path_len


def main():
    print("Stage 2 calibration fixture\n" + "="*60)
    out_dir = Path(__file__).resolve().parent
    artifacts = []

    # Trajectory A — straight line (predicted directness = 1.0)
    rows_A = trajectory_A_straight()
    csv_A  = out_dir / "STANDARD_CALIBRATION_stage2_A_straight.csv"
    json_A = out_dir / "STANDARD_CALIBRATION_stage2_A_straight_cnt.json"
    write_csv(rows_A, csv_A)
    j_A = run_engine(csv_A)
    Path(json_A).write_text(json.dumps(j_A, indent=2))
    d_A, net_A, path_A = navigation_directness(j_A)
    print(f"\nTrajectory A — straight line, T={len(rows_A)}")
    print(f"  net_distance      = {net_A:.10f}")
    print(f"  path_length       = {path_A:.10f}")
    print(f"  course_directness = {d_A:.10f}   (predicted 1.0)")
    err_A = abs(d_A - 1.0)
    print(f"  drift from 1.0    = {err_A:.2e}   {'OK' if err_A < 1e-12 else 'CHECK'}")
    artifacts += [csv_A, json_A]

    # Trajectory B — closed loop (predicted directness = 0)
    rows_B = trajectory_B_loop()
    csv_B  = out_dir / "STANDARD_CALIBRATION_stage2_B_loop.csv"
    json_B = out_dir / "STANDARD_CALIBRATION_stage2_B_loop_cnt.json"
    write_csv(rows_B, csv_B)
    j_B = run_engine(csv_B)
    Path(json_B).write_text(json.dumps(j_B, indent=2))
    d_B, net_B, path_B = navigation_directness(j_B)
    print(f"\nTrajectory B — closed loop, T={len(rows_B)}")
    print(f"  net_distance      = {net_B:.10f}   (predicted 0.0)")
    print(f"  path_length       = {path_B:.10f}")
    print(f"  course_directness = {d_B:.10f}   (predicted 0.0)")
    err_B = abs(d_B - 0.0)
    print(f"  drift from 0.0    = {err_B:.2e}   {'OK' if err_B < 1e-10 else 'CHECK'}")
    artifacts += [csv_B, json_B]

    # Render the full Stage 2 atlas for both fixtures
    import matplotlib; matplotlib.use("Agg")
    from matplotlib.backends.backend_pdf import PdfPages
    from stage2_locked import render_stage2

    pdf_A = out_dir / "STANDARD_CALIBRATION_stage2_A_straight.pdf"
    with PdfPages(pdf_A) as pdf:
        render_stage2(pdf, j_A, "calibration_A_straight", "calib_stage2")
    pdf_B = out_dir / "STANDARD_CALIBRATION_stage2_B_loop.pdf"
    with PdfPages(pdf_B) as pdf:
        render_stage2(pdf, j_B, "calibration_B_loop", "calib_stage2")
    artifacts += [pdf_A, pdf_B]

    print("\n" + "="*60)
    print("Calibration artifacts:")
    for p in artifacts:
        print(f"  {p.name:<55}  {p.stat().st_size:>9,} bytes")

    print()
    if err_A < 1e-12 and err_B < 1e-10:
        print(f"PASS  Stage 2 navigation metrics verified at IEEE floor.")
        print(f"      Straight-line directness = 1.0 (drift {err_A:.1e})")
        print(f"      Closed-loop  directness = 0.0 (drift {err_B:.1e})")
        sys.exit(0)
    else:
        print(f"FAIL  Drift exceeds tolerance.  A: {err_A:.2e}  B: {err_B:.2e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
