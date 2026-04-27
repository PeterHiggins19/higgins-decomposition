#!/usr/bin/env python3
"""
Hˢ SECONDARY TEST TOOLS GENERATOR
====================================
"The tool makes tools."

Generates validation scripts, comparison tests, regression suites, and
health-check tools from Hˢ pipeline results. Each tool is self-contained
Python that can be run independently.

Usage:
    python hs_testgen.py --regression /path/to/catalog   # Generate regression suite
    python hs_testgen.py --healthcheck results.json      # Generate health-check script
    python hs_testgen.py --crosscheck dir1 dir2          # Generate cross-database comparison
    python hs_testgen.py --stability results.json        # Generate stability test (perturbation)
    python hs_testgen.py --envelope results.json         # Generate operating-envelope probe

Author: Peter Higgins / Claude
Version: 1.0
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone


def generate_regression_suite(catalog_dir, output_path):
    """
    Generate a regression test suite from a catalog of results.

    The generated script re-runs the pipeline on stored datasets and
    verifies that classifications, shapes, and R² values haven't changed.
    """
    catalog_path = os.path.join(catalog_dir, 'catalog.json')
    if not os.path.isfile(catalog_path):
        print(f"Error: No catalog.json found in {catalog_dir}")
        return

    with open(catalog_path) as f:
        catalog = json.load(f)

    runs = catalog.get('runs', [])
    if not runs:
        print("No runs found in catalog.")
        return

    # Build the regression test script
    lines = [
        '#!/usr/bin/env python3',
        '"""',
        f'Hˢ REGRESSION TEST SUITE',
        f'Generated: {datetime.now(timezone.utc).isoformat()}',
        f'Source catalog: {catalog_dir}',
        f'Runs tested: {len(runs)}',
        '',
        'This script verifies that the Hˢ pipeline produces identical',
        'results on previously analysed datasets. Any change in classification,',
        'HVLD shape, or R² (beyond tolerance) indicates a regression.',
        '"""',
        '',
        'import numpy as np',
        'import csv',
        'import json',
        'import os',
        'import sys',
        '',
        '# Add pipeline to path',
        'PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))',
        'sys.path.insert(0, PIPELINE_DIR)',
        '',
        'from higgins_decomposition_12step import HigginsDecomposition',
        'from hs_codes import generate_codes',
        '',
        f'CATALOG_DIR = r"{os.path.abspath(catalog_dir)}"',
        'R2_TOLERANCE = 0.001  # Allowable R² drift',
        '',
        'EXPECTED_RESULTS = {',
    ]

    for run in runs:
        if run.get('classification') is None:
            continue  # Skip failed runs
        lines.append(f'    "{run["folder"]}": {{')
        lines.append(f'        "name": "{run["name"]}",')
        lines.append(f'        "classification": "{run["classification"]}",')
        lines.append(f'        "hvld_shape": "{run["hvld_shape"]}",')
        lines.append(f'        "hvld_r2": {run["hvld_r2"]},')
        lines.append(f'        "eitt_pass": {str(run["eitt_pass"])},')
        lines.append(f'        "structural_modes": {run["structural_modes"]},')
        lines.append(f'    }},')

    lines.extend([
        '}',
        '',
        '',
        'def load_dataset(run_dir):',
        '    """Load dataset.csv from a run directory."""',
        '    csv_path = os.path.join(run_dir, "dataset.csv")',
        '    data = []',
        '    with open(csv_path) as f:',
        '        reader = csv.reader(f)',
        '        header = next(reader)',
        '        for row in reader:',
        '            data.append([float(x) for x in row])',
        '    return np.array(data), header',
        '',
        '',
        'def run_regression():',
        '    """Run all regression tests."""',
        '    passed = 0',
        '    failed = 0',
        '    errors = []',
        '',
        '    print(f"Hˢ Regression Test Suite")',
        '    print(f"=" * 60)',
        '    print(f"Testing {len(EXPECTED_RESULTS)} runs...\\n")',
        '',
        '    for folder, expected in EXPECTED_RESULTS.items():',
        '        run_dir = os.path.join(CATALOG_DIR, folder)',
        '        if not os.path.isdir(run_dir):',
        '            print(f"  SKIP  {folder} (directory not found)")',
        '            continue',
        '',
        '        try:',
        '            data, carriers = load_dataset(run_dir)',
        '            hd = HigginsDecomposition(',
        '                folder, expected["name"], "TEST", carriers=carriers',
        '            )',
        '            hd.load_data(data)',
        '            result = hd.run_full_extended()',
        '',
        '            # Check classification',
        '            sq = result["steps"].get("step7_squeeze_closest", {})',
        '            delta = sq.get("delta", 999) if sq else 999',
        '            if delta < 0.01:',
        '                actual_cls = "NATURAL"',
        '            elif delta < 0.05:',
        '                actual_cls = "INVESTIGATE"',
        '            else:',
        '                actual_cls = "FLAG"',
        '',
        '            # Check shape',
        '            actual_shape = result["steps"]["step6_pll_shape"]',
        '            actual_r2 = result["steps"]["step6_pll_R2"]',
        '',
        '            # Verify',
        '            issues = []',
        '            if actual_cls != expected["classification"]:',
        '                issues.append(f"classification: {expected[\'classification\']} -> {actual_cls}")',
        '            if actual_shape != expected["hvld_shape"]:',
        '                issues.append(f"shape: {expected[\'hvld_shape\']} -> {actual_shape}")',
        '            if abs(actual_r2 - expected["hvld_r2"]) > R2_TOLERANCE:',
        '                issues.append(f"R²: {expected[\'hvld_r2\']:.4f} -> {actual_r2:.4f}")',
        '',
        '            if issues:',
        '                sep = "; "',
        '                print(f"  FAIL  {folder}: {sep.join(issues)}")',
        '                errors.append((folder, issues))',
        '                failed += 1',
        '            else:',
        '                print(f"  PASS  {folder} ({actual_cls}, {actual_shape}, R²={actual_r2:.4f})")',
        '                passed += 1',
        '',
        '        except Exception as e:',
        '            print(f"  ERROR {folder}: {e}")',
        '            errors.append((folder, [str(e)]))',
        '            failed += 1',
        '',
        '    eq = "=" * 60',
        '    print(f"\\n{eq}")',
        '    print(f"Results: {passed} passed, {failed} failed")',
        '',
        '    if errors:',
        '        print(f"\\nREGRESSIONS DETECTED:")',
        '        for folder, issues in errors:',
        '            for issue in issues:',
        '                print(f"  [{folder}] {issue}")',
        '        sys.exit(1)',
        '    else:',
        '        print(f"\\nAll tests passed. Pipeline is stable.")',
        '        sys.exit(0)',
        '',
        '',
        'if __name__ == "__main__":',
        '    run_regression()',
    ])

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Regression suite generated: {output_path}")
    print(f"  Tests: {len([r for r in runs if r.get('classification')])}")
    print(f"  Run with: python {os.path.basename(output_path)}")


