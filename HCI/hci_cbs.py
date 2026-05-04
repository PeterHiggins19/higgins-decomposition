#!/usr/bin/env python3
"""
Higgins Compositional Bearing Scope (CBS)
=========================================
Oscilloscope-style instrument for compositional navigation.

Pure monochrome. ASCII symbology. No colour. No scale factor.
Full sweep: Hs [0, 1], bearing [0, 360].

Tensor engine: Compositional Navigation Tensor (CNT)
  CNT(x) = (theta, omega, kappa, sigma)

Input:  Pipeline results JSON (from hs_run.py or direct analysis)
Output: ASCII oscilloscope traces + optional PDF

Mathematical lineage:
  Aitchison (1986) - CLR transform, Aitchison distance
  Shannon (1948)   - Entropy
  Higgins (2025)   - Hs = 1 - H/ln(D), ring classification
  Higgins (2026)   - CNT bearing/velocity/sensitivity/helmsman

The instrument reads. The expert decides. The loop stays open.
"""

import json
import math
import sys
import os

# ── Symbology (ASCII only) ─────────────────────────────────────────
SYM_POINT    = "."   # data point
SYM_HELM     = "*"   # helmsman transition
SYM_ORIGIN   = "+"   # barycenter
SYM_LOCK     = "x"   # lock point (fraction = 0)
SYM_HAXIS    = "-"   # horizontal axis
SYM_VAXIS    = "|"   # vertical axis
SYM_GRID     = "#"   # grid intersection
SYM_LOCKBAND = "="   # lock corridor
SYM_VELTHRES = "~"   # angular velocity threshold
SYM_REVERSAL = "^"   # bearing reversal
SYM_ARROW    = ">"   # trajectory direction
SYM_RING     = ":"   # ring boundary marker

# Grayscale density characters (8 levels, black to white)
GRAY_CHARS = "@#8o:.- "

# ── Ring boundaries ────────────────────────────────────────────────
RING_BOUNDS = [0.00, 0.05, 0.15, 0.30, 0.50, 0.75, 0.95, 1.00]
RING_NAMES  = ["Hs-0", "Hs-1", "Hs-2", "Hs-3", "Hs-4", "Hs-5", "Hs-6"]


# ══════════════════════════════════════════════════════════════════
# COMPOSITIONAL NAVIGATION TENSOR (CNT)
# ══════════════════════════════════════════════════════════════════

def cnt_bearing(h, i, j):
    """Pairwise bearing theta_{ij} in degrees.

    Definition 1: theta_{ij}(x) = atan2(h_j, h_i)
    where h = clr(x).
    """
    return math.degrees(math.atan2(h[j], h[i]))


def cnt_bearing_tensor(h):
    """Full bearing tensor: all D(D-1)/2 pairwise bearings.

    Returns dict of (i,j) -> theta_{ij} in degrees.
    """
    D = len(h)
    bearings = {}
    for i in range(D):
        for j in range(i + 1, D):
            bearings[(i, j)] = cnt_bearing(h, i, j)
    return bearings


def cnt_angular_velocity(h1, h2):
    """Angular velocity between two CLR vectors in full D-space.

    Definition 2: omega = arccos(<h1,h2> / (||h1||*||h2||))

    Implementation uses the numerically stable atan2 form:
      omega = atan2(||h1 x h2||, <h1,h2>)
    where ||h1 x h2||^2 = ||h1||^2 ||h2||^2 - <h1,h2>^2 (Lagrange identity).

    This avoids arccos instability near 0 and 180 degrees, where arccos
    loses up to 8 digits of precision (see P03 precision experiment).
    Verified equivalent to arccos within 10^{-13} degrees on all
    well-conditioned data (see P04).

    Returns degrees.
    """
    dot = sum(a * b for a, b in zip(h1, h2))
    m1_sq = sum(a ** 2 for a in h1)
    m2_sq = sum(a ** 2 for a in h2)
    m1 = math.sqrt(m1_sq)
    m2 = math.sqrt(m2_sq)
    if m1 < 1e-300 or m2 < 1e-300:
        return 0.0
    # Lagrange identity: ||a x b||^2 = ||a||^2 ||b||^2 - (a.b)^2
    cross_sq = max(0.0, m1_sq * m2_sq - dot * dot)
    cross_mag = math.sqrt(cross_sq)
    return math.degrees(math.atan2(cross_mag, dot))


