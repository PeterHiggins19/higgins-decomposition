#!/usr/bin/env python3
"""
Hˢ STANDARD I/O — Unified Pipeline Runner
==========================================
One command. Data in, science out.

Takes any compositional dataset (CSV, TSV, JSON, NPY) and produces the
complete Hˢ standard output:

  1. Full 12-step pipeline + extended diagnostics
  2. Diagnostic codes + structural modes
  3. Reports (single or all 5 languages)
  4. Five mandatory projection PDFs:
     - Exploded Helix    (bill of materials)
     - Manifold Helix    (isometric 3D trajectory)
     - Projection Suite   (4-page orthographic + polar)
     - Polar Stack        (per-interval polar cross-sections + ghost + diff + table)
     - Manifold on Paper  (3D polar slice stack in projected space)
  5. Polar stack JSON     (structured data for journal integration)

Everything auto-sizes to the data. D=3 or D=300, N=10 or N=5000 — the
pipeline reads it, the projections render it, the tables report it.

Usage:
  python hs_run.py mydata.csv
  python hs_run.py mydata.csv --name "My System" --domain "GEOLOGY"
  python hs_run.py mydata.csv --output results/ --all-languages
  python hs_run.py mydata.csv --exp-id "Hs-M03" --metrology

Programmatic:
  from hs_run import run_full
  outputs = run_full("mydata.csv", name="My System", domain="GEOLOGY")

The instrument reads. The expert decides. The loop stays open.

Author: Peter Higgins / Claude
Version: 1.0
Dependency: NumPy only (+ reportlab for PDFs)
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime

# ── PATH SETUP ──
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PIPELINE_DIR)


def run_full(filepath, exp_id=None, name=None, domain=None, lang=None,
             output_dir=None, all_languages=False, metrology=False,
             skip_projections=False, quiet=False):
    """
    Full Hˢ Standard I/O: data file → pipeline → projections → reports.

    Parameters
    ----------
    filepath : str
        Path to input data file (CSV, TSV, JSON, or .npy).
    exp_id : str, optional
        Experiment ID (e.g. "Hs-M03"). Auto-derived from filename if omitted.
    name : str, optional
        Human-readable system name. Auto-derived from filename if omitted.
    domain : str, optional
        Domain label (e.g. "ENERGY", "GEOLOGY"). Default: "USER_DATA".
    lang : str, optional
        Report language: en, zh, hi, pt, it. Default: "en".
    output_dir : str, optional
        Output directory. Default: same directory as input file.
    all_languages : bool
        Generate reports in all 5 languages. Default: False.
    metrology : bool
        Run instrument metrology check. Default: False.
    skip_projections : bool
        Skip PDF generation (pipeline + reports only). Default: False.
    quiet : bool
        Suppress progress output. Default: False.

    Returns
    -------
    dict
        {
            "exp_id": str,
            "results_json": str,       # path to pipeline results JSON
            "outputs": {
                "helix_exploded": str,  # path to exploded helix PDF
                "manifold_helix": str,  # path to manifold helix PDF
                "projections": str,     # path to projection suite PDF
                "polar_stack": str,     # path to polar stack PDF
                "polar_json": str,      # path to polar stack JSON
                "manifold_paper": str,  # path to manifold on paper PDF
                "reports": [str],       # paths to report text files
            },
            "summary": {
                "N": int,
                "D": int,
                "carriers": [str],
                "classification": str,
                "structural_modes": int,
                "total_codes": int,
                "pages_generated": int,
            },
            "elapsed_seconds": float,
        }
    """

    t_start = time.time()

    def log(msg):
        if not quiet:
            print(msg)

    # ══════════════════════════════════════════════════════════════
    #  STAGE 1: INGEST — load, validate, run pipeline
    # ══════════════════════════════════════════════════════════════

    log("")
    log("╔══════════════════════════════════════════════════════════╗")
    log("║          Hˢ STANDARD I/O — Unified Pipeline             ║")
    log("╚══════════════════════════════════════════════════════════╝")
    log(f"  Input:  {os.path.abspath(filepath)}")
    log(f"  Time:   {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    log("")

    # Import ingest
    from hs_ingest import load_data, validate_compositional, run_ingest

    # Derive IDs from filename if not given
    basename = os.path.splitext(os.path.basename(filepath))[0]
    if exp_id is None:
        exp_id = basename.upper().replace(' ', '_').replace('-', '_')[:20]
    if name is None:
        name = basename.replace('_', ' ').replace('-', ' ').title()
    if domain is None:
        domain = "USER_DATA"
    if lang is None:
        lang = "en"
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(filepath))

    os.makedirs(output_dir, exist_ok=True)

    log(f"  Experiment: {exp_id}")
    log(f"  Name:       {name}")
    log(f"  Domain:     {domain}")
    log(f"  Output:     {output_dir}")
    log("")

    # ── Run ingest (pipeline + codes + reports) ──
    log("── STAGE 1: Pipeline Ingest ─────────────────────────────")
    t1 = time.time()

    result = run_ingest(
        filepath=filepath,
        name=name,
        domain=domain,
        lang=lang,
        output_dir=output_dir,
        all_languages=all_languages,
        metrology=metrology,
    )

    if result is None:
        log("  ABORT: Ingest failed — data validation errors.")
        return None

    t1_elapsed = time.time() - t1
    log(f"  Pipeline complete in {t1_elapsed:.2f}s")
    log("")

    # Locate the results JSON written by ingest
    # Ingest uses the basename-derived exp_id internally
    ingest_exp_id = basename.upper().replace(' ', '_')[:20]
    results_json = os.path.join(output_dir, f"{ingest_exp_id}_results.json")

    if not os.path.exists(results_json):
        # Try with our exp_id
        results_json = os.path.join(output_dir, f"{exp_id}_results.json")

    if not os.path.exists(results_json):
        # Search for any results JSON in the output directory
        candidates = [f for f in os.listdir(output_dir) if f.endswith('_results.json')]
        if candidates:
            # Use the most recently modified one
            candidates.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
            results_json = os.path.join(output_dir, candidates[0])
        else:
            log("  ERROR: Cannot find results JSON from ingest.")
            return None

    log(f"  Results JSON: {os.path.basename(results_json)}")

    # Collect report files
    report_files = []
    if all_languages:
        for l in ['en', 'pt', 'it', 'zh', 'hi']:
            rpt = os.path.join(output_dir, f"{ingest_exp_id}_report_{l}.txt")
            if os.path.exists(rpt):
                report_files.append(rpt)
    else:
        rpt = os.path.join(output_dir, f"{ingest_exp_id}_report_{lang}.txt")
        if os.path.exists(rpt):
            report_files.append(rpt)

    # ══════════════════════════════════════════════════════════════
    #  STAGE 2: MANDATORY PROJECTIONS — four PDF generators
    # ══════════════════════════════════════════════════════════════

    outputs = {
        "helix_exploded": None,
        "manifold_helix": None,
        "projections": None,
        "polar_stack": None,
        "polar_json": None,
        "manifold_paper": None,
        "reports": report_files,
    }

    total_pages = 0

    if skip_projections:
        log("── STAGE 2: Projections SKIPPED (--no-projections) ──────")
    else:
        log("── STAGE 2: Mandatory Projections ───────────────────────")
        log("")

        # Use exp_id for output naming (consistent with experiment conventions)
        prefix = os.path.join(output_dir, exp_id)

        # ── 2a. Exploded Helix ──
        log("  [1/5] Exploded Helix (bill of materials)...")
        t2a = time.time()
        try:
            from hs_helix_exploded import build_helix_pdf
            out_helix = f"{prefix}_helix_exploded.pdf"
            build_helix_pdf(results_json, out_helix)
            outputs["helix_exploded"] = out_helix
            # Exploded helix is 1 page
            total_pages += 1
            log(f"        → {os.path.basename(out_helix)} ({time.time()-t2a:.1f}s)")
        except Exception as e:
            log(f"        ✗ FAILED: {e}")

        # ── 2b. Manifold Helix ──
        log("  [2/5] Manifold Helix (isometric 3D trajectory)...")
        t2b = time.time()
        try:
            from hs_manifold_helix import build_manifold_helix_pdf
            out_manifold = f"{prefix}_manifold_helix.pdf"
            build_manifold_helix_pdf(results_json, out_manifold)
            outputs["manifold_helix"] = out_manifold
            # Manifold helix is 1 page
            total_pages += 1
            log(f"        → {os.path.basename(out_manifold)} ({time.time()-t2b:.1f}s)")
        except Exception as e:
            log(f"        ✗ FAILED: {e}")

        # ── 2c. Projection Suite ──
        log("  [3/5] Projection Suite (4-page orthographic + polar)...")
        t2c = time.time()
        try:
            from hs_manifold_projections import build_projections_pdf
            out_proj = f"{prefix}_projections.pdf"
            build_projections_pdf(results_json, out_proj)
            outputs["projections"] = out_proj
            # Projection suite is 4 pages
            total_pages += 4
            log(f"        → {os.path.basename(out_proj)} ({time.time()-t2c:.1f}s)")
        except Exception as e:
            log(f"        ✗ FAILED: {e}")

        # ── 2d. Polar Stack ──
        log("  [4/5] Polar Stack (per-interval cross-sections + ghost + diff + table)...")
        t2d = time.time()
        try:
            from hs_polar_stack import build_polar_stack_pdf
            out_polar = f"{prefix}_polar_stack.pdf"
            build_polar_stack_pdf(results_json, out_polar)
            outputs["polar_stack"] = out_polar

            # Polar stack companion JSON
            polar_json = out_polar.replace('.pdf', '.json')
            if os.path.exists(polar_json):
                outputs["polar_json"] = polar_json

            # Estimate polar stack pages: 1 + N + 1 + 1 + 1 + ceil(N/32) + 1
            import math
            N = result.get('N', 10)
            polar_pages = 1 + N + 1 + 1 + 1 + math.ceil(N / 32) + 1
            total_pages += polar_pages
            log(f"        → {os.path.basename(out_polar)} ({time.time()-t2d:.1f}s)")
            if outputs["polar_json"]:
                log(f"        → {os.path.basename(polar_json)}")
        except Exception as e:
            log(f"        ✗ FAILED: {e}")

        # ── 2e. Manifold on Paper ──
        log("  [5/5] Manifold on Paper (3D polar slice stack in projected space)...")
        t2e = time.time()
        try:
            from hs_manifold_paper import build_manifold_paper_pdf
            out_manifold_paper = f"{prefix}_manifold_paper.pdf"
            # Manifold paper works best with polar stack JSON (real per-year CLR values)
            # Fall back to pipeline results JSON if polar JSON not available
            manifold_input = outputs.get("polar_json") or results_json
            build_manifold_paper_pdf(manifold_input, out_manifold_paper)
            outputs["manifold_paper"] = out_manifold_paper
            # Manifold paper is 3 pages
            total_pages += 3
            log(f"        → {os.path.basename(out_manifold_paper)} ({time.time()-t2e:.1f}s)")
        except Exception as e:
            log(f"        ✗ FAILED: {e}")

        log("")

    # ══════════════════════════════════════════════════════════════
    #  STAGE 3: SUMMARY
    # ══════════════════════════════════════════════════════════════

    elapsed = time.time() - t_start

    # Read back results for summary data
    with open(results_json, 'r') as f:
        res_data = json.load(f)

    N = res_data.get('N', 0)
    D = res_data.get('D', 0)
    carriers = res_data.get('carriers', [])

    # Count codes from the result
    from hs_codes import generate_codes
    codes = generate_codes(res_data)
    sm_codes = [c for c in codes if c['code'].startswith('SM-')]

    classification = 'NATURAL' if any(c['code'] == 'S8-NAT-INF' for c in codes) \
        else 'INVESTIGATE' if any(c['code'] == 'S8-INV-WRN' for c in codes) \
        else 'FLAG'

    # Count generated files
    generated_files = []
    if outputs["helix_exploded"]:
        generated_files.append(os.path.basename(outputs["helix_exploded"]))
    if outputs["manifold_helix"]:
        generated_files.append(os.path.basename(outputs["manifold_helix"]))
    if outputs["projections"]:
        generated_files.append(os.path.basename(outputs["projections"]))
    if outputs["polar_stack"]:
        generated_files.append(os.path.basename(outputs["polar_stack"]))
    if outputs["polar_json"]:
        generated_files.append(os.path.basename(outputs["polar_json"]))
    if outputs["manifold_paper"]:
        generated_files.append(os.path.basename(outputs["manifold_paper"]))
    generated_files.append(os.path.basename(results_json))
    for r in report_files:
        generated_files.append(os.path.basename(r))

    summary = {
        "N": N,
        "D": D,
        "carriers": carriers,
        "classification": classification,
        "structural_modes": len(sm_codes),
        "total_codes": len(codes),
        "pages_generated": total_pages,
    }

    log("╔══════════════════════════════════════════════════════════╗")
    log("║                  Hˢ STANDARD I/O COMPLETE               ║")
    log("╚══════════════════════════════════════════════════════════╝")
    log(f"  Experiment:     {exp_id}")
    log(f"  System:         {name}")
    log(f"  Data:           N={N} observations, D={D} carriers")
    log(f"  Classification: {classification}")
    log(f"  Codes:          {len(codes)} ({len(sm_codes)} structural modes)")
    log(f"  Pages:          {total_pages}")
    log(f"  Files:          {len(generated_files)}")
    log(f"  Elapsed:        {elapsed:.2f}s")
    log("")
    log("  ── Generated Files ──")
    for gf in generated_files:
        log(f"    {gf}")
    log("")
    log("  The instrument reads. The expert decides. The loop stays open.")
    log("")

    return {
        "exp_id": exp_id,
        "results_json": results_json,
        "outputs": outputs,
        "summary": summary,
        "elapsed_seconds": elapsed,
    }


# ══════════════════════════════════════════════════════════════════
#  CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hˢ Standard I/O — Unified Pipeline Runner",
        epilog="One command. Data in, science out.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file",
        help="Path to data file (CSV, TSV, JSON, or .npy)")
    parser.add_argument("--exp-id", "-e",
        help="Experiment ID (e.g. 'Hs-M03'). Default: derived from filename")
    parser.add_argument("--name", "-n",
        help="System name (e.g. 'Gold/Silver Ratio'). Default: derived from filename")
    parser.add_argument("--domain", "-d",
        help="Domain label (e.g. 'ENERGY', 'GEOLOGY'). Default: USER_DATA")
    parser.add_argument("--lang", "-l", default="en",
        help="Report language: en, zh, hi, pt, it. Default: en")
    parser.add_argument("--all-languages", "-a", action="store_true",
        help="Generate reports in all 5 languages")
    parser.add_argument("--output", "-o",
        help="Output directory. Default: same as input file")
    parser.add_argument("--metrology", "-m", action="store_true",
        help="Also run instrument metrology check")
    parser.add_argument("--no-projections", action="store_true",
        help="Skip PDF projection generation (pipeline + reports only)")
    parser.add_argument("--quiet", "-q", action="store_true",
        help="Suppress progress output")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    result = run_full(
        filepath=args.file,
        exp_id=args.exp_id,
        name=args.name,
        domain=args.domain,
        lang=args.lang,
        output_dir=args.output,
        all_languages=args.all_languages,
        metrology=args.metrology,
        skip_projections=args.no_projections,
        quiet=args.quiet,
    )

    if result is None:
        sys.exit(1)

    sys.exit(0)
