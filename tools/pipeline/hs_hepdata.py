#!/usr/bin/env python3
"""
Hˢ HEPData Fetch — Compositional Data from High-Energy Physics
================================================================
Pulls published experimental data from HEPData (hepdata.net) and
converts it into CSV files ready for hs_ingest.py.

HEPData is the international repository for publication-related
High-Energy Physics data. Many HEP measurements are inherently
compositional — branching ratios, cross-section decompositions,
energy budget partitions, decay channel fractions.

Output Structure:
  Each run creates a numbered subfolder inside a test directory:

  hs_analyses/                    # default test folder (or --testdir <name>)
  ├── catalog.json                # master index of all runs
  ├── 001_w_decay/
  │   ├── dataset.csv             # compositional data (N×D)
  │   ├── diagnostics.json        # pipeline diagnostic codes + structural modes
  │   ├── results.json            # full pipeline output
  │   ├── metadata.json           # source, reference, fetch info
  │   └── report_en.txt           # human-readable report (+ other languages)
  ├── 002_higgs_br/
  │   └── ...
  └── ...

Usage:
  # List curated compositional datasets
  python hs_hepdata.py --list

  # Fetch and run (output to hs_analyses/ in current directory)
  python hs_hepdata.py --fetch w_decay --run

  # Fetch all into a named test folder
  python hs_hepdata.py --fetch-all --run --testdir my_experiment

  # Probe a HEPData record to see its table structure
  python hs_hepdata.py --probe 1249595

  # Fetch any HEPData record by INSPIRE ID + table
  python hs_hepdata.py --inspire 1249595 --table "Table 1" --run

Author: Peter Higgins / Claude
Version: 1.1
For: CoDaWork 2026 — real-world validation from published experiments
"""

import sys
import os
import json
import csv
import argparse
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library required. Install with: pip install requests")
    sys.exit(1)

# Pipeline imports (if available — not required for fetch-only mode)
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PIPELINE_DIR)


# ═══════════════════════════════════════════════════════════════════
# CURATED COMPOSITIONAL HEP DATASETS
# ═══════════════════════════════════════════════════════════════════

