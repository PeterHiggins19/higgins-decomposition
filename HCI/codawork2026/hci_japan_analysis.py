#!/usr/bin/env python3
"""
HCI Japan EMBER Energy — Full 3-Stage Analysis
================================================

CoDaWork 2026 Experiment 1: Japan electricity generation (2000-2025)
through the complete HCI pipeline (Stage 1 → Stage 2 → Stage 3).

Reads: ember_JPN_Japan_generation_TWh.csv
Outputs: hci_japan_results.json (all stages, all metrics, all regimes)

The instrument reads. The expert decides. The loop stays open.
"""

import sys
import os
import json
import math
import csv

# Add parent HCI folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hci_stage2 import run_stage2, Stage1Data, _closure, _clr, _metric_tensor
from hci_stage3 import run_stage3
from hci_cbs import (cnt_closure, cnt_bearing_tensor,
                     cnt_angular_velocity, cnt_steering_sensitivity,
                     cnt_helmsman, cnt_aitchison_metric_tensor,
                     cnt_condition_number)


def load_japan_data(csv_path):
    """Load Japan EMBER CSV and return compositions, carriers, years."""
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


def compute_cbs_data(compositions, carrier_names, years):
    """Run full CBS/CNT computation for each year."""
    D = len(carrier_names)
    N = len(compositions)

    records = []
    prev_h = None

    for t in range(N):
        x = _closure(compositions[t])
        h = _clr(x)

        # Higgins Scale
        entropy = -sum(xi * math.log(xi) for xi in x if xi > 0)
        hs = 1.0 - entropy / math.log(D)

        # Metric tensor diagnostics
        G = cnt_aitchison_metric_tensor(x)
        diag_sensitivities = {carrier_names[j]: G[j][j] for j in range(D)}
        energy = sum(v ** 2 for v in h)  # metric energy = ||h||^2
        cond = cnt_condition_number(x)

        # Bearing tensor (all pairwise bearings) — takes CLR vector h
        bearings = cnt_bearing_tensor(h)

        # Steering sensitivity (diagonal only) — takes CLR vector h
        steering = cnt_steering_sensitivity(h)

        # Angular velocity and helmsman (need previous CLR) — both take CLR vectors
        omega = 0.0
        helmsman_name = None
        helmsman_delta = 0.0
        if prev_h is not None:
            omega = cnt_angular_velocity(prev_h, h)  # returns degrees
            helm_idx, helm_name, helm_delta = cnt_helmsman(prev_h, h, carrier_names)
            helmsman_name = helm_name
            helmsman_delta = abs(helm_delta)

        record = {
            "year": years[t],
            "composition": [round(xi, 6) for xi in x],
            "clr": [round(hi, 6) for hi in h],
            "hs": round(hs, 6),
            "metric_energy": round(energy, 4),
            "condition_number": round(cond, 2),
            "angular_velocity_deg": round(omega, 4),
            "helmsman": helmsman_name,
            "helmsman_delta": round(helmsman_delta, 6),
            "steering_sensitivity": {carrier_names[j]: round(steering[j], 4) for j in range(D)},
            "diagonal_metric": {carrier_names[j]: round(G[j][j], 4) for j in range(D)},
            "bearings_deg": {},
        }

        # Store key bearings (all pairwise) — already in degrees from cnt_bearing_tensor
        for (i, j), angle in bearings.items():
            pair_name = f"{carrier_names[i]}-{carrier_names[j]}"
            record["bearings_deg"][pair_name] = round(angle, 4)

        records.append(record)
        prev_h = h

    return records