def generate_healthcheck(results_path, output_path):
    """
    Generate a health-check script for a specific result.

    The script tests boundary conditions around the analysed system:
    what happens if you perturb it slightly? Does the classification hold?
    """
    with open(results_path) as f:
        result = json.load(f)

    steps = result.get('steps', {})
    shape = steps.get('step6_pll_shape', 'unknown')
    r2 = steps.get('step6_pll_R2', 0)
    sq = steps.get('step7_squeeze_closest', {})
    const = sq.get('constant', 'none') if sq else 'none'
    delta = sq.get('delta', 999) if sq else 999

    lines = [
        '#!/usr/bin/env python3',
        '"""',
        f'Hˢ HEALTH CHECK — Perturbation Stability Test',
        f'Generated: {datetime.now(timezone.utc).isoformat()}',
        f'Source: {results_path}',
        f'Expected: {shape}, R²={r2:.4f}, nearest={const} (δ={delta:.6f})',
        '',
        'Tests whether small perturbations to the input data change',
        'the pipeline classification. A healthy system should be stable',
        'under ±5% noise.',
        '"""',
        '',
        'import numpy as np',
        'import csv',
        'import os',
        'import sys',
        '',
        'PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))',
        'sys.path.insert(0, PIPELINE_DIR)',
        '',
        'from higgins_decomposition_12step import HigginsDecomposition',
        '',
        f'EXPECTED_SHAPE = "{shape}"',
        f'EXPECTED_R2 = {r2}',
        'NOISE_LEVELS = [0.001, 0.005, 0.01, 0.02, 0.05]',
        'TRIALS_PER_LEVEL = 10',
        '',
        '',
        'def run_healthcheck(data_path):',
        '    """Run perturbation stability test."""',
        '    # Load data',
        '    data = []',
        '    with open(data_path) as f:',
        '        reader = csv.reader(f)',
        '        header = next(reader)',
        '        for row in reader:',
        '            data.append([float(x) for x in row])',
        '    data = np.array(data)',
        '    N, D = data.shape',
        '',
        '    print(f"Hˢ Perturbation Stability Test")',
        '    print(f"=" * 50)',
        '    print(f"Input: {N} observations, {D} carriers")',
        '    print(f"Expected: {EXPECTED_SHAPE}, R²={EXPECTED_R2:.4f}")',
        '    print()',
        '',
        '    for noise in NOISE_LEVELS:',
        '        shapes = []',
        '        r2s = []',
        '        for trial in range(TRIALS_PER_LEVEL):',
        '            perturbed = data + np.random.normal(0, noise, data.shape)',
        '            perturbed = np.abs(perturbed)',
        '            perturbed = perturbed / perturbed.sum(axis=1, keepdims=True)',
        '',
        '            hd = HigginsDecomposition(',
        '                f"HC-{noise}-{trial}", "Health Check", "TEST",',
        '                carriers=header',
        '            )',
        '            hd.load_data(perturbed)',
        '            result = hd.run_full_extended()',
        '',
        '            shapes.append(result["steps"]["step6_pll_shape"])',
        '            r2s.append(result["steps"]["step6_pll_R2"])',
        '',
        '        shape_stable = all(s == EXPECTED_SHAPE for s in shapes)',
        '        r2_mean = np.mean(r2s)',
        '        r2_std = np.std(r2s)',
        '',
        '        status = "STABLE" if shape_stable else "UNSTABLE"',
        '        print(f"  noise={noise:.3f}: {status}  '
               'shape={shapes.count(EXPECTED_SHAPE)}/{len(shapes)}  '
               'R²={r2_mean:.4f}±{r2_std:.4f}")',
        '',
        '    print(f"\\nDone.")',
        '',
        '',
        'if __name__ == "__main__":',
        '    if len(sys.argv) < 2:',
        '        print("Usage: python healthcheck.py dataset.csv")',
        '        sys.exit(1)',
        '    run_healthcheck(sys.argv[1])',
    ]

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Health check generated: {output_path}")


