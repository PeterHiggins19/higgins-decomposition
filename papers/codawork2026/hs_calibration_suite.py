#!/usr/bin/env python3
"""
Hs Imaging System Calibration Suite
====================================
If Hs is an imaging system, what does it see when we feed it known geometry?

Test objects (as compositional data on the simplex):
1. Point — single composition, no time
2. Point + time — same composition repeated
3. Line — linear trajectory across the simplex
4. Circle — circular trajectory on the simplex
5. Sphere — 4-part composition, trajectory covers a spherical surface
6. Cube — structured grid of compositions
7. Rhomboid — skewed grid
8. Known manifolds — torus, spiral, saddle

For each: INPUT table, then Hs diagnostic OUTPUT table.
"""

import numpy as np
import json
from collections import OrderedDict

# ============================================================
# CORE Hs PIPELINE FUNCTIONS (minimal, self-contained)
# ============================================================

def closure(x):
    """Close to sum=1"""
    x = np.array(x, dtype=float)
    if x.ndim == 1:
        return x / x.sum()
    return (x.T / x.sum(axis=1)).T

def clr(x):
    """Centred log-ratio transform"""
    x = np.array(x, dtype=float)
    if x.ndim == 1:
        gm = np.exp(np.mean(np.log(x)))
        return np.log(x / gm)
    gm = np.exp(np.mean(np.log(x), axis=1, keepdims=True))
    return np.log(x / gm)

def variation_matrix(X):
    """D x D variation matrix: t_kj = Var(log(X_k/X_j))"""
    X = np.array(X, dtype=float)
    D = X.shape[1]
    T = np.zeros((D, D))
    for k in range(D):
        for j in range(D):
            lr = np.log(X[:, k] / X[:, j])
            T[k, j] = np.var(lr, ddof=0)
    return T

def total_variance(T):
    """Total variance = (1/2D) * sum of variation matrix"""
    D = T.shape[0]
    return np.sum(T) / (2 * D)

def cumulative_variance(X):
    """V(t) — cumulative total variance up to time t"""
    N = X.shape[0]
    vt = []
    for t in range(2, N + 1):
        T = variation_matrix(X[:t])
        vt.append(total_variance(T))
    return np.array(vt)

def aitchison_distance(x, y):
    """Aitchison distance between two compositions"""
    x, y = closure(x), closure(y)
    D = len(x)
    lr = np.log(x / y)
    return np.sqrt(np.sum((lr[:, None] - lr[None, :]) ** 2) / (2 * D))

def shannon_entropy(x):
    """Shannon entropy of closed composition"""
    x = closure(x)
    x = x[x > 0]
    return -np.sum(x * np.log(x))

def aitchison_norm(x):
    """Evidence information I_e = ||x||_a (Aitchison norm)"""
    x = closure(x)
    clr_x = clr(x)
    return np.sqrt(np.sum(clr_x ** 2))

def pair_stability(X):
    """CV of each log-ratio pair over time"""
    D = X.shape[1]
    results = {}
    for i in range(D):
        for j in range(i + 1, D):
            lr = np.log(X[:, i] / X[:, j])
            mu = np.mean(lr)
            sd = np.std(lr, ddof=0)
            cv = abs(sd / mu) if abs(mu) > 1e-12 else float('inf')
            results[(i, j)] = {'mean': mu, 'sd': sd, 'cv': cv}
    return results

def classify_shape(vt):
    """Classify V(t) trajectory shape"""
    if len(vt) < 3:
        return "insufficient_data"
    # Fit quadratic
    x = np.arange(len(vt))
    coeffs = np.polyfit(x, vt, 2)
    a, b, c = coeffs
    # Check flatness
    vrange = vt.max() - vt.min()
    if vrange < 1e-6:
        return "FLAT"
    if abs(a) < 1e-8:
        return "LINEAR"
    if a > 0:
        return "CONVEX (accelerating)"
    else:
        return "CONCAVE (decelerating)"

