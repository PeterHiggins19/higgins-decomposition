#!/usr/bin/env python3
"""
T-sweep on Ball/Region to confirm the E_depth ~ alpha * T scaling.

Takes the top-T regions from the Ball/Region barycenter table (sorted
by sample count) for T in {10, 20, 40, 60, 80, 95} and runs the depth
sounder on each. The comparison isolates T as the independent variable
within a single dataset (constant population, constant binning rule),
so any change in E_depth is purely a T effect.

Combined with the cross-dataset points (Ball/Age T=10, Stracke T=15,
Tappe T=8, Qin T=30, Ball/Region T=95), this gives ~9 data points to
fit E_depth = alpha * T + beta.
"""
import csv, json, subprocess, statistics, math, sys
from pathlib import Path

OUT  = Path(__file__).resolve().parent
SRC  = OUT / "ball_oxides_by_region_long.csv"
SUMM = OUT / "ball_oxides_by_region_summary.json"

import collections, math as m

def aitchison_barycenter(rows):
    if not rows: return None
    D = len(rows[0])
    log_means = [sum(m.log(r[j]) for r in rows) / len(rows) for j in range(D)]
    g = [m.exp(lm) for lm in log_means]
    return [x/sum(g) for x in g]


def main():
    summ = json.load(open(SUMM))
    OXIDES = summ["oxides"]
    # Sort regions by n_samples, descending
    ranked = sorted(summ["regions"], key=lambda r: -r["n_samples"])

    T_values = [10, 20, 40, 60, 80, 95]
    results = []

    # Read all sample-level data once
    samples_by_region = collections.defaultdict(list)
    with SRC.open() as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            region = row[0]
            vals = [float(v) for v in row[2:]]
            samples_by_region[region].append(vals)

    for T in T_values:
        top_regions = [r["region"] for r in ranked[:T]]
        print(f"\n=== T={T}: top-{T} regions, total samples = "
              f"{sum(len(samples_by_region[r]) for r in top_regions)} ===")

        # Build barycenter CSV for this subset
        sub_csv = OUT / f"ball_top{T}_barycenters.csv"
        with sub_csv.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Region"] + OXIDES)
            for region in sorted(top_regions):
                bary = aitchison_barycenter(samples_by_region[region])
                w.writerow([region] + [f"{v:.10f}" for v in bary])

        # Run CNT tensor engine
        cnt_json = OUT / f"ball_top{T}_cnt.json"
        depth_json = OUT / f"ball_top{T}_depth.json"
        subprocess.run([sys.executable, "cnt_tensor_engine.py",
                       str(sub_csv), str(cnt_json)],
                      cwd=str(OUT), capture_output=True, check=True)
        subprocess.run([sys.executable, "cnt_depth_sounder.py",
                       str(cnt_json), str(depth_json)],
                      cwd=str(OUT), capture_output=True, check=True)

        d = json.load(depth_json.open())
        ds = d["depth_summary"]
        results.append({
            "T": T,
            "energy_depth":   ds["energy_depth"],
            "energy_period":  ds["energy_cycle"]["period"] if ds["energy_cycle"]["detected"] else 0,
            "curv_depth":     ds["curvature_depth"],
            "curv_period":    ds["curvature_cycle"]["period"] if ds["curvature_cycle"]["detected"] else 0,
            "energy_to_T":    ds["energy_depth"] / T,
        })
        r = results[-1]
        print(f"  → curv_depth={r['curv_depth']} (P{r['curv_period']}), "
              f"energy_depth={r['energy_depth']} (P{r['energy_period']}), "
              f"E/T={r['energy_to_T']:.3f}")

    # Linear regression E_depth = a*T + b on all 5 cross-dataset points
    # plus this T-sweep
    xt_pts = [(r["T"], r["energy_depth"]) for r in results]
    cross_pts = [
        ("Tappe-KIM",   8,  4),
        ("Ball-Age",   10,  6),
        ("Stracke-OIB",15, 11),
        ("Qin-Cpx",    30, 26),
    ]
    all_pts = xt_pts + [(t, e) for _,t,e in cross_pts]
    Ts = [p[0] for p in all_pts]
    Es = [p[1] for p in all_pts]
    n = len(Ts)
    mean_T = sum(Ts)/n; mean_E = sum(Es)/n
    sxx = sum((t-mean_T)**2 for t in Ts)
    sxy = sum((t-mean_T)*(e-mean_E) for t,e in zip(Ts, Es))
    a = sxy/sxx
    b = mean_E - a*mean_T
    # R^2
    ss_tot = sum((e-mean_E)**2 for e in Es)
    ss_res = sum((e - (a*t+b))**2 for t,e in zip(Ts,Es))
    r2 = 1 - ss_res/ss_tot

    out = {
        "t_sweep_results": results,
        "cross_dataset_points": [{"name": n, "T": t, "energy_depth": e}
                                 for n,t,e in cross_pts],
        "fit": {
            "model": "E_depth = alpha * T + beta",
            "alpha": a,
            "beta":  b,
            "R2":    r2,
            "n_points": n,
        },
    }
    with (OUT / "t_sweep_results.json").open("w") as f:
        json.dump(out, f, indent=2)

    print(f"\n=== Linear fit on {n} points (T-sweep + cross-dataset) ===")
    print(f"  E_depth = {a:.4f} * T + {b:.4f}")
    print(f"  R² = {r2:.4f}")
    print()
    print(f"{'Run':<22}{'T':>5}{'E':>5}{'predicted':>12}{'residual':>10}")
    print("-"*54)
    for n,t,e in cross_pts:
        pred = a*t + b
        print(f"{n:<22}{t:>5}{e:>5}{pred:>12.2f}{e-pred:>10.2f}")
    for r in results:
        pred = a*r['T'] + b
        print(f"{'Ball/top-'+str(r['T']):<22}{r['T']:>5}{r['energy_depth']:>5}"
              f"{pred:>12.2f}{r['energy_depth']-pred:>10.2f}")


if __name__ == "__main__":
    main()
