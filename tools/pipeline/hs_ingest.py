#!/usr/bin/env python3
"""
Hˢ UNIVERSAL INGEST — CoDa-Ready Data Loader
===============================================
Accepts any standard compositional dataset and runs the full Hˢ pipeline.
No domain knowledge required. No configuration beyond the data file.

Designed for CoDa practitioners: if you have a CSV of compositions,
this tool reads it, decomposes it, and reports what it finds.

Supported input formats:
  - CSV (comma-separated, with header row naming the carriers)
  - TSV (tab-separated)
  - JSON (array of objects, or {"data": [...], "carriers": [...]})
  - Numpy .npy (N×D array, carriers auto-named)

The tool auto-detects:
  - Whether data needs closure (sums to constant ≠ 1)
  - Whether zeros need replacement
  - Whether the data is compositional at all (non-negative, D ≥ 2)
  - Experiment name from filename

Usage:
  python hs_ingest.py mydata.csv
  python hs_ingest.py mydata.csv --name "My System" --domain "GEOLOGY"
  python hs_ingest.py mydata.csv --lang pt --output results/
  python hs_ingest.py mydata.csv --metrology  # also run instrument check

What you get:
  - Full 12-step pipeline + extended panel
  - Diagnostic codes (69 codes + 10 structural modes)
  - Reports in 1 or 5 languages
  - Investigation prompts based on structural mode analysis
  - Results JSON for archival

What you need to know:
  - CoDa basics (what a composition is, what carriers are)
  - Nothing else. The tool handles the rest.

Author: Peter Higgins / Claude
Version: 1.0
For: CoDaWork 2026 — "bring your data, the tool reads it"
"""

import sys, os, json, argparse
import numpy as np
from datetime import datetime

# Pipeline imports
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PIPELINE_DIR)

from higgins_decomposition_12step import HigginsDecomposition, NumpyEncoder
from hs_codes import generate_codes
from hs_reporter import report, report_all_languages


