#!/usr/bin/env python3
"""
EITT bench-test for the Stage 1 plate-cap specification.

Tests whether geometric-mean (Aitchison) block decimation preserves
Shannon entropy on the Ball intraplate-volcanic dataset at the
compression ratio implied by the 101-plate cap (M = 261 for N = 26,266).

The Math Handbook canonical claim: entropy variation < 5% at all tested
compression ratios. Tests in HUF_FAST_REFRESH go to M = 8. This pushes
to M = 261 — a 32-fold extrapolation.

Output: eitt_benchtest_ball.json with the full M-sweep, plus a console
report with pass/fail at the spec gate (M = 261, 5%).

Two orderings tested:
  (a) CSV-as-given (essentially random)
  (b) Aitchison-distance-from-barycenter (principled, smooth trajectory)

If (a) passes the bench-test cleanly, the spec gate is conservative
and can rely on it for any ordering. If only (b) passes, the spec needs
to add an ordering-convention clause.
"""
import csv, json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC  = ROOT / "Current-Repo" / "Hs" / "data" / "Geochemistry" / "ball_oxides_composition.csv"
OUT  = Path(__file__).resolve().parent

OXIDES = ["SiO2","TiO2","Al2O3","FeO","CaO","MgO","MnO","K2O","Na2O","P2O5"]
GATE_PCT = 5.0
SPEC_M   = 261       # ceil(26266 / 101) = 261
M_SWEEP  = [2, 4, 8, 16, 32, 64, 128, 261, 512]


def shannon_entropy(x):
    """H(x) = -sum x_j ln(x_j) for closed positive composition."""
    return -sum(v * math.log(v) for v in x if v > 0)


def aitchison_barycenter(rows):
    D = len(rows[0])
    log_means = [sum(math.log(r[j]) for r in rows) / len(rows) for j in range(D)]
    g = [math.exp(lm) for lm in log_means]
    s = sum(g)
    return [v/s for v in g]


def close(x):
    s = sum(x)
    return [v/s for v in x]


def aitchison_distance(x, y):
    """d_A(x,y) = sqrt( sum_j (clr(x)_j - clr(y)_j)^2 ) for closed x,y."""
    D = len(x)
    log_x = [math.log(v) for v in x]; mx = sum(log_x)/D
    log_y = [math.log(v) for v in y]; my = sum(log_y)/D
    return math.sqrt(sum((log_x[j]-mx - (log_y[j]-my))**2 for j in range(D)))


def decimate_blocks(records, M):
    """Block decimation: every M consecutive records → 1 Aitchison barycenter."""
    blocks = []
    for b in range(0, len(records), M):
        block = records[b:b+M]
        if len(block) >= 2:   # require at least 2 to form a barycenter
            blocks.append(aitchison_barycenter(block))
        elif len(block) == 1:
            blocks.append(block[0])
    return blocks


def eitt_test(records, M):
    H_full      = statistics.mean(shannon_entropy(r) for r in records)
    decimated   = decimate_blocks(records, M)
    H_decimated = statistics.mean(shannon_entropy(r) for r in decimated)
    variation   = abs(H_decimated - H_full) / H_full * 100
    return {
        "M":                M,
        "n_full":           len(records),
        "n_decimated":      len(decimated),
        "H_mean_full":      H_full,
        "H_mean_decimated": H_decimated,
        "variation_pct":    variation,
        "pass":             variation < GATE_PCT,
    }


def main():
    print("Reading Ball oxide compositions...")
    rows = []
    with SRC.open() as f:
        reader = csv.reader(f)
        next(reader)  # header
        for r in reader:
            try:
                vals = [float(v) for v in r]
            except ValueError:
                continue
            if any(v <= 0 for v in vals):
                continue
            rows.append(close(vals))
    print(f"Loaded {len(rows)} positive-oxide compositions")

    # Ordering (a): CSV as given
    rows_csv = list(rows)

    # Ordering (b): sorted by Aitchison distance from global barycenter
    print("Computing global Aitchison barycenter and per-row distances...")
    g_bary = aitchison_barycenter(rows)
    rows_dA = sorted(rows, key=lambda x: aitchison_distance(x, g_bary))

    results = {"orderings": {}}
    for label, ordered in [("CSV-as-given", rows_csv),
                           ("Aitchison-distance", rows_dA)]:
        print(f"\n=== Ordering: {label} ===")
        sweep = []
        for M in M_SWEEP:
            r = eitt_test(ordered, M)
            sweep.append(r)
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  M = {M:>4}  →  {r['n_decimated']:>5} blocks  "
                  f"H_full = {r['H_mean_full']:.6f}  "
                  f"H_dec = {r['H_mean_decimated']:.6f}  "
                  f"Δ = {r['variation_pct']:>6.3f} %  [{tag}]")
        results["orderings"][label] = sweep

    # Spec-gate verdict
    print("\n" + "="*64)
    print(f"SPEC GATE: M = {SPEC_M}  (101-plate cap on Ball/Region)")
    print(f"Threshold: variation < {GATE_PCT}%")
    print("="*64)
    for label in results["orderings"]:
        r = next(x for x in results["orderings"][label] if x["M"] == SPEC_M)
        verdict = "✓ PASS" if r["pass"] else "✗ FAIL"
        print(f"  {label:<22s} : Δ = {r['variation_pct']:>6.3f} %  {verdict}")

    # Math Handbook reference points (M = 2, 4, 8 — claimed to all pass < 5%)
    print("\nMath Handbook reference (claim: variation < 5% at M = 2, 4, 8):")
    for label in results["orderings"]:
        small_M = [r for r in results["orderings"][label] if r["M"] <= 8]
        ok = all(r["pass"] for r in small_M)
        print(f"  {label:<22s} : "
              f"M=2 Δ={small_M[0]['variation_pct']:.3f}, "
              f"M=4 Δ={small_M[1]['variation_pct']:.3f}, "
              f"M=8 Δ={small_M[2]['variation_pct']:.3f}  "
              f"{'(consistent with claim)' if ok else '(INCONSISTENT)'}")

    # Save
    results["meta"] = {
        "source":  str(SRC.name),
        "n_rows":  len(rows),
        "spec_M":  SPEC_M,
        "gate_pct": GATE_PCT,
        "M_sweep": M_SWEEP,
        "oxides":  OXIDES,
    }
    out = OUT / "eitt_benchtest_ball.json"
    with out.open("w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
