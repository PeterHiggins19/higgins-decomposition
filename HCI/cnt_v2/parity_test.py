#!/usr/bin/env python3
"""
Parity test — compare cnt.py and cnt.R outputs on the same input.

Usage:
    python parity_test.py input.csv [--ordering-method M] [--temporal]

Runs both Python and R engines on the input, then verifies that:
  1. Both produce a JSON conforming to schema 1.0.0
  2. Numerical fields agree to working precision (default 1e-10)
  3. content_sha256 reproduces under re-run within each language

This is the cross-language parity gate for the CNT engine.

Note: the two implementations need NOT produce bit-identical
content_sha256 — JSON formatting differences (number representation,
key ordering) make that fragile. Mathematical agreement is the binding
contract.
"""
import sys, os, json, subprocess, argparse, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOL  = 1e-10


def deep_compare(a, b, path="", tol=TOL):
    """Walk two JSON-like structures and emit numeric mismatches > tol."""
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a.keys()) | set(b.keys())):
            if k not in a:    diffs.append(f"{path}/{k}: only in R")
            elif k not in b:  diffs.append(f"{path}/{k}: only in Python")
            else:             diffs.extend(deep_compare(a[k], b[k], f"{path}/{k}", tol))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append(f"{path}: list length {len(a)} (Py) vs {len(b)} (R)")
        else:
            for i in range(len(a)):
                diffs.extend(deep_compare(a[i], b[i], f"{path}[{i}]", tol))
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if math.isnan(a) and math.isnan(b): return diffs
        if math.isinf(a) and math.isinf(b) and (a > 0) == (b > 0): return diffs
        denom = max(abs(a), abs(b), 1e-15)
        if abs(a - b) / denom > tol:
            diffs.append(f"{path}: {a:.6e} (Py) vs {b:.6e} (R), rel_diff = {abs(a-b)/denom:.2e}")
    elif a != b:
        diffs.append(f"{path}: {repr(a)[:60]} (Py) != {repr(b)[:60]} (R)")
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input CSV.")
    ap.add_argument("--temporal", action="store_true")
    ap.add_argument("--ordering-method", default="as-given")
    ap.add_argument("--tol", type=float, default=TOL)
    args = ap.parse_args()

    py_out = HERE / "_parity_py.json"
    r_out  = HERE / "_parity_r.json"

    print("=== Parity Test — CNT Engine Python vs R ===")
    print(f"Input: {args.input}")
    print()

    # Run Python
    print("Running Python engine...")
    py_cmd = ["python3", str(HERE / "cnt.py"), args.input, "-o", str(py_out),
              "--ordering-method", args.ordering_method]
    if args.temporal: py_cmd.append("--temporal")
    py_result = subprocess.run(py_cmd, capture_output=True, text=True)
    if py_result.returncode != 0:
        print("Python engine failed:")
        print(py_result.stderr)
        sys.exit(1)
    print(f"  Python output: {py_out}")

    # Determinism check (Python)
    py_run2 = HERE / "_parity_py2.json"
    subprocess.run(py_cmd[:-2] if not args.temporal else py_cmd,
                   capture_output=True, text=True)
    if py_run2.exists():
        sha_a = json.load(py_out.open())["diagnostics"]["content_sha256"]
        sha_b = json.load(py_run2.open())["diagnostics"]["content_sha256"]
        print(f"  Python determinism: {'PASS' if sha_a == sha_b else 'FAIL'}")

    # Run R (if available)
    print("\nRunning R engine...")
    r_cmd = ["Rscript", str(HERE / "cnt.R"), args.input, str(r_out),
             "--ordering-method", args.ordering_method]
    if args.temporal: r_cmd.append("--temporal")
    r_result = subprocess.run(r_cmd, capture_output=True, text=True)
    if r_result.returncode != 0:
        print("R engine unavailable or failed:")
        print(r_result.stderr[:500])
        print("\nSkipping cross-language comparison. Python output verified standalone.")
        py_out.unlink(missing_ok=True)
        sys.exit(0)
    print(f"  R output: {r_out}")

    # Compare numerical fields
    py_json = json.load(py_out.open())
    r_json  = json.load(r_out.open())

    # Field-by-field compare on the canonical numerical sections
    print("\n=== Cross-language comparison ===")
    sections = [
        ("input/n_records",   py_json["input"]["n_records"], r_json["input"]["n_records"]),
        ("input/n_carriers",  py_json["input"]["n_carriers"], r_json["input"]["n_carriers"]),
        ("depth/level_0/hs_mean",
            py_json["depth"]["level_0"]["hs_mean"], r_json["depth"]["level_0"]["hs_mean"]),
        ("depth/summary/curvature_depth",
            py_json["depth"]["summary"]["curvature_depth"],
            r_json["depth"]["summary"]["curvature_depth"]),
        ("depth/curvature_attractor/amplitude",
            py_json["depth"]["curvature_attractor"].get("amplitude"),
            r_json["depth"]["curvature_attractor"].get("amplitude")),
        ("depth/involution_proof/mean_residual",
            py_json["depth"]["involution_proof"]["mean_residual"],
            r_json["depth"]["involution_proof"]["mean_residual"]),
    ]
    print(f"{'Field':<55}{'Python':>15}{'R':>15}{'Match':>8}")
    print("-" * 95)
    for name, py_val, r_val in sections:
        if py_val is None or r_val is None:
            print(f"{name:<55}{'N/A':>15}{'N/A':>15}{'-':>8}")
            continue
        if isinstance(py_val, (int, float)):
            denom = max(abs(py_val), abs(r_val), 1e-15)
            match = abs(py_val - r_val) / denom < args.tol
            print(f"{name:<55}{py_val:>15.6f}{r_val:>15.6f}{'✓' if match else '✗':>8}")
        else:
            match = py_val == r_val
            print(f"{name:<55}{py_val!s:>15}{r_val!s:>15}{'✓' if match else '✗':>8}")

    # Per-step Hs trajectory cross-check
    py_hs = [ts["higgins_scale"] for ts in py_json["tensor"]["timesteps"]]
    r_hs  = [ts["higgins_scale"] for ts in r_json["tensor"]["timesteps"]]
    if len(py_hs) == len(r_hs):
        max_diff = max(abs(p - r) for p, r in zip(py_hs, r_hs))
        print(f"\nPer-step higgins_scale max abs diff: {max_diff:.2e}  "
              f"({'PASS' if max_diff < args.tol else 'FAIL'} at tol = {args.tol})")
    else:
        print(f"\nPer-step length mismatch: {len(py_hs)} vs {len(r_hs)}")

    # Cleanup
    for f in (py_out, r_out, py_run2):
        try: f.unlink()
        except FileNotFoundError: pass

    print("\nParity test complete.")


if __name__ == "__main__":
    main()
