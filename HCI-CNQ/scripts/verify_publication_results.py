#!/usr/bin/env python3
"""Verify observed CNQ results against the locked expected_results.json.

Used as the strict gate for publication readiness. Compares each
experiment's observed values (from confirmation_summary.json or by
re-running cnq.py on the spot) against the locked expectations and
exits non-zero if anything drifts.

Usage:
    # Verify against the most recent run_all_confirmations.py output:
    python HCI-CNQ/scripts/verify_publication_results.py --repo-root .

    # Strict mode: re-run each experiment and verify against expected.
    python HCI-CNQ/scripts/verify_publication_results.py --repo-root . --rerun
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "engine"))

from cnt_adapter import find_repo_root  # noqa: E402


def _resolve_under(repo_root: Path, rel: str) -> Path:
    p1 = (repo_root / rel).resolve()
    if p1.exists():
        return p1
    p2 = (repo_root / "Hs" / rel).resolve()
    if p2.exists():
        return p2
    return p1


def _close_enough(observed, expected, *, rel_tol=1e-12, abs_tol=0.0) -> bool:
    """Float comparison with explicit tolerances. NaN-safe."""
    if observed is None or expected is None:
        return observed == expected
    try:
        return math.isclose(float(observed), float(expected),
                            rel_tol=rel_tol, abs_tol=abs_tol)
    except (TypeError, ValueError):
        return observed == expected


def verify_experiment(name: str, observed: dict, expected: dict) -> list:
    """Compare observed vs expected for one experiment.
    Returns a list of failure descriptions (empty list = all good).
    """
    failures = []

    exp_block = expected.get("expected", {})

    # Strict equality on the published max_residual (when applicable).
    if "max_residual" in exp_block:
        if not _close_enough(observed.get("max_residual"),
                             exp_block["max_residual"], rel_tol=0, abs_tol=0):
            # Allow rel_tol of 1e-15 to absorb the tiny variation that
            # different BLAS implementations can introduce, but flag any
            # drift > 1 ULP.
            if not _close_enough(observed.get("max_residual"),
                                 exp_block["max_residual"], rel_tol=1e-15):
                failures.append(
                    f"max_residual: observed={observed.get('max_residual')} "
                    f"expected={exp_block['max_residual']}"
                )

    # Gate pass must be true if expected.
    if exp_block.get("gate_pass") is True and observed.get("gate_pass") is not True:
        failures.append(
            f"gate_pass: observed={observed.get('gate_pass')} expected=True"
        )

    # Dimension label.
    if exp_block.get("dimension_label") and (
        observed.get("dimension_label") != exp_block["dimension_label"]
    ):
        failures.append(
            f"dimension_label: observed={observed.get('dimension_label')!r} "
            f"expected={exp_block['dimension_label']!r}"
        )

    # Parent CNT content hash (when expected).
    if exp_block.get("parent_cnt_content_sha256"):
        if observed.get("parent_cnt_content_sha256") != exp_block["parent_cnt_content_sha256"]:
            failures.append(
                f"parent_cnt_content_sha256: observed={observed.get('parent_cnt_content_sha256')} "
                f"expected={exp_block['parent_cnt_content_sha256']}"
            )

    return failures


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify CNQ confirmation results against expected_results.json."
    )
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(
        "--rerun",
        action="store_true",
        help="Re-run all experiments via run_all_confirmations.py before verifying.",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Path to a confirmation_summary.json from a prior run. "
             "Defaults to <repo_root>/HCI-CNQ/results/confirmation_summary.json.",
    )
    args = parser.parse_args(argv)

    repo_root = find_repo_root(explicit=args.repo_root)

    if args.rerun:
        # Spawn run_all_confirmations.py
        import subprocess
        runner = _resolve_under(repo_root, "HCI-CNQ/scripts/run_all_confirmations.py")
        rc = subprocess.call([sys.executable, str(runner), "--repo-root", str(repo_root)])
        if rc != 0:
            print(f"[verify] run_all_confirmations.py exited {rc}; aborting verification")
            return rc

    summary_path = args.summary_json or _resolve_under(
        repo_root, "HCI-CNQ/results/confirmation_summary.json"
    )
    expected_path = _resolve_under(repo_root, "HCI-CNQ/results/expected_results.json")

    if not summary_path.exists():
        print(f"[verify] ERROR: confirmation_summary.json not found at {summary_path}")
        print("[verify]        run with --rerun to produce it.")
        return 2
    if not expected_path.exists():
        print(f"[verify] ERROR: expected_results.json not found at {expected_path}")
        return 2

    with summary_path.open() as f:
        summary = json.load(f)
    with expected_path.open() as f:
        expected_doc = json.load(f)

    expected_experiments = expected_doc["experiments"]
    observed_experiments = {e["name"]: e for e in summary["experiments"]}

    print("=" * 72)
    print("CNQ publication-readiness verification")
    print("=" * 72)

    total_failures = 0
    for name, exp in expected_experiments.items():
        observed = observed_experiments.get(name)
        if observed is None:
            print(f"\n[{name}] MISSING from confirmation_summary.json")
            total_failures += 1
            continue
        if not observed.get("ok", False):
            print(f"\n[{name}] RUN FAILED: {observed.get('error', '')}")
            total_failures += 1
            continue

        failures = verify_experiment(name, observed, exp)
        status = "PASS" if not failures else "FAIL"
        print(f"\n[{name}] {status}")
        for f_desc in failures:
            print(f"  - {f_desc}")
        total_failures += len(failures)

    print("\n" + "=" * 72)
    if total_failures == 0:
        print("  ALL EXPERIMENTS VERIFIED — publication-ready")
    else:
        print(f"  {total_failures} discrepancies found")
    print("=" * 72)

    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
