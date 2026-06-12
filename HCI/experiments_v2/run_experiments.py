#!/usr/bin/env python3
"""
Master experiment runner — CNT v2.0.0 over the full data corpus.

Reads the registry below, runs cnt.py on each dataset, writes the JSON
into the experiment folder, generates JOURNAL.md from the JSON, and
updates INDEX.json with the run summary.

Run with:
    python3 run_experiments.py                    # run everything
    python3 run_experiments.py codawork2026       # one subset
    python3 run_experiments.py codawork2026/jpn   # one experiment
"""
from __future__ import annotations
import sys, os, json, csv, math, subprocess, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                            # Claude CoWorker/
CNT  = HERE.parent / "cnt_v2" / "cnt.py"

# ──────────────────────────────────────────────────────────────────
# REGISTRY — every CNT v2.0.0 experiment we run
#
# Each entry:
#   id           : unique experiment id, becomes the folder name
#   subdir       : codawork2026 / domain / reference
#   source_csv   : absolute path to ingestible CSV
#   is_temporal  : true if records are a time series
#   ordering     : as-given / by-time / by-label / by-d_A / custom
#   description  : one-sentence purpose
# ──────────────────────────────────────────────────────────────────

EMBER_DIR = ROOT / "Current-Repo/Hs/data/Energy/EMBER_pipeline_ready"
GEOCHEM_BINNING = ROOT / "Current-Repo/Hs/experiments/Hs-05_Geochemistry/region_binning"

REGISTRY = [
    # ── CoDaWork 2026 — EMBER countries individually ──
    *[
        {
            "id":          f"ember_{code.lower()}",
            "subdir":      "codawork2026",
            "source_csv":  str(EMBER_DIR / f"ember_{code}_{name}_generation_TWh.csv"),
            "is_temporal": True,
            "ordering":    "by-time",
            "description": f"EMBER {long_name} electricity generation 2000-2025, {n_carriers} carriers.",
        }
        for code, name, long_name, n_carriers in [
            ("CHN", "China",          "China",         "8"),
            ("DEU", "Germany",        "Germany",       "9"),
            ("FRA", "France",         "France",        "9"),
            ("GBR", "United_Kingdom", "United Kingdom","9"),
            ("IND", "India",          "India",         "8"),
            ("JPN", "Japan",          "Japan",         "8"),
            ("USA", "United_States",  "United States", "9"),
            ("WLD", "World",          "World",         "9"),
        ]
    ],

    # ── CoDaWork 2026 — Combined panel ──
    {
        "id":          "ember_combined_panel",
        "subdir":      "codawork2026",
        "source_csv":  None,  # built dynamically by build_combined_panel()
        "is_temporal": True,
        "ordering":    "by-label",
        "description": "EMBER all 8 countries × 26 years, panel ordered by country then year.",
        "build_fn":    "build_combined_panel",
    },

    # ── Domain — Geochemistry within-domain robustness battery ──
    {
        "id":          "geochem_ball_region",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "ball_oxides_by_region_barycenters.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Ball 2022 intraplate volcanics, 95 region barycenters, D=10 oxides.",
    },
    {
        "id":          "geochem_ball_age",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "ball_oxides_by_age_barycenters.csv"),
        "is_temporal": True,
        "ordering":    "by-time",
        "description": "Ball 2022, 10 IUGS chronostratigraphic epochs, D=10.",
    },
    {
        "id":          "geochem_ball_tas",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "ball_oxides_by_tas_barycenters.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Ball 2022, 15 TAS rock-type classes (silica-ordered, degenerate), D=10.",
    },
    {
        "id":          "geochem_stracke_oib",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "stracke_oib_by_location_barycenters.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Stracke 2022 OIB, 15 location barycenters, D=10.",
    },
    {
        "id":          "geochem_stracke_morb",
        "subdir":      "domain",
        "source_csv":  str(HERE / "domain/geochem_stracke_morb/geochem_stracke_morb_input.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Stracke 2022 MORB, 5 ocean-basin barycenters (Pacific/Indian/Atlantic/Arctic/Gakkel), D=10. Sister to geochem_stracke_oib.",
    },
    {
        "id":          "geochem_tappe_kim1",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "tappe_kim1_by_country_barycenters.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Tappe 2024 Group-1 kimberlite, 8 country/region barycenters, D=10.",
    },
    {
        "id":          "geochem_qin_cpx",
        "subdir":      "domain",
        "source_csv":  str(GEOCHEM_BINNING / "qin_cpx_by_location_barycenters.csv"),
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "Qin 2024 mantle xenolith clinopyroxene, top-30 location barycenters, D=9 (no K2O).",
    },

    # ── Domain — FAO Aquastat irrigation methods cross-section ──
    {
        "id":          "fao_irrigation_methods",
        "subdir":      "domain",
        "source_csv":  str(HERE / "domain/fao_irrigation_methods/fao_irrigation_input.csv"),
        "is_temporal": False,
        "ordering":    "by-d_A",
        "description": ("FAO Aquastat irrigation-method composition per country (latest year). "
                        "D=3 carriers: Surface, Sprinkler, Localized. T=83 countries+aggregates "
                        "with all three categories reported. Sum equals 'Area equipped for "
                        "full-control irrigation: total' (FAO_AS_4311) — natural compositional partition."),
    },

    # ── CoDaWork 2026 — BackBlaze fleet, daily 2024-2025 ──
    {
        "id":          "backblaze_fleet",
        "subdir":      "codawork2026",
        "source_csv":  str(HERE / "codawork2026/backblaze_fleet/backblaze_fleet_input.csv"),
        "is_temporal": True,
        "ordering":    "by-time",
        "description": ("BackBlaze fleet, daily SMART means 2024-2025 (T=731 days), "
                        "D=4 carriers (Mechanical, Thermal, Age, Errors) per Hs-17 preparser v1.0. "
                        "Built from 8 quarterly zips via adapters/backblaze_adapter.py; "
                        "input SHA-256 captured by cnt.py."),
    },

    # ── Reference — adapters needed; built dynamically ──
    {
        "id":          "commodities_gold_silver",
        "subdir":      "reference",
        "source_csv":  None,  # built by build_gold_silver()
        "is_temporal": True,
        "ordering":    "by-time",
        "description": "Gold/silver ratio 1688-2026 from MeasuringWorth; D=2 trajectory.",
        "build_fn":    "build_gold_silver",
    },
    {
        "id":          "nuclear_semf",
        "subdir":      "reference",
        "source_csv":  None,  # built by build_nuclear_semf()
        "is_temporal": False,
        "ordering":    "by-label",
        "description": "AME2020 SEMF binding-energy decomposition, D=5 (Vol, Surf, Coul, Asym, Pair) per nuclide.",
        "build_fn":    "build_nuclear_semf",
    },
]