def cnt_steering_sensitivity(h):
    """Steering sensitivity tensor (diagonal): kappa_{jj} = 1/x_j.

    Definition 3: g_{jj} = 1/x_j where x = softmax(h).
    Returns list of sensitivities.
    """
    exp_h = [math.exp(v) for v in h]
    total = sum(exp_h)
    fracs = [e / total for e in exp_h]
    return [1.0 / max(f, 1e-15) for f in fracs]


def cnt_helmsman(h1, h2, carriers=None):
    """Helmsman index: carrier with maximum |delta CLR|.

    Definition 4: sigma = argmax_j |h_j(t+1) - h_j(t)|
    Returns (index, name, delta_clr).
    """
    deltas = [(abs(h2[j] - h1[j]), h2[j] - h1[j], j) for j in range(len(h1))]
    deltas.sort(reverse=True)
    best = deltas[0]
    name = carriers[best[2]] if carriers else f"C{best[2]}"
    return best[2], name, best[1]


def cnt_closure(x, eps=1e-15):
    """Close a positive vector to the simplex with a numerical floor.

    Returns a list of D values summing to 1.0.
    """
    x_pos = [max(float(v), eps) for v in x]
    total = sum(x_pos)
    if total <= 0:
        raise ValueError("Composition must have positive sum.")
    return [v / total for v in x_pos]


def cnt_aitchison_metric_tensor(x, normalized=False, eps=1e-15):
    """Full Higgins Steering Metric Tensor kappa^Hs(x).

    Given a closed composition x in the D-simplex, the CLR differential is:
        dh = P diag(1/x) dx
        P  = I - (1/D) 11^T

    The covariant metric tensor in composition coordinates is:
        G(x) = diag(1/x) P diag(1/x)

    Component form:
        G_ij = (delta_ij - 1/D) / (x_i * x_j)

    This is the full Aitchison pullback metric. The repo's existing
    diagonal quantity 1/x_j is the diagonal steering sensitivity —
    a special case of this tensor.

    Set normalized=True for standard CoDa convention (scales G by 1/D).
    Default normalized=False is the Hs-native unnormalised CLR convention.

    Mathematical lineage:
        Aitchison (1986) — Aitchison geometry on the simplex
        Egozcue et al. (2003) — ILR and metric structure
        Higgins (2026) — Steering metric tensor in CNT/HCI instrument

    Returns D x D matrix as list of lists.
    """
    x = cnt_closure(x, eps=eps)
    D = len(x)
    G = []
    for i in range(D):
        row = []
        for j in range(D):
            delta = 1.0 if i == j else 0.0
            gij = (delta - 1.0 / D) / (x[i] * x[j])
            if normalized:
                gij /= D
            row.append(gij)
        G.append(row)
    return G


def cnt_metric_apply(G, u, v):
    """Compute u^T G v — inner product under the Higgins metric."""
    D = len(G)
    if len(u) != D or len(v) != D:
        raise ValueError("Vector dimensions must match metric tensor.")
    return sum(u[i] * G[i][j] * v[j] for i in range(D) for j in range(D))


def cnt_metric_norm(G, u):
    """Compute sqrt(u^T G u), guarded against roundoff."""
    q = cnt_metric_apply(G, u, u)
    return math.sqrt(max(0.0, q))


def cnt_metric_distance(x1, x2, eps=1e-15):
    """Aitchison distance between two compositions under the Higgins metric.

    d(x1, x2) = sqrt( sum_{i<j} (log(x1_i/x1_j) - log(x2_i/x2_j))^2 / D )

    This is equivalent to the CLR Euclidean distance sqrt(sum (h1_j - h2_j)^2).
    """
    x1 = cnt_closure(x1, eps=eps)
    x2 = cnt_closure(x2, eps=eps)
    D = len(x1)
    h1 = _clr(x1)
    h2 = _clr(x2)
    return math.sqrt(sum((h1[j] - h2[j]) ** 2 for j in range(D)))


