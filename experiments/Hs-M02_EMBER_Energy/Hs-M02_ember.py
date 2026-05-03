#!/usr/bin/env python3
"""
Hs-M02: EMBER Electricity Generation — Full CoDaWork Reference Experiment
==========================================================================
The par excellence experiment. Every number the CoDa community will examine.

Runs the complete Hs diagnostic pipeline on EMBER electricity generation data
for 7 systems: Germany, United Kingdom, Japan, France, China, India, and World.

9 carriers (or 8 where Other Renewables is absent):
  Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Other Renewables, Solar, Wind

26 years: 2000-2025

All computations are deterministic. Same input, same output, always.
"""

import numpy as np
import csv
import json
import os
from collections import OrderedDict

# ============================================================
# DATA PATHS
# ============================================================

DATA_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/DATA/Energy/Embers 2025/pipeline_ready"
OUT_DIR = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/Hs/experiments/Hs-M02_EMBER_Energy"

COUNTRIES = [
    ("DEU", "Germany"),
    ("GBR", "United Kingdom"),
    ("JPN", "Japan"),
    ("FRA", "France"),
    ("CHN", "China"),
    ("IND", "India"),
    ("WLD", "World"),
]

# ============================================================
# CORE Hs PIPELINE
# ============================================================

EPSILON = 1e-10  # replacement for structural zeros

def load_country(iso, name):
    """Load pipeline-ready CSV, return years, carriers, data matrix"""
    path = os.path.join(DATA_DIR, f"ember_{iso}_{name.replace(' ', '_')}_generation_TWh.csv")
    with open(path) as f:
        reader = csv.DictReader(f)
        carriers = [c for c in reader.fieldnames if c != "Year"]
        rows = []
        years = []
        for row in reader:
            years.append(int(float(row["Year"])))
            vals = []
            for c in carriers:
                v = float(row[c])
                if v <= 0:
                    v = EPSILON
                vals.append(v)
            rows.append(vals)
    return years, carriers, np.array(rows)

def closure(X):
    """Close each row to sum = 1"""
    if X.ndim == 1:
        return X / X.sum()
    return (X.T / X.sum(axis=1)).T

def clr(X):
    """Centred log-ratio transform"""
    if X.ndim == 1:
        gm = np.exp(np.mean(np.log(X)))
        return np.log(X / gm)
    gm = np.exp(np.mean(np.log(X), axis=1, keepdims=True))
    return np.log(X / gm)

def variation_matrix(X):
    """D x D variation matrix"""
    D = X.shape[1]
    T = np.zeros((D, D))
    for k in range(D):
        for j in range(D):
            lr = np.log(X[:, k] / X[:, j])
            T[k, j] = np.var(lr, ddof=0)
    return T

def total_variance(T):
    D = T.shape[0]
    return np.sum(T) / (2 * D)

def cumulative_variance(X):
    N = X.shape[0]
    vt = []
    for t in range(2, N + 1):
        T = variation_matrix(X[:t])
        vt.append(total_variance(T))
    return np.array(vt)

def aitchison_distance(x, y):
    x, y = closure(x), closure(y)
    D = len(x)
    lr = np.log(x / y)
    return np.sqrt(np.sum((lr[:, None] - lr[None, :]) ** 2) / (2 * D))

def shannon_entropy(x):
    x = closure(x)
    x = x[x > EPSILON * 10]
    return -np.sum(x * np.log(x))

def aitchison_norm(x):
    x = closure(x)
    c = clr(x)
    return np.sqrt(np.sum(c ** 2))

def pair_stability(X, carriers):
    """Compute all D(D-1)/2 log-ratio pair statistics"""
    D = X.shape[1]
    results = []
    for i in range(D):
        for j in range(i + 1, D):
            lr = np.log(X[:, i] / X[:, j])
            mu = np.mean(lr)
            sd = np.std(lr, ddof=0)
            cv = abs(sd / mu) if abs(mu) > 1e-12 else float('inf')
            results.append({
                'pair': f"{carriers[i]}/{carriers[j]}",
                'i': i, 'j': j,
                'mean_log_ratio': round(mu, 6),
                'sd': round(sd, 6),
                'cv': round(cv, 6) if cv < 1e6 else "inf"
            })
    # Sort by CV (most stable first)
    results.sort(key=lambda r: r['cv'] if isinstance(r['cv'], (int, float)) else 1e9)
    return results