# ──────────────────────────────────────────────────────────────────
# Adapter builders — convert raw data into ingestible CSV
# ──────────────────────────────────────────────────────────────────

def build_combined_panel(out_path: Path):
    """Concatenate all 8 EMBER country CSVs into one panel.

    Label = COUNTRY-YEAR. Carriers harmonised to the union of all 9
    EMBER carriers. Missing carriers (e.g. Other Renewables for D=8
    countries) are filled with the multiplicative zero-replacement
    floor (1e-15) so the row stays positive.
    """
    countries = ["CHN", "DEU", "FRA", "GBR", "IND", "JPN", "USA", "WLD"]
    full_carriers = [
        "Bioenergy", "Coal", "Gas", "Hydro", "Nuclear",
        "Other Fossil", "Other Renewables", "Solar", "Wind",
    ]
    rows = []
    for code in countries:
        cands = list(EMBER_DIR.glob(f"ember_{code}_*_generation_TWh.csv"))
        if not cands: continue
        with cands[0].open() as f:
            r = csv.reader(f)
            header = next(r)
            local_carriers = header[1:]
            for row in r:
                year = row[0]
                vals = []
                for c in full_carriers:
                    if c in local_carriers:
                        idx = local_carriers.index(c)
                        try:
                            v = float(row[1 + idx])
                            vals.append(v if v > 0 else 1e-15)
                        except (ValueError, IndexError):
                            vals.append(1e-15)
                    else:
                        vals.append(1e-15)
                rows.append([f"{code}-{year}"] + vals)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Country_Year"] + full_carriers)
        for r in rows:
            w.writerow([r[0]] + [f"{v:.6g}" for v in r[1:]])
    return out_path


def build_gold_silver(out_path: Path):
    """Build a D=2 simplex trajectory from the gold/silver normalized series.

    The MeasuringWorth gold/silver dataset gives a single ratio per year
    (silver-normalized price). We construct a D=2 composition (Gold, Silver)
    with Gold proportion = ratio/(ratio+1) (closure to simplex).

    Effectively: composition = [ratio/(ratio+1), 1/(ratio+1)] — the closed
    two-part composition encoding the gold/silver ratio.
    """
    src = ROOT / "DATA/Commodities/gold_silver_normalized.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with src.open() as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            try:
                date = row[0]
                ratio = float(row[1])
            except (ValueError, IndexError):
                continue
            if ratio <= 0: continue
            year = date[:4]
            gold = ratio / (ratio + 1.0)
            silver = 1.0 / (ratio + 1.0)
            rows.append([year, gold, silver])

    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Year", "Gold", "Silver"])
        for r in rows:
            w.writerow([r[0], f"{r[1]:.10f}", f"{r[2]:.10f}"])
    return out_path