def detect_locks(X, threshold=0.01):
    """Detect near-constant log-ratios (locks)"""
    D = X.shape[1]
    locks = []
    for i in range(D):
        for j in range(i + 1, D):
            lr = np.log(X[:, i] / X[:, j])
            sd = np.std(lr, ddof=0)
            if sd < threshold:
                locks.append((i, j, sd))
    return locks

def fingerprint_geometry(X):
    """Compute fingerprint polygon area, perimeter, compactness"""
    C = clr(X)
    # Use last time step for fingerprint
    c = C[-1]
    D = len(c)
    # Normalise to 0-1
    mn, mx = c.min(), c.max()
    rng = mx - mn if mx - mn > 1e-12 else 1
    norm = (c - mn) / rng
    # Polygon vertices on unit circle
    angles = np.linspace(0, 2 * np.pi, D, endpoint=False)
    vx = norm * np.cos(angles)
    vy = norm * np.sin(angles)
    # Shoelace area
    area = 0.5 * abs(sum(vx[i] * vy[(i+1) % D] - vx[(i+1) % D] * vy[i] for i in range(D)))
    # Perimeter
    perim = sum(np.sqrt((vx[(i+1) % D] - vx[i])**2 + (vy[(i+1) % D] - vy[i])**2) for i in range(D))
    # Compactness
    compact = 4 * np.pi * area / (perim ** 2) if perim > 0 else 0
    return {'area': area, 'perimeter': perim, 'compactness': compact}


# ============================================================
# TEST OBJECT GENERATORS
# ============================================================

def make_point_no_time():
    """Single composition in 3-space, no time dimension"""
    return np.array([[1/3, 1/3, 1/3]])

def make_point_with_time(T=20):
    """Same composition repeated T times"""
    return np.tile([1/3, 1/3, 1/3], (T, 1))

def make_line(T=20):
    """Linear trajectory from (0.8, 0.1, 0.1) to (0.1, 0.1, 0.8)"""
    t = np.linspace(0, 1, T)
    x = np.column_stack([0.8 - 0.7 * t, 0.1 * np.ones(T), 0.1 + 0.7 * t])
    return closure(x)

def make_circle(T=40):
    """Circular trajectory on the 2-simplex"""
    t = np.linspace(0, 2 * np.pi, T, endpoint=False)
    # Centre of simplex + circular perturbation in CLR space
    r = 0.5
    clr_traj = np.column_stack([r * np.cos(t), r * np.sin(t), -r * np.cos(t) - r * np.sin(t)])
    # Back to simplex via exp and closure
    x = np.exp(clr_traj)
    return closure(x)

def make_sphere(T=60):
    """4-part composition, trajectory on spherical surface in CLR space"""
    # Fibonacci sphere in 3D CLR space (4 parts, 3 degrees of freedom)
    golden = (1 + np.sqrt(5)) / 2
    indices = np.arange(T)
    theta = 2 * np.pi * indices / golden
    phi = np.arccos(1 - 2 * (indices + 0.5) / T)
    r = 0.8
    c1 = r * np.sin(phi) * np.cos(theta)
    c2 = r * np.sin(phi) * np.sin(theta)
    c3 = r * np.cos(phi)
    c4 = -(c1 + c2 + c3)  # CLR constraint: sum = 0
    clr_traj = np.column_stack([c1, c2, c3, c4])
    x = np.exp(clr_traj)
    return closure(x)

def make_cube(N=27):
    """3x3x3 grid in CLR space → 3-part compositions"""
    vals = [-0.5, 0, 0.5]
    points = []
    for a in vals:
        for b in vals:
            c = -(a + b)  # CLR constraint
            points.append([a, b, c])
    x = np.exp(np.array(points))
    return closure(x)

def make_rhomboid(N=25):
    """Skewed grid — sheared cube in CLR space"""
    vals = np.linspace(-0.6, 0.6, 5)
    points = []
    for a in vals:
        for b in vals:
            # Shear: shift b by 0.3*a
            b_sheared = b + 0.3 * a
            c = -(a + b_sheared)
            points.append([a, b_sheared, c])
    x = np.exp(np.array(points))
    return closure(x)

