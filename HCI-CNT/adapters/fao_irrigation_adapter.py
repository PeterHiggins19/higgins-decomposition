#!/usr/bin/env python3
"""
FAO Aquastat irrigation-method adapter.

Builds a cross-sectional D=3 composition over countries:
    Surface irrigation   (FAO_AS_4308)
    Sprinkler irrigation (FAO_AS_4309)
    Localized irrigation (FAO_AS_4310)

These three are the canonical 'full-control irrigation method' partition;
they sum to FAO_AS_4311 (Area equipped for full control irrigation: total).

For each country, take the most recent year where all three indicators
are reported (and positive). Skip countries with incomplete data.

Output: fao_irrigation_input.csv with rows = country, cols = D=3 carriers.
The composition is a country-level snapshot — non-temporal.

Source: DATA/World Bank Group Data/FAO_AS_WIDEF.csv
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "DATA" / "World Bank Group Data" / "FAO_AS_WIDEF.csv"
OUT = Path(__file__).resolve().parent.parent / "domain" / "fao_irrigation_methods" / "fao_irrigation_input.csv"

INDICATORS = {
    "FAO_AS_4308": "Surface",      # Surface irrigation
    "FAO_AS_4309": "Sprinkler",    # Sprinkler irrigation
    "FAO_AS_4310": "Localized",    # Localized (drip/micro) irrigation
}


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # country -> {indicator: {year: value}}
    data: dict[str, dict[str, dict[int, float]]] = {}

    with SRC.open() as f:
        r = csv.reader(f)
        h = next(r)
        country_idx = h.index("REF_AREA_LABEL")
        ind_idx     = h.index("INDICATOR")
        # year columns are after OBS_CONF_LABEL (col 19)
        year_cols = []
        for j, name in enumerate(h):
            try:
                yr = int(name)
                if 1900 <= yr <= 2030:
                    year_cols.append((j, yr))
            except ValueError:
                pass

        for row in r:
            ind = row[ind_idx]
            if ind not in INDICATORS:
                continue
            country = (row[country_idx] or "").strip()
            if not country:
                continue
            d = data.setdefault(country, {})
            ds = d.setdefault(ind, {})
            for j, yr in year_cols:
                if j < len(row) and row[j].strip():
                    try:
                        v = float(row[j])
                        if v > 0:
                            ds[yr] = v
                    except ValueError:
                        pass

    # For each country, find most recent year with all 3 indicators present
    rows = []
    for country, ds in sorted(data.items()):
        if not all(ind in ds for ind in INDICATORS):
            continue
        common_years = set(ds["FAO_AS_4308"].keys()) & set(ds["FAO_AS_4309"].keys()) & set(ds["FAO_AS_4310"].keys())
        if not common_years:
            continue
        latest = max(common_years)
        v_surf = ds["FAO_AS_4308"][latest]
        v_spr  = ds["FAO_AS_4309"][latest]
        v_loc  = ds["FAO_AS_4310"][latest]
        # All values are in 1000 ha (UNIT_MULT = 3 in source)
        rows.append([f"{country}_{latest}", v_surf, v_spr, v_loc])

    # Sort by total irrigated area descending — biggest irrigators first
    rows.sort(key=lambda r: -(r[1] + r[2] + r[3]))

    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Country_Year", "Surface", "Sprinkler", "Localized"])
        for r in rows:
            label = r[0].replace(" ", "_").replace(",", "")
            w.writerow([label] + [f"{v:.6g}" for v in r[1:]])

    print(f"FAO Aquastat irrigation-method adapter")
    print(f"  Total countries with all 3 carriers: {len(rows)}")
    print(f"  Top 10 by total irrigated area:")
    for r in rows[:10]:
        total = r[1] + r[2] + r[3]
        print(f"    {r[0]:<35s}  Surf={r[1]:>10.0f}  Spr={r[2]:>10.0f}  Loc={r[3]:>10.0f}  Total={total:>10.0f} (1000 ha)")
    print(f"  Output: {OUT}")


if __name__ == "__main__":
    main()
