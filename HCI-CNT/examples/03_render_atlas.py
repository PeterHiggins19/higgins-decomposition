#!/usr/bin/env python3
"""
HUF-CNT — render an atlas and save to the catalog.

Walks 5 reference experiments, renders an analytical-only atlas for
each, saves each into the local atlas catalog, then prints the
catalog list. Three minutes total on stock hardware.
"""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "atlas"))
import atlas as atlas_module
import catalog as catalog_module


def main():
    runs_dir     = ROOT / "atlas" / "runs"
    catalog_path = ROOT / "atlas" / "catalog" / "atlas_catalog.json"

    samples = [
        ("ember_jpn",            "codawork2026",  "EMBER Japan"),
        ("ember_deu",            "codawork2026",  "EMBER Germany"),
        ("backblaze_fleet",      "codawork2026",  "BackBlaze fleet"),
        ("commodities_gold_silver","reference",   "Gold/Silver D2"),
        ("nuclear_semf",         "reference",     "Nuclear SEMF"),
    ]

    print("Rendering 5 reference atlases (analytical-only)...")
    for eid, subdir, label in samples:
        json_path = ROOT / "experiments" / subdir / eid / f"{eid}_cnt.json"
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
            pdf_path = Path(tf.name)
        meta = atlas_module.render_atlas(str(json_path), str(pdf_path),
                                         skip_tours=True)
        run_meta = catalog_module.save_run(meta, pdf_path,
                                           catalog_path, runs_dir,
                                           user_notes=label)
        print(f"  PASS  {eid:25}  saved as run #{run_meta['run_id']}")

    print()
    print("Catalog summary:")
    catalog_module.cli_list(catalog_path)


if __name__ == "__main__":
    main()
