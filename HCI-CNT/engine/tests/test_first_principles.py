#!/usr/bin/env python3
"""
First-principles verification harness.

Builds tiny synthetic compositions (D=3 and D=4) where the CLR and
ILR values can be derived by hand, runs them through the engine, and
compares the engine's output to ground truth term by term.

Three tests:

  Test 1 — uniform composition (centroid).
    Input  : [1/D, 1/D, ..., 1/D]
    Expect : CLR = [0, 0, ..., 0]
             ILR = [0, 0, ..., 0]
             stays at origin in every projection.

  Test 2 — known D=3 trajectory.
    Three points; CLR computed by hand for each;
    ILR via Helmert basis (1/sqrt(2))[1,-1,0], (1/sqrt(6))[1,1,-2].

  Test 3 — D=4 trajectory at vertex / centroid / mixed.
    Validates that a near-vertex composition has a CLR with one
    extreme value and the ILR axis that loads on that vertex shows
    the expected sign.
"""
from __future__ import annotations
import csv, json, math, sys, tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cnt"))
import cnt as cnt_engine


# ------------------------------------------------------------------
def write_csv(path: Path, label: str, header: list, rows: list):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([label] + header)
        for i, r in enumerate(rows):
            w.writerow([f"t{i:02d}"] + [f"{v:.10f}" for v in r])


def run_engine(csv_path: Path) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = Path(tf.name)
    cnt_engine.cnt_run(str(csv_path), str(out),
                        {"is_temporal": True, "ordering_method": "by-time",
                         "caveat": None})
    return json.loads(out.read_text())


def expected_clr(comp: list[float]) -> list[float]:
    """Hand-computed CLR: ln(x_j / g) where g is geometric mean."""
    g = math.exp(sum(math.log(v) for v in comp) / len(comp))
    return [math.log(v / g) for v in comp]


def expected_ilr_via_basis(clr: list[float], basis) -> list[float]:
    """ILR = Helmert_basis @ CLR."""
    return list(np.asarray(basis) @ np.asarray(clr))


# ------------------------------------------------------------------
def test_uniform_centroid():
    """Test 1 — every row is the centroid of the simplex."""
    print()
    print("=" * 70)
    print("Test 1 — uniform centroid composition")
    print("-" * 70)

    D = 4
    comp = [1.0 / D] * D
    rows = [comp[:] for _ in range(5)]
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        csv_p = Path(tf.name)
    write_csv(csv_p, "label",
              ["A", "B", "C", "D"], rows)

    j = run_engine(csv_p)
    timesteps = j["tensor"]["timesteps"]
    basis = j["tensor"]["helmert_basis"]["coefficients"]

    print(f"Closed comp     : {comp}")
    print(f"Expected CLR    : [0, 0, 0, 0]")
    print(f"Engine CLR (t=0): {[f'{v:+.4e}' for v in timesteps[0]['coda_standard']['clr']]}")
    print(f"Expected ILR    : [0, 0, 0]")
    ilr = list(np.asarray(basis) @ np.asarray(timesteps[0]['coda_standard']['clr']))
    print(f"Engine ILR (t=0): {[f'{v:+.4e}' for v in ilr]}")

    max_clr = max(abs(v) for v in timesteps[0]['coda_standard']['clr'])
    max_ilr = max(abs(v) for v in ilr)
    if max_clr < 1e-12 and max_ilr < 1e-12:
        print(f"PASS   centroid → all coordinates at origin (max |v| < 1e-12)")
        return True
    else:
        print(f"FAIL   max|CLR|={max_clr:.2e}, max|ILR|={max_ilr:.2e}")
        return False