CURATED_DATASETS = {

    "w_decay": {
        "name": "W Boson Decay Branching Fractions",
        "domain": "PARTICLE_PHYSICS",
        "description": "W± decay channel fractions measured by LEP experiments. "
                       "Three leptonic channels (eν, μν, τν) plus hadronic. "
                       "A 4-carrier composition that must close to 1.",
        "inspire_id": 635851,
        "table": "Table 8",
        "collaboration": "DELPHI",
        "strategy": "w_boson_manual",
        "carriers": ["W_to_enu", "W_to_munu", "W_to_taunu", "W_to_hadrons"],
        "pdg_values": [0.1071, 0.1063, 0.1138, 0.6741],
        "reference": "Phys.Lett. B609 (2005) 35-48",
        "notes": "PDG 2024 world averages used as baseline."
    },

    "higgs_br": {
        "name": "Higgs Boson Branching Ratios (125 GeV)",
        "domain": "PARTICLE_PHYSICS",
        "description": "SM Higgs boson (mH=125 GeV) decay branching fractions. "
                       "Major channels: bb, WW*, gg, ττ, cc, ZZ*, γγ, Zγ, μμ. "
                       "A ~9-carrier composition dominated by bb (~58%).",
        "inspire_id": None,
        "strategy": "higgs_manual",
        "carriers": ["H_bb", "H_WW", "H_gg", "H_tautau", "H_cc",
                      "H_ZZ", "H_gamgam", "H_Zgam", "H_mumu"],
        "sm_predictions": [0.5809, 0.2152, 0.0856, 0.0630, 0.0289,
                            0.0264, 0.00228, 0.00154, 0.000219],
        "reference": "CERN Yellow Report CERN-2017-002-M (LHC HXSWG)",
        "notes": "SM predictions at mH=125.09 GeV."
    },

    "top_decay": {
        "name": "Top Quark Decay W Helicity Fractions",
        "domain": "PARTICLE_PHYSICS",
        "description": "W boson helicity fractions in top quark decay: "
                       "longitudinal (F0), left-handed (FL), right-handed (FR). "
                       "A perfect 3-carrier simplex (F0+FL+FR=1).",
        "inspire_id": 1249595,
        "table": "Table 3",
        "collaboration": "CMS",
        "strategy": "helicity_fractions",
        "carriers": ["F_longitudinal", "F_left", "F_right"],
        "sm_predictions": [0.687, 0.311, 0.0017],
        "reference": "JHEP 10 (2013) 167",
        "notes": "SM NNLO: F0=0.687, FL=0.311, FR=0.0017. "
                 "FR≈0 makes this a near-degenerate simplex."
    },

    "tau_decay": {
        "name": "Tau Lepton Decay Branching Fractions",
        "domain": "PARTICLE_PHYSICS",
        "description": "τ lepton decay modes: leptonic (eνν, μνν) plus "
                       "hadronic (1-prong, 3-prong, 5-prong). "
                       "5-carrier composition with hierarchy.",
        "inspire_id": None,
        "strategy": "tau_manual",
        "carriers": ["tau_to_enu", "tau_to_munu", "tau_to_1prong",
                      "tau_to_3prong", "tau_to_5prong"],
        "pdg_values": [0.1782, 0.1739, 0.4976, 0.1434, 0.0010],
        "reference": "PDG Review of Particle Physics 2024",
        "notes": "5-prong is ~0.1%, creating a near-zero carrier."
    },

    "z_decay": {
        "name": "Z Boson Partial Decay Widths",
        "domain": "PARTICLE_PHYSICS",
        "description": "Z⁰ boson decay fractions into fermion pairs. "
                       "Leptonic (ee, μμ, ττ, invisible/νν) plus hadronic. "
                       "5-carrier composition measured precisely at LEP.",
        "inspire_id": None,
        "strategy": "z_manual",
        "carriers": ["Z_to_ee", "Z_to_mumu", "Z_to_tautau",
                      "Z_to_invisible", "Z_to_hadrons"],
        "lep_values": [0.03363, 0.03366, 0.03370, 0.2000, 0.69911],
        "reference": "Phys.Rept. 427 (2006) 257-454 (LEP EWWG)",
        "notes": "Invisible width constrains neutrino generations (Nν=2.984±0.008)."
    },

    "b_meson_ckmfit": {
        "name": "CKM Matrix Elements |Vub|/|Vcb| Decomposition",
        "domain": "PARTICLE_PHYSICS",
        "description": "Unitarity triangle: CKM matrix row/column sums = 1. "
                       "First row: |Vud|² + |Vus|² + |Vub|² = 1. "
                       "A 3-carrier exact composition from quark mixing.",
        "inspire_id": None,
        "strategy": "ckm_manual",
        "carriers": ["Vud_sq", "Vus_sq", "Vub_sq"],
        "pdg_values": [0.97373**2, 0.2243**2, 0.00382**2],
        "reference": "PDG Review of Particle Physics 2024",
        "notes": "CKM unitarity is exact in SM. |Vub|² ≈ 1.5×10⁻⁵ — extreme carrier hierarchy."
    },

    "cosmic_energy": {
        "name": "Cosmic Energy Budget (Planck 2018)",
        "domain": "COSMOLOGY",
        "description": "Energy density fractions of the universe: "
                       "dark energy (ΩΛ), dark matter (Ωc), baryonic matter (Ωb), "
                       "radiation (Ωr). Must close to 1 (flat universe).",
        "inspire_id": None,
        "strategy": "cosmic_manual",
        "carriers": ["Dark_Energy", "Dark_Matter", "Baryonic_Matter", "Radiation"],
        "planck_values": [0.6847, 0.2589, 0.0486, 0.00009],
        "reference": "Planck 2018 results. VI. A&A 641, A6 (2020)",
        "notes": "Cross-validation against existing Hs-09."
    },

    "proton_momentum": {
        "name": "Proton Momentum Fractions (Parton Distribution)",
        "domain": "NUCLEAR_PHYSICS",
        "description": "Momentum fractions carried by parton species inside "
                       "the proton at Q²=10 GeV²: u-valence, d-valence, sea quarks, gluons. "
                       "Must sum to 1 (momentum sum rule).",
        "inspire_id": None,
        "strategy": "proton_manual",
        "carriers": ["u_valence", "d_valence", "sea_quarks", "gluons"],
        "nnpdf_values": [0.255, 0.115, 0.175, 0.455],
        "reference": "NNPDF4.0, Eur.Phys.J.C 82 (2022) 428",
        "notes": "Gluons carry ~45% of proton momentum."
    },
}


# ═══════════════════════════════════════════════════════════════════
# CATALOG & FOLDER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

def get_test_dir(testdir_name=None):
    """Get or create the test directory for storing analysis runs."""
    if testdir_name:
        base = os.path.join(os.getcwd(), testdir_name)
    else:
        base = os.path.join(os.getcwd(), "hs_analyses")
    os.makedirs(base, exist_ok=True)
    return base


def load_catalog(test_dir):
    """Load the master catalog, or create empty one."""
    cat_path = os.path.join(test_dir, "catalog.json")
    if os.path.exists(cat_path):
        with open(cat_path, encoding='utf-8') as f:
            return json.load(f)
    return {
        "title": "Hˢ Analysis Catalog",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool_version": "1.1",
        "runs": []
    }


def save_catalog(test_dir, catalog):
    """Save the master catalog."""
    cat_path = os.path.join(test_dir, "catalog.json")
    with open(cat_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)


def next_run_number(catalog):
    """Get the next sequential run number."""
    if not catalog["runs"]:
        return 1
    return max(r["run_number"] for r in catalog["runs"]) + 1


def create_run_folder(test_dir, catalog, run_key, run_name):
    """Create a numbered subfolder for this analysis run."""
    run_num = next_run_number(catalog)
    folder_name = f"{run_num:03d}_{run_key}"
    run_dir = os.path.join(test_dir, folder_name)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir, run_num, folder_name


# ═══════════════════════════════════════════════════════════════════
# HEPDATA API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

HEPDATA_BASE = "https://www.hepdata.net"


