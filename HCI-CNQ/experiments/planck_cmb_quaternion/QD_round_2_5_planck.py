#!/usr/bin/env python3
"""QD Round 2.5 — boson falsification test on Planck CMB polarization data.

Pulls Planck 2018 best-fit theoretical power spectrum (TT, TE, EE, BB, PP),
converts the pure-boson (photon) cut TT/EE/BB/PP into a CCTT-compatible CSV
at D=4, runs the canonical CNT engine on it, and reports:

  - The curvature_termination code (P1 = vector branch = boson prediction)
  - The IR class
  - The Concept-1 quaternion-reconstruction precision (Peter's noise hypothesis)
  - Comparison to the corpus's overwhelming P2 dominance

Source: http://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=
        COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt

NO modification to the canonical CNT engine, schema, or corpus.
"""
import csv
import json
import math
import subprocess
import urllib.request
from pathlib import Path

import numpy as np

PLANCK_URL = ("http://pla.esac.esa.int/pla/aio/product-action?"
              "COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-base-plikHM-TTTEEE-"
              "lowl-lowE-lensing-minimum-theory_R3.01.txt")
HERE = Path(__file__).parent
RAW_TXT = HERE / 'planck_theory_raw.txt'
ADAPTER_CSV = HERE / 'planck_cmb_boson_input.csv'
ENGINE_OUT = HERE / 'planck_cmb_boson_cnt.json'

HS_ENGINE = Path('/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/'
                 'Current-Repo/Hs/HCI-CNT/engine/cnt.py')


def step_1_download():
    """Pull Planck best-fit theory spectrum."""
    RAW_TXT.parent.mkdir(parents=True, exist_ok=True)
    if not RAW_TXT.exists():
        print(f"  Downloading {PLANCK_URL[:80]}...")
        urllib.request.urlretrieve(PLANCK_URL, RAW_TXT)
    print(f"  Local: {RAW_TXT}")
    print(f"  Size:  {RAW_TXT.stat().st_size:,} bytes")


def step_2_adapt():
    """Convert raw Planck txt to CCTT-compatible CSV.

    Carriers (D=4): TT (temperature), EE (E-mode polarization),
                    BB (B-mode polarization), PP (lensing potential).
    All four are pure photon (boson) quantities.
    Label: multipole ell.
    Filter: keep only multipoles where ALL FOUR are strictly positive
            (BB and PP go to zero at high ell in the theoretical spectrum;
            those rows are dropped).
    Closure: not applied here; the engine closes input rows automatically.
    """
    with RAW_TXT.open() as f:
        rows = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) != 6:
                continue
            ell = int(parts[0])
            TT, TE, EE, BB, PP = (float(x) for x in parts[1:])
            # Pure-boson cut: TT, EE, BB, PP (drop TE which can be negative;
            # all four kept must be strictly positive).
            if TT > 0 and EE > 0 and BB > 0 and PP > 0:
                rows.append((ell, TT, EE, BB, PP))

    # Write the CSV
    with ADAPTER_CSV.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['multipole_ell', 'TT', 'EE', 'BB', 'PP'])
        for ell, TT, EE, BB, PP in rows:
            w.writerow([f"ell{ell:04d}",
                        f"{TT:.10e}", f"{EE:.10e}", f"{BB:.10e}", f"{PP:.10e}"])

    print(f"  Wrote {len(rows)} multipoles to {ADAPTER_CSV.name}")
    print(f"  D=4, T={len(rows)}")
    print(f"  Multipole range: ell={rows[0][0]} to ell={rows[-1][0]}")
    print(f"  First row: TT={rows[0][1]:.3e}, EE={rows[0][2]:.3e}, "
          f"BB={rows[0][3]:.3e}, PP={rows[0][4]:.3e}")

    return len(rows)


def step_3_run_engine():
    """Run canonical CNT engine on the boson-only CSV."""
    if ENGINE_OUT.exists():
        ENGINE_OUT.unlink()
    cmd = ['python3', str(HS_ENGINE), str(ADAPTER_CSV),
           '-o', str(ENGINE_OUT),
           '--ordering-method', 'by-time']  # multipole ell is monotonic, treat as time-like
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print(f"  Engine FAILED: {r.stderr[-500:]}")
        return None

    # Print the last 8 lines of stdout (engine status block)
    for line in r.stdout.splitlines()[-10:]:
        print(f"    {line}")
    return ENGINE_OUT


def step_4_report():
    """Read the resulting JSON, extract the verdict."""
    j = json.load(open(ENGINE_OUT))

    inp = j['input']
    diag = j['diagnostics']
    sm = j['depth']['higgins_extensions']['summary']
    ir = j['depth']['higgins_extensions']['impulse_response']

    print("\n  ENGINE OUTPUT:")
    print(f"    metadata.engine_version:    {j['metadata']['engine_version']}")
    print(f"    metadata.schema_version:    {j['metadata']['schema_version']}")
    print(f"    input.n_records (T):        {inp.get('n_records', '?')}")
    print(f"    input.n_carriers (D):       {inp.get('n_carriers', '?')}")
    print(f"    input.source_file_sha256:   {inp['source_file_sha256']}")
    print(f"    diagnostics.content_sha256: {diag['content_sha256']}")
    print()
    print(f"  CNT DYNAMICS:")
    print(f"    IR class:                   {ir['classification']}")
    print(f"    amplitude A:                {ir['amplitude_A']:.6f}")
    print(f"    damping zeta:               {ir['damping_zeta']:.6f}")
    print(f"    curvature_depth:            {sm['curvature_depth']}")
    print(f"    energy_depth:               {sm['energy_depth']}")
    print(f"    curvature_termination:      {sm['curvature_termination']}")
    print(f"    energy_termination:         {sm['energy_termination']}")
    print()
    print(f"  QD SPINOR-PARITY VERDICT:")
    term = sm['curvature_termination']
    if 'LIMIT_CYCLE_P1' in term:
        verdict = "VECTOR BRANCH (boson) — QD spinor-parity prediction CONFIRMED"
    elif 'LIMIT_CYCLE_P2' in term:
        verdict = "SPINOR BRANCH (fermion-like) — QD prediction FALSIFIED for this dataset"
    else:
        verdict = f"INCONCLUSIVE — terminator '{term}' is outside the binary spinor/vector test"
    print(f"    {verdict}")
    return j


