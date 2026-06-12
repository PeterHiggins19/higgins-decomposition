#!/usr/bin/env python3
"""
Tr × BASIS × STEP EXPERIMENT
==============================
Tagged diagnostics for the Trace operator under all three log-ratio
bases (CLR, ILR, ALR), mapped 1-to-1 with the three downstream
pipeline steps: T (SuperSqueeze/HTP), C (HVLD), E (EITT).

9 combinations × 3 datasets = 27 cells.

Every diagnostic is tagged:
  [Step.N]   — pipeline step number
  [Op.NAME]  — operation name (e.g., Op.CLR, Op.HVLD, Op.EITT)

Author: Peter Higgins / Claude
Date: 2026-04-30
"""

import numpy as np
from itertools import product
np.random.seed(42)

ZERO_DELTA = 1e-6

TRANSCENDENTAL_CONSTANTS = {
    "π": np.pi, "1/π": 1/np.pi, "e": np.e, "1/e": 1/np.e,
    "ln2": np.log(2), "φ": (1+np.sqrt(5))/2, "1/φ": 2/(1+np.sqrt(5)),
    "√2": np.sqrt(2), "1/√2": 1/np.sqrt(2), "√3": np.sqrt(3),
    "γ": 0.5772156649015329, "π/4": np.pi/4, "π²/6": np.pi**2/6,
    "catalan": 0.9159655941772190, "ln10": np.log(10),
    "2π": 2*np.pi, "e^π": np.e**np.pi, "π^e": np.pi**np.e,
    "√5": np.sqrt(5), "ln_φ": np.log((1+np.sqrt(5))/2),
    "apéry": 1.2020569031595942, "khinchin": 2.6854520010653064,
    "feigenbaum_δ": 4.6692016091029906, "feigenbaum_α": 2.5029078750958928,
}

# ══════════════════════════════════════════════════════════════
# [Step.1] [Op.GENERATE] — Data Generation
# ══════════════════════════════════════════════════════════════

def nuclear_semf(N=92):
    """[Step.1] [Op.GENERATE] Nuclear SEMF binding energy (D=3)"""
    a_v, a_s, a_c, a_sym, a_p = 15.56, 17.23, 0.7, 23.285, 12.0
    data = np.zeros((N, 3))
    for Z in range(1, N+1):
        A = 2*Z
        vol = a_v * A
        sc = a_s * A**(2/3) + a_c * Z*(Z-1) / A**(1/3)
        sp = a_sym * (A-2*Z)**2 / A + abs(a_p / A**0.5 * ((-1)**Z + (-1)**(A-Z)) / 2)
        total = vol + sc + sp
        data[Z-1] = [vol/total, sc/total, sp/total]
    return data

def energy_mix(N=25):
    """[Step.1] [Op.GENERATE] Global energy mix (D=7)"""
    np.random.seed(42)
    data = np.zeros((N, 7))
    for t in range(N):
        coal = max(5, 50 - 2.0*t + np.random.normal(0, 1))
        gas = 10 + 0.3*t + np.random.normal(0, 0.5)
        nuc = max(1, 30 - 1.5*t) if (2000+t) < 2023 else 0.5
        hydro = 4 + np.random.normal(0, 0.3)
        wind = 1 + 1.5*t + 0.05*t**1.3
        solar = max(0.1, 0.5*t - 2)
        other = 3 + np.random.normal(0, 0.2)
        data[t] = [coal, gas, nuc, hydro, wind, solar, other]
    return np.abs(data)

def adversarial(N=50, D=5):
    """[Step.1] [Op.GENERATE] Adversarial Dirichlet (D=5)"""
    return np.random.dirichlet(np.ones(D), size=N)

# ══════════════════════════════════════════════════════════════
# [Step.2] [Op.CLOSE] — Simplex Closure
# ══════════════════════════════════════════════════════════════

def close_simplex(data):
    """[Step.2] [Op.CLOSE] Multiplicative zero replacement + closure"""
    d = data.copy().astype(float)
    mask = d <= 0
    d[mask] = ZERO_DELTA
    for i in range(d.shape[0]):
        n_rep = mask[i].sum()
        if 0 < n_rep < d.shape[1]:
            td = n_rep * ZERO_DELTA
            nm = ~mask[i]
            d[i, nm] *= (1.0 - td) / d[i, nm].sum()
            d[i, mask[i]] = ZERO_DELTA
    return d / d.sum(axis=1, keepdims=True)