def fetch_record_info(inspire_id):
    """Fetch record metadata from HEPData by INSPIRE ID."""
    url = f"{HEPDATA_BASE}/record/ins{inspire_id}?format=json"
    print(f"  Fetching record ins{inspire_id}...")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_table(inspire_id, table_name, version=None):
    """Fetch a specific data table from HEPData."""
    params = {"format": "json", "table": table_name}
    if version:
        params["version"] = version
    url = f"{HEPDATA_BASE}/record/ins{inspire_id}"
    print(f"  Fetching table '{table_name}' from ins{inspire_id}...")
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_hepdata(query, collaboration=None, size=10):
    """Search HEPData for records matching a query."""
    params = {"q": query, "format": "json", "size": size}
    if collaboration:
        params["collaboration"] = collaboration
    url = f"{HEPDATA_BASE}/search/"
    print(f"  Searching HEPData: '{query}'...")
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ═══════════════════════════════════════════════════════════════════
# PROBE — INSPECT HEPDATA RECORD STRUCTURE
# ═══════════════════════════════════════════════════════════════════

def probe_record(inspire_id, dump_raw=False):
    """Show all tables and their structure for a HEPData record.
    When dump_raw=True, saves full JSON to probe_ins{id}_raw.json."""

    print(f"\n{'=' * 60}")
    print(f"  Hˢ HEPData Probe: ins{inspire_id}")
    print(f"{'=' * 60}")

    # Fetch full record (not light — we need data)
    url = f"{HEPDATA_BASE}/record/ins{inspire_id}?format=json"
    print(f"  Fetching full record...")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        record = resp.json()
    except Exception as e:
        print(f"  ERROR fetching record: {e}")
        return

    # Dump raw JSON for debugging
    if dump_raw:
        raw_path = os.path.join(os.getcwd(), f"probe_ins{inspire_id}_raw.json")
        with open(raw_path, 'w') as f:
            json.dump(record, f, indent=2)
        print(f"  Raw JSON saved: {raw_path}")

    # Show top-level structure
    title = record.get("title", record.get("record", {}).get("title", "Unknown"))
    doi = record.get("doi", record.get("record", {}).get("doi", "N/A"))
    print(f"  Title: {title}")
    print(f"  DOI:   {doi}")
    print(f"  Top-level keys: {list(record.keys())}")

    # Find tables — HEPData uses different key names across versions
    tables = []
    for key in ["data_tables", "tables", "data"]:
        if key in record and isinstance(record[key], list):
            tables = record[key]
            print(f"  Table list key: '{key}' ({len(tables)} entries)")
            break

    if not tables:
        # The record itself might be a single table
        if "dependent_variables" in record or "independent_variables" in record:
            tables = [record]
            print(f"  Record IS the table data (single table)")
        else:
            print(f"  No table list found in standard keys.")
            print(f"  Attempting per-table fetch for Table 1-5...")
            for i in range(1, 6):
                tname = f"Table {i}"
                try:
                    tbl = fetch_table(inspire_id, tname)
                    tables.append({"name": tname, "_fetched": tbl})
                    print(f"    Found: {tname}")
                except:
                    break
            if not tables:
                print(f"  No tables found. Try --probe {inspire_id} --dump to save raw JSON.")
                return

    print(f"  Tables: {len(tables)}")
    print()

    # Probe each table
    for i, tbl in enumerate(tables):
        tbl_name = tbl.get("name", tbl.get("title", f"Table {i+1}"))
        print(f"  ── {tbl_name} ──")

        desc = tbl.get("description", tbl.get("title", "N/A"))
        if isinstance(desc, str):
            print(f"    Description: {desc[:140]}")

        # Get table data — might be inline or need fetching
        table_data = tbl.get("_fetched", tbl)

        # Try standard keys first
        dep_vars = table_data.get("dependent_variables", [])
        indep_vars = table_data.get("independent_variables", [])

        # If empty, try nested structures
        if not dep_vars and not indep_vars:
            for nested_key in ["data", "values", "content"]:
                if nested_key in table_data:
                    nested = table_data[nested_key]
                    if isinstance(nested, dict):
                        dep_vars = nested.get("dependent_variables", [])
                        indep_vars = nested.get("independent_variables", [])
                    if dep_vars or indep_vars:
                        print(f"    Data found under '{nested_key}' key")
                        break

        # If still empty, show what keys ARE present
        if not dep_vars and not indep_vars:
            data_keys = [k for k in table_data.keys()
                         if k not in ("name", "title", "description", "_fetched",
                                      "keywords", "doi", "location", "review")]
            print(f"    ⚠ No standard dep/indep variables found")
            print(f"    Available keys: {data_keys}")
            # Show a sample of the raw structure
            for dk in data_keys[:3]:
                val = table_data[dk]
                if isinstance(val, list):
                    print(f"    [{dk}]: list of {len(val)} items")
                    if val and isinstance(val[0], dict):
                        print(f"      First item keys: {list(val[0].keys())}")
                        sample = json.dumps(val[0], indent=2)[:200]
                        print(f"      Sample: {sample}")
                elif isinstance(val, dict):
                    print(f"    [{dk}]: dict with keys {list(val.keys())[:8]}")
                else:
                    print(f"    [{dk}]: {str(val)[:100]}")
        else:
            # Show standard structure
            print(f"    Independent vars: {len(indep_vars)}")
            for iv in indep_vars:
                hdr = iv.get("header", {}).get("name", "?")
                n_vals = len(iv.get("values", []))
                sample = iv["values"][:3] if iv.get("values") else []
                sample_str = [str(v.get("value", "?")) for v in sample]
                print(f"      [{hdr}] {n_vals} values, e.g.: {', '.join(sample_str)}")

            print(f"    Dependent vars: {len(dep_vars)}")
            for dv in dep_vars:
                hdr = dv.get("header", {}).get("name", "?")
                n_vals = len(dv.get("values", []))
                sample = dv["values"][:3] if dv.get("values") else []
                sample_str = []
                for v in sample:
                    val = v.get("value", "?")
                    errs = v.get("errors", [])
                    err_str = ""
                    if errs:
                        err_str = f" ±{errs[0].get('symerror', errs[0].get('asymerror', {}).get('plus', '?'))}"
                    sample_str.append(f"{val}{err_str}")
                print(f"      [{hdr}] {n_vals} values, e.g.: {', '.join(sample_str)}")

            if len(dep_vars) >= 2:
                print(f"    → COMPOSITIONAL CANDIDATE (multi-column)")
            elif len(dep_vars) == 1 and indep_vars:
                print(f"    → COMPOSITIONAL CANDIDATE (category-value)")

        print()

    print(f"  Usage:")
    print(f"    python hs_hepdata.py --inspire {inspire_id} --table \"<table_name>\" --run")
    if not dump_raw:
        print(f"    python hs_hepdata.py --probe {inspire_id} --dump  # save raw JSON for inspection")
    print()