def classify_shape(vt):
    if len(vt) < 3:
        return "insufficient_data"
    x = np.arange(len(vt))
    coeffs = np.polyfit(x, vt, 2)
    a = coeffs[0]
    r = np.corrcoef(x, vt)[0, 1]
    vrange = vt.max() - vt.min()
    if vrange < 1e-6:
        return "FLAT"
    if abs(a) < 1e-8:
        return "LINEAR"
    if a > 0:
        return "CONVEX (accelerating)"
    else:
        return "CONCAVE (decelerating)"

def detect_locks(X, carriers, threshold=0.15):
    """Detect near-constant log-ratios"""
    D = X.shape[1]
    locks = []
    for i in range(D):
        for j in range(i + 1, D):
            lr = np.log(X[:, i] / X[:, j])
            sd = np.std(lr, ddof=0)
            if sd < threshold:
                locks.append({
                    'pair': f"{carriers[i]}/{carriers[j]}",
                    'sd': round(sd, 6),
                    'mean': round(np.mean(lr), 6)
                })
    locks.sort(key=lambda l: l['sd'])
    return locks

def fingerprint_geometry(C, carriers):
    """Compute fingerprint polygon from CLR of last time step"""
    c = C[-1]
    D = len(c)
    mn, mx = c.min(), c.max()
    rng = mx - mn if mx - mn > 1e-12 else 1
    norm = (c - mn) / rng
    angles = np.linspace(0, 2 * np.pi, D, endpoint=False)
    vx = norm * np.cos(angles)
    vy = norm * np.sin(angles)
    area = 0.5 * abs(sum(vx[i] * vy[(i+1) % D] - vx[(i+1) % D] * vy[i] for i in range(D)))
    perim = sum(np.sqrt((vx[(i+1) % D] - vx[i])**2 + (vy[(i+1) % D] - vy[i])**2) for i in range(D))
    compact = 4 * np.pi * area / (perim ** 2) if perim > 0 else 0
    axes = {carriers[i]: round(norm[i], 6) for i in range(D)}
    return {
        'area': round(area, 6),
        'perimeter': round(perim, 6),
        'compactness': round(compact, 6),
        'axes': axes
    }

def amalgamation_test(X, carriers, schemes):
    """Test classification stability under amalgamation"""
    results = []
    # Base classification
    vt_base = cumulative_variance(X)
    shape_base = classify_shape(vt_base)
    tv_base = total_variance(variation_matrix(X))

    for scheme_name, groups in schemes.items():
        # Build amalgamated composition
        new_carriers = []
        col_indices = []
        for gname, members in groups.items():
            new_carriers.append(gname)
            idxs = [carriers.index(m) for m in members if m in carriers]
            col_indices.append(idxs)

        X_amal = np.zeros((X.shape[0], len(new_carriers)))
        for g, idxs in enumerate(col_indices):
            for idx in idxs:
                X_amal[:, g] += X[:, idx]

        # Replace zeros
        X_amal = np.where(X_amal <= 0, EPSILON, X_amal)

        vt_amal = cumulative_variance(X_amal)
        shape_amal = classify_shape(vt_amal)
        tv_amal = total_variance(variation_matrix(X_amal))

        results.append({
            'scheme': scheme_name,
            'groups': {k: v for k, v in groups.items()},
            'new_D': len(new_carriers),
            'shape_original': shape_base,
            'shape_amalgamated': shape_amal,
            'shape_preserved': shape_base == shape_amal,
            'total_variance_original': round(tv_base, 6),
            'total_variance_amalgamated': round(tv_amal, 6)
        })

    return results