# ══════════════════════════════════════════════════════════════
# [Step.3] [Op.CLR / Op.ILR / Op.ALR] — Log-Ratio Transforms
# ══════════════════════════════════════════════════════════════

def transform_clr(simplex):
    """[Step.3] [Op.CLR] Centered log-ratio: clr_j = ln(x_j) - (1/D)Σln(x_k)
    Maps S^(D-1) → ℝ^D  (rank D-1, sum-to-zero constraint)"""
    log_d = np.log(simplex)
    return log_d - log_d.mean(axis=1, keepdims=True)

def helmert_basis(D):
    """Helmert sub-composition matrix Ψ: D × (D-1)
    Orthonormal basis for the CLR hyperplane."""
    Psi = np.zeros((D, D-1))
    for j in range(D-1):
        k = j + 1
        Psi[:j+1, j] = 1.0 / k
        Psi[j+1, j] = -1.0
        Psi[:, j] *= np.sqrt(k / (k + 1))
    return Psi

def transform_ilr(simplex):
    """[Step.3] [Op.ILR] Isometric log-ratio: ilr = clr · Ψ (Helmert)
    Maps S^(D-1) → ℝ^(D-1)  (isometry of Aitchison inner product)"""
    D = simplex.shape[1]
    clr_data = transform_clr(simplex)
    Psi = helmert_basis(D)
    return clr_data @ Psi  # N × (D-1)

def transform_alr(simplex, ref=-1):
    """[Step.3] [Op.ALR] Additive log-ratio: alr_j = ln(x_j / x_ref)
    Maps S^(D-1) → ℝ^(D-1)  (non-isometric, reference-dependent)"""
    D = simplex.shape[1]
    log_d = np.log(simplex)
    ref_col = log_d[:, ref]
    indices = [i for i in range(D) if i != (D + ref if ref < 0 else ref)]
    return log_d[:, indices] - ref_col[:, np.newaxis]  # N × (D-1)

BASES = {
    "CLR": transform_clr,
    "ILR": transform_ilr,
    "ALR": transform_alr,
}

# ══════════════════════════════════════════════════════════════
# [Step.4] [Op.COV] — Covariance + Trace Extraction
# ══════════════════════════════════════════════════════════════

def compute_trace_trajectory(transformed_data, label=""):
    """[Step.4] [Op.COV] + [Step.5] [Op.TRACE]
    Cumulative covariance V(t) and its trace Tr(V(t)) = σ²(t)"""
    N, K = transformed_data.shape  # K = D for CLR, D-1 for ILR/ALR
    traces = np.zeros(N)
    for t in range(2, N):
        window = transformed_data[:t+1]
        V = np.cov(window.T)
        traces[t] = np.trace(V)
    return traces

# ══════════════════════════════════════════════════════════════
# [Step.6] [Op.HTP] — T: SuperSqueeze / Transcendental Proximity
# ══════════════════════════════════════════════════════════════

def step_T_supersqueeze(traces):
    """[Step.6] [Op.HTP] Test Tr(t) against transcendental constant library.
    Returns: match_count, closest_constant, closest_delta, closest_t"""
    valid = traces[2:]
    matches = []
    for idx, tr_val in enumerate(valid):
        if tr_val <= 0:
            continue
        for name, cval in TRANSCENDENTAL_CONSTANTS.items():
            if cval <= 0:
                continue
            for test_val, lbl in [(tr_val, "direct"), (1/tr_val if tr_val > 1e-10 else 0, "recip")]:
                if test_val <= 0:
                    continue
                delta = abs(test_val - cval)
                if delta < 0.01:
                    matches.append({
                        "t": int(idx + 2),
                        "tr": float(tr_val),
                        "const": f"{lbl}:{name}",
                        "cval": float(cval),
                        "delta": float(delta),
                    })
    matches.sort(key=lambda m: m["delta"])
    closest = matches[0] if matches else None
    return {
        "match_count": len(matches),
        "closest_const": closest["const"] if closest else "—",
        "closest_delta": closest["delta"] if closest else float('inf'),
        "closest_t": closest["t"] if closest else -1,
        "closest_tr": closest["tr"] if closest else 0.0,
    }

# ══════════════════════════════════════════════════════════════
# [Step.7] [Op.HVLD] — C: Vertex Lock Diagnostic (Quadratic Fit)
# ══════════════════════════════════════════════════════════════