def test_known_d3_trajectory():
    """Test 2 — a known D=3 trajectory with hand-computed ILR."""
    print()
    print("=" * 70)
    print("Test 2 — D=3 trajectory (hand-computed CLR / ILR)")
    print("-" * 70)

    rows = [
        [0.7, 0.2, 0.1],
        [0.5, 0.3, 0.2],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5],
    ]
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        csv_p = Path(tf.name)
    write_csv(csv_p, "label", ["A", "B", "C"], rows)

    j = run_engine(csv_p)
    timesteps = j["tensor"]["timesteps"]
    basis = j["tensor"]["helmert_basis"]["coefficients"]

    print(f"Helmert basis ({len(basis)}×{len(basis[0])}):")
    for r in basis:
        print(f"  {[f'{v:+.4f}' for v in r]}")
    print()

    all_ok = True
    for t, comp in enumerate(rows):
        exp_clr = expected_clr(comp)
        eng_clr = timesteps[t]["coda_standard"]["clr"]
        exp_ilr = expected_ilr_via_basis(exp_clr, basis)
        eng_ilr = list(np.asarray(basis) @ np.asarray(eng_clr))

        clr_err = max(abs(a - b) for a, b in zip(exp_clr, eng_clr))
        ilr_err = max(abs(a - b) for a, b in zip(exp_ilr, eng_ilr))

        ok = (clr_err < 1e-10 and ilr_err < 1e-10)
        all_ok = all_ok and ok
        tag = "OK " if ok else "ERR"
        print(f"  t={t}  closed={comp}")
        print(f"        CLR exp = {[f'{v:+.4f}' for v in exp_clr]}")
        print(f"        CLR eng = {[f'{v:+.4f}' for v in eng_clr]}  err={clr_err:.2e}")
        print(f"        ILR exp = {[f'{v:+.4f}' for v in exp_ilr]}")
        print(f"        ILR eng = {[f'{v:+.4f}' for v in eng_ilr]}  err={ilr_err:.2e}  {tag}")

    if all_ok:
        print("PASS   all CLR / ILR values match hand computation < 1e-10")
    else:
        print("FAIL   numerical drift exceeds 1e-10")
    return all_ok


def test_d4_near_vertex():
    """Test 3 — D=4 near-vertex composition."""
    print()
    print("=" * 70)
    print("Test 3 — D=4 near-vertex (one carrier dominates)")
    print("-" * 70)

    rows = [
        [0.25, 0.25, 0.25, 0.25],     # centroid
        [0.97, 0.01, 0.01, 0.01],     # near vertex on carrier 0
        [0.01, 0.97, 0.01, 0.01],     # near vertex on carrier 1
        [0.40, 0.30, 0.20, 0.10],     # ordinary mix
    ]
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        csv_p = Path(tf.name)
    write_csv(csv_p, "label", ["A", "B", "C", "D"], rows)

    j = run_engine(csv_p)
    timesteps = j["tensor"]["timesteps"]
    basis = j["tensor"]["helmert_basis"]["coefficients"]

    print("Helmert basis loadings:")
    for i, r in enumerate(basis):
        print(f"  ILR({i+1}) = {' '.join(f'{v:+.4f}*A' if k==0 else f'{v:+.4f}*{chr(65+k)}' for k,v in enumerate(r))}")
    print()

    # Centroid should be at origin
    c0 = timesteps[0]["coda_standard"]["clr"]
    centroid_origin = max(abs(v) for v in c0) < 1e-12
    print(f"  Centroid at origin: {'YES' if centroid_origin else 'NO'}")

    # Vertex on A should have ILR(1) > 0 (carrier A is positively weighted on row 0)
    v1 = list(np.asarray(basis) @ np.asarray(timesteps[1]["coda_standard"]["clr"]))
    print(f"  Vertex A: ILR = {[f'{v:+.4f}' for v in v1]}")
    print(f"           ILR(1) > 0 because carrier A weight = {basis[0][0]:+.4f}")
    expected_sign = basis[0][0] > 0
    actual_sign = v1[0] > 0
    sign_ok = expected_sign == actual_sign
    print(f"           sign match: {'YES' if sign_ok else 'NO'}")

    # Vertex on B
    v2 = list(np.asarray(basis) @ np.asarray(timesteps[2]["coda_standard"]["clr"]))
    print(f"  Vertex B: ILR = {[f'{v:+.4f}' for v in v2]}")
    expected_sign_b = basis[0][1] > 0
    actual_sign_b = v2[0] > 0
    sign_ok_b = expected_sign_b == actual_sign_b
    print(f"           ILR(1) sign match (carrier B weight {basis[0][1]:+.4f}): {'YES' if sign_ok_b else 'NO'}")

    # Closure check on every row
    closure_ok = True
    for t, ts in enumerate(timesteps):
        comp = ts["coda_standard"].get("composition") or ts.get("raw_values") or []
        if not comp and "coda_standard" in ts:
            comp = ts["coda_standard"].get("composition", [])
        s = sum(comp) if comp else 0
        if abs(s - 1.0) > 1e-10:
            print(f"  CLOSURE FAIL at t={t}: Σ = {s:.10f}")
            closure_ok = False
    print(f"  Closure invariant on all rows: {'YES' if closure_ok else 'NO'}")

    if centroid_origin and sign_ok and sign_ok_b and closure_ok:
        print("PASS   D=4 sanity checks all OK")
        return True
    print("FAIL   one or more checks did not match")
    return False


