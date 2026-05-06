#!/usr/bin/env python3
"""
USA EMBER yearly aggregator — extends USA EMBER pipeline-ready CSV from
T=25 (2000-2024 in the older 2024 release) to T=26 (2000-2025) by
aggregating monthly TWh values from the EMBER 2025 monthly long-format
release.

Source: DATA/Energy/Embers 2025/monthly_full_release_long_format.csv
Output: rebuilt USA yearly CSV with same carrier columns as the other
        EMBER countries. Writes alongside the existing pipeline_ready CSV.

Carriers: Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil,
          Other Renewables, Solar, Wind  (D = 9)
"""
from __future__ import annotations
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "DATA" / "Energy" / "Embers 2025" / "monthly_full_release_long_format.csv"
OUT = ROOT / "Current-Repo" / "Hs" / "data" / "Energy" / "EMBER_pipeline_ready" / "ember_USA_United_States_generation_TWh.csv"

CARRIERS = ["Bioenergy", "Coal", "Gas", "Hydro", "Nuclear",
            "Other Fossil", "Other Renewables", "Solar", "Wind"]


def main():
    # year → carrier → TWh (sum of months)
    data = defaultdict(lambda: defaultdict(float))
    with SRC.open() as f:
        r = csv.reader(f)
        h = next(r)
        idx = {n: h.index(n) for n in
               ["Area", "Date", "Category", "Subcategory", "Variable", "Unit", "Value"]}
        for row in r:
            if row[idx["Area"]] != "United States of America": continue
            if row[idx["Category"]]    != "Electricity generation": continue
            if row[idx["Subcategory"]] != "Fuel": continue
            if row[idx["Unit"]]        != "TWh": continue
            carrier = row[idx["Variable"]]
            if carrier not in CARRIERS: continue
            try:
                val = float(row[idx["Value"]])
            except ValueError:
                continue
            year = row[idx["Date"]][:4]   # YYYY-MM-DD → YYYY
            data[int(year)][carrier] += val

    # Drop any partial year beyond 2025 (the canonical EMBER 2025 release window)
    all_years = sorted(data.keys())
    years = [y for y in all_years if 2000 <= y <= 2025]
    if any(y > 2025 for y in all_years):
        print(f"  Note: dropping partial-year data beyond 2025 ({[y for y in all_years if y > 2025]})")
    print(f"Years kept: {years[0]}–{years[-1]} ({len(years)} years)")
    print(f"Carriers per year: {len(CARRIERS)}")

    # Validate completeness
    missing = []
    for y in years:
        for c in CARRIERS:
            if c not in data[y] or data[y][c] <= 0:
                missing.append((y, c))
    if missing:
        print(f"WARNING: {len(missing)} (year, carrier) cells missing or zero — adapter will substitute zero-replacement floor")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Year"] + CARRIERS)
        for y in years:
            row = [y]
            for c in CARRIERS:
                v = data[y].get(c, 0.0)
                row.append(f"{v:.2f}" if v > 0 else "0")
            w.writerow(row)
    print(f"\nOutput: {OUT}")
    print(f"Rows written: {len(years)}")
    print(f"\nFirst row: {years[0]} — {[f'{c}: {data[years[0]].get(c,0):.2f}' for c in CARRIERS]}")
    print(f"Last row:  {years[-1]} — {[f'{c}: {data[years[-1]].get(c,0):.2f}' for c in CARRIERS]}")


if __name__ == "__main__":
    main()
