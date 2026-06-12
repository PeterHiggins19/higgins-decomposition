#!/usr/bin/env python3
"""
Two alternative bin schemes for the Ball (2022) intraplate-volcanic dataset.

(a) Age epochs   — chronostratigraphic intervals from the IUGS chart
(b) TAS rock type — Total-Alkali-Silica classification (Le Bas 1986)

Used to test whether the helmsman lineage K2O -> MgO -> Na2O -> SiO2
observed under Region binning is a property of the simplex or an artefact
of geographic aggregation.

Outputs (in this folder):
  ball_oxides_by_age_barycenters.csv
  ball_oxides_by_tas_barycenters.csv
  ball_oxides_by_age_summary.json
  ball_oxides_by_tas_summary.json
"""
import csv, json, math, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC  = ROOT / "DATA" / "Geochemistry" / "2022-3-RY3BRK_Ball_data.csv"
OUT  = Path(__file__).resolve().parent

OXIDES = ["SiO2","TiO2","Al2O3","FeO","CaO","MgO","MnO","K2O","Na2O","P2O5"]
MIN_N  = 10

# IUGS chronostratigraphy — geological epochs, Ma boundaries
AGE_EPOCHS = [
    ("Holocene",          0.000,  0.0117),
    ("Late_Pleistocene",  0.0117, 0.129),
    ("Middle_Pleistocene",0.129,  0.774),
    ("Early_Pleistocene", 0.774,  2.58),
    ("Pliocene",          2.58,   5.333),
    ("Late_Miocene",      5.333,  11.63),
    ("Mid_Miocene",       11.63,  15.97),
    ("Early_Miocene",     15.97,  23.03),
    ("Oligocene",         23.03,  33.9),
    ("Eocene_or_older",   33.9,   200.0),
]


def aitchison_barycenter(rows):
    if not rows: return None
    D = len(rows[0])
    log_means = [sum(math.log(r[j]) for r in rows) / len(rows) for j in range(D)]
    g = [math.exp(lm) for lm in log_means]
    t = sum(g)
    return [x/t for x in g]


def epoch_for_age(age_ma):
    for name, lo, hi in AGE_EPOCHS:
        if lo <= age_ma < hi:
            return name
    return None