def generate_crosscheck(dir1, dir2, output_path):
    """
    Generate a cross-database comparison script.

    Compares fingerprints between two catalog directories to find
    compositionally similar systems across different databases.
    """
    lines = [
        '#!/usr/bin/env python3',
        '"""',
        f'Hˢ CROSS-DATABASE COMPARISON',
        f'Generated: {datetime.now(timezone.utc).isoformat()}',
        f'Database 1: {dir1}',
        f'Database 2: {dir2}',
        '',
        'Compares compositional fingerprints across two analysis catalogs',
        'to discover structurally similar systems in different domains.',
        '"""',
        '',
        'import json',
        'import os',
        'import sys',
        '',
        'PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))',
        'sys.path.insert(0, PIPELINE_DIR)',
        '',
        'from hs_fingerprint import extract_fingerprint, compare_fingerprints',
        '',
        f'DB1 = r"{os.path.abspath(dir1)}"',
        f'DB2 = r"{os.path.abspath(dir2)}"',
        'THRESHOLD = 0.7',
        '',
        '',
        'def load_fingerprints(db_dir):',
        '    """Load or generate fingerprints for all runs in a catalog."""',
        '    fps = []',
        '    for entry in sorted(os.listdir(db_dir)):',
        '        run_dir = os.path.join(db_dir, entry)',
        '        if not os.path.isdir(run_dir):',
        '            continue',
        '',
        '        # Try fingerprint.json first, then generate from results.json',
        '        fp_path = os.path.join(run_dir, "fingerprint.json")',
        '        if os.path.isfile(fp_path):',
        '            with open(fp_path) as f:',
        '                fps.append(json.load(f))',
        '            continue',
        '',
        '        results_path = os.path.join(run_dir, "results.json")',
        '        if os.path.isfile(results_path):',
        '            with open(results_path) as f:',
        '                result = json.load(f)',
        '            meta_path = os.path.join(run_dir, "metadata.json")',
        '            name = domain = None',
        '            if os.path.isfile(meta_path):',
        '                with open(meta_path) as f:',
        '                    meta = json.load(f)',
        '                name = meta.get("name")',
        '                domain = meta.get("domain")',
        '            fps.append(extract_fingerprint(result, name=name, domain=domain))',
        '    return fps',
        '',
        '',
        'def run_crosscheck():',
        '    """Compare all pairs between two databases."""',
        '    fps1 = load_fingerprints(DB1)',
        '    fps2 = load_fingerprints(DB2)',
        '',
        '    print(f"Hˢ Cross-Database Comparison")',
        '    print(f"=" * 60)',
        '    print(f"Database 1: {len(fps1)} systems")',
        '    print(f"Database 2: {len(fps2)} systems")',
        '    print()',
        '',
        '    matches = []',
        '    for fp1 in fps1:',
        '        for fp2 in fps2:',
        '            comp = compare_fingerprints(fp1, fp2)',
        '            if comp["similarity"] >= THRESHOLD:',
        '                matches.append((comp["similarity"], fp1, fp2, comp))',
        '',
        '    matches.sort(key=lambda x: x[0], reverse=True)',
        '',
        '    if not matches:',
        '        print(f"No matches above {THRESHOLD:.0%} threshold.")',
        '    else:',
        '        print(f"Found {len(matches)} cross-database match(es):\\n")',
        '        for sim, fp1, fp2, comp in matches:',
        '            n1 = fp1["identity"]["name"]',
        '            n2 = fp2["identity"]["name"]',
        '            d1 = fp1["identity"]["domain"]',
        '            d2 = fp2["identity"]["domain"]',
        '            print(f"  {sim:.1%}  {n1} ({d1}) <-> {n2} ({d2})")',
        '            if comp["shared_modes"]:',
        '                shared_str = ", ".join(comp["shared_modes"])',
        '                print(f"         Shared: {shared_str}")',
        '            print()',
        '',
        '',
        'if __name__ == "__main__":',
        '    run_crosscheck()',
    ]

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Cross-check script generated: {output_path}")