def cnt_metric_angle(x1, x2, eps=1e-15):
    """Angle between two CLR vectors in degrees.

    Uses the atan2 form for numerical stability.
    """
    x1 = cnt_closure(x1, eps=eps)
    x2 = cnt_closure(x2, eps=eps)
    h1 = _clr(x1)
    h2 = _clr(x2)
    return cnt_angular_velocity(h1, h2)


def cnt_metric_energy(x, eps=1e-15):
    """Metric energy: ||h||^2 = h^T h.

    Measures displacement from the barycenter in Higgins coordinate space.
    """
    x = cnt_closure(x, eps=eps)
    h = _clr(x)
    return sum(v ** 2 for v in h)


def _clr(x):
    """Internal CLR transform for closed composition x."""
    D = len(x)
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]


def cnt_condition_number(x, eps=1e-15):
    """Condition number of the Aitchison metric tensor.

    kappa(G) = max(1/x_j) / min(1/x_j) = max(x) / min(x)

    The full tensor G is rank D-1 in ambient coordinates, so its
    raw matrix condition number is singular. This proxy is the
    correct simplex-facing conditioning diagnostic.

    Precision diagnostic: CNT operations lose approximately
    log10(kappa) digits of precision. For well-conditioned
    compositions (kappa < 100), all 15 significant digits are
    available. For extreme compositions (kappa > 10^10),
    only 5 digits remain reliable.

    Verified in P07/P08 precision experiments.
    """
    x_pos = [max(v, 1e-300) for v in x]
    return max(x_pos) / min(x_pos)


def cnt_steering_sensitivity_tensor(x, eps=1e-15):
    """Back-compatible CNT kappa channel.

    Returns both:
      - diagonal_sensitivity: existing repo quantity 1/x_j
      - metric_tensor: full Aitchison pullback metric G_ij
      - condition_number: max(x)/min(x)

    This bridges the old diagonal-only readout to the full
    Higgins Steering Metric Tensor.
    """
    x = cnt_closure(x, eps=eps)
    return {
        "x": x,
        "diagonal_sensitivity": [1.0 / v for v in x],
        "metric_tensor": cnt_aitchison_metric_tensor(x, eps=eps),
        "condition_number": cnt_condition_number(x, eps=eps),
    }


def cnt_helmert_basis(D):
    """Helmert submatrix: orthonormal basis for the CLR zero-sum plane.

    Returns (D-1) x D matrix. Row k (0-indexed):
      e_k = [1/sqrt(k(k+1)), ..., -k/sqrt(k(k+1)), 0, ..., 0]

    This is the standard basis used in ILR (Egozcue et al. 2003).
    Verified to machine precision: orthonormal, zero-sum, norm-preserving
    across D=3..100 (see P06, P09 precision experiments).
    """
    basis = []
    for k in range(1, D):
        row = [0.0] * D
        norm = math.sqrt(k * (k + 1))
        for j in range(k):
            row[j] = 1.0 / norm
        row[k] = -k / norm
        basis.append(row)
    return basis


def cnt_ilr_project(h, basis):
    """Project CLR vector to ILR coordinates using Helmert basis.

    ILR_k = <h, e_k>. Returns (D-1)-dimensional vector.
    The Aitchison isometry guarantees ||h||_CLR = ||z||_ILR
    (verified to machine precision in P06).
    """
    return [sum(h[j] * basis[k][j] for j in range(len(h)))
            for k in range(len(basis))]


def cnt_lock_detect(bearing_series, epsilon=10.0):
    """Detect informationally locked carrier pairs.

    Corollary 3: locked when max(theta) - min(theta) < epsilon.
    Returns list of (i, j, spread_degrees).
    """
    locks = []
    if not bearing_series:
        return locks
    pairs = list(bearing_series[0].keys())
    for pair in pairs:
        vals = [b[pair] for b in bearing_series if pair in b]
        if vals:
            spread = max(vals) - min(vals)
            if spread < epsilon:
                locks.append((pair[0], pair[1], spread))
    return locks


