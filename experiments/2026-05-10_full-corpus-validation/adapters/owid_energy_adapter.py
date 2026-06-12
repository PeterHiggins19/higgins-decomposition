"""
owid-energy adapter — primary-energy-source compositional time series per country.

Reads owid-energy-data.csv (Our World in Data energy dataset) and produces
one pipeline-ready compositional CSV per country with sufficient coverage.

Carriers (D = 8): coal, gas, oil, nuclear, hydro, solar, wind, biofuel.
We deliberately exclude `other_renewable_consumption` — it is partially
double-counted with biofuel in OWID's pre-2010 records and reduces dataset
quality. Each country's output is a year-indexed composition over those 8
primary-energy sources.

Output: experiments/2026-05-10_full-corpus-validation/raw_inputs/owid_energy_<iso>.csv
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

# Walk up to find DATA folder containing the OWID file
_THIS = Path(__file__).resolve()
def _find_owid_csv():
    cur = _THIS
    for _ in range(10):
        cand = cur / "DATA" / "Energy" / "owid-energy-data.csv"
        if cand.is_file():
            return cand
        if cur.parent == cur:
            break
        cur = cur.parent
    raise FileNotFoundError("Could not locate owid-energy-data.csv")

SRC = _find_owid_csv()
OUT_DIR = _THIS.parent.parent / "raw_inputs"

# Carrier columns to extract (consumption in TWh)
CARRIERS = [
    ("coal_consumption", "Coal"),
    ("gas_consumption", "Gas"),
    ("oil_consumption", "Oil"),
    ("nuclear_consumption", "Nuclear"),
    ("hydro_consumption", "Hydro"),
    ("solar_consumption", "Solar"),
    ("wind_consumption", "Wind"),
    ("biofuel_consumption", "Biofuel"),
]
CARRIER_KEYS = [c[0] for c in CARRIERS]
CARRIER_LABELS = [c[1] for c in CARRIERS]

MIN_YEARS = 15      # require at least 15 years of complete data
MIN_NON_ZERO = 4    # require at least 4 carriers with non-zero in any given year


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # First pass: index by country
    by_country: Dict[str, List[Dict]] = {}
    with SRC.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            country = row["country"]
            iso = row.get("iso_code", "").strip()
            if not iso or len(iso) != 3:
                continue  # skip aggregates like "Africa", "ASEAN (Ember)"
            year_str = row["year"]
            try:
                year = int(year_str)
            except ValueError:
                continue

            # Extract carrier values; skip if any are missing
            carrier_vals = []
            ok = True
            for k in CARRIER_KEYS:
                v = row.get(k, "")
                if v == "" or v is None:
                    ok = False
                    break
                try:
                    carrier_vals.append(float(v))
                except ValueError:
                    ok = False
                    break
            if not ok:
                continue
            # Need at least MIN_NON_ZERO non-zero carriers (closure needs this)
            non_zero = sum(1 for v in carrier_vals if v > 0)
            if non_zero < MIN_NON_ZERO:
                continue
            # Replace exact-zero values with a small fraction of the row total
            # so closure works (compositional analysis can't accept zeros).
            row_total = sum(carrier_vals)
            if row_total <= 0:
                continue
            eps = row_total * 1e-6
            carrier_vals = [max(v, eps) for v in carrier_vals]

            by_country.setdefault(iso, []).append({
                "country": country,
                "year": year,
                "values": carrier_vals,
            })

    # Second pass: write one CSV per country with enough years
    written = []
    skipped = []
    for iso, rows in sorted(by_country.items()):
        rows.sort(key=lambda r: r["year"])
        if len(rows) < MIN_YEARS:
            skipped.append((iso, len(rows)))
            continue
        out_path = OUT_DIR / f"owid_energy_{iso}.csv"
        with out_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Year"] + CARRIER_LABELS)
            for r in rows:
                w.writerow([r["year"]] + [f"{v:.6f}" for v in r["values"]])
        written.append({
            "iso": iso,
            "country_name": rows[0]["country"],
            "n_years": len(rows),
            "year_min": rows[0]["year"],
            "year_max": rows[-1]["year"],
            "out_path": str(out_path.relative_to(_THIS.parents[2])),
        })

    print(f"Source: {SRC}")
    print(f"Output dir: {OUT_DIR}")
    print(f"Countries written: {len(written)}")
    print(f"Countries skipped (too few years, < {MIN_YEARS}): {len(skipped)}")
    print()
    print("Per-country summary:")
    for w in written:
        print(f"  {w['iso']}  {w['country_name']:30s}  T={w['n_years']:3d}  {w['year_min']}-{w['year_max']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