def main():
    # Find Japan data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir,
        "../../experiments/Hs-M02_EMBER_Energy/codawork2026/data/ember_JPN_Japan_generation_TWh.csv")
    data_path = os.path.normpath(data_path)

    if not os.path.exists(data_path):
        print(f"ERROR: Japan data not found at {data_path}")
        sys.exit(1)

    print("=" * 72)
    print("HCI JAPAN EMBER ENERGY — FULL 3-STAGE ANALYSIS")
    print("CoDaWork 2026 Experiment 1")
    print("=" * 72)
    print()

    # Load data
    print(f"Loading: {data_path}")
    compositions, carrier_names, years = load_japan_data(data_path)
    D = len(carrier_names)
    N = len(compositions)
    print(f"  Years: {years[0]}-{years[-1]} ({N} observations)")
    print(f"  Carriers: {D} ({', '.join(carrier_names)})")
    print()

    # Stage 1: CBS/CNT computation
    print("Stage 1 — CBS/CNT Computation...")
    cbs_records = compute_cbs_data(compositions, carrier_names, years)
    print(f"  {len(cbs_records)} CBS records computed")
    print()

    # Stage 2: Metric Cross-Examination
    print("Stage 2 — Metric Cross-Examination Engine...")
    # Use years as day_ids (each year = one group with one point)
    day_ids = years
    point_ids = [0] * N

    output_dir = os.path.join(script_dir)
    s2_results = run_stage2(compositions, carrier_names, day_ids, point_ids,
                            output_dir=output_dir)
    print(f"  Groups:        {len(s2_results['group_results'])}")
    print(f"  Group pairs:   {len(s2_results['group_pairwise'])}")
    print(f"  Carrier pairs: {len(s2_results['carrier_pairwise'])}")
    print(f"  Section pairs: {len(s2_results['section_pairwise'])}")
    print()

    # Stage 3: Higher-Degree Analysis
    print("Stage 3 — Higher-Degree Analysis Engine...")
    data = s2_results["data"]
    s3_results = run_stage3(data, output_dir=output_dir)
    print(f"  Day triads:     {len(s3_results['day_triads'])}")
    print(f"  Carrier triads: {len(s3_results['carrier_triads'])}")
    print(f"  Subcomp sets:   {len(s3_results['subcomposition'])}")
    print(f"  Regimes:        {len(s3_results['regimes'])}")
    print()

    # Compile master results JSON
    results = {
        "experiment": "HCI CoDaWork2026 Experiment 1",
        "dataset": "Japan EMBER Electricity Generation (TWh)",
        "years": years,
        "carriers": carrier_names,
        "D": D,
        "N": N,
        "cbs_records": cbs_records,
        "stage2": {
            "group_results": s2_results["group_results"],
            "group_pairwise": s2_results["group_pairwise"][:20],  # top 20
            "carrier_pairwise": s2_results["carrier_pairwise"],   # all 28
            "section_pairwise": s2_results["section_pairwise"],
        },
        "stage3": {
            "day_triads": s3_results["day_triads"][:20],          # top 20
            "carrier_triads": s3_results["carrier_triads"][:20],  # top 20
            "subcomposition": s3_results["subcomposition"][:20],  # top 20
            "regimes": s3_results["regimes"],                     # all
        },
    }

    output_path = os.path.join(script_dir, "hci_japan_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Results written to: {output_path}")
    print()

    # Summary statistics
    print("KEY FINDINGS:")
    print("-" * 72)

    # Top 5 group divergences
    print("\nTop 5 Year-Pair Divergences:")
    for r in s2_results["group_pairwise"][:5]:
        print(f"  {r['group_A']}-{r['group_B']}: d={r['metric_distance']:.4f}  "
              f"({r['classification']})  dominant={r['dominant_contrast_carrier']}")

    # Top 5 carrier oppositions
    print("\nTop 5 Carrier Pair Oppositions:")
    for r in s2_results["carrier_pairwise"][:5]:
        print(f"  {r['carrier_pair']}: opp={r['opposition_score']:.4f}  "
              f"co={r['co_movement_score']:.4f}  ({r['classification']})")

    # Regimes
    print(f"\nMetric Regimes Detected: {len(s3_results['regimes'])}")
    for r in s3_results["regimes"]:
        print(f"  Regime {r['regime_id']}: {r['time_window_start']} to {r['time_window_end']}  "
              f"({r['member_points']} pts)  dominant={r.get('dominant_carriers', '---')}")

    # Helmsman history
    print("\nHelmsman (DCDI) History:")
    for rec in cbs_records:
        if rec["helmsman"]:
            print(f"  {rec['year']}: {rec['helmsman']}  "
                  f"omega={rec['angular_velocity_deg']:.2f}deg  "
                  f"delta={rec['helmsman_delta']:.4f}")

    print()
    print("=" * 72)
    print("Analysis complete.")
    print("=" * 72)


if __name__ == "__main__":
    main()
