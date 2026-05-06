#!/usr/bin/env python3
"""
Region-binned aggregation of the Ball (2022) intraplate-volcanic dataset.

Reduces 25,449 oxide-complete rock samples (D=10 oxides) into 95 region-level
Aitchison barycenters (n>=10 samples per region kept), enabling Stage 3
day-triad analysis to complete on a dataset that is non-temporal at the
sample level.

Rationale
---------
The CNT/HCI Stage 3 day-triad analysis enumerates C(N, 3) day combinations.
At N=26,266 (the raw Ball dataset), this is 3.02 trillion triads, which times
out the engine and would require ~750 TB of result memory. Region binning
reduces N to 95, giving C(95, 3) = 138,415 triads (sub-second runtime).

The choice of binning covariate (Region, 114 distinct values in the raw data)
preserves geographic structure while letting the simplex tell its story
across continental and oceanic provinces. Each region's barycenter is the
geometric (Aitchison) mean of its component samples, which is the natural
centre of mass on the simplex.

Inputs
------
DATA/Geochemistry/2022-3-RY3BRK_Ball_data.csv
   Patrick Ball (2022) intraplate volcanic compilation, CC-BY 4.0.
   DOI: 10.25625/RY3BRK
   Header at line 4. 67 columns. We use:
     Region (col 3), Larger_Region (2), TAS_Description (5),
     Alkalinity (6), Age (7), and the 10 oxide columns (12-21):
     SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5

Outputs (in this folder)
------------------------
ball_oxides_by_region_long.csv          One row per sample, with Region
                                        and closed (sum=1) oxide proportions.
ball_oxides_by_region_barycenters.csv   95 rows, Aitchison barycenter per region.
                                        Suitable input for cnt_tensor_engine.py.
ball_oxides_by_region_summary.json      Per-region n, dominant TAS, dominant
                                        alkalinity, median age, parent
                                        Larger_Region.

Filtering
---------
1. Drop rows with empty Region.
2. Drop rows with any oxide missing or non-positive.
3. Drop regions with n < 10 samples (not enough to estimate a stable
   geometric-mean barycenter).

After filtering: 25,382 of 25,449 oxide-complete samples (99.7%) survive,
distributed across 95 regions.

The instrument reads. The expert decides. The loop stays open.
"""
import csv, json, math, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]   # ...\Claude CoWorker\
SRC  = ROOT / "DATA" / "Geochemistry" / "2022-3-RY3BRK_Ball_data.csv"
OUT  = Path(__file__).resolve().parent

OXIDES = ["SiO2", "TiO2", "Al2O3", "FeO", "CaO",
          "MgO",  "MnO",  "K2O",   "Na2O", "P2O5"]
MIN_N  = 10


def aitchison_barycenter(rows):
    """Geometric mean of N positive D-vectors, re-closed to sum=1."""
    if not rows:
        return None
    D = len(rows[0])
    log_means = []
    for j in range(D):
        log_means.append(sum(math.log(r[j]) for r in rows) / len(rows))
    g = [math.exp(lm) for lm in log_means]
    total = sum(g)
    return [x / total for x in g]


def main():
    with SRC.open(encoding="utf-8", errors="replace") as f:
        all_rows = list(csv.reader(f))
    header = all_rows[3]
    data_rows = all_rows[4:]

    cols = {name: header.index(name) for name in
            ["Region", "Larger_Region", "TAS_Description",
             "Alkalinity", "Age"] + OXIDES}
    oxide_idx = [cols[ox] for ox in OXIDES]

    clean = []
    for r in data_rows:
        if len(r) < max(oxide_idx) + 1:
            continue
        region = (r[cols["Region"]] or "").strip()
        if not region:
            continue
        try:
            vals = [float(r[k]) for k in oxide_idx]
        except ValueError:
            continue
        if any(v <= 0 for v in vals):
            continue
        clean.append({
            "Region":        region,
            "Larger_Region": (r[cols["Larger_Region"]]   or "").strip(),
            "TAS":           (r[cols["TAS_Description"]] or "").strip(),
            "Alkalinity":    (r[cols["Alkalinity"]]      or "").strip(),
            "Age":           (r[cols["Age"]]             or "").strip(),
            "oxides":        vals,
        })

    by_region = collections.defaultdict(list)
    for s in clean:
        by_region[s["Region"]].append(s)
    kept = {k: v for k, v in by_region.items() if len(v) >= MIN_N}

    print(f"Clean rows:              {len(clean)}")
    print(f"Distinct regions:        {len(by_region)}")
    print(f"Regions kept (n>={MIN_N}):    {len(kept)}")
    print(f"Samples in kept regions: {sum(len(v) for v in kept.values())}")

    # Long-format CSV
    with (OUT / "ball_oxides_by_region_long.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Region", "Sample_Idx"] + OXIDES)
        for region, samples in sorted(kept.items()):
            for i, s in enumerate(samples):
                t = sum(s["oxides"])
                w.writerow([region, i] + [f"{v/t:.10f}" for v in s["oxides"]])

    # Barycenters CSV
    summary = []
    with (OUT / "ball_oxides_by_region_barycenters.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Region"] + OXIDES)
        for region, samples in sorted(kept.items()):
            closed = []
            for s in samples:
                t = sum(s["oxides"])
                closed.append([v / t for v in s["oxides"]])
            bary = aitchison_barycenter(closed)
            w.writerow([region] + [f"{v:.10f}" for v in bary])

            ages = []
            for s in samples:
                try:
                    ages.append(float(s["Age"]))
                except ValueError:
                    pass
            tas = collections.Counter(s["TAS"] for s in samples if s["TAS"]).most_common(1)
            alk = collections.Counter(s["Alkalinity"] for s in samples if s["Alkalinity"]).most_common(1)
            lr  = collections.Counter(s["Larger_Region"] for s in samples if s["Larger_Region"]).most_common(1)
            summary.append({
                "region":              region,
                "n_samples":           len(samples),
                "larger_region":       lr[0][0]  if lr  else None,
                "dominant_TAS":        tas[0][0] if tas else None,
                "dominant_TAS_frac":   tas[0][1] / len(samples) if tas else None,
                "dominant_alkalinity": alk[0][0] if alk else None,
                "median_age_Ma":       statistics.median(ages) if ages else None,
                "barycenter":          bary,
            })

    with (OUT / "ball_oxides_by_region_summary.json").open("w") as f:
        json.dump({
            "source":              str(SRC.name),
            "n_total_data_rows":   len(data_rows),
            "n_clean":             len(clean),
            "n_regions_total":     len(by_region),
            "min_samples_per_region": MIN_N,
            "n_regions_kept":      len(kept),
            "n_samples_kept":      sum(len(v) for v in kept.values()),
            "oxides":              OXIDES,
            "regions":             summary,
        }, f, indent=2)

    print("Written:")
    print(f"  {OUT / 'ball_oxides_by_region_long.csv'}")
    print(f"  {OUT / 'ball_oxides_by_region_barycenters.csv'}")
    print(f"  {OUT / 'ball_oxides_by_region_summary.json'}")


if __name__ == "__main__":
    main()