# ── Concept-1 noise reduction test (Peter's hypothesis) ────────────────

def helmert_basis(D):
    H = np.zeros((D - 1, D))
    for k in range(D - 1):
        n = k + 1
        norm = 1.0 / math.sqrt(n * (n + 1))
        H[k, :n] = norm
        H[k, n] = -n * norm
    return H


def quat_from_axis_angle(axis, angle):
    axis = axis / np.linalg.norm(axis)
    half = angle / 2
    return np.array([math.cos(half),
                     math.sin(half) * axis[0],
                     math.sin(half) * axis[1],
                     math.sin(half) * axis[2]])


def quat_conj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quat_mul(p, q):
    p0, p1, p2, p3 = p; q0, q1, q2, q3 = q
    return np.array([p0*q0 - p1*q1 - p2*q2 - p3*q3,
                     p0*q1 + p1*q0 + p2*q3 - p3*q2,
                     p0*q2 - p1*q3 + p2*q0 + p3*q1,
                     p0*q3 + p1*q2 - p2*q1 + p3*q0])


def quat_rotate(q, v):
    p = np.array([0.0, v[0], v[1], v[2]])
    return quat_mul(quat_mul(q, p), quat_conj(q))[1:]


def step_5_concept_1_noise_test():
    """Repeat Round-2 Concept-1 test on the Planck D=4 boson dataset.
    Predicts: should pass at IEEE floor, same as backblaze_fleet."""
    rows = list(csv.reader(ADAPTER_CSV.open()))
    header, data = rows[0], rows[1:]
    D = len(header) - 1
    closed = np.array([np.array([float(v) for v in r[1:]]) /
                       sum(float(v) for v in r[1:]) for r in data])
    clr_vecs = np.array([np.log(c) - np.log(c).mean() for c in closed])
    H = helmert_basis(D)
    r3 = clr_vecs @ H.T
    r3_unit = r3 / np.linalg.norm(r3, axis=1)[:, None]

    diffs = []
    for t in range(len(r3_unit) - 1):
        u1, u2 = r3_unit[t], r3_unit[t + 1]
        dot = np.clip(np.dot(u1, u2), -1.0, 1.0)
        if dot > 1.0 - 1e-15:
            q = np.array([1.0, 0.0, 0.0, 0.0])
        else:
            axis = np.cross(u1, u2)
            angle = math.atan2(np.linalg.norm(axis), dot)
            q = quat_from_axis_angle(axis, angle)
        u2_reconstructed = quat_rotate(q, u1)
        diffs.append(np.max(np.abs(u2_reconstructed - u2)))

    diffs = np.array(diffs)
    print(f"\n  CONCEPT-1 ON PLANCK CMB (Peter's noise hypothesis):")
    print(f"    Tested {len(diffs)} consecutive multipole pairs")
    print(f"    Max diff:  {diffs.max():.3e}")
    print(f"    Mean diff: {diffs.mean():.3e}")
    print(f"    Comparison to backblaze_fleet Round 2: 4.441e-16 max")
    print(f"    GATE (≤ 1e-12): {'PASS' if diffs.max() <= 1e-12 else 'FAIL'}")
    return float(diffs.max()), float(diffs.mean())


# ── Run the full pipeline ──────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 72)
    print("QD ROUND 2.5 — Planck CMB boson falsification test")
    print("=" * 72)

    print("\n[Step 1] Download Planck 2018 theory spectrum")
    print("-" * 72)
    step_1_download()

    print("\n[Step 2] Adapt to CCTT CSV (pure-boson cut: TT/EE/BB/PP)")
    print("-" * 72)
    n_rows = step_2_adapt()

    print("\n[Step 3] Run canonical CNT engine")
    print("-" * 72)
    step_3_run_engine()

    print("\n[Step 4] Report verdict")
    print("-" * 72)
    j = step_4_report()

    print("\n[Step 5] Concept-1 noise-precision test")
    print("-" * 72)
    max_diff, mean_diff = step_5_concept_1_noise_test()

    # Save summary
    summary = {
        'dataset': 'Planck CMB best-fit theory spectrum (TT/EE/BB/PP)',
        'source': PLANCK_URL,
        'T': n_rows,
        'D': 4,
        'cnt_termination': j['depth']['higgins_extensions']['summary']['curvature_termination'],
        'cnt_ir_class': j['depth']['higgins_extensions']['impulse_response']['classification'],
        'cnt_content_sha256': j['diagnostics']['content_sha256'],
        'concept_1_max_diff': max_diff,
        'concept_1_mean_diff': mean_diff,
    }
    out = HERE / 'QD_round_2_5_results.json'
    out.write_text(json.dumps(summary, indent=2))
    print(f"\nSummary saved: {out}")
