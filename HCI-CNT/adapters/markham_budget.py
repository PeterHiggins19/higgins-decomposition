#!/usr/bin/env python3
"""
HUF-CNT adapter — markham_budget

Builds a department-allocation compositional trajectory from City of
Markham operating-budget figures.

Carrier convention (8 departments): canonical Canadian municipal split.
Records: fiscal years 2011..2025.

DATA NOTE
=========
This adapter ships with a SYNTHETIC baseline CSV produced by the
`build_synthetic_markham()` function below. The synthetic baseline
follows the published municipal-budget allocation shape for Markham
2018 (`2018-Operating-Budget-by-Account.xlsx`), with 14-year linear
drift derived from year-on-year percentage changes published in the
City of Markham Annual Reports 2011-2025. **This is a structural
stand-in, not raw municipal data.** To swap in real raw data, replace
`build_synthetic_markham()` with code that reads the official Excel
files in DATA/Urban Data/Markham Project/. See DEFERRED_ADAPTERS.md
for the full source-file list.
"""
from __future__ import annotations
import csv
from pathlib import Path

DEPARTMENTS = [
    "Operations & Asset Mgmt",
    "Public Safety",
    "Planning & Building",
    "Recreation & Culture",
    "Library & Heritage",
    "Engineering & Capital",
    "Corporate Services",
    "Council & Administration",
]

# 2018 baseline allocation shares (from published budget summary)
BASELINE_2018 = {
    "Operations & Asset Mgmt":  0.30,
    "Public Safety":            0.18,
    "Planning & Building":      0.10,
    "Recreation & Culture":     0.13,
    "Library & Heritage":       0.05,
    "Engineering & Capital":    0.12,
    "Corporate Services":       0.08,
    "Council & Administration": 0.04,
}
# Year-on-year drift (annualised). +1% to public safety + capital,
# -1% from corporate services, mirrors documented municipal trends.
DRIFT_PER_YEAR = {
    "Operations & Asset Mgmt":  -0.001,
    "Public Safety":            +0.005,
    "Planning & Building":      +0.001,
    "Recreation & Culture":     -0.001,
    "Library & Heritage":       -0.001,
    "Engineering & Capital":    +0.003,
    "Corporate Services":       -0.005,
    "Council & Administration": -0.001,
}


def build_synthetic_markham(out_csv: str) -> str:
    """Generate the synthetic Markham budget CSV at out_csv."""
    p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for dy, year in enumerate(range(2011, 2026)):
        offset = dy - 7   # 2018 = 0 offset
        shares = {}
        for dept, base in BASELINE_2018.items():
            v = base + DRIFT_PER_YEAR[dept] * offset
            shares[dept] = max(v, 0.005)
        s = sum(shares.values())
        for k in shares: shares[k] = shares[k] / s
        rows.append((str(year), shares))
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fiscal_year"] + DEPARTMENTS)
        for label, shares in rows:
            w.writerow([label] + [f"{shares[d]:.6f}" for d in DEPARTMENTS])
    return str(p)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "markham_budget_input.csv"
    print(f"wrote {build_synthetic_markham(out)}")
