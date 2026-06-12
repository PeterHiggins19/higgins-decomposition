#!/usr/bin/env python3
"""
HCI Stage 1 Engine — CSV to JSON + ASCII Section Plates
========================================================

Automated instrument chain:
  EMBER CSV  -->  Stage 1 CBS/CNT computation  -->  JSON + ASCII

Output structure (per HCI_FOUNDATION.md spec):
  - Section triads: XY + XZ + YZ metric sections at each time index
  - Metric ledger: numerical output table (the measurement authority)
  - Morphographic section plates: symbolic visual renderings
  - Section cine-deck: one plate per year

Display standard:
  XY Face (plan view): Bearing polar plot — all D(D-1)/2 pairwise bearings
  XZ Face: Bearing vs Time — full trajectory, current year highlighted
  YZ Face: Hs vs Time — full trajectory, current year highlighted

No scale factor. Full sweep: Hs [0,1], Bearing [-180,+180].
8-bit monochrome. ASCII symbology. No colour.

Usage:
  python stage1_engine.py <ember_csv> [output.json]

The instrument reads. The expert decides. The loop stays open.
"""

import sys
import os
import json
import math
import csv

# Add HCI parent folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from hci_cbs import (cnt_closure, cnt_bearing, cnt_bearing_tensor,
                     cnt_angular_velocity, cnt_steering_sensitivity,
                     cnt_helmsman, cnt_aitchison_metric_tensor,
                     cnt_condition_number, cnt_metric_energy,
                     cnt_lock_detect, _clr,
                     RING_BOUNDS, RING_NAMES)


# ── Symbology ─────────────────────────────────────────────────────
SYM_POINT   = "."
SYM_CURRENT = "O"   # current year (highlighted)
SYM_HELM    = "*"
SYM_ORIGIN  = "+"
SYM_HAXIS   = "-"
SYM_VAXIS   = "|"
SYM_GRID    = "#"
SYM_RING    = ":"


# ══════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════

def load_ember_csv(csv_path):
    """Load EMBER-format CSV. Returns compositions, carrier_names, years."""
    compositions = []
    years = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        carrier_names = [h for h in reader.fieldnames if h != 'Year']
        for row in reader:
            years.append(int(row['Year']))
            comp = [float(row[c]) for c in carrier_names]
            compositions.append(comp)
    return compositions, carrier_names, years


def classify_ring(hs):
    """Classify Hs value into ring code."""
    for k in range(len(RING_BOUNDS) - 1):
        if hs < RING_BOUNDS[k + 1]:
            return RING_NAMES[k]
    return RING_NAMES[-1]


# ══════════════════════════════════════════════════════════════════
# STAGE 1 COMPUTATION
# ══════════════════════════════════════════════════════════════════

def compute_stage1(compositions, carrier_names, years):
    """Run full Stage 1 CBS/CNT computation. Returns list of records."""
    D = len(carrier_names)
    N = len(compositions)
    records = []
    prev_h = None

    for t in range(N):
        x = cnt_closure(compositions[t])
        h = _clr(x)

        # Higgins Scale
        entropy = -sum(xi * math.log(xi) for xi in x if xi > 0)
        hs = 1.0 - entropy / math.log(D)
        ring = classify_ring(hs)

        # Metric tensor
        G = cnt_aitchison_metric_tensor(x)
        energy = cnt_metric_energy(x)
        cond = cnt_condition_number(x)

        # Full bearing tensor
        bearings_raw = cnt_bearing_tensor(h)
        bearings = {}
        for (i, j), angle in bearings_raw.items():
            pair_key = f"{carrier_names[i]}-{carrier_names[j]}"
            bearings[pair_key] = round(angle, 4)

        # Steering sensitivity
        sens = cnt_steering_sensitivity(h)

        # Angular velocity + helmsman
        omega = 0.0
        helmsman_name = None
        helmsman_idx = None
        helmsman_delta = 0.0
        d_aitchison = 0.0

        if prev_h is not None:
            omega = cnt_angular_velocity(prev_h, h)
            helm_idx, helm_name, helm_dc = cnt_helmsman(prev_h, h, carrier_names)
            helmsman_name = helm_name
            helmsman_idx = helm_idx
            helmsman_delta = helm_dc
            d_aitchison = math.sqrt(sum((h[j] - prev_h[j]) ** 2 for j in range(D)))

        record = {
            "year": years[t],
            "composition": [round(xi, 8) for xi in x],
            "clr": [round(hi, 8) for hi in h],
            "hs": round(hs, 6),
            "ring": ring,
            "metric_energy": round(energy, 6),
            "condition_number": round(cond, 4),
            "angular_velocity_deg": round(omega, 4),
            "d_aitchison": round(d_aitchison, 6),
            "helmsman": helmsman_name,
            "helmsman_idx": helmsman_idx,
            "helmsman_delta": round(helmsman_delta, 8),
            "steering_sensitivity": {
                carrier_names[j]: round(sens[j], 4) for j in range(D)
            },
            "metric_diagonal": {
                carrier_names[j]: round(G[j][j], 4) for j in range(D)
            },
            "bearings_deg": bearings,
        }

        records.append(record)
        prev_h = h

    return records