# ══════════════════════════════════════════════════════════════════
# OSCILLOSCOPE DISPLAY ENGINE
# ══════════════════════════════════════════════════════════════════

def build_trace_yz(years, hs_values, width=72, height=30):
    """YZ Face: Hs vs Time. Full sweep [0, 1].

    Cartesian plot. Vertical = Hs [0.0, 1.0]. Horizontal = time.
    Ring boundaries marked. No scale factor.
    """
    lines = []

    # Title
    lines.append("  YZ FACE : Hs vs TIME")
    lines.append("  " + SYM_HAXIS * (width + 2))

    T = len(years)
    col_spacing = max(1, (width - 8) // max(T - 1, 1))

    # Build grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Ring boundary rows
    ring_labels = {}
    for rb, rn in zip(RING_BOUNDS[1:-1], RING_NAMES):
        row = height - 1 - int(rb * (height - 1))
        row = max(0, min(height - 1, row))
        ring_labels[row] = rn
        for c in range(width):
            if grid[row][c] == " ":
                grid[row][c] = SYM_RING

    # Vertical axis
    for r in range(height):
        grid[r][4] = SYM_VAXIS

    # Data points
    for t, (yr, hs) in enumerate(zip(years, hs_values)):
        col = 5 + int(t * col_spacing)
        if col >= width:
            col = width - 1
        row = height - 1 - int(hs * (height - 1))
        row = max(0, min(height - 1, row))
        grid[row][col] = SYM_POINT

    # Render
    for r in range(height):
        hs_val = 1.0 - r / (height - 1)
        label = ring_labels.get(r, "")
        axis_label = f"{hs_val:.1f}" if r % (height // 5) == 0 else "   "
        line = f"  {axis_label:>4}" + "".join(grid[r]) + f"  {label}"
        lines.append(line)

    # Horizontal axis
    lines.append("  " + " " * 4 + SYM_HAXIS * width)

    # Year labels
    year_line = "  " + " " * 5
    for t, yr in enumerate(years):
        col = int(t * col_spacing)
        if t == 0 or t == T - 1 or t == T // 2:
            year_line += f"{yr}"
            year_line += " " * max(0, col_spacing - 4)
        else:
            year_line += " " * col_spacing
    lines.append(year_line[:width + 10])

    return "\n".join(lines)


def build_trace_xz(years, bearings_2d, helmsman_years, width=72, height=30):
    """XZ Face: Bearing vs Time. Full sweep [-180, +180] degrees.

    Cartesian plot. Vertical = bearing. Horizontal = time.
    Helmsman transitions marked with *.
    """
    lines = []

    lines.append("  XZ FACE : BEARING (theta) vs TIME")
    lines.append("  " + SYM_HAXIS * (width + 2))

    T = len(years)
    col_spacing = max(1, (width - 8) // max(T - 1, 1))

    # Build grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Zero-degree line (center)
    center_row = height // 2
    for c in range(width):
        if grid[center_row][c] == " ":
            grid[center_row][c] = SYM_HAXIS

    # 90-degree grid lines
    for deg in [-90, 90]:
        row = center_row - int(deg / 180 * (height // 2))
        row = max(0, min(height - 1, row))
        for c in range(width):
            if grid[row][c] == " ":
                grid[row][c] = SYM_GRID

    # Vertical axis
    for r in range(height):
        grid[r][4] = SYM_VAXIS

    # Data points
    for t, (yr, theta) in enumerate(zip(years, bearings_2d)):
        col = 5 + int(t * col_spacing)
        if col >= width:
            col = width - 1
        # Map [-180, +180] to [0, height-1]
        row = center_row - int(theta / 180 * (height // 2))
        row = max(0, min(height - 1, row))

        # Mark helmsman transitions
        if yr in helmsman_years:
            grid[row][col] = SYM_HELM
        else:
            grid[row][col] = SYM_POINT

    # Render
    for r in range(height):
        deg_val = (center_row - r) / (height // 2) * 180
        if r == 0:
            axis_label = "+180"
        elif r == center_row:
            axis_label = "   0"
        elif r == height - 1:
            axis_label = "-180"
        elif abs(deg_val - 90) < 180 / height:
            axis_label = " +90"
        elif abs(deg_val + 90) < 180 / height:
            axis_label = " -90"
        else:
            axis_label = "    "
        line = f"  {axis_label}" + "".join(grid[r]) + " deg"
        lines.append(line)

    # Horizontal axis
    lines.append("  " + " " * 4 + SYM_HAXIS * width)

    # Year labels
    year_line = "  " + " " * 5
    for t, yr in enumerate(years):
        col = int(t * col_spacing)
        if t == 0 or t == T - 1 or t == T // 2:
            year_line += f"{yr}"
            year_line += " " * max(0, col_spacing - 4)
    lines.append(year_line[:width + 10])

    return "\n".join(lines)


def build_navigation_table(results, carriers):
    """Navigation data table: bearing, velocity, helmsman, sensitivity."""
    lines = []
    lines.append("  COMPOSITIONAL NAVIGATION TENSOR (CNT) — DATA TABLE")
    lines.append("  " + "=" * 90)
    lines.append(f"  {'Year':>6} {'theta':>8} {'omega':>8} {'r':>8} "
                 f"{'d_A':>8} {'Hs':>7} {'Ring':>6}  {'Helm':>5} {'dCLR':>8}  "
                 f"{'g_max':>8} {'g_min':>6}")
    lines.append("  " + "-" * 90)

    abbr_map = {
        "Bioenergy": "Bio", "Coal": "Coa", "Gas": "Gas", "Hydro": "Hyd",
        "Nuclear": "Nuc", "Other Fossil": "OFo", "Solar": "Sol", "Wind": "Win"
    }

    for idx, r in enumerate(results):
        h = r["h"]
        hs = r["H_s"]
        dA = r["d_A"]
        ring = r["ring_code"]

        # Bearing in Hydro-OFossil plane (or first two largest CLR)
        theta = cnt_bearing(h, 3, 5) if len(h) > 5 else cnt_bearing(h, 0, 1)

        # Angular velocity
        if idx > 0:
            omega = cnt_angular_velocity(results[idx - 1]["h"], h)
        else:
            omega = 0.0

        # Projection radius
        if len(h) > 5:
            proj_r = math.sqrt(h[3] ** 2 + h[5] ** 2)
        else:
            proj_r = math.sqrt(h[0] ** 2 + h[1] ** 2)

        # Helmsman
        if idx > 0:
            _, helm_name, helm_dc = cnt_helmsman(
                results[idx - 1]["h"], h, carriers)
            helm_abbr = abbr_map.get(helm_name, helm_name[:3])
        else:
            helm_abbr = "---"
            helm_dc = 0.0

        # Steering sensitivity
        sens = cnt_steering_sensitivity(h)
        g_max = max(sens)
        g_min = min(sens)

        omega_mark = " ~" if omega > 20 else (" ^" if omega > 10 else "  ")

        lines.append(
            f"  {r['year']:>6} {theta:>+8.1f} {omega:>8.1f} {proj_r:>8.3f} "
            f"{dA:>8.3f} {hs:>7.4f} {ring:>6}  {helm_abbr:>5} {helm_dc:>+8.3f}  "
            f"{g_max:>8.0f} {g_min:>6.0f}{omega_mark}"
        )

    lines.append("  " + "-" * 90)
    lines.append("  Legend: ~ = omega > 20 deg (major rotation)")
    lines.append("          ^ = omega > 10 deg (course correction)")
    lines.append("          theta = bearing in Hydro-OFossil plane (degrees)")
    lines.append("          omega = 8D angular velocity (degrees)")
    lines.append("          Helm = carrier with max |delta CLR| (helmsman)")
    lines.append("          g_max/g_min = steering sensitivity range (1/x_j)")

    return "\n".join(lines)


def build_lock_report(results, carriers, epsilon=10.0):
    """Detect and report informationally locked carrier pairs."""
    lines = []
    lines.append("  INFORMATIONAL LOCK DETECTION")
    lines.append("  " + "=" * 60)

    abbr_map = {
        "Bioenergy": "Bio", "Coal": "Coa", "Gas": "Gas", "Hydro": "Hyd",
        "Nuclear": "Nuc", "Other Fossil": "OFo", "Solar": "Sol", "Wind": "Win"
    }

    # Compute all pairwise bearings across time
    bearing_series = [cnt_bearing_tensor(r["h"]) for r in results]
    locks = cnt_lock_detect(bearing_series, epsilon)

    if locks:
        locks.sort(key=lambda x: x[2])
        for i, j, spread in locks:
            ci = abbr_map.get(carriers[i], carriers[i][:3])
            cj = abbr_map.get(carriers[j], carriers[j][:3])
            lines.append(f"  LOCKED: {ci}-{cj}  spread = {spread:.1f} deg  "
                         f"(< {epsilon:.0f} deg threshold)")
    else:
        lines.append(f"  No locked pairs found at epsilon = {epsilon:.0f} deg")

    lines.append("")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def run_cbs(json_path, width=72, height=25):
    """Run the Compositional Bearing Scope on a results JSON file."""

    with open(json_path) as f:
        data = json.load(f)

    results = data["results"]
    carriers = data["metadata"]["carriers"]
    name = data["metadata"].get("name", os.path.basename(json_path))

    years = [r["year"] for r in results]
    hs_values = [r["H_s"] for r in results]

    # Compute bearings (Hydro=3, OFossil=5 if available, else 0,1)
    if len(carriers) > 5:
        ix, iy = 3, 5
        bname = f"{carriers[ix]}-{carriers[iy]}"
    else:
        ix, iy = 0, 1
        bname = f"{carriers[ix]}-{carriers[iy]}"

    bearings_2d = [cnt_bearing(r["h"], ix, iy) for r in results]

    # Identify helmsman transitions (omega > 10)
    helmsman_years = set()
    for i in range(1, len(results)):
        omega = cnt_angular_velocity(results[i - 1]["h"], results[i]["h"])
        if omega > 10:
            helmsman_years.add(results[i]["year"])

    # Build output
    output = []
    output.append("")
    output.append("  " + "=" * 74)
    output.append("  HIGGINS COMPOSITIONAL BEARING SCOPE (CBS)")
    output.append("  Tensor Engine: Compositional Navigation Tensor (CNT)")
    output.append(f"  System: {name}")
    output.append(f"  Carriers: D = {len(carriers)}")
    output.append(f"  Observations: T = {len(results)}")
    output.append(f"  Bearing plane: {bname}")
    output.append("  Display: 8-bit monochrome | ASCII symbology | no colour")
    output.append("  " + "=" * 74)
    output.append("")

    # Trace 1: XZ Face — Bearing vs Time
    output.append(build_trace_xz(years, bearings_2d, helmsman_years,
                                  width=width, height=height))
    output.append("")

    # Trace 2: YZ Face — Hs vs Time
    output.append(build_trace_yz(years, hs_values,
                                  width=width, height=height))
    output.append("")

    # Navigation table
    output.append(build_navigation_table(results, carriers))
    output.append("")

    # Lock detection
    output.append(build_lock_report(results, carriers))

    # Footer
    output.append("  " + "-" * 74)
    output.append("  The instrument reads. The expert decides. The loop stays open.")
    output.append("  " + "-" * 74)
    output.append("")

    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hci_cbs.py <results.json> [width] [height]")
        print("  Higgins Compositional Bearing Scope")
        print("  Oscilloscope display of compositional navigation")
        sys.exit(1)

    json_path = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 72
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 25

    result = run_cbs(json_path, width, height)
    print(result)