def generate_stability_test(results_path, output_path):
    """
    Generate a bootstrap stability test for a result.

    Subsamples the data at different ratios and checks whether the
    classification and fingerprint are stable under decimation.
    """
    with open(results_path) as f:
        result = json.load(f)

    steps = result.get('steps', {})
    shape = steps.get('step6_pll_shape', 'unknown')

    lines = [
        '#!/usr/bin/env python3',
        '"""',
        f'Hˢ STABILITY TEST — Bootstrap Subsampling',
        f'Generated: {datetime.now(timezone.utc).isoformat()}',
        '',
        'Subsamples the dataset at different ratios (90%, 75%, 50%) and',
        'checks whether the classification and HVLD shape are stable.',
        'A stable system should maintain its fingerprint under subsampling.',
        '"""',
        '',
        'import numpy as np',
        'import csv',
        'import os',
        'import sys',
        '',
        'PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))',
        'sys.path.insert(0, PIPELINE_DIR)',
        '',
        'from higgins_decomposition_12step import HigginsDecomposition',
        'from hs_fingerprint import extract_fingerprint',
        '',
        f'EXPECTED_SHAPE = "{shape}"',
        'SUBSAMPLE_RATIOS = [0.9, 0.75, 0.5]',
        'TRIALS = 20',
        '',
        '',
        'def run_stability(data_path):',
        '    """Run bootstrap stability analysis."""',
        '    data = []',
        '    with open(data_path) as f:',
        '        reader = csv.reader(f)',
        '        header = next(reader)',
        '        for row in reader:',
        '            data.append([float(x) for x in row])',
        '    data = np.array(data)',
        '    N, D = data.shape',
        '',
        '    print(f"Hˢ Bootstrap Stability Test")',
        '    print(f"=" * 50)',
        '    print(f"Input: N={N}, D={D}")',
        '    print(f"Expected shape: {EXPECTED_SHAPE}")',
        '    print()',
        '',
        '    for ratio in SUBSAMPLE_RATIOS:',
        '        n_sub = max(5, int(N * ratio))  # Guard: minimum 5',
        '        shapes = []',
        '        hashes = []',
        '',
        '        for trial in range(TRIALS):',
        '            idx = np.random.choice(N, n_sub, replace=False)',
        '            subset = data[idx]',
        '',
        '            hd = HigginsDecomposition(',
        '                f"BS-{ratio}-{trial}", "Bootstrap", "TEST",',
        '                carriers=header',
        '            )',
        '            hd.load_data(subset)',
        '            result = hd.run_full_extended()',
        '',
        '            shapes.append(result["steps"]["step6_pll_shape"])',
        '            fp = extract_fingerprint(result)',
        '            hashes.append(fp["fingerprint"]["hash"])',
        '',
        '        shape_rate = shapes.count(EXPECTED_SHAPE) / len(shapes)',
        '        unique_hashes = len(set(hashes))',
        '',
        '        status = "STABLE" if shape_rate >= 0.8 else "MARGINAL" if shape_rate >= 0.5 else "UNSTABLE"',
        '        print(f"  {ratio:.0%} subsample (n={n_sub}): {status}  '
               f'shape={shape_rate:.0%}  unique_fps={unique_hashes}/{TRIALS}")',
        '',
        '    print(f"\\nDone.")',
        '',
        '',
        'if __name__ == "__main__":',
        '    if len(sys.argv) < 2:',
        '        print("Usage: python stability_test.py dataset.csv")',
        '        sys.exit(1)',
        '    run_stability(sys.argv[1])',
    ]

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Stability test generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Hˢ Secondary Test Tools Generator — the tool makes tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
The tool makes tools. Each generated script is self-contained and can
be run independently against any dataset or catalog.