def build_nuclear_semf(out_path: Path):
    """Build a D=5 SEMF binding-energy composition per nuclide.

    Reads Raymond's SEMF ratios CSV. Each row is one nuclide with the
    five SEMF terms: Volume, Surface, Coulomb, Asymmetry, Pairing.
    Pairing is signed (±) — we take its absolute value so all parts
    are positive (this is the canonical Hs-03 treatment).

    Only stable nuclides are kept (is_stable == True).
    """
    src = ROOT / "DATA/Nuclear/raymond_semf_ratios.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with src.open() as f:
        r = csv.DictReader(f)
        for d in r:
            try:
                Z   = int(d["Z"]); A = int(d["A"])
                vol  = float(d["B_vol"])
                surf = float(d["B_surf"])
                coul = float(d["B_coul"])
                asym = float(d["B_asym"])
                pair = abs(float(d["B_pair"]))
                stable = d.get("is_stable", "").strip().lower() == "true"
            except (ValueError, KeyError):
                continue
            if not stable: continue
            if min(vol, surf, coul, asym, pair) <= 0: continue
            label = f"Z{Z}_A{A}"
            rows.append([label, vol, surf, coul, asym, pair])

    # Sort by Z then A for a canonical "by-label" ordering
    rows.sort(key=lambda r: (int(r[0].split("_")[0][1:]), int(r[0].split("_")[1][1:])))

    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Nuclide", "Volume", "Surface", "Coulomb", "Asymmetry", "Pairing"])
        for r in rows:
            w.writerow([r[0]] + [f"{v:.6g}" for v in r[1:]])
    return out_path


BUILDERS = {
    "build_combined_panel": build_combined_panel,
    "build_gold_silver":    build_gold_silver,
    "build_nuclear_semf":   build_nuclear_semf,
}


# ──────────────────────────────────────────────────────────────────
# Runner — executes one experiment, writes JSON + JOURNAL.md
# ──────────────────────────────────────────────────────────────────