# ═══════════════════════════════════════════════════════════════════
# DATA EXTRACTION STRATEGIES
# ═══════════════════════════════════════════════════════════════════

def extract_compositions_from_table(table_json, carriers=None):
    """Extract compositional data from a HEPData JSON table."""
    dep_vars = table_json.get("dependent_variables", [])
    indep_vars = table_json.get("independent_variables", [])

    # Strategy 0: Check for nested data structure
    if not dep_vars:
        for nested_key in ["data", "values", "content"]:
            if nested_key in table_json:
                inner = table_json[nested_key]
                if isinstance(inner, dict):
                    dep_vars = inner.get("dependent_variables", [])
                    indep_vars = inner.get("independent_variables", [])
                elif isinstance(inner, list) and inner and isinstance(inner[0], dict):
                    keys = [k for k in inner[0].keys()
                            if k not in ("x", "label", "name", "bin")]
                    if len(keys) >= 2:
                        return [[float(row.get(k, 0)) for k in keys] for row in inner], keys
                if dep_vars:
                    break

    if not dep_vars:
        raise ValueError("No dependent variables found in table. "
                         "Use --probe <id> --dump to inspect the raw JSON.")

    # Strategy 1: Each dependent variable is a carrier (multi-column)
    if len(dep_vars) >= 2:
        carrier_names = [dv["header"]["name"] for dv in dep_vars]
        n_rows = len(dep_vars[0]["values"])
        data = []
        for i in range(n_rows):
            row = []
            for dv in dep_vars:
                val = dv["values"][i].get("value", 0)
                if val is None or val == "-":
                    val = 0
                row.append(float(val))
            data.append(row)
        return data, carrier_names

    # Strategy 2: Single dependent variable with independent categories
    elif len(dep_vars) == 1 and indep_vars:
        dv = dep_vars[0]
        iv = indep_vars[0]
        carrier_names = []
        values = []
        for i, iv_val in enumerate(iv["values"]):
            label = str(iv_val.get("value", f"C{i+1}"))
            carrier_names.append(label.replace(" ", "_"))
            val = dv["values"][i].get("value", 0)
            if val is None:
                val = 0
            values.append(float(val))
        return [values], carrier_names

    else:
        raise ValueError("Cannot determine compositional structure. "
                         "Use --probe <id> --dump to inspect the raw JSON.")


def build_manual_dataset(config):
    """Build a dataset from curated manual values with systematic perturbations."""
    import random
    random.seed(42)

    carriers = config["carriers"]
    D = len(carriers)

    central = None
    for key in ["pdg_values", "sm_predictions", "lep_values",
                "planck_values", "nnpdf_values"]:
        if key in config:
            central = config[key]
            break

    if central is None:
        raise ValueError(f"No central values found for {config['name']}")

    total = sum(central)
    central = [v / total for v in central]

    data = [central[:]]

    for i in range(D):
        row_up = central[:]
        row_up[i] *= 1.01
        t = sum(row_up)
        data.append([v / t for v in row_up])

    for i in range(D):
        row_dn = central[:]
        row_dn[i] *= 0.99
        t = sum(row_dn)
        data.append([v / t for v in row_dn])

    for i in range(D):
        for j in range(i + 1, D):
            row = central[:]
            row[i] *= 1.005
            row[j] *= 0.995
            t = sum(row)
            data.append([v / t for v in row])

    # Dirichlet perturbation — floor alpha at 1.0 to prevent
    # extreme-hierarchy carriers (e.g. |Vub|²≈10⁻⁵) from producing
    # values near machine epsilon that blow up Guard 4
    alpha = [max(v * 1000, 1.0) for v in central]
    for _ in range(5):
        raw = [random.gammavariate(a, 1.0) for a in alpha]
        t = sum(raw)
        # Re-weight to preserve the original carrier hierarchy
        row = [(r / t) * c for r, c in zip(raw, central)]
        row_t = sum(row)
        data.append([v / row_t for v in row])

    return data, carriers


