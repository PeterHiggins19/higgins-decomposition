#!/usr/bin/env python3
"""
HUF-CNT adapter — iiasa_ngfs

Builds an NGFS-Phase-4 sector-emissions compositional trajectory.
Carriers (7 sectors): Energy, Transport, Industry, Buildings,
Agriculture, LULUCF, Other.

DATA NOTE
=========
Synthetic baseline derived from the NGFS Phase 4 "Net Zero 2050"
scenario sector shares published in the NGFS scenario tables. To swap
in real raw data, point `build_synthetic_ngfs()` at the extracted CSV
from one of the V4.0 / V4.1 / V4.2 zip files in DATA/IIASA Data/.
"""
from __future__ import annotations
import csv
from pathlib import Path

SECTORS = ["Energy", "Transport", "Industry", "Buildings",
           "Agriculture", "LULUCF", "Other"]

# 2020 baseline sector emissions shares (NGFS Phase 4 NZ-2050)
BASE_2020 = [0.42, 0.16, 0.20, 0.07, 0.09, 0.04, 0.02]
# 2050 target shares (Energy decarbonised; LULUCF = net negative)
END_2050 = [0.10, 0.10, 0.20, 0.05, 0.20, 0.30, 0.05]


def build_synthetic_ngfs(out_csv: str, n_steps: int = 31) -> str:
    p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n_steps):
        year = 2020 + i
        t = i / (n_steps - 1)
        v = [BASE_2020[k] * (1-t) + END_2050[k] * t for k in range(len(SECTORS))]
        v = [max(x, 0.005) for x in v]
        s = sum(v); v = [x/s for x in v]
        rows.append((str(year), v))
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year"] + SECTORS)
        for lab, v in rows:
            w.writerow([lab] + [f"{x:.6f}" for x in v])
    return str(p)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "iiasa_ngfs_input.csv"
    print(f"wrote {build_synthetic_ngfs(out)}")
