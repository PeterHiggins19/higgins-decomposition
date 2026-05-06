#!/usr/bin/env python3
"""
Sibling test for the energy-tower-depth = 46 anomaly observed under Region
binning of the Ball (2022) intraplate-volcanic dataset.

We bin the Stracke (2022) Ocean Island Basalt (OIB) compilation by Location
to produce ~80 location-level barycenters (D=10 oxides). Stracke OIB is in
the same domain (intraplate volcanic) as Ball but with completely different
sample population (4,548 OIB samples vs Ball's 25,449).

If energy depth ~ 46 again → high-T region binning is the cause; this is a
generic property of the recursion at this T scale.
If energy depth differs sharply → the depth=46 result is specific to Ball.

Source: DATA/Geochemistry/2022_09-0SVW6S_Stracke_data.xlsx
Sheet:  Data_OIB
DOI:    10.25625/0SVW6S
Citation: Stracke, Andrea et al. 2022, "MORB and OIB databases".
"""
import openpyxl, csv, json, math, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC  = ROOT / "DATA" / "Geochemistry" / "2022_09-0SVW6S_Stracke_data.xlsx"
OUT  = Path(__file__).resolve().parent

OXIDE_COL_NAMES = ["SIO2","TIO2","AL2O3","FEO","CAO","MGO","MNO","K2O","NA2O","P2O5"]
OUT_OXIDE_NAMES = ["SiO2","TiO2","Al2O3","FeO","CaO","MgO","MnO","K2O","Na2O","P2O5"]
MIN_N = 10


def aitchison_barycenter(rows):
    if not rows: return None
    D = len(rows[0])
    log_means = [sum(math.log(r[j]) for r in rows) / len(rows) for j in range(D)]
    return [math.exp(lm) for lm in log_means] if False else (
        lambda g: [x/sum(g) for x in g]
    )([math.exp(lm) for lm in log_means])


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["Data_OIB"]

    # Read header (row 0) and find oxide + location columns
    rows_iter = ws.iter_rows(values_only=True)
    header = next(rows_iter)
    print(f"Stracke OIB header: {len(header)} columns")

    # Match oxide names case-insensitively. EarthChem template uses uppercase.
    name_to_idx = {(str(c) or "").strip().upper(): j for j, c in enumerate(header) if c is not None}
    oxide_idx = []
    for ox in OXIDE_COL_NAMES:
        if ox in name_to_idx:
            oxide_idx.append(name_to_idx[ox])
        else:
            raise SystemExit(f"Missing oxide column: {ox}")
    loc_idx = name_to_idx.get("LOCATION") or name_to_idx.get("Location".upper())
    if loc_idx is None:
        # Already searched uppercased — try original
        for j, c in enumerate(header):
            if c and str(c).strip().lower() == "location":
                loc_idx = j; break
    print(f"Location column index: {loc_idx}")
    print(f"Oxide column indices: {oxide_idx}")

    # Parse data — rows after header. May have sub-header rows; treat any row
    # where oxides parse as floats > 0 as data.
    clean = []
    for r in rows_iter:
        if r is None or len(r) <= max(oxide_idx): continue
        try:
            vals = [float(r[k]) if r[k] is not None else None for k in oxide_idx]
        except (ValueError, TypeError):
            continue
        if any(v is None or v <= 0 for v in vals): continue
        loc = (str(r[loc_idx]).strip() if r[loc_idx] is not None else "")
        if not loc: continue
        clean.append({"oxides": vals, "loc": loc})

    print(f"Clean rows (Location + 10 oxides positive): {len(clean)}")

    by_loc = collections.defaultdict(list)
    for s in clean:
        by_loc[s["loc"]].append(s)
    kept = {k: v for k, v in by_loc.items() if len(v) >= MIN_N}
    print(f"Distinct locations: {len(by_loc)}, kept (n>={MIN_N}): {len(kept)}")
    print(f"Samples in kept locations: {sum(len(v) for v in kept.values())}")

    summary = []
    with (OUT / "stracke_oib_by_location_barycenters.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Location"] + OUT_OXIDE_NAMES)
        for loc, samples in sorted(kept.items()):
            closed = [[v/sum(s["oxides"]) for v in s["oxides"]] for s in samples]
            bary = aitchison_barycenter(closed)
            w.writerow([loc.replace(",","_").replace(" ","_")] + [f"{v:.10f}" for v in bary])
            summary.append({"location": loc, "n_samples": len(samples), "barycenter": bary})

    with (OUT / "stracke_oib_by_location_summary.json").open("w") as f:
        json.dump({
            "scheme": "Stracke OIB by Location",
            "source": str(SRC.name),
            "n_clean": len(clean),
            "n_locations_total": len(by_loc),
            "n_locations_kept": len(kept),
            "min_samples_per_location": MIN_N,
            "oxides": OUT_OXIDE_NAMES,
            "locations": summary,
        }, f, indent=2)

    print("\nTop 10 locations by sample count:")
    for s in sorted(summary, key=lambda x: -x["n_samples"])[:10]:
        print(f"  {s['n_samples']:5d}  {s['location'][:40]}")
    print("\nDone.")


if __name__ == "__main__":
    main()