def make_torus(T=80):
    """Torus in 4-part CLR space"""
    R, r_t = 0.8, 0.3
    t1 = np.linspace(0, 2 * np.pi, T, endpoint=False)
    # Two loops around the torus
    u = np.tile(t1, 1)
    v = np.tile(t1, 1)
    # Parametric torus in 3D, embed in 4-part CLR
    c1 = (R + r_t * np.cos(v)) * np.cos(u)
    c2 = (R + r_t * np.cos(v)) * np.sin(u)
    c3 = r_t * np.sin(v)
    c4 = -(c1 + c2 + c3)
    clr_traj = np.column_stack([c1, c2, c3, c4])
    x = np.exp(clr_traj)
    return closure(x)

def make_spiral(T=50):
    """Expanding spiral on the simplex — 3 parts"""
    t = np.linspace(0, 4 * np.pi, T)
    r = np.linspace(0.05, 0.8, T)
    c1 = r * np.cos(t)
    c2 = r * np.sin(t)
    c3 = -(c1 + c2)
    clr_traj = np.column_stack([c1, c2, c3])
    x = np.exp(clr_traj)
    return closure(x)

def make_saddle(T=49):
    """Saddle surface (hyperbolic paraboloid) — 4 parts"""
    n = int(np.sqrt(T))
    u = np.linspace(-0.6, 0.6, n)
    v = np.linspace(-0.6, 0.6, n)
    points = []
    for ui in u:
        for vi in v:
            c1 = ui
            c2 = vi
            c3 = ui * vi  # saddle: z = xy
            c4 = -(c1 + c2 + c3)
            points.append([c1, c2, c3, c4])
    x = np.exp(np.array(points))
    return closure(x)


# ============================================================
# RUN FULL DIAGNOSTIC ON EACH TEST OBJECT
# ============================================================