# ═══════════════════════════════════════════════════════════════════
# FILE OUTPUT — CATALOGED FOLDER STRUCTURE
# ═══════════════════════════════════════════════════════════════════

def save_as_csv(data, carriers, filepath):
    """Save compositional data as CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(carriers)
        for row in data:
            writer.writerow([f"{v:.8f}" for v in row])
    return filepath


def save_diagnostics(codes, structural_modes, run_dir):
    """Save diagnostic codes and structural modes to diagnostics.json."""
    diag = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_codes": len(codes),
        "structural_mode_count": len(structural_modes),
        "warnings": [c for c in codes if c["code"].endswith("-WRN")],
        "discoveries": [c for c in codes if c["code"].endswith("-DIS")],
        "structural_modes": structural_modes,
        "all_codes": codes
    }
    path = os.path.join(run_dir, "diagnostics.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(diag, f, indent=2, default=str)
    return path


def save_run_metadata(config, run_dir, n_rows, n_carriers, run_num,
                       classification=None, hvld_shape=None, hvld_r2=None,
                       nearest_constant=None, eitt_pass=None):
    """Save comprehensive metadata for this analysis run."""
    meta = {
        "run_number": run_num,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "HEPData / Published HEP measurements",
        "name": config.get("name", "Unknown"),
        "domain": config.get("domain", "UNKNOWN"),
        "description": config.get("description", ""),
        "reference": config.get("reference", ""),
        "collaboration": config.get("collaboration", ""),
        "inspire_id": config.get("inspire_id"),
        "notes": config.get("notes", ""),
        "data": {
            "N": n_rows,
            "D": n_carriers,
            "carriers": config.get("carriers", [])
        },
        "results_summary": {
            "classification": classification,
            "hvld_shape": hvld_shape,
            "hvld_r2": hvld_r2,
            "nearest_constant": nearest_constant,
            "eitt_pass": eitt_pass
        },
        "files": {
            "dataset": "dataset.csv",
            "results": "results.json",
            "diagnostics": "diagnostics.json",
            "metadata": "metadata.json"
        }
    }
    path = os.path.join(run_dir, "metadata.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)
    return meta


# ═══════════════════════════════════════════════════════════════════
# MAIN FETCH + ANALYZE PIPELINE
# ═══════════════════════════════════════════════════════════════════

def fetch_and_analyze(key, test_dir, run_pipeline=True):
    """Fetch a curated dataset, save to cataloged folder, optionally run pipeline."""
    if key not in CURATED_DATASETS:
        print(f"ERROR: Unknown dataset key '{key}'.")
        print(f"Available: {', '.join(CURATED_DATASETS.keys())}")
        return None

    config = CURATED_DATASETS[key]

    # Load catalog and create run folder
    catalog = load_catalog(test_dir)
    run_dir, run_num, folder_name = create_run_folder(test_dir, catalog, key, config["name"])

    print(f"\n{'=' * 60}")
    print(f"  Hˢ HEPData: {config['name']}")
    print(f"  Run #{run_num:03d} → {folder_name}/")
    print(f"{'=' * 60}")
    print(f"  Domain:  {config['domain']}")
    print(f"  Source:  {config.get('reference', 'N/A')}")

    # Try HEPData API first, fall back to manual values
    data = None
    carriers = None
    data_source = "curated"

    if config.get("inspire_id") and config.get("table"):
        try:
            table_json = fetch_table(config["inspire_id"], config["table"])
            data, carriers = extract_compositions_from_table(
                table_json, config.get("carriers"))
            data_source = "hepdata_api"
            print(f"  Fetched: {len(data)} observations, {len(carriers)} carriers (HEPData API)")
        except Exception as e:
            print(f"  HEPData API: {e}")
            print(f"  Using curated values...")

    if data is None:
        data, carriers = build_manual_dataset(config)
        print(f"  Built: {len(data)} observations, {len(carriers)} carriers (curated values)")

    N, D = len(data), len(carriers)
    if D < 2:
        print(f"  ERROR: D={D} — need ≥ 2 carriers.")
        return None

    # Save dataset
    csv_path = os.path.join(run_dir, "dataset.csv")
    save_as_csv(data, carriers, csv_path)
    print(f"  Dataset: {csv_path}")

    # Run pipeline if requested
    classification = None
    hvld_shape = None
    hvld_r2 = None
    nearest_constant = None
    eitt_pass = None
    codes = []
    sm_codes = []

    if run_pipeline:
        try:
            from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder
            from hs_codes import generate_codes
            from hs_reporter import report, report_all_languages
            import numpy as np

            print(f"\n  Running 12-Step Pipeline + Extended Panel...")

            hd = HigginsDecomposition(
                experiment_id=f"HEP-{run_num:03d}",
                name=config["name"],
                domain=config["domain"],
                carriers=carriers,
                data_source_type=f"HEPDATA ({data_source})",
                data_source_description=config.get("reference", "")
            )
            hd.load_data(np.array(data))
            result = hd.run_full_extended()

            # Extract key results
            hvld_shape = result['steps'].get('step6_pll_shape', '?')
            hvld_r2 = result['steps'].get('step6_pll_R2', 0)
            sq = result['steps'].get('step7_squeeze_closest')
            if sq:
                nearest_constant = f"{sq.get('constant', '?')} (δ={sq.get('delta', 0):.6f})"
            eitt = result['steps'].get('step8_eitt_invariance', {})
            eitt_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False

            print(f"  HVLD: {hvld_shape} (R²={hvld_r2:.4f})")
            if nearest_constant:
                print(f"  Nearest constant: {nearest_constant}")
            print(f"  EITT: {'PASS' if eitt_pass else 'FAIL'}")

            # Generate codes
            codes = generate_codes(result)
            sm_codes = [c for c in codes if c['code'].startswith('SM-')]

            classification = 'NATURAL' if any(c['code'] == 'S8-NAT-INF' for c in codes) \
                else 'INVESTIGATE' if any(c['code'] == 'S8-INV-WRN' for c in codes) \
                else 'FLAG'

            print(f"  Classification: {classification}")
            print(f"  Codes: {len(codes)} ({len(sm_codes)} structural modes)")

            if sm_codes:
                print(f"\n  ── STRUCTURAL MODES ──")
                for c in sm_codes:
                    print(f"    ▸ [{c['code']}] {c['short']}")

            # Save results JSON
            results_path = os.path.join(run_dir, "results.json")
            with open(results_path, 'w') as f:
                json.dump(result, f, indent=2, cls=NumpyEncoder)

            # Save diagnostics
            save_diagnostics(codes, sm_codes, run_dir)

            # Generate reports in all languages
            reports = report_all_languages(codes, result=result)
            for lang, rpt in reports.items():
                rpt_path = os.path.join(run_dir, f"report_{lang}.txt")
                with open(rpt_path, 'w', encoding='utf-8') as f:
                    f.write(rpt)

            print(f"\n  Files saved to: {run_dir}/")
            print(f"    dataset.csv, results.json, diagnostics.json,")
            print(f"    metadata.json, report_{{en,zh,hi,pt,it}}.txt")

        except ImportError as e:
            print(f"  Pipeline not available: {e}")
            print(f"  Dataset saved. Run manually: python hs_ingest.py {csv_path}")
        except Exception as e:
            print(f"  Pipeline error: {e}")
            import traceback
            traceback.print_exc()

    # Save metadata (includes results summary)
    config_with_carriers = dict(config)
    config_with_carriers["carriers"] = carriers
    meta = save_run_metadata(
        config_with_carriers, run_dir, N, D, run_num,
        classification=classification, hvld_shape=hvld_shape,
        hvld_r2=hvld_r2, nearest_constant=nearest_constant,
        eitt_pass=eitt_pass
    )

    # Update catalog
    catalog_entry = {
        "run_number": run_num,
        "folder": folder_name,
        "key": key,
        "name": config["name"],
        "domain": config["domain"],
        "data_source": data_source,
        "N": N,
        "D": D,
        "classification": classification,
        "hvld_shape": hvld_shape,
        "hvld_r2": round(hvld_r2, 4) if hvld_r2 else None,
        "nearest_constant": nearest_constant,
        "eitt_pass": eitt_pass,
        "structural_modes": len(sm_codes),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    catalog["runs"].append(catalog_entry)
    catalog["last_updated"] = catalog_entry["timestamp"]
    catalog["total_runs"] = len(catalog["runs"])
    save_catalog(test_dir, catalog)

    print(f"\n  Catalog updated: {len(catalog['runs'])} total runs")
    print()

    return {"run_dir": run_dir, "run_num": run_num, "data": data,
            "carriers": carriers, "config": config, "N": N, "D": D,
            "classification": classification}


def fetch_custom_and_analyze(inspire_id, table_name, test_dir,
                              name=None, domain=None, run_pipeline=True):
    """Fetch any HEPData table and analyze it."""
    catalog = load_catalog(test_dir)
    run_key = f"ins{inspire_id}_{table_name.replace(' ', '_').lower()}"
    run_dir, run_num, folder_name = create_run_folder(
        test_dir, catalog, run_key, name or f"HEPData ins{inspire_id}")

    print(f"\n{'=' * 60}")
    print(f"  Hˢ HEPData Custom Fetch")
    print(f"  Run #{run_num:03d} → {folder_name}/")
    print(f"{'=' * 60}")
    print(f"  INSPIRE ID: {inspire_id}")
    print(f"  Table:      {table_name}")

    try:
        record = fetch_record_info(inspire_id)
        rec_name = name or record.get("title", f"HEPData ins{inspire_id}")
        print(f"  Record:     {rec_name}")

        table_json = fetch_table(inspire_id, table_name)
        data, carriers = extract_compositions_from_table(table_json)

        N, D = len(data), len(carriers)
        print(f"  Extracted:  {N} observations, {D} carriers")
        print(f"  Carriers:   {', '.join(carriers)}")

        # Build a config dict for the standard pipeline
        config = {
            "name": rec_name,
            "domain": domain or "PARTICLE_PHYSICS",
            "description": f"Custom fetch from HEPData ins{inspire_id}, {table_name}",
            "inspire_id": inspire_id,
            "reference": record.get("doi", ""),
            "carriers": carriers
        }

        # Save dataset
        csv_path = os.path.join(run_dir, "dataset.csv")
        save_as_csv(data, carriers, csv_path)

        # Save raw API response for reference
        raw_path = os.path.join(run_dir, "hepdata_raw_response.json")
        with open(raw_path, 'w') as f:
            json.dump(table_json, f, indent=2)

        if run_pipeline:
            # Reuse the same pipeline logic
            try:
                from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder
                from hs_codes import generate_codes
                from hs_reporter import report, report_all_languages
                import numpy as np

                print(f"\n  Running 12-Step Pipeline...")
                hd = HigginsDecomposition(
                    experiment_id=f"HEP-{run_num:03d}",
                    name=rec_name,
                    domain=domain or "PARTICLE_PHYSICS",
                    carriers=carriers,
                    data_source_type="HEPDATA (api)",
                    data_source_description=config.get("reference", "")
                )
                hd.load_data(np.array(data))
                result = hd.run_full_extended()

                hvld_shape = result['steps'].get('step6_pll_shape', '?')
                hvld_r2 = result['steps'].get('step6_pll_R2', 0)
                sq = result['steps'].get('step7_squeeze_closest')
                nearest_constant = f"{sq['constant']} (δ={sq['delta']:.6f})" if sq else None
                eitt = result['steps'].get('step8_eitt_invariance', {})
                eitt_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False

                codes = generate_codes(result)
                sm_codes = [c for c in codes if c['code'].startswith('SM-')]
                classification = 'NATURAL' if any(c['code'] == 'S8-NAT-INF' for c in codes) \
                    else 'INVESTIGATE' if any(c['code'] == 'S8-INV-WRN' for c in codes) \
                    else 'FLAG'

                print(f"  HVLD: {hvld_shape} (R²={hvld_r2:.4f})")
                print(f"  Classification: {classification}")
                print(f"  Codes: {len(codes)} ({len(sm_codes)} structural modes)")

                with open(os.path.join(run_dir, "results.json"), 'w') as f:
                    json.dump(result, f, indent=2, cls=NumpyEncoder)
                save_diagnostics(codes, sm_codes, run_dir)
                reports = report_all_languages(codes, result=result)
                for lang, rpt in reports.items():
                    with open(os.path.join(run_dir, f"report_{lang}.txt"), 'w', encoding='utf-8') as f:
                        f.write(rpt)

            except Exception as e:
                print(f"  Pipeline error: {e}")
                classification = None
                hvld_shape = None
                hvld_r2 = None
                nearest_constant = None
                eitt_pass = None
                sm_codes = []
        else:
            classification = hvld_shape = hvld_r2 = nearest_constant = eitt_pass = None
            sm_codes = []

        # Save metadata and update catalog
        save_run_metadata(config, run_dir, N, D, run_num,
                          classification=classification, hvld_shape=hvld_shape,
                          hvld_r2=hvld_r2, nearest_constant=nearest_constant,
                          eitt_pass=eitt_pass)

        catalog["runs"].append({
            "run_number": run_num, "folder": folder_name,
            "key": run_key, "name": rec_name,
            "domain": domain or "PARTICLE_PHYSICS",
            "data_source": "hepdata_api",
            "N": N, "D": D,
            "classification": classification,
            "hvld_r2": round(hvld_r2, 4) if hvld_r2 else None,
            "structural_modes": len(sm_codes),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        catalog["last_updated"] = catalog["runs"][-1]["timestamp"]
        catalog["total_runs"] = len(catalog["runs"])
        save_catalog(test_dir, catalog)

        print(f"\n  Files saved to: {run_dir}/")
        return {"run_dir": run_dir, "run_num": run_num, "N": N, "D": D}

    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def list_datasets():
    """Print the curated dataset catalog."""
    print(f"\n{'=' * 70}")
    print(f"  Hˢ HEPData — Curated Compositional Datasets")
    print(f"{'=' * 70}")
    print(f"  {len(CURATED_DATASETS)} datasets available\n")

    for key, config in CURATED_DATASETS.items():
        D = len(config["carriers"])
        print(f"  [{key}]")
        print(f"    {config['name']}")
        print(f"    Domain: {config['domain']}  |  D={D} carriers")
        print(f"    Carriers: {', '.join(config['carriers'])}")
        if config.get("reference"):
            print(f"    Ref: {config['reference']}")
        print()

    print(f"  Usage:")
    print(f"    python hs_hepdata.py --fetch <key> --run             # single dataset")
    print(f"    python hs_hepdata.py --fetch-all --run               # all datasets")
    print(f"    python hs_hepdata.py --fetch-all --run --testdir exp # named folder")
    print(f"    python hs_hepdata.py --probe <inspire_id>            # inspect record")
    print()


def fetch_all(test_dir, run_pipeline=True):
    """Fetch all curated datasets into cataloged folders."""
    results = {}
    for key in CURATED_DATASETS:
        result = fetch_and_analyze(key, test_dir, run_pipeline=run_pipeline)
        if result:
            results[key] = result

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"  FETCH COMPLETE: {len(results)}/{len(CURATED_DATASETS)} datasets")
    print(f"{'=' * 70}")
    catalog = load_catalog(test_dir)
    print(f"  Test folder: {test_dir}")
    print(f"  Total runs:  {catalog['total_runs']}")
    print()
    print(f"  {'#':>4}  {'Dataset':<28} {'D':>2}  {'N':>3}  {'R²':>6}  {'Class':<8}  SM")
    print(f"  {'─'*4}  {'─'*28} {'─'*2}  {'─'*3}  {'─'*6}  {'─'*8}  {'─'*3}")
    for r in catalog["runs"]:
        r2_str = f"{r['hvld_r2']:.3f}" if r.get('hvld_r2') else "  —  "
        cls_str = r.get('classification', '—') or '—'
        sm_str = str(r.get('structural_modes', 0))
        print(f"  {r['run_number']:>4}  {r['name']:<28} {r['D']:>2}  {r['N']:>3}  {r2_str:>6}  {cls_str:<8}  {sm_str:>2}")
    print()

    return results


def show_catalog(test_dir):
    """Display the current analysis catalog."""
    catalog = load_catalog(test_dir)
    if not catalog["runs"]:
        print(f"\n  No analyses found in {test_dir}/")
        print(f"  Run: python hs_hepdata.py --fetch-all --run")
        return

    print(f"\n{'=' * 70}")
    print(f"  Hˢ Analysis Catalog — {test_dir}")
    print(f"{'=' * 70}")
    print(f"  Total runs: {len(catalog['runs'])}")
    print(f"  Last updated: {catalog.get('last_updated', '?')}")
    print()
    print(f"  {'#':>4}  {'Dataset':<28} {'D':>2}  {'N':>3}  {'R²':>6}  {'Class':<8}  SM  Folder")
    print(f"  {'─'*4}  {'─'*28} {'─'*2}  {'─'*3}  {'─'*6}  {'─'*8}  {'─'*3} {'─'*20}")
    for r in catalog["runs"]:
        r2_str = f"{r['hvld_r2']:.3f}" if r.get('hvld_r2') else "  —  "
        cls_str = r.get('classification', '—') or '—'
        sm_str = str(r.get('structural_modes', 0))
        print(f"  {r['run_number']:>4}  {r['name']:<28} {r['D']:>2}  {r['N']:>3}  {r2_str:>6}  {cls_str:<8}  {sm_str:>2}  {r['folder']}")
    print()
    print(f"  The instrument reads. The expert decides. The loop stays open.")
    print()


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hˢ HEPData Fetch — Compositional Data from High-Energy Physics",
        epilog="All data is public. No account needed. Just physics on the simplex."
    )
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all curated compositional datasets")
    parser.add_argument("--fetch", "-f", metavar="KEY",
                        help="Fetch a curated dataset by key")
    parser.add_argument("--fetch-all", action="store_true",
                        help="Fetch all curated datasets")
    parser.add_argument("--inspire", "-i", type=int, metavar="ID",
                        help="Fetch by INSPIRE record ID (custom)")
    parser.add_argument("--table", "-t", metavar="NAME",
                        help="Table name for custom fetch (e.g. 'Table 1')")
    parser.add_argument("--name", "-n", metavar="NAME",
                        help="System name for custom fetch")
    parser.add_argument("--domain", "-d", metavar="DOMAIN", default="PARTICLE_PHYSICS",
                        help="Domain label for custom fetch")
    parser.add_argument("--testdir", metavar="NAME", default=None,
                        help="Test folder name (default: hs_analyses)")
    parser.add_argument("--run", "-r", action="store_true",
                        help="Run hs_ingest.py pipeline on fetched data")
    parser.add_argument("--search", "-s", metavar="QUERY",
                        help="Search HEPData for records")
    parser.add_argument("--probe", "-p", type=int, metavar="ID",
                        help="Probe a HEPData record: show all tables and structure")
    parser.add_argument("--dump", action="store_true",
                        help="With --probe: save raw JSON for inspection")
    parser.add_argument("--catalog", "-c", action="store_true",
                        help="Show the analysis catalog for the test folder")

    args = parser.parse_args()
    test_dir = get_test_dir(args.testdir)

    if args.probe:
        probe_record(args.probe, dump_raw=args.dump)

    elif args.catalog:
        show_catalog(test_dir)

    elif args.list or (not args.fetch and not args.fetch_all and
                       not args.inspire and not args.search):
        list_datasets()

    elif args.search:
        results = search_hepdata(args.search, size=20)
        print(json.dumps(results, indent=2)[:3000])

    elif args.fetch:
        fetch_and_analyze(args.fetch, test_dir, run_pipeline=args.run)

    elif args.fetch_all:
        fetch_all(test_dir, run_pipeline=args.run)

    elif args.inspire and args.table:
        fetch_custom_and_analyze(args.inspire, args.table, test_dir,
                                  name=args.name, domain=args.domain,
                                  run_pipeline=args.run)

    elif args.inspire:
        print("ERROR: --inspire requires --table. Use --probe to find tables.")

    print("  The instrument reads. The expert decides. The loop stays open.")
