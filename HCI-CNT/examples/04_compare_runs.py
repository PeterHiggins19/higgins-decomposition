#!/usr/bin/env python3
"""
HUF-CNT — compare two runs in the atlas catalog using the delta tool.

Runs the same dataset twice and demonstrates the delta tool's smart
interpretation of "same input, identical engine result" vs "different
input, different result".
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "atlas"))
import atlas as atlas_module
import catalog as catalog_module
import delta as delta_module
import tempfile


def main():
    runs_dir     = ROOT / "atlas" / "runs"
    catalog_path = ROOT / "atlas" / "catalog" / "atlas_catalog.json"

    # Render Japan twice, then Germany once
    print("Rendering 3 atlases for delta comparison...")
    for label_eid in [("first jpn", "ember_jpn"),
                      ("second jpn", "ember_jpn"),
                      ("germany", "ember_deu")]:
        eid = label_eid[1]
        notes = label_eid[0]
        json_path = ROOT / "experiments" / "codawork2026" / eid / f"{eid}_cnt.json"
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
            pdf_path = Path(tf.name)
        meta = atlas_module.render_atlas(str(json_path), str(pdf_path),
                                         skip_tours=True)
        run_meta = catalog_module.save_run(meta, pdf_path,
                                           catalog_path, runs_dir,
                                           user_notes=notes)
        print(f"  saved run #{run_meta['run_id']}: {eid} ({notes})")

    # Get the last 3 runs
    runs = catalog_module.list_runs(catalog_path)
    last3 = runs[-3:]
    a_id, b_id, c_id = last3[0]["run_id"], last3[1]["run_id"], last3[2]["run_id"]

    print()
    print("=" * 70)
    print(f"DELTA: same input, two japan runs (run {a_id} vs {b_id})")
    print("=" * 70)
    print(delta_module.render_delta(last3[0], last3[1]))

    print()
    print("=" * 70)
    print(f"DELTA: different input — japan vs germany (run {a_id} vs {c_id})")
    print("=" * 70)
    print(delta_module.render_delta(last3[0], last3[2]))


if __name__ == "__main__":
    main()