def decimation_test(X, ratios=[2, 4, 8]):
    """Test entropy invariance under temporal decimation"""
    H_full = np.mean([shannon_entropy(X[i]) for i in range(X.shape[0])])
    Ie_full = np.mean([aitchison_norm(X[i]) for i in range(X.shape[0])])

    results = []
    for r in ratios:
        X_dec = X[::r]
        if X_dec.shape[0] < 2:
            continue
        H_dec = np.mean([shannon_entropy(X_dec[i]) for i in range(X_dec.shape[0])])
        Ie_dec = np.mean([aitchison_norm(X_dec[i]) for i in range(X_dec.shape[0])])

        results.append({
            'decimation_ratio': r,
            'observations_remaining': X_dec.shape[0],
            'entropy_full': round(H_full, 6),
            'entropy_decimated': round(H_dec, 6),
            'entropy_change_pct': round(100 * abs(H_dec - H_full) / H_full, 4),
            'aitchison_norm_full': round(Ie_full, 6),
            'aitchison_norm_decimated': round(Ie_dec, 6),
            'norm_change_pct': round(100 * abs(Ie_dec - Ie_full) / Ie_full, 4) if Ie_full > 1e-12 else 0
        })

    return results


# ============================================================
# DEFINE AMALGAMATION SCHEMES (same for all countries)
# ============================================================

def get_amalgamation_schemes(carriers):
    """Build amalgamation schemes based on available carriers"""
    schemes = {}

    has_other_renew = "Other Renewables" in carriers

    # Scheme 1: Fossil vs Clean
    fossil_members = [c for c in ["Coal", "Gas", "Other Fossil"] if c in carriers]
    clean_members = [c for c in ["Nuclear", "Hydro", "Wind", "Solar", "Bioenergy", "Other Renewables"] if c in carriers]
    schemes["Binary: Fossil vs Clean"] = {
        "Fossil": fossil_members,
        "Clean": clean_members
    }

    # Scheme 2: Fossil / Nuclear / Renewable
    renew_members = [c for c in ["Hydro", "Wind", "Solar", "Bioenergy", "Other Renewables"] if c in carriers]
    schemes["Ternary: Fossil/Nuclear/Renewable"] = {
        "Fossil": fossil_members,
        "Nuclear": ["Nuclear"],
        "Renewable": renew_members
    }

    # Scheme 3: Coal / Gas / Other Fossil / Nuclear / Hydro / VRE / Other Clean
    vre = [c for c in ["Wind", "Solar"] if c in carriers]
    other_clean = [c for c in ["Bioenergy", "Other Renewables"] if c in carriers]
    schemes["7-group: detailed"] = {
        "Coal": ["Coal"],
        "Gas": ["Gas"],
        "Other Fossil": ["Other Fossil"],
        "Nuclear": ["Nuclear"],
        "Hydro": ["Hydro"],
        "VRE": vre,
        "Other Clean": other_clean if other_clean else ["Bioenergy"]
    }

    # Scheme 4: Thermal / Non-thermal
    thermal = [c for c in ["Coal", "Gas", "Other Fossil", "Nuclear", "Bioenergy"] if c in carriers]
    non_thermal = [c for c in ["Hydro", "Wind", "Solar", "Other Renewables"] if c in carriers]
    schemes["Binary: Thermal vs Non-thermal"] = {
        "Thermal": thermal,
        "Non-thermal": non_thermal
    }

    return schemes


# ============================================================
# RUN FULL PIPELINE ON ONE COUNTRY
# ============================================================