def main():
    with SRC.open(encoding="utf-8", errors="replace") as f:
        all_rows = list(csv.reader(f))
    header = all_rows[3]
    data_rows = all_rows[4:]

    cols = {n: header.index(n) for n in
            ["TAS_Description", "Age", "Region", "Larger_Region"] + OXIDES}
    oxide_idx = [cols[ox] for ox in OXIDES]

    # ── Pass 1: clean filtering ──
    clean = []
    for r in data_rows:
        if len(r) < max(oxide_idx) + 1: continue
        try:
            vals = [float(r[k]) for k in oxide_idx]
        except ValueError:
            continue
        if any(v <= 0 for v in vals): continue
        try:
            age = float(r[cols["Age"]])
        except (ValueError, IndexError):
            age = None
        tas = (r[cols["TAS_Description"]] or "").strip()
        clean.append({"oxides": vals, "age": age, "tas": tas,
                      "region": (r[cols["Region"]] or "").strip(),
                      "larger_region": (r[cols["Larger_Region"]] or "").strip()})

    print(f"Clean rows (oxides positive): {len(clean)}")

    # ── (a) Age binning ──
    by_age = collections.defaultdict(list)
    for s in clean:
        if s["age"] is None: continue
        ep = epoch_for_age(s["age"])
        if ep:
            by_age[ep].append(s)

    age_kept = {k: v for k, v in by_age.items() if len(v) >= MIN_N}
    print(f"\n[Age] Distinct epochs with samples: {len(by_age)}, kept (n>={MIN_N}): {len(age_kept)}")
    print(f"[Age] Samples in kept epochs: {sum(len(v) for v in age_kept.values())}")

    # Write age barycenters in chronological order (oldest first or youngest first?)
    # Use youngest-to-oldest so the trajectory reads "now -> past"
    epoch_order = [name for name, lo, hi in AGE_EPOCHS if name in age_kept]
    age_summary = []
    with (OUT / "ball_oxides_by_age_barycenters.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Epoch"] + OXIDES)
        for ep in epoch_order:
            samples = age_kept[ep]
            closed = [[v/sum(s["oxides"]) for v in s["oxides"]] for s in samples]
            bary = aitchison_barycenter(closed)
            w.writerow([ep] + [f"{v:.10f}" for v in bary])
            tas_top = collections.Counter(s["tas"] for s in samples if s["tas"]).most_common(1)
            ages = [s["age"] for s in samples if s["age"] is not None]
            age_summary.append({
                "epoch": ep,
                "n_samples": len(samples),
                "median_age_Ma": statistics.median(ages) if ages else None,
                "age_range_Ma": [min(ages), max(ages)] if ages else None,
                "dominant_TAS": tas_top[0][0] if tas_top else None,
                "barycenter": bary,
            })
            print(f"  {ep:<22s}  n={len(samples):5d}  median_age={statistics.median(ages):6.2f} Ma  TAS={tas_top[0][0] if tas_top else '-'}")

    with (OUT / "ball_oxides_by_age_summary.json").open("w") as f:
        json.dump({
            "scheme": "Age (IUGS epoch)",
            "n_total_clean": len(clean),
            "n_with_age": sum(1 for s in clean if s["age"] is not None),
            "n_epochs_kept": len(age_kept),
            "ordering": "youngest_to_oldest",
            "min_samples_per_epoch": MIN_N,
            "oxides": OXIDES,
            "epochs": age_summary,
        }, f, indent=2)

    # ── (b) TAS binning ──
    by_tas = collections.defaultdict(list)
    for s in clean:
        if s["tas"]:
            by_tas[s["tas"]].append(s)
    tas_kept = {k: v for k, v in by_tas.items() if len(v) >= MIN_N}
    print(f"\n[TAS] Distinct TAS classes: {len(by_tas)}, kept (n>={MIN_N}): {len(tas_kept)}")
    print(f"[TAS] Samples in kept classes: {sum(len(v) for v in tas_kept.values())}")

    # Order TAS classes along the IUGS TAS-diagram silica axis (low SiO2 -> high SiO2).
    # Use median SiO2 of each class as the ordering key.
    tas_order = sorted(tas_kept.keys(),
                       key=lambda k: statistics.median(s["oxides"][0]/sum(s["oxides"])
                                                       for s in tas_kept[k]))
    tas_summary = []
    with (OUT / "ball_oxides_by_tas_barycenters.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["TAS_class"] + OXIDES)
        for cls in tas_order:
            samples = tas_kept[cls]
            closed = [[v/sum(s["oxides"]) for v in s["oxides"]] for s in samples]
            bary = aitchison_barycenter(closed)
            w.writerow([cls.replace(" ","_")] + [f"{v:.10f}" for v in bary])
            sio2s = [s["oxides"][0]/sum(s["oxides"]) for s in samples]
            tas_summary.append({
                "tas_class": cls,
                "n_samples": len(samples),
                "median_SiO2_frac": statistics.median(sio2s),
                "barycenter": bary,
            })
            print(f"  {cls:<25s}  n={len(samples):5d}  med_SiO2={statistics.median(sio2s):.4f}")

    with (OUT / "ball_oxides_by_tas_summary.json").open("w") as f:
        json.dump({
            "scheme": "TAS (Total Alkali-Silica) class",
            "n_total_clean": len(clean),
            "n_with_TAS": sum(1 for s in clean if s["tas"]),
            "n_classes_kept": len(tas_kept),
            "ordering": "ascending_median_SiO2",
            "min_samples_per_class": MIN_N,
            "oxides": OXIDES,
            "classes": tas_summary,
        }, f, indent=2)

    print("\nDone.")


if __name__ == "__main__":
    main()