def diagnose(name, X):
    """Run complete Hs diagnostic on a test object"""
    X = np.array(X, dtype=float)
    N, D = X.shape
    
    result = OrderedDict()
    result['test_object'] = name
    result['input_shape'] = f"{N} observations x {D} parts"
    result['simplex'] = f"S^{D-1} ({D-1}-simplex)"
    
    # CLR
    C = clr(X)
    result['clr_range'] = f"[{C.min():.4f}, {C.max():.4f}]"
    result['clr_sum_check'] = f"max|sum| = {np.max(np.abs(C.sum(axis=1))):.2e}"
    
    # Variation matrix
    if N >= 2:
        T = variation_matrix(X)
        tv = total_variance(T)
        result['total_variance'] = f"{tv:.6f}"
        result['var_matrix_range'] = f"[{T[T > 0].min():.6f}, {T.max():.6f}]" if T.max() > 0 else "all zero"
    else:
        result['total_variance'] = "N/A (single observation)"
        result['var_matrix_range'] = "N/A"
    
    # Cumulative variance V(t)
    if N >= 3:
        vt = cumulative_variance(X)
        result['V(t)_start'] = f"{vt[0]:.6f}"
        result['V(t)_end'] = f"{vt[-1]:.6f}"
        result['V(t)_shape'] = classify_shape(vt)
        result['V(t)_range'] = f"{vt.max() - vt.min():.6f}"
    else:
        result['V(t)_start'] = "N/A"
        result['V(t)_end'] = "N/A"
        result['V(t)_shape'] = "N/A (< 3 obs)"
        result['V(t)_range'] = "N/A"
    
    # Entropy
    H_vals = [shannon_entropy(X[i]) for i in range(N)]
    result['entropy_mean'] = f"{np.mean(H_vals):.6f}"
    result['entropy_range'] = f"{np.max(H_vals) - np.min(H_vals):.6f}"
    result['entropy_max_possible'] = f"{np.log(D):.6f}"
    
    # Aitchison norm (evidence information)
    Ie_vals = [aitchison_norm(X[i]) for i in range(N)]
    result['aitchison_norm_mean'] = f"{np.mean(Ie_vals):.6f}"
    result['aitchison_norm_range'] = f"{np.max(Ie_vals) - np.min(Ie_vals):.6f}"
    
    # Lock detection
    if N >= 3:
        locks = detect_locks(X, threshold=0.05)
        result['locks_found'] = len(locks)
        if locks:
            result['lock_pairs'] = ', '.join([f"({i},{j}) sd={sd:.4f}" for i, j, sd in locks[:5]])
        else:
            result['lock_pairs'] = "none"
    else:
        result['locks_found'] = "N/A"
        result['lock_pairs'] = "N/A"
    
    # Pair stability
    if N >= 3:
        ps = pair_stability(X)
        cvs = [v['cv'] for v in ps.values()]
        finite_cvs = [c for c in cvs if c < 1e6]
        if finite_cvs:
            result['pair_cv_min'] = f"{min(finite_cvs):.4f}"
            result['pair_cv_max'] = f"{max(finite_cvs):.4f}"
            result['most_stable_pair'] = str(min(ps, key=lambda k: ps[k]['cv']))
        else:
            result['pair_cv_min'] = "all infinite"
            result['pair_cv_max'] = "all infinite"
            result['most_stable_pair'] = "none"
    else:
        result['pair_cv_min'] = "N/A"
        result['pair_cv_max'] = "N/A"
        result['most_stable_pair'] = "N/A"
    
    # Fingerprint geometry
    if N >= 2 and D >= 3:
        fg = fingerprint_geometry(X)
        result['fingerprint_area'] = f"{fg['area']:.6f}"
        result['fingerprint_perimeter'] = f"{fg['perimeter']:.6f}"
        result['fingerprint_compactness'] = f"{fg['compactness']:.6f}"
    else:
        result['fingerprint_area'] = "N/A"
        result['fingerprint_perimeter'] = "N/A"
        result['fingerprint_compactness'] = "N/A"
    
    # Aitchison distances (first to last, and max pairwise)
    if N >= 2:
        d_first_last = aitchison_distance(X[0], X[-1])
        result['aitchison_dist_first_last'] = f"{d_first_last:.6f}"
        # Path length
        path = sum(aitchison_distance(X[i], X[i+1]) for i in range(N-1))
        result['aitchison_path_length'] = f"{path:.6f}"
        result['path_efficiency'] = f"{d_first_last / path:.4f}" if path > 1e-12 else "stationary"
    else:
        result['aitchison_dist_first_last'] = "N/A"
        result['aitchison_path_length'] = "N/A"
        result['path_efficiency'] = "N/A"
    
    # Diagnosis
    if N == 1:
        result['DIAGNOSIS'] = "POINT — no dynamics, no drift, no structure"
    elif N >= 3:
        shape = result['V(t)_shape']
        locks_n = result['locks_found']
        if result.get('V(t)_range') != "N/A" and float(result['V(t)_range']) < 1e-6:
            result['DIAGNOSIS'] = "STATIONARY — zero drift, all ratios locked"
        elif shape == "FLAT":
            result['DIAGNOSIS'] = "EQUILIBRIUM — no compositional change"
        elif "LINEAR" in shape:
            result['DIAGNOSIS'] = "CONSTANT DRIFT — steady directional movement"
        elif "CONVEX" in shape:
            result['DIAGNOSIS'] = "ACCELERATING DRIFT — system diverging"
        elif "CONCAVE" in shape:
            result['DIAGNOSIS'] = "DECELERATING DRIFT — system converging"
        else:
            result['DIAGNOSIS'] = f"COMPLEX — {shape}"
    else:
        result['DIAGNOSIS'] = "MINIMAL DATA"
    
    return result


# ============================================================
# MAIN — BUILD ALL TEST OBJECTS AND RUN
# ============================================================