def detect_format(filepath):
    """Detect file format from extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.csv', '.txt'):
        return 'csv'
    elif ext == '.tsv':
        return 'tsv'
    elif ext == '.json':
        return 'json'
    elif ext == '.npy':
        return 'npy'
    else:
        return 'csv'  # default to CSV


def load_csv(filepath, delimiter=','):
    """Load a CSV/TSV file with header row."""
    with open(filepath, encoding='utf-8') as f:
        header = f.readline().strip()

    # Detect delimiter if not specified
    if delimiter == ',' and '\t' in header and ',' not in header:
        delimiter = '\t'

    carriers = [c.strip().strip('"').strip("'") for c in header.split(delimiter)]

    # Remove any index/ID column (non-numeric first column)
    data = np.genfromtxt(filepath, delimiter=delimiter, skip_header=1)

    if data.ndim == 1:
        raise ValueError(f"Data has only 1 row. Need N ≥ 5.")

    # If first column looks like an index (integers 0,1,2...), remove it
    if data.shape[1] == len(carriers) + 1:
        first_col = data[:, 0]
        if np.allclose(first_col, np.arange(len(first_col))) or np.allclose(first_col, np.arange(1, len(first_col)+1)):
            data = data[:, 1:]
        else:
            # First column might be a real carrier, header was missing one
            carriers = [f"C{i+1}" for i in range(data.shape[1])]
    elif data.shape[1] != len(carriers):
        # Header doesn't match data columns
        carriers = [f"C{i+1}" for i in range(data.shape[1])]

    return data, carriers


def load_json_data(filepath):
    """Load a JSON file — supports multiple formats."""
    with open(filepath, encoding='utf-8') as f:
        raw = json.load(f)

    if isinstance(raw, list):
        # Array of objects: [{"SiO2": 0.5, "Al2O3": 0.3, ...}, ...]
        if isinstance(raw[0], dict):
            carriers = list(raw[0].keys())
            data = np.array([[row.get(c, 0) for c in carriers] for row in raw])
            return data, carriers
        # Array of arrays: [[0.5, 0.3, 0.2], ...]
        elif isinstance(raw[0], (list, tuple)):
            data = np.array(raw)
            carriers = [f"C{i+1}" for i in range(data.shape[1])]
            return data, carriers

    elif isinstance(raw, dict):
        # Object with "data" and "carriers" keys
        if 'data' in raw:
            data = np.array(raw['data'])
            carriers = raw.get('carriers', [f"C{i+1}" for i in range(data.shape[1])])
            return data, carriers

    raise ValueError("JSON format not recognized. Expected array of objects, array of arrays, or {data: [...], carriers: [...]}.")


def load_data(filepath):
    """Load data from any supported format."""
    fmt = detect_format(filepath)

    if fmt == 'csv':
        return load_csv(filepath, delimiter=',')
    elif fmt == 'tsv':
        return load_csv(filepath, delimiter='\t')
    elif fmt == 'json':
        return load_json_data(filepath)
    elif fmt == 'npy':
        data = np.load(filepath)
        carriers = [f"C{i+1}" for i in range(data.shape[1])]
        return data, carriers
    else:
        raise ValueError(f"Unsupported format: {fmt}")


def validate_compositional(data, carriers):
    """Validate the data is compositional (or close to it)."""
    issues = []

    N, D = data.shape

    # Check D ≥ 2
    if D < 2:
        issues.append(f"ERROR: D={D} — need at least 2 carriers (columns).")

    # Check N ≥ 5
    if N < 5:
        issues.append(f"ERROR: N={N} — need at least 5 observations (rows).")

    # Check non-negative
    if np.any(data < 0):
        neg_count = np.sum(data < 0)
        issues.append(f"WARNING: {neg_count} negative values detected. Taking absolute values.")

    # Check for NaN/Inf
    if np.any(np.isnan(data)):
        nan_count = np.sum(np.isnan(data))
        issues.append(f"ERROR: {nan_count} NaN values detected. Clean data first.")

    if np.any(np.isinf(data)):
        inf_count = np.sum(np.isinf(data))
        issues.append(f"ERROR: {inf_count} Inf values detected. Clean data first.")

    # Check if already closed (rows sum to constant)
    row_sums = data.sum(axis=1)
    sum_cv = np.std(row_sums) / np.mean(row_sums) * 100 if np.mean(row_sums) > 0 else 0
    if sum_cv < 0.1:
        sum_val = np.mean(row_sums)
        if abs(sum_val - 1.0) < 0.01:
            issues.append(f"INFO: Data already closed to 1.000. Simplex-ready.")
        elif abs(sum_val - 100.0) < 1:
            issues.append(f"INFO: Data closed to ~100 (percentages). Will re-close to 1.0.")
        elif abs(sum_val - 1e6) < 1e4:
            issues.append(f"INFO: Data closed to ~1M (ppm). Will re-close to 1.0.")
        else:
            issues.append(f"INFO: Data closed to ~{sum_val:.2f}. Will re-close to 1.0.")
    else:
        issues.append(f"INFO: Row sums vary (CV={sum_cv:.1f}%). Pipeline will close to simplex.")

    # Check for zero columns
    zero_cols = np.where(data.sum(axis=0) == 0)[0]
    if len(zero_cols) > 0:
        names = [carriers[i] for i in zero_cols]
        issues.append(f"WARNING: Zero columns detected: {names}. Removing.")

    return issues


def run_ingest(filepath, name=None, domain=None, lang=None, output_dir=None,
               all_languages=False, metrology=False):
    """Full ingest pipeline: load → validate → run → report."""

    print("=" * 60)
    print("  Hˢ Universal Ingest — CoDa-Ready Data Loader")
    print("=" * 60)
    print(f"  Input: {filepath}")
    print(f"  Time:  {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print()

    # ── LOAD ──
    data, carriers = load_data(filepath)
    N, D = data.shape
    print(f"  Loaded: N={N} observations, D={D} carriers")
    print(f"  Carriers: {', '.join(carriers)}")
    print()

    # ── VALIDATE ──
    issues = validate_compositional(data, carriers)
    has_errors = any(i.startswith('ERROR') for i in issues)
    for issue in issues:
        prefix = issue.split(':')[0]
        print(f"  {prefix}: {issue.split(':', 1)[1].strip()}")
    print()

    if has_errors:
        print("  Cannot proceed — fix errors above.")
        return None

    # Handle negatives
    if np.any(data < 0):
        data = np.abs(data)

    # Remove zero columns
    nonzero = data.sum(axis=0) > 0
    if not np.all(nonzero):
        data = data[:, nonzero]
        carriers = [c for c, nz in zip(carriers, nonzero) if nz]
        D = data.shape[1]

    # ── CONFIGURE ──
    basename = os.path.splitext(os.path.basename(filepath))[0]
    exp_id = basename.upper().replace(' ', '_')[:20]
    if name is None:
        name = basename.replace('_', ' ').replace('-', ' ').title()
    if domain is None:
        domain = "USER_DATA"
    if lang is None:
        lang = "en"
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(filepath))

    os.makedirs(output_dir, exist_ok=True)

    # ── RUN PIPELINE ──
    print("─" * 60)
    print("  Running Hˢ 12-Step Pipeline + Extended Panel...")
    print("─" * 60)

    hd = HigginsDecomposition(
        experiment_id=exp_id,
        name=name,
        domain=domain,
        carriers=carriers,
        data_source_type="LOCAL FILE",
        data_source_description=f"Ingested from {os.path.basename(filepath)}"
    )
    hd.load_data(data)
    result = hd.run_full_extended()

    print(f"  N={result['N']}, D={result['D']}")
    print(f"  HVLD: {result['steps'].get('step6_pll_shape', '?')} (R²={result['steps'].get('step6_pll_R2', 0):.4f})")

    sq = result['steps'].get('step7_squeeze_closest')
    if sq:
        print(f"  Nearest constant: {sq.get('constant', '?')} (δ={sq.get('delta', 0):.6f})")

    eitt = result['steps'].get('step8_eitt_invariance', {})
    eitt_pass = all(v.get('pass', False) for v in eitt.values()) if eitt else False
    print(f"  EITT: {'PASS' if eitt_pass else 'FAIL'}")
    print()

    # ── GENERATE CODES ──
    codes = generate_codes(result)
    sm_codes = [c for c in codes if c['code'].startswith('SM-')]

    print(f"  Diagnostic codes: {len(codes)}")
    print(f"  Structural modes: {len(sm_codes)}")

    # Show warnings and structural modes
    warnings = [c for c in codes if c['code'].endswith('-WRN')]
    discoveries = [c for c in codes if c['code'].endswith('-DIS') and not c['code'].startswith('SM-')]

    if warnings:
        print(f"\n  ── WARNINGS ──")
        for c in warnings:
            print(f"    [{c['code']}] {c['short']}")

    if sm_codes:
        print(f"\n  ── STRUCTURAL MODES — INVESTIGATE ──")
        for c in sm_codes:
            print(f"    ▸ [{c['code']}] {c['verbose'][:100]}")
    print()

    # ── GENERATE REPORTS ──
    print("─" * 60)
    print("  Generating reports...")
    print("─" * 60)

    if all_languages:
        reports = report_all_languages(codes, result=result)
        for l, rpt in reports.items():
            rpt_path = os.path.join(output_dir, f"{exp_id}_report_{l}.txt")
            with open(rpt_path, 'w', encoding='utf-8') as f:
                f.write(rpt)
            print(f"  {l}: {rpt_path}")
    else:
        rpt = report(codes, lang=lang, result=result)
        rpt_path = os.path.join(output_dir, f"{exp_id}_report_{lang}.txt")
        with open(rpt_path, 'w', encoding='utf-8') as f:
            f.write(rpt)
        print(f"  {lang}: {rpt_path}")

    # Save results JSON
    result_path = os.path.join(output_dir, f"{exp_id}_results.json")
    with open(result_path, 'w') as f:
        json.dump(result, f, indent=2, cls=NumpyEncoder)
    print(f"  Results: {result_path}")

    # ── METROLOGY (optional) ──
    if metrology:
        print()
        print("─" * 60)
        print("  Running instrument metrology...")
        print("─" * 60)
        from hs_metrology import run_full_metrology
        run_full_metrology()

    # ── SUMMARY ──
    print()
    print("=" * 60)
    print("  INGEST COMPLETE")
    print("=" * 60)
    classification = 'NATURAL' if any(c['code'] == 'S8-NAT-INF' for c in codes) \
        else 'INVESTIGATE' if any(c['code'] == 'S8-INV-WRN' for c in codes) \
        else 'FLAG'
    print(f"  Classification: {classification}")
    print(f"  Codes: {len(codes)} ({len(sm_codes)} structural modes)")
    if sm_codes:
        print(f"  Next steps:")
        for c in sm_codes:
            print(f"    ▸ {c['short']}")
    print()
    print("  The instrument reads. The expert decides. The loop stays open.")
    print()

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hˢ Universal Ingest — CoDa-Ready Data Loader",
        epilog="Any CSV of compositions works. No domain knowledge needed."
    )
    parser.add_argument("file", help="Path to data file (CSV, TSV, JSON, or .npy)")
    parser.add_argument("--name", "-n", help="System name (default: derived from filename)")
    parser.add_argument("--domain", "-d", help="Domain label (default: USER_DATA)")
    parser.add_argument("--lang", "-l", default="en", help="Report language: en, zh, hi, pt, it (default: en)")
    parser.add_argument("--all-languages", "-a", action="store_true", help="Generate reports in all 5 languages")
    parser.add_argument("--output", "-o", help="Output directory (default: same as input file)")
    parser.add_argument("--metrology", "-m", action="store_true", help="Also run instrument metrology check")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    run_ingest(
        filepath=args.file,
        name=args.name,
        domain=args.domain,
        lang=args.lang,
        output_dir=args.output,
        all_languages=args.all_languages,
        metrology=args.metrology,
    )
