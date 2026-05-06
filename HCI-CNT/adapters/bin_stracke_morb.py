#!/usr/bin/env python3
"""
Stracke 2022 MORB adapter — same EarthChem template as the OIB sheet.

Bins MORB samples by Location, takes Aitchison barycenter per location,
emits D=10 oxide composition per location.

Source: DATA/Geochemistry/2022_09-0SVW6S_Stracke_data.xlsx, sheet Data_MORB.
"""
import openpyxl, csv, json, math, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "DATA" / "Geochemistry" / "2022_09-0SVW6S_Stracke_data.xlsx"
OUT = Path(__file__).resolve().parent.parent / "domain" / "geochem_stracke_morb" / "geochem_stracke_morb_input.csv"

OXIDE_COL_NAMES = ["SIO2","TIO2","AL2O3","FEO","CAO","MGO","MNO","K2O","NA2O","P2O5"]
OUT_OXIDE_NAMES = ["SiO2","TiO2","Al2O3","FeO","CaO","MgO","MnO","K2O","Na2O","P2O5"]
MIN_N = 5


def aitchison_barycenter(rows):
    if not rows: return None
    D = len(rows[0])
    log_means = [sum(math.log(r[j]) for r in rows) / len(rows) for j in range(D)]
    g = [math.exp(lm) for lm in log_means]
    return [v/sum(g) for v in g]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    ws = wb["Data_MORB"]
    rows_iter = ws.iter_rows(values_only=True)
    header = None
    for row in rows_iter:
        if row and row[0] and str(row[0]).strip().upper() == "SAMPLE ID":
            header = row
            break
    if header is None:
        raise SystemExit("Could not find header row containing SAMPLE ID")
    name_to_idx = {(str(c) or "").strip().upper(): j for j, c in enumerate(header) if c is not None}
    oxide_idx = [name_to_idx[ox] for ox in OXIDE_COL_NAMES if ox in name_to_idx]
    if len(oxide_idx) != 10:
        raise SystemExit(f"Missing oxide columns; found indices: {oxide_idx}")
    loc_idx = name_to_idx.get("LOCATION", None)
    if loc_idx is None:
        for j, c in enumerate(header):
            if c and str(c).strip().lower() == "location":
                loc_idx = j; break

    by_loc = collections.defaultdict(list)
    for r in rows_iter:
        if r is None or len(r) <= max(oxide_idx): continue
        try:
            vals = [float(r[k]) if r[k] is not None else None for k in oxide_idx]
        except (ValueError, TypeError):
            continue
        if any(v is None or v <= 0 for v in vals): continue
        loc = (str(r[loc_idx]).strip() if r[loc_idx] is not None else "")
        if not loc: continue
        by_loc[loc].append(vals)

    kept = {k: v for k, v in by_loc.items() if len(v) >= MIN_N}
    print(f"[Stracke MORB] clean rows: {sum(len(v) for v in by_loc.values())}, "
          f"locations: {len(by_loc)}, kept (n>={MIN_N}): {len(kept)}")

    summary = []
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Location"] + OUT_OXIDE_NAMES)
        for loc, vals_list in sorted(kept.items()):
            closed = [[v/sum(vs) for v in vs] for vs in vals_list]
            bary = aitchison_barycenter(closed)
            short = loc.replace(",", "_").replace(" ", "_").replace("/", "_")[:30]
            w.writerow([short] + [f"{v:.10f}" for v in bary])
            summary.append({"location": loc, "n_samples": len(vals_list)})

    with OUT.with_name("geochem_stracke_morb_summary.json").open("w") as f:
        json.dump({"scheme": "Stracke 2022 MORB by Location",
                   "source": str(SRC.name),
                   "oxides": OUT_OXIDE_NAMES,
                   "n_locations_kept": len(kept),
                   "min_samples_per_location": MIN_N,
                   "locations": summary}, f, indent=2)

    print(f"\nTop locations by sample count:")
    for s in sorted(summary, key=lambda x: -x["n_samples"])[:10]:
        print(f"  {s['n_samples']:5d}  {s['location'][:40]}")
    print(f"\nOutput: {OUT}")


if __name__ == "__main__":
    main()