def step_C_hvld(traces):
    """[Step.7] [Op.HVLD] Fit quadratic y = at² + bt + c to Tr(t).
    Returns: a, b, c, R², shape, vertex_x, vertex_y"""
    N = len(traces)
    valid_idx = np.arange(2, N)
    x = valid_idx.astype(float)
    y = traces[valid_idx]

    if len(x) < 3:
        return {"a": 0, "b": 0, "c": 0, "R2": 0, "shape": "N/A",
                "vertex_x": 0, "vertex_y": 0}

    coeffs = np.polyfit(x, y, 2)
    a, b, c = coeffs
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    vx = -b / (2 * a) if abs(a) > 1e-15 else 0.0
    vy = c - b**2 / (4 * a) if abs(a) > 1e-15 else c

    return {
        "a": float(a),
        "b": float(b),
        "c": float(c),
        "R2": float(R2),
        "shape": "bowl" if a > 0 else "hill",
        "vertex_x": float(vx),
        "vertex_y": float(vy),
    }

# ══════════════════════════════════════════════════════════════
# [Step.8] [Op.EITT] — E: Entropy Invariance Under Decimation
# ══════════════════════════════════════════════════════════════

def step_E_eitt(simplex_data, transform_fn):
    """[Step.8] [Op.EITT] Decimate simplex → re-transform → re-trace → compare.
    Tests whether Tr survives geometric-mean coarse-graining.
    Returns: Tr_original_final, Tr_decimated_final, variation_pct, pass/fail"""
    N, D = simplex_data.shape
    factor = 2
    if N < factor * 4:
        return {"tr_orig": 0, "tr_dec": 0, "variation_pct": 0, "eitt_pass": True,
                "H_orig": 0, "H_dec": 0, "H_var_pct": 0}

    # Original trace
    orig_transformed = transform_fn(simplex_data)
    tr_orig = compute_trace_trajectory(orig_transformed)
    tr_orig_final = tr_orig[-1]

    # Decimate: geometric mean in blocks of `factor`
    n_trim = (N // factor) * factor
    reshaped = simplex_data[:n_trim].reshape(-1, factor, D)
    geo_mean = np.exp(np.log(reshaped + 1e-30).mean(axis=1))
    geo_mean = geo_mean / geo_mean.sum(axis=1, keepdims=True)

    # Re-transform and re-trace
    dec_transformed = transform_fn(geo_mean)
    tr_dec = compute_trace_trajectory(dec_transformed)
    tr_dec_final = tr_dec[-1] if len(tr_dec) > 2 else 0

    # Variation
    var_pct = abs(tr_orig_final - tr_dec_final) / tr_orig_final * 100 if tr_orig_final > 1e-15 else 0

    # Also Shannon entropy comparison
    H_max = np.log(D) if D > 1 else 1
    def shannon(s):
        h = np.zeros(len(s))
        for i in range(len(s)):
            p = s[i][s[i] > 0]
            h[i] = -np.sum(p * np.log(p))
        return h / H_max

    H_orig = shannon(simplex_data[:n_trim]).mean()
    H_dec = shannon(geo_mean).mean()
    H_var = abs(H_orig - H_dec) / H_orig * 100 if H_orig > 1e-15 else 0

    return {
        "tr_orig": float(tr_orig_final),
        "tr_dec": float(tr_dec_final),
        "variation_pct": float(var_pct),
        "eitt_pass": var_pct < 15.0,
        "H_orig": float(H_orig),
        "H_dec": float(H_dec),
        "H_var_pct": float(H_var),
    }


# ══════════════════════════════════════════════════════════════
# MAIN EXPERIMENT
# ══════════════════════════════════════════════════════════════

def run_experiment():
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║   Tr × {CLR, ILR, ALR} × {T, C, E}  EXPERIMENT                        ║")
    print("║   Tagged Pipeline Diagnostics — All 27 Combinations                     ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")

    datasets = {
        "Nuclear":     (nuclear_semf(),     "D=3, N=92"),
        "Energy":      (energy_mix(),       "D=7, N=25"),
        "Adversarial": (adversarial(),      "D=5, N=50"),
    }
    basis_names = ["CLR", "ILR", "ALR"]
    step_names  = ["T (HTP)", "C (HVLD)", "E (EITT)"]

    # Storage for the big table
    results = {}  # (dataset, basis, step) → dict of values

    for ds_name, (raw_data, ds_desc) in datasets.items():
        print(f"\n{'═'*75}")
        print(f"  DATASET: {ds_name} ({ds_desc})")
        print(f"{'═'*75}")

        # [Step.2] [Op.CLOSE]
        simplex = close_simplex(raw_data)
        N, D = simplex.shape
        print(f"  [Step.2] [Op.CLOSE] → S^({D-1}), N={N}")

        for basis_name in basis_names:
            transform_fn = BASES[basis_name]

            # [Step.3] [Op.{BASIS}]
            transformed = transform_fn(simplex)
            K = transformed.shape[1]
            print(f"\n  [Step.3] [Op.{basis_name}] → ℝ^{K}  (rank {'D-1='+str(D-1) if basis_name == 'CLR' else str(K)})")

            # [Step.4-5] [Op.COV] + [Op.TRACE]
            traces = compute_trace_trajectory(transformed)
            print(f"  [Step.4] [Op.COV]  → V(t) ∈ Sym_{K}")
            print(f"  [Step.5] [Op.TRACE] Tr(V({N})) = {traces[-1]:.8f}")

            # ── T: SuperSqueeze ──
            t_result = step_T_supersqueeze(traces)
            print(f"  [Step.6] [Op.HTP]  matches={t_result['match_count']}, "
                  f"closest={t_result['closest_const']} (δ={t_result['closest_delta']:.6f})")
            results[(ds_name, basis_name, "T")] = {
                "trace_final": traces[-1],
                "matches": t_result["match_count"],
                "closest": t_result["closest_const"],
                "delta": t_result["closest_delta"],
            }

            # ── C: HVLD ──
            c_result = step_C_hvld(traces)
            print(f"  [Step.7] [Op.HVLD] shape={c_result['shape']}, R²={c_result['R2']:.6f}, "
                  f"vertex=({c_result['vertex_x']:.2f}, {c_result['vertex_y']:.6f})")
            results[(ds_name, basis_name, "C")] = {
                "trace_final": traces[-1],
                "shape": c_result["shape"],
                "R2": c_result["R2"],
                "a": c_result["a"],
                "vertex_x": c_result["vertex_x"],
                "vertex_y": c_result["vertex_y"],
            }

            # ── E: EITT ──
            e_result = step_E_eitt(simplex, transform_fn)
            print(f"  [Step.8] [Op.EITT] Tr_orig={e_result['tr_orig']:.6f}, "
                  f"Tr_dec={e_result['tr_dec']:.6f}, Δ={e_result['variation_pct']:.2f}%, "
                  f"{'PASS' if e_result['eitt_pass'] else 'FAIL'}")
            results[(ds_name, basis_name, "E")] = {
                "trace_final": traces[-1],
                "tr_dec": e_result["tr_dec"],
                "var_pct": e_result["variation_pct"],
                "eitt_pass": e_result["eitt_pass"],
                "H_orig": e_result["H_orig"],
                "H_dec": e_result["H_dec"],
            }

    # ══════════════════════════════════════════════════════════
    # TABLE 1: TRACE VALUES — Basis Invariance Test
    # ══════════════════════════════════════════════════════════
    print(f"\n\n{'═'*75}")
    print(f"  TABLE 1: TRACE VALUES  Tr(V(N)) under each basis")
    print(f"  [Step.5] [Op.TRACE]  — Testing basis invariance: Tr(P⁻¹AP) = Tr(A)")
    print(f"{'═'*75}")
    print(f"\n  {'Dataset':<14} {'CLR':<16} {'ILR':<16} {'ALR':<16} {'CLR≡ILR?':<10} {'CLR≡ALR?':<10}")
    print(f"  {'─'*82}")
    for ds_name in datasets:
        tr_clr = results[(ds_name, "CLR", "T")]["trace_final"]
        tr_ilr = results[(ds_name, "ILR", "T")]["trace_final"]
        tr_alr = results[(ds_name, "ALR", "T")]["trace_final"]
        clr_ilr = "✓ YES" if np.isclose(tr_clr, tr_ilr, rtol=1e-6) else f"✗ Δ={abs(tr_clr-tr_ilr):.2e}"
        clr_alr = "✓ YES" if np.isclose(tr_clr, tr_alr, rtol=1e-6) else f"✗ Δ={abs(tr_clr-tr_alr):.2e}"
        print(f"  {ds_name:<14} {tr_clr:<16.8f} {tr_ilr:<16.8f} {tr_alr:<16.8f} {clr_ilr:<10} {clr_alr:<10}")

    # ══════════════════════════════════════════════════════════
    # TABLE 2: T (SuperSqueeze/HTP) — 3 bases × 3 datasets
    # ══════════════════════════════════════════════════════════
    print(f"\n\n{'═'*75}")
    print(f"  TABLE 2: [Step.6] [Op.HTP] SuperSqueeze — Transcendental Proximity")
    print(f"  Tr(t) tested against {len(TRANSCENDENTAL_CONSTANTS)} constants, δ < 0.01 = match")
    print(f"{'═'*75}")
    print(f"\n  {'Dataset':<14} {'Basis':<6} {'Matches':<10} {'Closest Constant':<20} {'δ':<12}")
    print(f"  {'─'*62}")
    for ds_name in datasets:
        for basis in basis_names:
            r = results[(ds_name, basis, "T")]
            print(f"  {ds_name:<14} {basis:<6} {r['matches']:<10} {r['closest']:<20} {r['delta']:<12.8f}")
        print(f"  {'─'*62}")

    # ══════════════════════════════════════════════════════════
    # TABLE 3: C (HVLD) — 3 bases × 3 datasets
    # ══════════════════════════════════════════════════════════
    print(f"\n\n{'═'*75}")
    print(f"  TABLE 3: [Step.7] [Op.HVLD] Vertex Lock — Quadratic Fit to Tr(t)")
    print(f"  Tr(t) = at² + bt + c → shape, vertex, R²")
    print(f"{'═'*75}")
    print(f"\n  {'Dataset':<14} {'Basis':<6} {'Shape':<7} {'R²':<10} {'a (curv.)':<14} {'Vertex_x':<12} {'Vertex_y':<14}")
    print(f"  {'─'*77}")
    for ds_name in datasets:
        for basis in basis_names:
            r = results[(ds_name, basis, "C")]
            print(f"  {ds_name:<14} {basis:<6} {r['shape']:<7} {r['R2']:<10.6f} {r['a']:<14.6e} {r['vertex_x']:<12.2f} {r['vertex_y']:<14.6f}")
        print(f"  {'─'*77}")

    # ══════════════════════════════════════════════════════════
    # TABLE 4: E (EITT) — 3 bases × 3 datasets
    # ══════════════════════════════════════════════════════════
    print(f"\n\n{'═'*75}")
    print(f"  TABLE 4: [Step.8] [Op.EITT] Entropy Invariance Under 2× Decimation")
    print(f"  Decimate simplex → re-transform → re-trace → compare")
    print(f"{'═'*75}")
    print(f"\n  {'Dataset':<14} {'Basis':<6} {'Tr_orig':<14} {'Tr_dec':<14} {'ΔTr %':<10} {'Pass?':<7} {'H_orig':<10} {'H_dec':<10}")
    print(f"  {'─'*85}")
    for ds_name in datasets:
        for basis in basis_names:
            r = results[(ds_name, basis, "E")]
            p = "✓" if r["eitt_pass"] else "✗"
            print(f"  {ds_name:<14} {basis:<6} {r['trace_final']:<14.6f} {r['tr_dec']:<14.6f} "
                  f"{r['var_pct']:<10.2f} {p:<7} {r['H_orig']:<10.4f} {r['H_dec']:<10.4f}")
        print(f"  {'─'*85}")

    # ══════════════════════════════════════════════════════════
    # TABLE 5: THE 9-CELL SUMMARY — Basis × Step agreement
    # ══════════════════════════════════════════════════════════
    print(f"\n\n{'═'*75}")
    print(f"  TABLE 5: THE 3×3 AGREEMENT MATRIX")
    print(f"  Does the downstream step produce IDENTICAL results across bases?")
    print(f"{'═'*75}")
    print(f"\n  For each (Dataset, Step), check if CLR ≡ ILR ≡ ALR:\n")

    for ds_name in datasets:
        print(f"  {ds_name}:")
        print(f"  {'Step':<12} {'CLR ≡ ILR?':<14} {'CLR ≡ ALR?':<14} {'Diagnosis'}")
        print(f"  {'─'*60}")

        # T agreement
        t_clr = results[(ds_name, "CLR", "T")]
        t_ilr = results[(ds_name, "ILR", "T")]
        t_alr = results[(ds_name, "ALR", "T")]
        t_ci = "✓ SAME" if t_clr["matches"] == t_ilr["matches"] and np.isclose(t_clr["delta"], t_ilr["delta"], rtol=1e-4) else "✗ DIFF"
        t_ca = "✓ SAME" if t_clr["matches"] == t_alr["matches"] and np.isclose(t_clr["delta"], t_alr["delta"], rtol=1e-4) else "✗ DIFF"
        t_diag = "Basis-invariant" if "SAME" in t_ci and "SAME" in t_ca else ("ILR-invariant only" if "SAME" in t_ci else "Basis-dependent")
        print(f"  {'T (HTP)':<12} {t_ci:<14} {t_ca:<14} {t_diag}")

        # C agreement
        c_clr = results[(ds_name, "CLR", "C")]
        c_ilr = results[(ds_name, "ILR", "C")]
        c_alr = results[(ds_name, "ALR", "C")]
        c_ci = "✓ SAME" if c_clr["shape"] == c_ilr["shape"] and np.isclose(c_clr["R2"], c_ilr["R2"], rtol=1e-4) else "✗ DIFF"
        c_ca = "✓ SAME" if c_clr["shape"] == c_alr["shape"] and np.isclose(c_clr["R2"], c_alr["R2"], rtol=1e-4) else "✗ DIFF"
        c_diag = "Basis-invariant" if "SAME" in c_ci and "SAME" in c_ca else ("ILR-invariant only" if "SAME" in c_ci else "Basis-dependent")
        print(f"  {'C (HVLD)':<12} {c_ci:<14} {c_ca:<14} {c_diag}")

        # E agreement
        e_clr = results[(ds_name, "CLR", "E")]
        e_ilr = results[(ds_name, "ILR", "E")]
        e_alr = results[(ds_name, "ALR", "E")]
        e_ci = "✓ SAME" if np.isclose(e_clr["var_pct"], e_ilr["var_pct"], atol=0.5) else "✗ DIFF"
        e_ca = "✓ SAME" if np.isclose(e_clr["var_pct"], e_alr["var_pct"], atol=0.5) else "✗ DIFF"
        e_diag = "Basis-invariant" if "SAME" in e_ci and "SAME" in e_ca else ("ILR-invariant only" if "SAME" in e_ci else "Basis-dependent")
        print(f"  {'E (EITT)':<12} {e_ci:<14} {e_ca:<14} {e_diag}")
        print()

    # ══════════════════════════════════════════════════════════
    # SYNTHESIS
    # ══════════════════════════════════════════════════════════
    print(f"\n{'═'*75}")
    print(f"  SYNTHESIS: What the 3×3 experiment reveals")
    print(f"{'═'*75}")
    print(f"""
  TAG LEGEND:
    [Step.1] [Op.GENERATE] — Raw data generation
    [Step.2] [Op.CLOSE]    — Simplex closure (zero replacement)
    [Step.3] [Op.CLR]      — Centered log-ratio transform
    [Step.3] [Op.ILR]      — Isometric log-ratio transform (Helmert)
    [Step.3] [Op.ALR]      — Additive log-ratio transform (ref=last)
    [Step.4] [Op.COV]      — Cumulative covariance matrix V(t)
    [Step.5] [Op.TRACE]    — Trace extraction Tr: Sym_K → ℝ
    [Step.6] [Op.HTP]      — Transcendental proximity test (SuperSqueeze)
    [Step.7] [Op.HVLD]     — Vertex Lock diagnostic (quadratic fit)
    [Step.8] [Op.EITT]     — Entropy invariance under decimation

  THEORY PREDICTION:
    CLR ≡ ILR: Tr(Ψᵀ·Cov_CLR·Ψ) = Tr(Cov_CLR) because Ψ is orthonormal
               and Cov_CLR is already rank D-1. Isometry preserves trace.
    CLR ≢ ALR: ALR uses non-orthogonal projection. Tr(A·Cov·Aᵀ) ≠ Tr(Cov)
               unless A is orthogonal. ALR's A is not.

  CONSEQUENCE:
    If CLR ≡ ILR across all steps → the pipeline IS coordinate-free
    (within the Aitchison isometry class).

    If ALR ≠ CLR → ALR breaks the trace invariance, and downstream
    operators T, C, E will see DIFFERENT trajectories. The shape (bowl/hill)
    may survive, but the numerical values shift.

    This is why CLR/ILR are the natural bases for Hˢ.
    ALR introduces a reference-carrier bias that Trace does not absorb.
""")


if __name__ == "__main__":
    run_experiment()