def detect_locks(records, carrier_names, epsilon=10.0):
    """Detect informationally locked carrier pairs."""
    clr_vectors = [r["clr"] for r in records]
    bearing_series = [cnt_bearing_tensor(h) for h in clr_vectors]
    locks = cnt_lock_detect(bearing_series, epsilon)
    result = []
    for i, j, spread in sorted(locks, key=lambda x: x[2]):
        result.append({
            "carrier_i": carrier_names[i],
            "carrier_j": carrier_names[j],
            "bearing_spread_deg": round(spread, 4)
        })
    return result


# ══════════════════════════════════════════════════════════════════
# ASCII SECTION TRIAD — ONE PER YEAR
# ══════════════════════════════════════════════════════════════════

def ascii_section_header(year, t, N, D, carrier_names):
    """Section plate header for one year."""
    lines = []
    lines.append("=" * 78)
    lines.append(f"  SECTION PLATE  t = {t}  |  Year {year}  |  D = {D}")
    lines.append("=" * 78)
    return "\n".join(lines)


def ascii_yz_face(records, t, width=68, height=20):
    """YZ Face: Hs vs Time — full trajectory, current year highlighted."""
    lines = []
    lines.append(f"  YZ FACE : Hs vs TIME  [current = {records[t]['year']}]")

    N = len(records)
    col_spacing = max(1, (width - 6) // max(N - 1, 1))

    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Ring boundaries
    for rb, rn in zip(RING_BOUNDS[1:-1], RING_NAMES):
        row = height - 1 - int(rb * (height - 1))
        row = max(0, min(height - 1, row))
        for c in range(width):
            if grid[row][c] == " ":
                grid[row][c] = SYM_RING

    # Vertical axis
    for r in range(height):
        grid[r][4] = SYM_VAXIS

    # All data points
    for i, rec in enumerate(records):
        col = 5 + int(i * col_spacing)
        if col >= width:
            col = width - 1
        row = height - 1 - int(rec["hs"] * (height - 1))
        row = max(0, min(height - 1, row))
        if i == t:
            grid[row][col] = SYM_CURRENT  # highlight current year
        else:
            grid[row][col] = SYM_POINT

    for r in range(height):
        hs_val = 1.0 - r / (height - 1)
        axis_label = f"{hs_val:.1f}" if r % (height // 4) == 0 else "   "
        lines.append(f"  {axis_label:>4}" + "".join(grid[r]))

    lines.append("  " + " " * 4 + SYM_HAXIS * width)
    return "\n".join(lines)


def ascii_xz_face(records, t, carrier_names, ci, cj, width=68, height=16):
    """XZ Face: Bearing(ci-cj) vs Time — full trajectory, current year highlighted."""
    lines = []
    pair_name = f"{carrier_names[ci]}-{carrier_names[cj]}"
    lines.append(f"  XZ FACE : Bearing({pair_name}) vs TIME  [current = {records[t]['year']}]")

    N = len(records)
    col_spacing = max(1, (width - 6) // max(N - 1, 1))
    center = height // 2

    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Zero line
    for c in range(width):
        if grid[center][c] == " ":
            grid[center][c] = SYM_HAXIS

    # Vertical axis
    for r in range(height):
        grid[r][4] = SYM_VAXIS

    # All data points
    for i, rec in enumerate(records):
        col = 5 + int(i * col_spacing)
        if col >= width:
            col = width - 1
        theta = rec["bearings_deg"].get(pair_name, 0.0)
        row = center - int(theta / 180 * (height // 2))
        row = max(0, min(height - 1, row))
        if i == t:
            grid[row][col] = SYM_CURRENT
        elif rec.get("helmsman") in [carrier_names[ci], carrier_names[cj]]:
            grid[row][col] = SYM_HELM
        else:
            grid[row][col] = SYM_POINT

    for r in range(height):
        if r == 0:
            al = "+180"
        elif r == center:
            al = "   0"
        elif r == height - 1:
            al = "-180"
        else:
            al = "    "
        lines.append(f"  {al}" + "".join(grid[r]))

    return "\n".join(lines)


def ascii_xy_face(record, carrier_names, width=40, height=20):
    """XY Face (plan view): Bearing polar diagram at one time index.

    Shows all D(D-1)/2 pairwise bearings as radial lines from origin.
    Horizontal = bearing angle, Vertical = CLR projection radius.
    Each carrier pair plotted at its bearing angle with radius = sqrt(h_i^2 + h_j^2).
    """
    lines = []
    lines.append(f"  XY FACE (PLAN VIEW) : Bearing Polar  |  Year {record['year']}")

    D = len(carrier_names)
    h = record["clr"]

    # Abbreviation map
    abbr = {}
    for c in carrier_names:
        abbr[c] = c[:3]

    # Compute all bearing angles and radii
    pair_data = []
    for i in range(D):
        for j in range(i + 1, D):
            pair_key = f"{carrier_names[i]}-{carrier_names[j]}"
            theta_deg = record["bearings_deg"].get(pair_key, 0.0)
            radius = math.sqrt(h[i] ** 2 + h[j] ** 2)
            pair_data.append((theta_deg, radius, abbr[carrier_names[i]], abbr[carrier_names[j]]))

    max_r = max(pd[1] for pd in pair_data) if pair_data else 1.0
    if max_r < 0.001:
        max_r = 1.0

    # Build grid — origin at center
    cx, cy = width // 2, height // 2
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Axes through center
    for c in range(width):
        if grid[cy][c] == " ":
            grid[cy][c] = SYM_HAXIS
    for r in range(height):
        if grid[r][cx] == " ":
            grid[r][cx] = SYM_VAXIS

    grid[cy][cx] = SYM_ORIGIN

    # Plot each bearing pair
    for theta_deg, radius, ci_name, cj_name in pair_data:
        theta_rad = math.radians(theta_deg)
        norm_r = radius / max_r
        px = cx + int(norm_r * (width // 2 - 2) * math.cos(theta_rad))
        py = cy - int(norm_r * (height // 2 - 1) * math.sin(theta_rad))
        px = max(0, min(width - 1, px))
        py = max(0, min(height - 1, py))
        if grid[py][px] in (" ", SYM_HAXIS, SYM_VAXIS):
            grid[py][px] = SYM_POINT

    # Axis labels
    lines.append(f"  {'':>6}+90")
    for r in range(height):
        if r == cy:
            lines.append(f"  -180" + "".join(grid[r]) + "+0")
        else:
            lines.append(f"  {'':>4}" + "".join(grid[r]))
    lines.append(f"  {'':>6}-90")
    lines.append(f"  {'':>6}r_max = {max_r:.3f}")

    return "\n".join(lines)


def ascii_metric_ledger(record, carrier_names):
    """Metric ledger — the numerical authority for one year."""
    D = len(carrier_names)
    lines = []
    lines.append(f"  METRIC LEDGER  |  Year {record['year']}")
    lines.append("  " + "-" * 74)

    # Row 1: Hs and ring
    lines.append(f"  Hs = {record['hs']:.6f}   Ring = {record['ring']}   "
                 f"E_m = {record['metric_energy']:.6f}   "
                 f"kappa = {record['condition_number']:.4f}")

    # Row 2: Angular velocity and helmsman
    helm = record['helmsman'] if record['helmsman'] else "---"
    lines.append(f"  omega = {record['angular_velocity_deg']:.4f} deg   "
                 f"d_A = {record['d_aitchison']:.6f}   "
                 f"Helmsman = {helm}   "
                 f"delta = {record['helmsman_delta']:+.6f}")

    # CLR coordinates
    lines.append("  " + "-" * 74)
    lines.append("  CLR:")
    clr_line = "   "
    for j, c in enumerate(carrier_names):
        clr_line += f" {c[:4]:>5}={record['clr'][j]:+.4f}"
    lines.append(clr_line)

    # Composition (closed fractions)
    lines.append("  x(closed):")
    comp_line = "   "
    for j, c in enumerate(carrier_names):
        comp_line += f" {c[:4]:>5}={record['composition'][j]:.4f}"
    lines.append(comp_line)

    # Steering sensitivity
    lines.append("  1/x_j (steering):")
    sens_line = "   "
    for c in carrier_names:
        val = record['steering_sensitivity'].get(c, 0)
        if val > 9999:
            sens_line += f" {c[:4]:>5}={val:.0e}"
        else:
            sens_line += f" {c[:4]:>5}={val:>7.1f}"
    lines.append(sens_line)

    # Key bearings (top 5 by magnitude)
    bearing_list = sorted(record['bearings_deg'].items(), key=lambda x: abs(x[1]), reverse=True)
    lines.append("  Bearings (top 5 by |theta|):")
    for pair, angle in bearing_list[:5]:
        short = pair.replace("Other Fossil", "OFos")
        lines.append(f"    {short:>20} = {angle:>+8.2f} deg")

    lines.append("  " + "-" * 74)
    return "\n".join(lines)


def ascii_section_plate(records, t, carrier_names):
    """Full section plate for year t: XY + XZ + YZ + metric ledger."""
    D = len(carrier_names)
    lines = []

    lines.append(ascii_section_header(records[t]["year"], t, len(records), D, carrier_names))
    lines.append("")

    # YZ Face: Hs vs Time
    lines.append(ascii_yz_face(records, t))
    lines.append("")

    # XZ Face: pick a representative bearing pair (highest-energy pair for this year)
    # Use the pair with largest bearing magnitude
    best_pair = None
    best_angle = 0
    for i in range(D):
        for j in range(i + 1, D):
            pair_key = f"{carrier_names[i]}-{carrier_names[j]}"
            angle = abs(records[t]["bearings_deg"].get(pair_key, 0))
            if angle > best_angle:
                best_angle = angle
                best_pair = (i, j)

    if best_pair:
        lines.append(ascii_xz_face(records, t, carrier_names, best_pair[0], best_pair[1]))
    lines.append("")

    # XY Face: plan view polar bearing diagram
    lines.append(ascii_xy_face(records[t], carrier_names))
    lines.append("")

    # Metric ledger
    lines.append(ascii_metric_ledger(records[t], carrier_names))
    lines.append("")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python stage1_engine.py <ember_csv> [output.json]")
        print()
        print("  HCI Stage 1 Engine — Section Triads + Metric Ledgers")
        print("  Output: JSON (all data) + ASCII section plates (1 per year)")
        print()
        print("  The instrument reads. The expert decides. The loop stays open.")
        sys.exit(1)

    csv_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else "stage1_output.json"

    if not os.path.exists(csv_path):
        print(f"ERROR: CSV not found: {csv_path}")
        sys.exit(1)

    # Load
    compositions, carrier_names, years = load_ember_csv(csv_path)
    D = len(carrier_names)
    N = len(compositions)

    # Compute Stage 1
    records = compute_stage1(compositions, carrier_names, years)

    # Lock detection
    locks = detect_locks(records, carrier_names, epsilon=10.0)

    # Build JSON output
    output = {
        "instrument": "Higgins Compositional Bearing Scope (CBS)",
        "engine": "Compositional Navigation Tensor (CNT)",
        "stage": 1,
        "dataset": os.path.basename(csv_path),
        "carriers": carrier_names,
        "D": D,
        "N": N,
        "years": years,
        "records": records,
        "locks": locks,
        "ring_boundaries": RING_BOUNDS,
        "ring_names": RING_NAMES,
        "signature": "The instrument reads. The expert decides. The loop stays open."
    }

    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)

    # ASCII section plates — one per year
    print()
    print("=" * 78)
    print("  HIGGINS COMPOSITIONAL BEARING SCOPE (CBS)")
    print("  Tensor Engine: Compositional Navigation Tensor (CNT)")
    print(f"  Dataset: {os.path.basename(csv_path)}")
    print(f"  Carriers: D = {D}  ({', '.join(carrier_names)})")
    print(f"  Observations: T = {N}  ({years[0]}-{years[-1]})")
    print("  Output: Section cine-deck — 1 plate per year")
    print("  Display: 8-bit monochrome | ASCII symbology | no colour")
    print("=" * 78)
    print()

    for t in range(N):
        print(ascii_section_plate(records, t, carrier_names))

    # Lock report
    print("=" * 78)
    print(f"  INFORMATIONAL LOCK DETECTION  (epsilon = 10 deg)")
    print("=" * 78)
    if locks:
        for lk in locks:
            print(f"  LOCKED: {lk['carrier_i']}-{lk['carrier_j']}  "
                  f"spread = {lk['bearing_spread_deg']:.1f} deg")
    else:
        print("  No locked pairs detected")
    print()

    # Footer
    print("=" * 78)
    print("  The instrument reads. The expert decides. The loop stays open.")
    print("=" * 78)
    print()
    print(f"  JSON written: {json_path}")
    print(f"  Section plates: {N} (1 per year)")
    print(f"  Bearing pairs: {D * (D - 1) // 2}")
    print(f"  Locks detected: {len(locks)}")
    print()


if __name__ == "__main__":
    main()
