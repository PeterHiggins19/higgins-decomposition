#!/usr/bin/env python3
"""
HUF-CNT adapter — financial_sector

Builds a 10-sector portfolio-allocation compositional trajectory
across 252 trading days (one calendar year).

Sectors (S&P GICS): Tech, Health Care, Financials, Cons Discretionary,
Comm Services, Industrials, Cons Staples, Energy, Utilities, Materials.

DATA NOTE
=========
Synthetic baseline derived from S&P 500 GICS sector weights at
2025-01-01 (published index composition), with daily drift modelled
as small Gaussian random walks around the published trends. To swap
in real raw data, point at DATA/financial data/Portfolio.csv +
all_stocks_5yr.csv (see DEFERRED_ADAPTERS.md §4).
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

SECTORS = ["Information Tech", "Health Care", "Financials",
           "Cons Discretionary", "Comm Services", "Industrials",
           "Cons Staples", "Energy", "Utilities", "Materials"]

# 2025-01 S&P 500 GICS weights (approx, normalised)
BASE = [0.31, 0.13, 0.13, 0.10, 0.09, 0.08, 0.06, 0.04, 0.025, 0.025]
# Annual drift (rough sector-rotation signal)
DRIFT = [+0.04, -0.01, -0.005, +0.003, +0.005, -0.002, -0.005,
         -0.015, -0.005, -0.010]


def build_synthetic_financial(out_csv: str, n_days: int = 252,
                              seed: int = 42) -> str:
    import random
    rng = random.Random(seed)
    p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    cur = list(BASE)
    for d in range(n_days):
        # Daily rebalance: linear drift + small Gaussian shock
        for k in range(len(cur)):
            cur[k] = cur[k] * (1 + DRIFT[k] / n_days) \
                     * (1 + rng.gauss(0.0, 0.005))
            cur[k] = max(cur[k], 0.001)
        s = sum(cur)
        norm = [x / s for x in cur]
        rows.append((f"day_{d:03d}", norm))
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day"] + SECTORS)
        for lab, v in rows:
            w.writerow([lab] + [f"{x:.6f}" for x in v])
    return str(p)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "financial_sector_input.csv"
    print(f"wrote {build_synthetic_financial(out)}")
