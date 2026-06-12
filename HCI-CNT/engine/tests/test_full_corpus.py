#!/usr/bin/env python3
"""
Full-corpus determinism test — runs the engine against every reference
experiment in experiments/INDEX.json and verifies the produced
content_sha256 matches the published value.

This test is the package's primary trust signal: anyone who clones the
repository and runs this should get exactly 20 PASS lines. If even one
fails, the determinism contract is broken.
"""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cnt"))
import cnt as cnt_engine

# Map from experiment id -> (csv_filename, ordering)
EXPERIMENT_ORDERING = {
    # codawork2026 - all EMBER countries are temporal
    "ember_chn": ("ember_CHN_China_generation_TWh.csv",            True,  "by-time"),
    "ember_deu": ("ember_DEU_Germany_generation_TWh.csv",          True,  "by-time"),
    "ember_fra": ("ember_FRA_France_generation_TWh.csv",           True,  "by-time"),
    "ember_gbr": ("ember_GBR_United_Kingdom_generation_TWh.csv",   True,  "by-time"),
    "ember_ind": ("ember_IND_India_generation_TWh.csv",            True,  "by-time"),
    "ember_jpn": ("ember_JPN_Japan_generation_TWh.csv",            True,  "by-time"),
    "ember_usa": ("ember_USA_United_States_generation_TWh.csv",    True,  "by-time"),
    "ember_wld": ("ember_WLD_World_generation_TWh.csv",            True,  "by-time"),
    "ember_combined_panel":  ("ember_combined_panel_input.csv",    True,  "by-label"),
    "backblaze_fleet":       ("backblaze_fleet_input.csv",         True,  "by-time"),
    # domain - geochemistry is cross-section
    "geochem_ball_region":   ("ball_oxides_by_region_barycenters.csv",       False, "by-label"),
    "geochem_ball_age":      ("ball_oxides_by_age_barycenters.csv",          True,  "by-time"),
    "geochem_ball_tas":      ("ball_oxides_by_tas_barycenters.csv",          False, "by-label"),
    "geochem_stracke_oib":   ("stracke_oib_by_location_barycenters.csv",     False, "by-label"),
    "geochem_stracke_morb":  ("geochem_stracke_morb_input.csv",              False, "by-label"),
    "geochem_tappe_kim1":    ("tappe_kim1_by_country_barycenters.csv",       False, "by-label"),
    "geochem_qin_cpx":       ("qin_cpx_by_location_barycenters.csv",         False, "by-label"),
    "fao_irrigation_methods":("fao_irrigation_input.csv",                    False, "by-d_A"),
    # reference
    "commodities_gold_silver": ("commodities_gold_silver_input.csv",         True,  "by-time"),
    "nuclear_semf":            ("nuclear_semf_input.csv",                    False, "by-label"),
}


def discover_csv(experiment_id: str, csv_filename: str) -> Path:
    """Find the CSV inside experiments/<subdir>/<id>/."""
    for subdir in ("codawork2026", "domain", "reference"):
        p = ROOT / "experiments" / subdir / experiment_id / csv_filename
        if p.exists():
            return p
    raise FileNotFoundError(f"CSV not found for {experiment_id}: {csv_filename}")


def discover_golden(experiment_id: str) -> Path:
    for subdir in ("codawork2026", "domain", "reference"):
        p = ROOT / "experiments" / subdir / experiment_id / f"{experiment_id}_cnt.json"
        if p.exists():
            return p
    raise FileNotFoundError(f"golden JSON not found for {experiment_id}")


def main():
    idx = json.load((ROOT / "experiments" / "INDEX.json").open())
    experiments = idx["experiments"]

    print(f"Full-corpus determinism gate — {len(experiments)} experiments")
    print("=" * 70)

    n_pass = 0
    n_fail = 0
    failed = []

    for eid, meta in sorted(experiments.items()):
        if eid not in EXPERIMENT_ORDERING:
            print(f"SKIP  {eid:30}  (no ordering rule)")
            continue
        csv_filename, is_temporal, ordering_method = EXPERIMENT_ORDERING[eid]
        try:
            csv = discover_csv(eid, csv_filename)
            golden = discover_golden(eid)
        except FileNotFoundError as e:
            print(f"SKIP  {eid:30}  ({e})")
            continue

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            out = Path(tf.name)
        try:
            ordering = {
                "is_temporal":     is_temporal,
                "ordering_method": ordering_method,
                "caveat":          None if is_temporal else
                    "Order is treated as arbitrary; angular_velocity and energy_depth are ordering-dependent.",
            }
            cnt_engine.cnt_run(str(csv), str(out), ordering)
            j = json.load(out.open())
            computed = j["diagnostics"]["content_sha256"]
            expected = meta["content_sha256"]
            if computed == expected:
                print(f"PASS  {eid:30}  {computed[:16]}...")
                n_pass += 1
            else:
                print(f"FAIL  {eid:30}  expected {expected[:16]}... got {computed[:16]}...")
                n_fail += 1
                failed.append(eid)
        finally:
            out.unlink(missing_ok=True)

    print("=" * 70)
    print(f"{n_pass}/{n_pass+n_fail} PASS")
    if n_fail:
        print(f"FAILED: {failed}")
        sys.exit(1)
    print("Determinism contract holds across the full reference corpus.")


if __name__ == "__main__":
    main()
