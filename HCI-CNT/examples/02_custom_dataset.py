#!/usr/bin/env python3
"""
HUF-CNT — running the engine on your own data.

Synthetic three-carrier composition demonstrating the minimal CSV
format and shows how to interpret the output. Replace the synthetic
generator with your own data loading.
"""
from __future__ import annotations
import csv
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cnt"))
import cnt as cnt_engine


def make_synthetic_csv(out_csv: Path, T: int = 30):
    """Synthetic 3-carrier trajectory drifting from one corner of the
    simplex toward the centroid. T = 30 records of (a, b, c) summing
    to 100. The engine will close to 1 internally."""
    import math
    rows = []
    for t in range(T):
        # parametric drift
        x = math.cos(t * 0.2) * 0.5 + 1.0
        y = math.sin(t * 0.2) * 0.5 + 1.0
        z = 1.0 + t * 0.05
        s = x + y + z
        rows.append([f"t{t:02d}", x / s * 100, y / s * 100, z / s * 100])
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "carrier_A", "carrier_B", "carrier_C"])
        for r in rows:
            w.writerow([r[0], f"{r[1]:.6f}", f"{r[2]:.6f}", f"{r[3]:.6f}"])


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        csv_path = tmp / "synthetic.csv"
        json_path = tmp / "synthetic_cnt.json"
        make_synthetic_csv(csv_path)
        print(f"Wrote synthetic CSV to {csv_path}")

        ordering = {"is_temporal": True, "ordering_method": "by-time", "caveat": None}
        cnt_engine.cnt_run(str(csv_path), str(json_path), ordering)

        j = json.load(json_path.open())
        ir = j["depth"]["higgins_extensions"]["impulse_response"]
        ca = j["depth"]["higgins_extensions"]["curvature_attractor"]
        di = j["diagnostics"]

        print()
        print("=" * 60)
        print(f"T (records)     : {j['input']['n_records']}")
        print(f"D (carriers)    : {j['input']['n_carriers']}")
        print(f"IR class        : {ir['classification']}")
        amp = ir.get("amplitude_A")
        if amp is not None:
            print(f"Amplitude A     : {amp:.4f}")
        print(f"Period          : {ca.get('period')}")
        print(f"content_sha256  : {di['content_sha256']}")
        print()
        print("This SHA is deterministic for this exact input + engine config.")
        print("Run again — you will get the same SHA.")


if __name__ == "__main__":
    main()
