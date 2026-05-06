#!/usr/bin/env python3
"""
Determinism contract test.

The CNT engine MUST produce identical content_sha256 for the same input
under the same configuration. This test runs the engine on a small fixed
CSV and verifies the SHA matches the value committed to the golden file.

If this test fails, the determinism contract has been broken — investigate
before merging. Likely causes:
  * Non-deterministic sort order (set iteration, dict iteration on Py<3.7)
  * Floating-point library drift (numpy / system libm version)
  * Engine logic change that should have bumped the engine version
"""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cnt"))

import cnt as cnt_engine

GOLDEN_DIR = Path(__file__).parent / "golden"


def _run_against_golden(csv_path: Path, golden_json: Path,
                        is_temporal: bool = True,
                        ordering_method: str = "by-time") -> tuple[str, str]:
    """Run the engine on csv_path; return (computed_sha, expected_sha)."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        ordering = {
            "is_temporal":     is_temporal,
            "ordering_method": ordering_method,
            "caveat":          None if is_temporal else
                "Order is treated as arbitrary; angular_velocity and energy_depth are ordering-dependent.",
        }
        cnt_engine.cnt_run(str(csv_path), str(out_path), ordering)
        produced = json.load(out_path.open())
        expected = json.load(golden_json.open())
        return (
            produced["diagnostics"]["content_sha256"],
            expected["diagnostics"]["content_sha256"],
        )
    finally:
        out_path.unlink(missing_ok=True)


def test_japan_ember_determinism():
    """EMBER Japan T=26, D=8 — golden run produces fded914144fd…"""
    csv = ROOT / "experiments" / "codawork2026" / "ember_jpn" / \
          "ember_JPN_Japan_generation_TWh.csv"
    golden = ROOT / "experiments" / "codawork2026" / "ember_jpn" / "ember_jpn_cnt.json"
    assert csv.exists(), f"Missing input CSV: {csv}"
    assert golden.exists(), f"Missing golden JSON: {golden}"

    computed, expected = _run_against_golden(csv, golden)
    assert computed == expected, (
        f"Determinism gate FAILED on ember_jpn:\n"
        f"  computed: {computed}\n"
        f"  expected: {expected}\n"
        f"Investigate before merging."
    )


def test_ball_geochem_region_determinism():
    """Ball geochem by region T=95, D=10 (cross-section, not temporal)."""
    csv = ROOT / "experiments" / "domain" / "geochem_ball_region" / \
          "ball_oxides_by_region_barycenters.csv"
    golden = ROOT / "experiments" / "domain" / "geochem_ball_region" / \
             "geochem_ball_region_cnt.json"
    assert csv.exists()
    assert golden.exists()

    computed, expected = _run_against_golden(
        csv, golden, is_temporal=False, ordering_method="by-label",
    )
    assert computed == expected, f"Determinism FAIL ball/region: {computed} != {expected}"


def test_nuclear_semf_determinism():
    """Nuclear SEMF reference run T=76, D=5 (mass-number ordered)."""
    csv = ROOT / "experiments" / "reference" / "nuclear_semf" / "nuclear_semf_input.csv"
    golden = ROOT / "experiments" / "reference" / "nuclear_semf" / "nuclear_semf_cnt.json"
    assert csv.exists()
    assert golden.exists()

    computed, expected = _run_against_golden(
        csv, golden, is_temporal=False, ordering_method="by-label",
    )
    assert computed == expected, f"Determinism FAIL nuclear_semf: {computed} != {expected}"


if __name__ == "__main__":
    # Allow running directly: python test_determinism.py
    test_japan_ember_determinism()
    test_ball_geochem_region_determinism()
    test_nuclear_semf_determinism()
    print("All determinism tests passed.")