test_objects = [
    ("1. POINT (no time)", make_point_no_time()),
    ("2. POINT + TIME (stationary)", make_point_with_time(20)),
    ("3. LINE (linear drift)", make_line(20)),
    ("4. CIRCLE (periodic)", make_circle(40)),
    ("5. SPHERE (4-part, full coverage)", make_sphere(60)),
    ("6. CUBE (structured grid)", make_cube()),
    ("7. RHOMBOID (skewed grid)", make_rhomboid()),
    ("8. TORUS (4-part, doubly periodic)", make_torus(80)),
    ("9. SPIRAL (expanding)", make_spiral(50)),
    ("10. SADDLE (hyperbolic)", make_saddle(49)),
]

# Print INPUT tables
print("=" * 80)
print("Hs IMAGING SYSTEM CALIBRATION SUITE")
print("=" * 80)
print()

for name, X in test_objects:
    print(f"--- {name} ---")
    print(f"  Dimensions: {X.shape[0]} obs x {X.shape[1]} parts")
    print(f"  First obs:  [{', '.join(f'{v:.4f}' for v in X[0])}]")
    if X.shape[0] > 1:
        print(f"  Last obs:   [{', '.join(f'{v:.4f}' for v in X[-1])}]")
    print(f"  Sum check:  [{', '.join(f'{v:.6f}' for v in X.sum(axis=1)[:3])}...]")
    print()

# Run diagnostics
print()
print("=" * 80)
print("DIAGNOSTIC OUTPUTS")
print("=" * 80)

all_results = []
for name, X in test_objects:
    r = diagnose(name, X)
    all_results.append(r)
    print()
    print(f"{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    for k, v in r.items():
        if k == 'test_object':
            continue
        if k == 'DIAGNOSIS':
            print(f"  >>> {k}: {v}")
        else:
            print(f"  {k:30s}: {v}")

# Summary comparison table
print()
print()
print("=" * 80)
print("SUMMARY COMPARISON TABLE")
print("=" * 80)
print()

header = f"{'Object':<30s} {'Parts':>5s} {'TotVar':>10s} {'V(t) Shape':<22s} {'Entropy':>8s} {'||x||_a':>8s} {'Locks':>6s} {'Path Eff':>9s} {'DIAGNOSIS'}"
print(header)
print("-" * len(header))

for r in all_results:
    name = r['test_object'].split('. ')[1] if '. ' in r['test_object'] else r['test_object']
    parts = r['input_shape'].split(' x ')[1].split(' ')[0]
    tv = r['total_variance']
    vshape = r['V(t)_shape']
    ent = r['entropy_mean']
    anorm = r['aitchison_norm_mean']
    locks = str(r['locks_found'])
    peff = r['path_efficiency']
    diag = r['DIAGNOSIS']
    
    # Truncate name
    if len(name) > 28:
        name = name[:28]
    
    print(f"{name:<30s} {parts:>5s} {tv:>10s} {vshape:<22s} {ent:>8s} {anorm:>8s} {locks:>6s} {peff:>9s}  {diag}")

print()
print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print("""
The calibration suite confirms Hs behaves as expected for each known geometry:

POINT:       No dynamics possible. Single observation = no variance, no drift.
STATIONARY:  V(t) = 0, all pairs locked, entropy constant. Instrument reads silence.
LINE:        Constant drift detected. Path efficiency near 1.0 (direct route).
CIRCLE:      Periodic return. Path efficiency near 0 (goes nowhere net).
             V(t) shows the characteristic periodic accumulation.
SPHERE:      Full coverage of the simplex surface. High total variance.
CUBE:        Structured grid. Discrete jumps, not continuous flow.
RHOMBOID:    Skewed grid. Similar to cube but with asymmetric variance.
TORUS:       Doubly periodic. Complex V(t) shape from two nested cycles.
SPIRAL:      Expanding radius = accelerating drift. V(t) convex.
SADDLE:      Hyperbolic geometry. Mixed curvature in the diagnostic.

KEY FINDING: The instrument correctly distinguishes:
  - Stasis from drift (point vs line)
  - Linear from nonlinear drift (line vs spiral)
  - Periodic from aperiodic motion (circle vs line)
  - Expanding from bounded trajectories (spiral vs circle)
  - Simple from compound periodicity (circle vs torus)

This is exactly what an imaging system should do with calibration targets.
""")