def run_country(iso, name):
    """Complete Hs pipeline for one country"""
    print(f"\n{'='*70}")
    print(f"  {name} ({iso})")
    print(f"{'='*70}")

    years, carriers, raw = load_country(iso, name)
    N, D = raw.shape

    print(f"  Carriers ({D}): {', '.join(carriers)}")
    print(f"  Years: {years[0]}-{years[-1]} ({N} observations)")

    # Stage S: Closure
    X = closure(raw)
    closure_check = np.max(np.abs(X.sum(axis=1) - 1))
    print(f"  Closure check: max|sum-1| = {closure_check:.2e}")

    # Stage C: CLR Transform
    C = clr(X)
    clr_check = np.max(np.abs(C.sum(axis=1)))
    print(f"  CLR check: max|sum| = {clr_check:.2e}")

    # CLR values at key years
    clr_table = {}
    for t in range(N):
        clr_table[years[t]] = {carriers[i]: round(C[t, i], 6) for i in range(D)}

    # Stage V: Variation matrix and cumulative variance
    T = variation_matrix(X)
    tv = total_variance(T)
    vt = cumulative_variance(X)
    print(f"  Total variance: {tv:.6f}")

    # Variation matrix as labeled dict
    var_matrix = {}
    for i in range(D):
        var_matrix[carriers[i]] = {carriers[j]: round(T[i, j], 6) for j in range(D)}

    # V(t) trajectory
    vt_trajectory = {years[t+1]: round(vt[t], 6) for t in range(len(vt))}

    # Stage T: Shape classification
    shape = classify_shape(vt)
    # Also compute R-squared of quadratic fit
    x_fit = np.arange(len(vt))
    coeffs = np.polyfit(x_fit, vt, 2)
    vt_pred = np.polyval(coeffs, x_fit)
    ss_res = np.sum((vt - vt_pred) ** 2)
    ss_tot = np.sum((vt - np.mean(vt)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    print(f"  V(t) shape: {shape} (R² = {r_squared:.4f})")

    # Stage L: Lock detection
    locks = detect_locks(X, carriers)
    print(f"  Locks found: {len(locks)}")

    # Stage P: Pair stability
    pairs = pair_stability(X, carriers)
    print(f"  Most stable pair: {pairs[0]['pair']} (CV = {pairs[0]['cv']})")
    print(f"  Least stable pair: {pairs[-1]['pair']} (CV = {pairs[-1]['cv']})")

    # Fingerprint geometry
    fg = fingerprint_geometry(C, carriers)
    print(f"  Fingerprint: area={fg['area']:.4f}, compactness={fg['compactness']:.4f}")

    # Entropy and Aitchison norm trajectories
    entropy_traj = {years[t]: round(shannon_entropy(X[t]), 6) for t in range(N)}
    norm_traj = {years[t]: round(aitchison_norm(X[t]), 6) for t in range(N)}

    # Path metrics
    path_length = sum(aitchison_distance(X[t], X[t+1]) for t in range(N-1))
    net_dist = aitchison_distance(X[0], X[-1])
    path_eff = net_dist / path_length if path_length > 1e-12 else 0
    print(f"  Aitchison path: length={path_length:.4f}, net={net_dist:.4f}, efficiency={path_eff:.4f}")

    # Year-over-year Aitchison distances
    yoy_distances = {}
    for t in range(N - 1):
        yoy_distances[f"{years[t]}-{years[t+1]}"] = round(aitchison_distance(X[t], X[t+1]), 6)

    # Amalgamation test
    schemes = get_amalgamation_schemes(carriers)
    amal_results = amalgamation_test(raw, carriers, schemes)
    amal_pass = all(r['shape_preserved'] for r in amal_results)
    print(f"  Amalgamation test: {'ALL PASS' if amal_pass else 'SOME FAIL'} ({len(amal_results)} schemes)")

    # Decimation test
    dec_results = decimation_test(X)
    max_entropy_change = max(r['entropy_change_pct'] for r in dec_results) if dec_results else 0
    print(f"  Decimation test: max entropy change = {max_entropy_change:.2f}%")

    # Dominant carrier at each year
    dominant = {years[t]: carriers[np.argmax(X[t])] for t in range(N)}

    # Composition at first and last year
    comp_first = {carriers[i]: round(X[0, i] * 100, 2) for i in range(D)}
    comp_last = {carriers[i]: round(X[-1, i] * 100, 2) for i in range(D)}

    # Build result
    result = OrderedDict()
    result['country'] = name
    result['iso'] = iso
    result['carriers'] = carriers
    result['D'] = D
    result['simplex'] = f"S^{D-1}"
    result['years'] = years
    result['N'] = N
    result['composition_first_year_pct'] = comp_first
    result['composition_last_year_pct'] = comp_last
    result['dominant_carrier_by_year'] = dominant
    result['clr_coordinates'] = clr_table
    result['variation_matrix'] = var_matrix
    result['total_variance'] = round(tv, 6)
    result['cumulative_variance_trajectory'] = vt_trajectory
    result['vt_shape'] = shape
    result['vt_r_squared'] = round(r_squared, 6)
    result['locks'] = locks
    result['pair_stability_ranked'] = pairs
    result['fingerprint'] = fg
    result['entropy_trajectory'] = entropy_traj
    result['aitchison_norm_trajectory'] = norm_traj
    result['aitchison_path_length'] = round(path_length, 6)
    result['aitchison_net_distance'] = round(net_dist, 6)
    result['path_efficiency'] = round(path_eff, 6)
    result['yoy_aitchison_distances'] = yoy_distances
    result['amalgamation_test'] = amal_results
    result['amalgamation_all_pass'] = amal_pass
    result['decimation_test'] = dec_results
    result['max_entropy_change_pct'] = round(max_entropy_change, 4)
    result['closure_check'] = f"{closure_check:.2e}"
    result['clr_sum_check'] = f"{clr_check:.2e}"

    return result


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("Hs-M02: EMBER Electricity Generation")
print("Full CoDaWork 2026 Reference Experiment")
print("=" * 70)

all_results = OrderedDict()
all_results['experiment'] = 'Hs-M02'
all_results['title'] = 'EMBER Electricity Generation — CoDaWork 2026 Reference'
all_results['date'] = '2026-04-29'
all_results['series'] = 'M-series (Manifold Projection Systems)'
all_results['data_source'] = 'EMBER Global Electricity Review 2025'
all_results['data_url'] = 'https://ember-climate.org/data/'
all_results['methodology'] = 'Higgins Decomposition (Hs) v3.0 — deterministic 12-step diagnostic on Aitchison simplex'
all_results['epsilon'] = EPSILON
all_results['countries'] = {}

summary_rows = []

for iso, name in COUNTRIES:
    result = run_country(iso, name)
    all_results['countries'][iso] = result
    summary_rows.append({
        'country': name,
        'iso': iso,
        'D': result['D'],
        'N': result['N'],
        'total_variance': result['total_variance'],
        'vt_shape': result['vt_shape'],
        'r_squared': result['vt_r_squared'],
        'locks': len(result['locks']),
        'most_stable_pair': result['pair_stability_ranked'][0]['pair'],
        'path_efficiency': result['path_efficiency'],
        'fingerprint_compactness': result['fingerprint']['compactness'],
        'amalgamation_pass': result['amalgamation_all_pass'],
        'max_entropy_change': result['max_entropy_change_pct']
    })

all_results['summary'] = summary_rows

# Print summary table
print("\n")
print("=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
print(f"\n{'Country':<20s} {'D':>3s} {'TotVar':>8s} {'Shape':<25s} {'R²':>6s} {'Locks':>5s} {'PathEff':>8s} {'Amal':>5s}")
print("-" * 80)
for r in summary_rows:
    print(f"{r['country']:<20s} {r['D']:>3d} {r['total_variance']:>8.4f} {r['vt_shape']:<25s} {r['r_squared']:>6.4f} {r['locks']:>5d} {r['path_efficiency']:>8.4f} {'PASS' if r['amalgamation_pass'] else 'FAIL':>5s}")

# Save JSON
out_path = os.path.join(OUT_DIR, "Hs-M02_results.json")
with open(out_path, 'w') as f:
    json.dump(all_results, f, indent=2, default=str)
print(f"\nResults saved to {out_path}")

# Also save per-country CSVs of CLR coordinates
for iso, name in COUNTRIES:
    result = all_results['countries'][iso]
    csv_path = os.path.join(OUT_DIR, f"Hs-M02_{iso}_clr.csv")
    with open(csv_path, 'w') as f:
        carriers = result['carriers']
        f.write("Year," + ",".join(carriers) + "\n")
        for year in result['years']:
            vals = [str(result['clr_coordinates'][year][c]) for c in carriers]
            f.write(f"{year}," + ",".join(vals) + "\n")

print("\nPer-country CLR CSV files saved.")
print("\nDONE.")
