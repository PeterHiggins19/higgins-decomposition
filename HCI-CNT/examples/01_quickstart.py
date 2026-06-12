#!/usr/bin/env python3
"""
HUF-CNT five-minute quickstart.

Runs the engine on the EMBER Japan reference CSV and prints the headline
numbers. Verifies the determinism gate: the computed content_sha256 must
match the published reference SHA character-for-character.
"""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cnt"))
import cnt as cnt_engine

INPUT_CSV = ROOT / "experiments" / "codawork2026" / "ember_jpn" / \
            "ember_JPN_Japan_generation_TWh.csv"

PUBLISHED_SHA = "fded914144fd6a8542717c357440dce7bdca3a537a4fe0a237bee2f1784456fc"


def main():
    print(f"HUF-CNT quickstart - running engine on {INPUT_CSV.name}")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out_json = Path(tf.name)

    ordering = {
        "is_temporal":     True,
        "ordering_method": "by-time",
        "caveat":          None,
    }
    cnt_engine.cnt_run(str(INPUT_CSV), str(out_json), ordering)

    j = json.load(out_json.open())

    md   = j["metadata"]
    di   = j["diagnostics"]
    dphe = j["depth"]["higgins_extensions"]
    summ = dphe["summary"]
    ca   = dphe["curvature_attractor"]
    ir   = dphe["impulse_response"]
    invl = dphe["involution_proof"]

    sha_str = di["content_sha256"]

    print()
    print("=" * 60)
    print(f"Engine          : {md['engine_version']}")
    print(f"Schema          : {md['schema_version']}")
    print(f"T (records)     : {j['input']['n_records']}")
    print(f"D (carriers)    : {j['input']['n_carriers']}")
    print(f"IR class        : {ir['classification']}")
    print(f"Curvature depth : {summ['curvature_depth']}")
    print(f"Energy depth    : {summ['energy_depth']}")
    if ca.get("amplitude") is not None:
        print(f"Period          : {ca.get('period')}")
        print(f"Amplitude A     : {ca.get('amplitude'):.4f}")
        clyap = ca.get("contraction_lyapunov")
        if clyap is not None:
            print(f"Contraction L   : {clyap:.4f}")
    print(f"M^2 residual    : {invl['mean_residual']:.2e}")
    print(f"content_sha256  : {sha_str}")
    print()

    if sha_str == PUBLISHED_SHA:
        print("PASS  Determinism gate matched published reference SHA.")
    else:
        print("FAIL  Determinism gate did NOT match.")
        print(f"  Published: {PUBLISHED_SHA}")
        print(f"  Computed : {sha_str}")
        sys.exit(1)

    print(f"\nFull JSON written to: {out_json}")
    print("Open it in any text editor to see every computed value.")


if __name__ == "__main__":
    main()