Examples:
  python hs_testgen.py --regression /path/to/hep_validation
  python hs_testgen.py --healthcheck results.json
  python hs_testgen.py --crosscheck /path/db1 /path/db2
  python hs_testgen.py --stability results.json
        """
    )

    parser.add_argument('--regression', metavar='CATALOG_DIR',
                        help='Generate regression test suite from a catalog')
    parser.add_argument('--healthcheck', metavar='RESULTS_JSON',
                        help='Generate perturbation health-check script')
    parser.add_argument('--crosscheck', nargs=2, metavar=('DIR1', 'DIR2'),
                        help='Generate cross-database comparison script')
    parser.add_argument('--stability', metavar='RESULTS_JSON',
                        help='Generate bootstrap stability test')
    parser.add_argument('-o', '--output', help='Output file path (auto-generated if omitted)')

    args = parser.parse_args()

    if args.regression:
        out = args.output or os.path.join(args.regression, 'regression_test.py')
        generate_regression_suite(args.regression, out)

    elif args.healthcheck:
        out = args.output or args.healthcheck.replace('.json', '_healthcheck.py')
        generate_healthcheck(args.healthcheck, out)

    elif args.crosscheck:
        out = args.output or 'crosscheck_test.py'
        generate_crosscheck(args.crosscheck[0], args.crosscheck[1], out)

    elif args.stability:
        out = args.output or args.stability.replace('.json', '_stability.py')
        generate_stability_test(args.stability, out)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