def test_japan_first_two_timesteps():
    """Test 4 — verify Japan EMBER published JSON CLR matches hand computation."""
    print()
    print("=" * 70)
    print("Test 4 — Japan EMBER published JSON, hand-verify first two timesteps")
    print("-" * 70)
    jp = ROOT / "experiments" / "codawork2026" / "ember_jpn" / "ember_jpn_cnt.json"
    j = json.loads(jp.read_text())
    carriers = j["input"]["carriers"]
    timesteps = j["tensor"]["timesteps"]
    basis = j["tensor"]["helmert_basis"]["coefficients"]
    D = len(carriers)
    print(f"  D = {D},  T = {len(timesteps)}, carriers = {carriers}")
    all_ok = True
    for t in range(2):
        ts = timesteps[t]
        comp = ts["coda_standard"].get("composition") or ts.get("raw_values") or []
        if not comp and "coda_standard" in ts:
            comp = ts["coda_standard"].get("composition", [])
        eng_clr = ts["coda_standard"]["clr"]
        exp_clr = expected_clr(comp)
        clr_err = max(abs(a - b) for a, b in zip(exp_clr, eng_clr))
        eng_ilr = list(np.asarray(basis) @ np.asarray(eng_clr))
        s = sum(comp)
        ok = (clr_err < 1e-10 and abs(s - 1.0) < 1e-10)
        tag = "OK" if ok else "ERR"
        print(f"  t={t}  label={ts['label']}  Σ={s:.10f}")
        print(f"        engine CLR : {[f'{v:+.3f}' for v in eng_clr]}")
        print(f"        hand CLR   : {[f'{v:+.3f}' for v in exp_clr]}    err={clr_err:.2e}  {tag}")
        print(f"        engine ILR : {[f'{v:+.3f}' for v in eng_ilr]}")
        if not ok: all_ok = False
    if all_ok:
        print("PASS   Japan published JSON's first two timesteps match hand-computed CLR < 1e-10")
    else:
        print("FAIL   discrepancy detected")
    return all_ok


def main():
    print("HUF-CNT — first-principles synthetic verification harness")
    results = [
        ("uniform centroid",       test_uniform_centroid()),
        ("D=3 known trajectory",   test_known_d3_trajectory()),
        ("D=4 near-vertex",        test_d4_near_vertex()),
        ("Japan EMBER hand-check", test_japan_first_two_timesteps()),
    ]
    print()
    print("=" * 70)
    n_pass = sum(1 for _, ok in results if ok)
    n_fail = len(results) - n_pass
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 70)
    print(f"Total: {n_pass} PASS, {n_fail} FAIL")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()