def run_one(spec: dict, force: bool = False) -> dict:
    out_dir = HERE / spec["subdir"] / spec["id"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve input CSV (build if needed)
    if spec.get("build_fn"):
        csv_path = out_dir / f"{spec['id']}_input.csv"
        if not csv_path.exists() or force:
            print(f"  building input via {spec['build_fn']}...")
            BUILDERS[spec["build_fn"]](csv_path)
    else:
        csv_path = Path(spec["source_csv"])
        if not csv_path.exists():
            return {"id": spec["id"], "status": "missing_input", "csv_path": str(csv_path)}

    # Run cnt.py
    json_path = out_dir / f"{spec['id']}_cnt.json"
    if json_path.exists() and not force:
        print(f"  {spec['id']}: cached, skipping (use --force to rerun)")
    else:
        cmd = ["python3", str(CNT), str(csv_path), "-o", str(json_path),
               "--ordering-method", spec["ordering"]]
        if spec["is_temporal"]:
            cmd.append("--temporal")
        t0 = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        wall_s = time.time() - t0
        if result.returncode != 0:
            (out_dir / "stderr.log").write_text(result.stderr)
            return {"id": spec["id"], "status": "failed",
                    "wall_s": wall_s, "stderr_excerpt": result.stderr[:300]}
        print(f"  {spec['id']}: ran in {wall_s:.2f}s")

    # Generate JOURNAL.md from the JSON
    j = json.load(json_path.open())
    journal_path = out_dir / "JOURNAL.md"
    journal_path.write_text(generate_journal(spec, j))

    return {
        "id":               spec["id"],
        "subdir":           spec["subdir"],
        "status":           "ok",
        "csv_path":         str(csv_path),
        "json_path":        str(json_path),
        "n_records":        j["input"]["n_records"],
        "n_carriers":       j["input"]["n_carriers"],
        "curvature_depth":  j["depth"]["higgins_extensions"]["summary"]["curvature_depth"],
        "energy_depth":     j["depth"]["higgins_extensions"]["summary"]["energy_depth"],
        "ir_class":         j["depth"]["higgins_extensions"]["impulse_response"].get("classification", "n/a"),
        "amplitude_A":      j["depth"]["higgins_extensions"]["curvature_attractor"].get("amplitude"),
        "lock_events":      len(j["diagnostics"]["higgins_extensions"]["lock_events"]),
        "M2_residual":      j["depth"]["higgins_extensions"]["involution_proof"]["mean_residual"],
        "content_sha256":   j["diagnostics"]["content_sha256"],
        "wall_clock_ms":    j["metadata"]["wall_clock_ms"],
    }


# ──────────────────────────────────────────────────────────────────
# Journal generator — pretty-prints the JSON's key findings as Markdown
# ──────────────────────────────────────────────────────────────────

def generate_journal(spec: dict, j: dict) -> str:
    md = j["metadata"]; inp = j["input"]
    dpt = j["depth"]["higgins_extensions"]["summary"]
    cur = j["depth"]["higgins_extensions"]["curvature_attractor"]
    ir  = j["depth"]["higgins_extensions"]["impulse_response"]
    inv = j["depth"]["higgins_extensions"]["involution_proof"]
    eitt = j["diagnostics"]["higgins_extensions"]["eitt_residuals"]
    locks = j["diagnostics"]["higgins_extensions"]["lock_events"]
    flags = j["diagnostics"]["higgins_extensions"]["degeneracy_flags"]
    s2_cps = j["stages"]["stage2"]["higgins_extensions"]["carrier_pair_examination"]

    lines = [
        f"# Experiment Journal — `{spec['id']}`",
        "",
        f"**Subdir:** `{spec['subdir']}`  ",
        f"**Description:** {spec['description']}  ",
        f"**Generated:** {md['generated']}  ",
        f"**Engine:** {md['engine_version']}, schema {md['schema_version']}  ",
        f"**Run time:** {md['wall_clock_ms']} ms  ",
        f"**content_sha256:** `{j['diagnostics']['content_sha256']}`  ",
        "",
        "## Input",
        "",
        f"- Source: `{inp['source_file']}`",
        f"- Source SHA-256: `{inp['source_file_sha256']}`",
        f"- Closed-data SHA-256: `{inp['closed_data_sha256']}`",
        f"- Records (T): **{inp['n_records']}**",
        f"- Carriers (D): **{inp['n_carriers']}**",
        f"- Carriers: {', '.join(inp['carriers'])}",
        f"- Ordering: temporal={inp['ordering']['is_temporal']}, "
        f"method={inp['ordering']['ordering_method']}",
    ]
    if inp['ordering'].get('caveat'):
        lines.append(f"- Ordering caveat: {inp['ordering']['caveat']}")
    if inp['zero_replacement']['applied']:
        lines.append(f"- Zero replacement applied: {inp['zero_replacement']['n_replacements']} values "
                     f"floored at {inp['zero_replacement']['delta']:.0e}")

    lines += [
        "",
        "## Headline Results",
        "",
        f"| Quantity | Value |",
        f"|---|---|",
        f"| Curvature tower depth | **{dpt['curvature_depth']}** |",
        f"| Curvature termination | {dpt['curvature_termination']} |",
        f"| Energy tower depth    | {dpt['energy_depth']} |",
        f"| Energy termination    | {dpt['energy_termination']} |",
        f"| M² = I residual       | {inv['mean_residual']:.2e} (verified: {inv['verified']}) |",
        f"| Mean duality distance | {dpt['mean_duality_distance']:.4f} HLR |",
    ]
    if cur.get("amplitude") is not None:
        lines += [
            f"| Period                | {cur.get('period', '?')} |",
            f"| Attractor c_even      | {cur.get('c_even', float('nan')):.4f} |",
            f"| Attractor c_odd       | {cur.get('c_odd', float('nan')):.4f} |",
            f"| Amplitude A           | **{cur.get('amplitude'):.4f}** |",
            f"| Contraction λ         | **{cur.get('contraction_lyapunov', float('nan')):.4f}** |",
            f"| Mean contraction ratio| {cur.get('mean_contraction_ratio', float('nan')):.4f} |",
            f"| Banach satisfied      | {cur.get('banach_satisfied', '?')} |",
            f"| IR classification     | **{ir.get('classification', '?')}** |",
            f"| Damping ζ             | {ir.get('damping_zeta', float('nan')):.4f} |",
        ]

    # EITT residuals
    if eitt["M_sweep"]:
        lines += ["", "## EITT Residuals (Egozcue: empirical observation, not Aitchison theorem)", "",
                  "| M | n_blocks | variation_pct | gate (5%) |", "|---|---|---|---|"]
        for r in eitt["M_sweep"]:
            tag = "PASS" if r.get("pass_gate", r.get("pass_5pct", False)) else "FAIL"
            lines.append(f"| {r['M']} | {r['n_blocks']} | {r['variation_pct']:.3f}% | {tag} |")

    # Lock events
    if locks:
        lines += ["", "## Lock Events", ""]
        for e in locks[:20]:
            carrier = e.get("carrier") or "(spread)"
            lines.append(f"- `{e['event_type']}` at t={e['timestep_index']} ({e['label']}): {carrier} — {e['context']}")
        if len(locks) > 20:
            lines.append(f"- ... + {len(locks) - 20} more")

    # Degeneracy flags
    if flags:
        lines += ["", "## Degeneracy Flags", ""]
        for f in flags:
            lines.append(f"- **{f['flag']}** ({f['severity']}): {f['message']} — `{f['condition']}`")

    # Top carrier-pair findings
    if s2_cps:
        # Top by lock and by opposition
        locked = [p for p in s2_cps if p.get("locked")]
        if locked:
            lines += ["", "## Locked Carrier Pairs (bearing spread < 10°)", ""]
            for p in sorted(locked, key=lambda x: x["bearing_spread_deg"])[:10]:
                lines.append(f"- {p['carrier_a']}–{p['carrier_b']}: spread = {p['bearing_spread_deg']:.2f}°, r = {p['pearson_r']:.3f}")
        opposed = sorted(s2_cps, key=lambda p: -p.get("opposition_score", 0))[:5]
        if opposed[0].get("opposition_score", 0) > 0.3:
            lines += ["", "## Most Opposed Carrier Pairs", ""]
            for p in opposed:
                lines.append(f"- {p['carrier_a']}–{p['carrier_b']}: r = {p['pearson_r']:.3f}, spread = {p['bearing_spread_deg']:.1f}°")

    # Helmsman lineage in curvature tower
    ct = j["depth"]["higgins_extensions"]["curvature_tower"]
    if ct:
        lines += ["", "## Curvature Tower Helmsman Lineage", ""]
        lines.append("| Level | Helmsman | Status |")
        lines.append("|---|---|---|")
        for lvl in ct:
            h = lvl.get("helmsman", "")
            if h.startswith("K_"): h = h[2:]
            lines.append(f"| L{lvl['level']} | {h} | {lvl.get('status', '')} |")

    lines += [
        "",
        "---",
        "",
        "*Generated by `run_experiments.py` from the canonical CNT JSON.",
        "Re-run with --force to refresh.*",
        "",
        f"*The instrument reads. The expert decides. The loop stays open.*",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    filter_str = args[0] if args else None

    selected = REGISTRY
    if filter_str:
        if "/" in filter_str:
            sub, eid = filter_str.split("/", 1)
            selected = [s for s in REGISTRY if s["subdir"] == sub and s["id"] == eid]
        else:
            selected = [s for s in REGISTRY if s["subdir"] == filter_str or s["id"] == filter_str]

    if not selected:
        print(f"No experiments matched '{filter_str}'")
        return 1

    print(f"Running {len(selected)} experiment(s)...")
    print("=" * 70)
    summaries = []
    for spec in selected:
        print(f"\n[{spec['subdir']}/{spec['id']}]")
        s = run_one(spec, force=force)
        summaries.append(s)
        if s["status"] != "ok":
            print(f"  ✗ {s['status']}: {s.get('stderr_excerpt', '')[:120]}")
        else:
            print(f"  ✓ T={s['n_records']}, D={s['n_carriers']}, "
                  f"curv_depth={s['curvature_depth']}, IR={s['ir_class']}")

    # Update INDEX.json
    index_path = HERE / "INDEX.json"
    if index_path.exists():
        index = json.load(index_path.open())
    else:
        index = {
            "_meta": {
                "type":   "CNT_V2_EXPERIMENT_INDEX",
                "schema": "1.0",
                "engine": "cnt 2.0.1",
            },
            "experiments": {},
        }
    for s in summaries:
        index["experiments"][s["id"]] = s
    index["_meta"]["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    index["_meta"]["n_experiments"] = len(index["experiments"])
    json.dump(index, index_path.open("w"), indent=2)

    n_ok   = sum(1 for s in summaries if s["status"] == "ok")
    n_fail = sum(1 for s in summaries if s["status"] != "ok")
    print()
    print("=" * 70)
    print(f"Done. {n_ok} ok, {n_fail} failed/missing.")
    print(f"Index: {index_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
